import json
import os
import time
import argparse
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import urlopen

# ---------------------------------------------------
# Configuration & Defaults
# ---------------------------------------------------
HTTP_SOURCE_URL = "http://127.0.0.1:8002/api/vw_000_fx_quotes"
MAX_COLUMNS = 15
ANSI_GREEN = "\033[92m"
ANSI_RED = "\033[91m"
ANSI_BRIGHT = "\033[1m"
ANSI_DIM = "\033[2m"
ANSI_RESET = "\033[0m"
PRICE_LABEL_WIDTH = 11
MAX_TRADE_EVENT_LINES = 18

# ---------------------------------------------------
# Argument Parsing
# ---------------------------------------------------
parser = argparse.ArgumentParser(description="Epic 016 Pattern Engine Analyzer V2 (Sync)")
parser.add_argument("--symbol", default="GBPAUD_C", help="Target symbol (e.g. GBPAUD_C)")
parser.add_argument("--h", type=int, default=72, help="High confidence threshold")
parser.add_argument("--m", type=int, default=30, help="Medium confidence threshold")
parser.add_argument("--l", type=int, default=18, help="Low confidence threshold")
parser.add_argument("--bucket", type=int, default=8, help="Bucket duration in minutes")
parser.add_argument("--cost", type=float, default=-2.0, help="Round turn cost in pips")
parser.add_argument("--offset", type=float, default=0.0, help="Price offset (limit order fill)")
parser.add_argument("--tp", type=float, default=None, help="Fixed profit target")
parser.add_argument("--sl", type=float, default=None, help="Fixed stop loss")
parser.add_argument("--poll", type=float, default=0.5, help="Poll interval in seconds (Match backtest: 5.0)")
parser.add_argument("--restart", action="store_true", help="Restart from scratch (deletes previous state for today)")
parser.add_argument("--live", action="store_true", help="Enable live JSON order generation to Z drive")
parser.add_argument("--target_pips", type=float, default=999.0, help="Daily profit target (stops live orders once reached)")
parser.add_argument("--live_floor", type=float, default=0.0, help="Live execution floor (Shadow Mode active if below this)")
parser.add_argument("--quantity", type=int, default=50000, help="Trade quantity (default 50000)")
parser.add_argument("--trade_symbol", help="Product symbol for JSON order (e.g. AUD). Defaults to --symbol.")
parser.add_argument("--comment", default="V6_Pattern_Engine", help="Strategy name for order comment")
parser.add_argument("--flip", action="store_true", help="Flip the trade action in the JSON order (BUY -> SELL, SELL -> BUY)")

args = parser.parse_args()

# Map constants
SYMBOL = args.symbol.upper()
TRADE_SYMBOL = (args.trade_symbol or SYMBOL).upper()
QUANTITY = args.quantity
COMMENT = args.comment
CONF_H = args.h
CONF_M = args.m
CONF_L = args.l
BUCKET_MINUTES = args.bucket
ROUND_TURN_COST = args.cost
PRICE_OFFSET = args.offset
FIXED_TP = args.tp
FIXED_SL = args.sl
POLL_INTERVAL = args.poll
LIVE_MODE = args.live
TARGET_PIPS = args.target_pips
LIVE_FLOOR = args.live_floor
FLIP_MODE = args.flip

# ---------------------------------------------------
# Persistence & Order Configuration
# ---------------------------------------------------
STATE_ROOT = Path(__file__).resolve().parent / "states"
STATE_ROOT.mkdir(exist_ok=True)
# Include COMMENT in the filename to prevent collisions between different strategies on the same symbol
STATE_FILE = STATE_ROOT / f"state_{SYMBOL}_{COMMENT}_{datetime.now().strftime('%Y-%m-%d')}.json"

ORDER_DIR = Path(r"Z:\trades_rt\ORDERS")
# Unique GUID for this session (8 chars)
SESSION_GUID = hex(int(time.time()))[2:10]

TRADE_SIGNAL_LOG_FILE = Path(__file__).resolve().parent / f"signals_{SYMBOL}_{datetime.now().strftime('%Y%H%M')}.txt"

# ---------------------------------------------------
# Global state
# ---------------------------------------------------
price_data = defaultdict(lambda: {"bid": defaultdict(lambda: defaultdict(int)), "ask": defaultdict(lambda: defaultdict(int))})
first_prices = defaultdict(lambda: {"bid": {}, "ask": {}})
bucket_times = []
last_timestamp_str = None
last_trade_state_by_symbol = {}
recent_trade_events = []
active_position_by_symbol = {}
pending_position_by_symbol = {}
cumulative_net_pips = 0.0
validated_net_pips = 0.0
alt_net_pips = 0.0

def save_state():
    """Serializes the current trading state to a JSON file."""
    state = {
        "params": {
            "h": CONF_H, "m": CONF_M, "l": CONF_L, 
            "bucket": BUCKET_MINUTES, "offset": PRICE_OFFSET,
            "tp": FIXED_TP, "sl": FIXED_SL, "live_floor": LIVE_FLOOR
        },
        "cumulative_net_pips": cumulative_net_pips,
        "validated_net_pips": validated_net_pips,
        "alt_net_pips": alt_net_pips,
        "active_position": active_position_by_symbol.get(SYMBOL),
        "pending_position": pending_position_by_symbol.get(SYMBOL),
        "bucket_times": bucket_times,
        "first_prices": {side: dict(first_prices[SYMBOL][side]) for side in ["bid", "ask"]},
        "price_data": {
            side: {str(p): dict(bucket_dict) for p, bucket_dict in price_data[SYMBOL][side].items()}
            for side in ["bid", "ask"]
        },
        "recent_trade_events": recent_trade_events
    }
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except: pass

def load_state():
    """Resumes the trading state from a previous session if available."""
    global cumulative_net_pips, validated_net_pips, alt_net_pips, bucket_times, recent_trade_events
    if args.restart:
        if STATE_FILE.exists():
            try: STATE_FILE.unlink()
            except: pass
            print(f"Restart: Deleted previous state for {SYMBOL} ({COMMENT}).")
        return

    if not STATE_FILE.exists(): return

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        
        # Logic Guard: Ensure we aren't resuming with different strategy rules
        s_p = state.get("params", {})
        if (s_p.get("h") != CONF_H or s_p.get("m") != CONF_M or 
            s_p.get("l") != CONF_L or s_p.get("bucket") != BUCKET_MINUTES):
            print(f"Warning: Strategy parameter mismatch in state file. Starting FRESH.")
            return

        cumulative_net_pips = state.get("cumulative_net_pips", 0.0)
        validated_net_pips = state.get("validated_net_pips", 0.0)
        alt_net_pips = state.get("alt_net_pips", 0.0)
        
        # SANITY GUARD: If loaded P&L is physically impossible, reset to zero.
        if abs(cumulative_net_pips) > 1000.0 or abs(validated_net_pips) > 1000.0:
            print(f"Warning: Corrupted P&L detected in state file. Resetting to 0.0.")
            cumulative_net_pips = 0.0
            validated_net_pips = 0.0
            alt_net_pips = 0.0
        recent_trade_events = state.get("recent_trade_events", [])
        bucket_times = state.get("bucket_times", [])
        
        active = state.get("active_position")
        if active: active_position_by_symbol[SYMBOL] = active
            
        pending = state.get("pending_position")
        if pending: pending_position_by_symbol[SYMBOL] = pending

        s_fp = state.get("first_prices", {})
        for side in ["bid", "ask"]:
            if side in s_fp:
                for b_t, p in s_fp[side].items():
                    first_prices[SYMBOL][side][b_t] = p
                    
        s_pd = state.get("price_data", {})
        for side in ["bid", "ask"]:
            if side in s_pd:
                for p_str, b_dict in s_pd[side].items():
                    p_val = float(p_str)
                    for b_t, count in b_dict.items():
                        price_data[SYMBOL][side][p_val][b_t] = count
                        
        print(f"Successfully resumed state for {SYMBOL} ({COMMENT}). Total P&L: {cumulative_net_pips} pips.")
    except Exception as e:
        print(f"Load State Error: {e}. Starting fresh.")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_bucket_time(dt):
    minute = (dt.minute // BUCKET_MINUTES) * BUCKET_MINUTES
    return dt.replace(minute=minute, second=0, microsecond=0).strftime("%H:%M")

def parse_quote_timestamp(timestamp_str):
    try: return datetime.fromisoformat(timestamp_str).replace(tzinfo=None)
    except ValueError: pass
    try: return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError: return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

def fetch_quotes():
    try:
        with urlopen(HTTP_SOURCE_URL, timeout=5) as response:
            payload = json.load(response)
        return payload.get("data", [])
    except: return []

def compute_side_metrics(symbol, side, bucket_time):
    open_price = first_prices[symbol][side].get(bucket_time)
    above = 0
    below = 0
    at_open = 0
    if open_price is None: return None

    for price, bucket_counts in price_data[symbol][side].items():
        count = bucket_counts.get(bucket_time, 0)
        if count <= 0: continue
        if price > open_price: above += count
        elif price == open_price: at_open += count
        else: below += count
            
    return {"open": open_price, "above": above, "at_open": at_open, "below": below, "net": above - below}

def classify_state(bid_m, ask_m, current_open, prior_open):
    bid_net = bid_m["net"]
    ask_net = ask_m["net"]
    open_move = None
    if current_open and prior_open:
        if current_open > prior_open: open_move = "higher"
        elif current_open < prior_open: open_move = "lower"
        else: open_move = "flat"

    state = "FLAT"
    if bid_net > 0 and ask_net > 0:
        if bid_net >= CONF_H and ask_net >= CONF_H: state = "LONG_HIGH"
        elif bid_net >= CONF_M and ask_net >= CONF_M: state = "LONG_MED"
        elif bid_net >= CONF_L and ask_net >= CONF_L: state = "LONG_LOW"
    elif bid_net < 0 and ask_net < 0:
        if bid_net <= -CONF_H and ask_net <= -CONF_H: state = "SHORT_HIGH"
        elif bid_net <= -CONF_M and ask_net <= -CONF_M: state = "SHORT_MED"
        elif bid_net <= -CONF_L and ask_net <= -CONF_L: state = "SHORT_LOW"

    if open_move == "higher" and bid_net < 0 and ask_net < 0: state = "EXIT_LONG"
    elif open_move == "lower" and bid_net > 0 and ask_net > 0: state = "EXIT_SHORT"
    return state, open_move

def infer_pip_multiplier(symbol):
    return 100 if "JPY" in str(symbol).upper() else 10000

def append_trade_signal_log(event):
    line = f"{event['ts']} | {event['symbol']} | {event['event']} | {event['state']} | P={event['price']:.5f}"
    if "net_pips" in event: 
        line += f" | PNL={event['net_pips']} | CUM={event.get('cum_pips', cumulative_net_pips)} | ALT={alt_net_pips}"
    with TRADE_SIGNAL_LOG_FILE.open("a", encoding="utf-8") as fh: fh.write(line + "\n")

def generate_order_json(event):
    """Generates a tradeable JSON order file in the Z drive."""
    if not LIVE_MODE: return
    
    # Format: breakout_{GUID}_{SYMBOL}_{STRATEGY}_{ACTION}_{TIMESTAMP}_{STATUS}_tradeable.json
    action = "BUY" if (event["event"] == "OPEN" and event["state"].startswith("LONG")) or \
                      (event["event"] == "CLOSE" and "SHORT" in event["state"]) else "SELL"
    
    if FLIP_MODE:
        action = "SELL" if action == "BUY" else "BUY"
        
    status = "open" if event["event"] == "OPEN" else "close"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Using COMMENT as the {STRATEGY} placeholder in the filename
    filename = f"breakout_{SESSION_GUID}_{SYMBOL}_{COMMENT}_{action}_{timestamp}_{status}_tradeable.json"
    filepath = ORDER_DIR / filename
    
    order_data = {
        "symbol": TRADE_SYMBOL,
        "secType": "CASH",
        "exchange": "IDEALPRO",
        "currency": "USD",
        "action": action,
        "orderType": "MKT",
        "quantity": QUANTITY,
        "guidePrice": event["price"],
        "comment": COMMENT,
        "source": "normal",
        "guid": SESSION_GUID
    }
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(order_data, f, indent=2)
        print(f"{ANSI_BRIGHT}Live Order Placed: {filename}{ANSI_RESET}")
    except Exception as e:
        print(f"{ANSI_RED}Order Error: {e}{ANSI_RESET}")

def display_frequency_locked(locked_state):
    clear_screen()
    if os.name == "nt":
        os.system(f"title Pattern Engine - {SYMBOL} - {COMMENT}")
        
    mode_str = f"{ANSI_BRIGHT}LIVE{ANSI_RESET}" if cumulative_net_pips >= LIVE_FLOOR else f"{ANSI_RED}SHADOW{ANSI_RESET}"
    flip_str = f" | {ANSI_RED}FLIP: ON{ANSI_RESET}" if FLIP_MODE else ""
    cum_color = ANSI_GREEN if cumulative_net_pips >= 0 else ANSI_RED
    val_color = ANSI_GREEN if validated_net_pips >= 0 else ANSI_RED
    alt_color = ANSI_GREEN if alt_net_pips >= 0 else ANSI_RED
    
    left_lines = [
        f"--- {ANSI_BRIGHT}{COMMENT}{ANSI_RESET} | {SYMBOL} | MODE: {mode_str}{flip_str} ---",
        f"H/M/L: {CONF_H}/{CONF_M}/{CONF_L} | Bucket: {BUCKET_MINUTES}m | Poll: {POLL_INTERVAL}s",
        f"TOTAL P&L (Accounting): {cum_color}{cumulative_net_pips}{ANSI_RESET} pips",
        f"ALT P&L (Flipped):      {alt_color}{alt_net_pips}{ANSI_RESET} pips",
        f"LIVE P&L (Validated):   {val_color}{validated_net_pips}{ANSI_RESET} pips",
        f"Updated: {datetime.now().strftime('%H:%M:%S')}",
        "-" * 80,
        f"LOCKED SIGNAL: {ANSI_BRIGHT}{locked_state}{ANSI_RESET}",
    ]
    
    pending = pending_position_by_symbol.get(SYMBOL)
    if pending:
        left_lines.append(f"STATUS: {ANSI_BRIGHT}{ANSI_GREEN}PENDING {pending['dir'].upper()}{ANSI_RESET} (Wait for Offset)")
        left_lines.append(f"Target: {pending['target_p']:.5f} | Offset: {PRICE_OFFSET} pips")
    
    recent_b = bucket_times[-MAX_COLUMNS:]
    current_b = recent_b[-1] if recent_b else None
    if current_b:
        bid_m = compute_side_metrics(SYMBOL, "bid", current_b)
        ask_m = compute_side_metrics(SYMBOL, "ask", current_b)
        if bid_m and ask_m:
            left_lines.append(f"  Bid Cluster: Open={bid_m['open']:.5f} | Above={bid_m['above']} | Below={bid_m['below']} | Net={bid_m['net']}")
            left_lines.append(f"  Ask Cluster: Open={ask_m['open']:.5f} | Above={ask_m['above']} | Below={ask_m['below']} | Net={ask_m['net']}")
    
    right_lines = ["Recent Trade History", "--------------------"]
    for ev in reversed(recent_trade_events[-MAX_TRADE_EVENT_LINES:]):
        pnl_str = f" ({ev.get('net_pips')} pips)" if "net_pips" in ev else ""
        right_lines.append(f"{ev['ts'][11:19]} {ev['event']} {pnl_str}")

    for i in range(max(len(left_lines), len(right_lines))):
        l = left_lines[i] if i < len(left_lines) else ""
        r = right_lines[i] if i < len(right_lines) else ""
        print(f"{l:<60} | {r}")

def run_analyzer():
    global last_timestamp_str, bucket_times, cumulative_net_pips, validated_net_pips, alt_net_pips
    load_state()
    
    # HARD RESTART: If restart flag is on, force everything to zero immediately
    if args.restart:
        cumulative_net_pips = 0.0
        validated_net_pips = 0.0
        alt_net_pips = 0.0
        print("Hard Restart Applied: All P&L counters reset to 0.0.")

    current_state = "FLAT"
    prior_open = None
    last_processed_bucket = None
    
    try:
        while True:
            should_render = False
            try:
                quotes = fetch_quotes()
                if not quotes: time.sleep(POLL_INTERVAL); continue
                ts_str = max((q.get("timestamp") or "") for q in quotes)
                
                current_bid = None
                current_ask = None
                for q in quotes:
                    sym = (q.get("code") or "").upper()
                    if sym == SYMBOL:
                        current_bid = round(float(q["bid"]), 5)
                        current_ask = round(float(q["ask"]), 5)
                
                # --- 5-SECOND SYNCHRONIZED LOGIC PULSE ---
                if ts_str != last_timestamp_str:
                    dt = parse_quote_timestamp(ts_str)
                    b_time = get_bucket_time(dt)
                    if b_time not in bucket_times: bucket_times.append(b_time); bucket_times.sort()
                    
                    if current_bid:
                        prec = 2 if "JPY" in SYMBOL else 4
                        for side, p_val in [("bid", current_bid), ("ask", current_ask)]:
                            p_r = round(p_val, prec)
                            if b_time not in first_prices[SYMBOL][side]: first_prices[SYMBOL][side][b_time] = p_r
                            price_data[SYMBOL][side][p_r][b_time] += 1
                        
                        # A. REAL-TIME RISK MANAGEMENT (TP/SL/OFFSET FILL) - Checked every 5s
                        active = active_position_by_symbol.get(SYMBOL)
                        pending = pending_position_by_symbol.get(SYMBOL)
                        
                        if active and (FIXED_TP or FIXED_SL):
                            mult = infer_pip_multiplier(SYMBOL)
                            pnl = (current_bid - active["entry_p"]) * mult if active["dir"] == "long" else (active["entry_p"] - current_ask) * mult
                            exit_reason = None
                            if FIXED_TP and pnl >= FIXED_TP: exit_reason = "TP"
                            elif FIXED_SL and pnl <= -FIXED_SL: exit_reason = "SL"
                            if exit_reason:
                                exit_p = current_bid if active["dir"] == "long" else current_ask
                                net_pips = round(pnl + ROUND_TURN_COST, 1)
                                alt_pips = round(-pnl + ROUND_TURN_COST, 1)
                                
                                cumulative_net_pips = round(cumulative_net_pips + net_pips, 1)
                                alt_net_pips = round(alt_net_pips + alt_pips, 1)
                                
                                if active.get("is_live"): validated_net_pips = round(validated_net_pips + net_pips, 1)
                                
                                ev = {"ts": ts_str, "symbol": SYMBOL, "event": "CLOSE", "state": f"EXIT_{exit_reason}", "price": exit_p, "net_pips": net_pips, "cum_pips": cumulative_net_pips}
                                recent_trade_events.append(ev); append_trade_signal_log(ev)
                                if active.get("is_live"): generate_order_json(ev)
                                active_position_by_symbol.pop(SYMBOL); active = None

                        if pending:
                            # Check for Offset Fill
                            is_hit = False
                            if pending["dir"] == "long" and current_ask <= pending["target_p"]: is_hit = True
                            elif pending["dir"] == "short" and current_bid >= pending["target_p"]: is_hit = True
                            
                            if is_hit:
                                # Convert Pending to Active
                                active_position_by_symbol[SYMBOL] = {"dir": pending["dir"], "entry_p": pending["target_p"], "ts": ts_str, "is_live": pending["is_live"]}
                                ev = {"ts": ts_str, "symbol": SYMBOL, "event": "OPEN", "state": pending["state"], "price": pending["target_p"]}
                                recent_trade_events.append(ev); append_trade_signal_log(ev)
                                if pending["is_live"]: generate_order_json(ev)
                                pending_position_by_symbol.pop(SYMBOL); pending = None
                            
                            # Cancel pending if signal changes away from it
                            elif current_state != pending["state"] and not current_state.startswith(pending["dir"].upper()):
                                pending_position_by_symbol.pop(SYMBOL); pending = None

                        # B. SIGNAL LOCKING (Decision only at Bucket Transitions)
                        if b_time != last_processed_bucket:
                            # Evaluate the signal for the NEW bucket based on the PRIOR bucket's completed cluster
                            idx = bucket_times.index(b_time)
                            prior_b = bucket_times[idx-1] if idx > 0 else None
                            
                            if prior_b:
                                bid_m = compute_side_metrics(SYMBOL, "bid", prior_b)
                                ask_m = compute_side_metrics(SYMBOL, "ask", prior_b)
                                if bid_m and ask_m:
                                    current_open = bid_m["open"]
                                    new_state, _ = classify_state(bid_m, ask_m, current_open, prior_open)
                                    
                                    # Trigger entries/exits based on the new Signal Lock
                                    if current_state != new_state:
                                        if not active and not pending and new_state.startswith("LONG_") and "EXIT" not in new_state:
                                            if validated_net_pips < TARGET_PIPS:
                                                # FLIP-AWARE SAFETY: If flipping, floor applies to ALT P&L
                                                is_live = (alt_net_pips >= LIVE_FLOOR) if FLIP_MODE else (cumulative_net_pips >= LIVE_FLOOR)
                                                target_p = current_ask + (PRICE_OFFSET / infer_pip_multiplier(SYMBOL))
                                                if PRICE_OFFSET >= 0:
                                                    active_position_by_symbol[SYMBOL] = {"dir": "long", "entry_p": target_p, "ts": ts_str, "is_live": is_live}
                                                    ev = {"ts": ts_str, "symbol": SYMBOL, "event": "OPEN", "state": new_state, "price": target_p}
                                                    recent_trade_events.append(ev); append_trade_signal_log(ev)
                                                    if is_live: generate_order_json(ev)
                                                else:
                                                    pending_position_by_symbol[SYMBOL] = {"dir": "long", "target_p": target_p, "state": new_state, "is_live": is_live}
                                        elif not active and not pending and new_state.startswith("SHORT_") and "EXIT" not in new_state:
                                            if validated_net_pips < TARGET_PIPS:
                                                is_live = (alt_net_pips >= LIVE_FLOOR) if FLIP_MODE else (cumulative_net_pips >= LIVE_FLOOR)
                                                target_p = current_bid - (PRICE_OFFSET / infer_pip_multiplier(SYMBOL))
                                                if PRICE_OFFSET >= 0:
                                                    active_position_by_symbol[SYMBOL] = {"dir": "short", "entry_p": target_p, "ts": ts_str, "is_live": is_live}
                                                    ev = {"ts": ts_str, "symbol": SYMBOL, "event": "OPEN", "state": new_state, "price": target_p}
                                                    recent_trade_events.append(ev); append_trade_signal_log(ev)
                                                    if is_live: generate_order_json(ev)
                                                else:
                                                    pending_position_by_symbol[SYMBOL] = {"dir": "short", "target_p": target_p, "state": new_state, "is_live": is_live}
                                        elif active:
                                            should_close = False
                                            if active["dir"] == "long" and (new_state.startswith("SHORT_") or new_state == "EXIT_LONG"): should_close = True
                                            elif active["dir"] == "short" and (new_state.startswith("LONG_") or new_state == "EXIT_SHORT"): should_close = True
                                            if should_close:
                                                exit_p = current_bid if active["dir"] == "long" else current_ask
                                                mult = infer_pip_multiplier(SYMBOL)
                                                pnl = (exit_p - active["entry_p"]) * mult if active["dir"] == "long" else (active["entry_p"] - exit_p) * mult
                                                
                                                net_pips = round(pnl + ROUND_TURN_COST, 1)
                                                alt_pips = round(-pnl + ROUND_TURN_COST, 1)
                                                
                                                cumulative_net_pips = round(cumulative_net_pips + net_pips, 1)
                                                alt_net_pips = round(alt_net_pips + alt_pips, 1)
                                                
                                                if active.get("is_live"): validated_net_pips = round(validated_net_pips + net_pips, 1)
                                                
                                                ev = {"ts": ts_str, "symbol": SYMBOL, "event": "CLOSE", "state": new_state, "price": exit_p, "net_pips": net_pips, "cum_pips": cumulative_net_pips}
                                                recent_trade_events.append(ev); append_trade_signal_log(ev)
                                                if active.get("is_live"): generate_order_json(ev)
                                                active_position_by_symbol.pop(SYMBOL)
                                    
                                    current_state = new_state
                                    prior_open = current_open
                            
                            last_processed_bucket = b_time
                        
                        # C. Persist State
                        save_state()
                        
                    last_timestamp_str = ts_str; should_render = True
            except: pass
            if should_render: 
                # Pass current locked state to display
                display_frequency_locked(current_state)
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt: print("\nStopped.")

if __name__ == "__main__":
    run_analyzer()
