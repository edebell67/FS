import json
import os
import re
import shutil
import sys
import time
import argparse
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

# ---------------------------------------------------
# Configuration & Defaults
# ---------------------------------------------------
HTTP_SOURCE_URL = "http://127.0.0.1:8002/api/vw_000_fx_quotes"
POLL_INTERVAL = 0.5
MAX_COLUMNS = 15
ANSI_GREEN = "\033[92m"
ANSI_RED = "\033[91m"
ANSI_BRIGHT = "\033[1m"
ANSI_DIM = "\033[2m"
ANSI_RESET = "\033[0m"
ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")
PRICE_LABEL_WIDTH = 11
MAX_TRADE_EVENT_LINES = 18
SNAPSHOT_INTERVAL_SECONDS = 5

# ---------------------------------------------------
# Argument Parsing for "Additional Parms"
# ---------------------------------------------------
parser = argparse.ArgumentParser(description="Epic 016 Pattern Engine Analyzer V2")
parser.add_argument("--symbol", default="GBPAUD_C", help="Target symbol (e.g. GBPAUD_C)")
parser.add_argument("--h", type=int, default=72, help="High confidence threshold")
parser.add_argument("--m", type=int, default=30, help="Medium confidence threshold")
parser.add_argument("--l", type=int, default=18, help="Low confidence threshold")
parser.add_argument("--bucket", type=int, default=8, help="Bucket duration in minutes")
parser.add_argument("--cost", type=float, default=-3.0, help="Round turn cost in pips")
parser.add_argument("--offset", type=float, default=0.0, help="Price offset (limit order fill)")
parser.add_argument("--tp", type=float, default=None, help="Fixed profit target")
parser.add_argument("--sl", type=float, default=None, help="Fixed stop loss")

args = parser.parse_args()

# Map back to internal constants
SYMBOL = args.symbol.upper()
CONF_H = args.h
CONF_M = args.m
CONF_L = args.l
BUCKET_MINUTES = args.bucket
ROUND_TURN_COST = args.cost
PRICE_OFFSET = args.offset
FIXED_TP = args.tp
FIXED_SL = args.sl

TRADE_SIGNAL_LOG_FILE = Path(__file__).resolve().parent / f"signals_{SYMBOL}_{datetime.now().strftime('%Y%H%M')}.txt"

# ---------------------------------------------------
# Load config for snapshot storage path
# ---------------------------------------------------
BREAKOUT_CONFIG_PATH = Path(__file__).resolve().parents[3] / "TradeApps" / "breakout" / "fs" / "config.json"
GENERATED_DATA_ROOT = None
try:
    with open(BREAKOUT_CONFIG_PATH, "r", encoding="utf-8") as f:
        _config = json.load(f)
        GENERATED_DATA_ROOT = Path(_config.get("path_settings", {}).get("generated_data_root", "X:\\eds"))
except (FileNotFoundError, json.JSONDecodeError):
    GENERATED_DATA_ROOT = Path("X:\\eds")

# ---------------------------------------------------
# Global state
# ---------------------------------------------------
price_data = defaultdict(lambda: {"bid": defaultdict(lambda: defaultdict(int)), "ask": defaultdict(lambda: defaultdict(int))})
first_prices = defaultdict(lambda: {"bid": {}, "ask": {}})
trade_marker_history = defaultdict(lambda: {"bid": defaultdict(lambda: defaultdict(list)), "ask": defaultdict(lambda: defaultdict(list))})
bucket_times = []
last_timestamp_str = None
last_pulse_phase = None
last_trade_state_by_symbol = {}
recent_trade_events = []
active_position_by_symbol = {}
last_snapshot_time = 0
last_raw_prices = {}
cumulative_net_pips = 0.0

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def capture_snapshot():
    global last_snapshot_time
    if not last_raw_prices: return
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    snapshot_dir = GENERATED_DATA_ROOT / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex" / date_str
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot_file = snapshot_dir / "_price_capture.jsonl"
    snapshot_data = {"ts": now.isoformat()}
    snapshot_data.update(last_raw_prices)
    try:
        with open(snapshot_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(snapshot_data) + "\n")
    except OSError: pass
    last_snapshot_time = time.time()

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
    for price, bucket_counts in price_data[symbol][side].items():
        count = bucket_counts.get(bucket_time, 0)
        if count <= 0 or open_price is None: continue
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

def get_bucket_marker(symbol, bucket_time, previous_bucket=None):
    bid_metrics = compute_side_metrics(symbol, "bid", bucket_time)
    ask_metrics = compute_side_metrics(symbol, "ask", bucket_time)
    prior_open = first_prices[symbol]["bid"].get(previous_bucket) if previous_bucket else None
    state, _ = classify_state(bid_metrics, ask_metrics, bid_metrics["open"], prior_open)
    if state.startswith("LONG_") or state == "EXIT_SHORT": return {"state": state, "side": "ask", "style": "open" if state.startswith("LONG_") else "close", "price": ask_metrics["open"]}
    if state.startswith("SHORT_") or state == "EXIT_LONG": return {"state": state, "side": "bid", "style": "open" if state.startswith("SHORT_") else "close", "price": bid_metrics["open"]}
    return None

def should_record_trade_event(symbol, marker_info, ts):
    global cumulative_net_pips
    if not marker_info: return False
    style = marker_info.get("style")
    active = active_position_by_symbol.get(symbol)
    if style == "open":
        if active: return False
        active_position_by_symbol[symbol] = {"dir": "long" if marker_info["state"].startswith("LONG_") else "short", "entry_p": marker_info["price"], "ts": ts}
        return True
    if style == "close":
        if not active: return False
        mult = infer_pip_multiplier(symbol)
        pnl = (marker_info["price"] - active["entry_p"]) * mult if active["dir"] == "long" else (active["entry_p"] - marker_info["price"]) * mult
        net_pips = round(pnl + ROUND_TURN_COST, 1)
        marker_info["net_pips"] = net_pips
        marker_info["entry_p"] = active["entry_p"]
        cumulative_net_pips = round(cumulative_net_pips + net_pips, 1)
        marker_info["cum_pips"] = cumulative_net_pips
        active_position_by_symbol.pop(symbol)
        return True
    return False

def append_trade_signal_log(event):
    line = f"{event['ts']} | {event['symbol']} | {event['event']} | {event['state']} | P={event['price']:.5f}"
    if "net_pips" in event: line += f" | PNL={event['net_pips']} | CUM={event.get('cum_pips', cumulative_net_pips)}"
    with TRADE_SIGNAL_LOG_FILE.open("a", encoding="utf-8") as fh: fh.write(line + "\n")

def display_frequency(pulse_phase=False):
    clear_screen()
    cum_color = ANSI_GREEN if cumulative_net_pips >= 0 else ANSI_RED
    left_lines = [
        f"--- Pattern Engine V2 | {SYMBOL} | H/M/L: {CONF_H}/{CONF_M}/{CONF_L} ---",
        f"Bucket: {BUCKET_MINUTES}m | Cost: {ROUND_TURN_COST} | CUMULATIVE: {cum_color}{cumulative_net_pips}{ANSI_RESET} pips",
        f"Updated: {datetime.now().strftime('%H:%M:%S')}",
        "-" * 80,
    ]
    recent_b = bucket_times[-MAX_COLUMNS:]
    current_b = recent_b[-1] if recent_b else None
    prior_b = recent_b[-2] if len(recent_b) > 1 else None
    if current_b:
        bid_m = compute_side_metrics(SYMBOL, "bid", current_b)
        ask_m = compute_side_metrics(SYMBOL, "ask", current_b)
        state, _ = classify_state(bid_m, ask_m, bid_m["open"], first_prices[SYMBOL]["bid"].get(prior_b))
        left_lines.append(f"\nSTATE: {ANSI_BRIGHT}{state}{ANSI_RESET} | BID_NET: {bid_m['net']} | ASK_NET: {ask_m['net']}")
        for side in ["ASK", "BID"]:
            m = ask_m if side == "ASK" else bid_m
            left_lines.append(f"  {side} Cluster: Open={m['open']:.5f} | Above={m['above']} | Below={m['below']} | Net={m['net']}")
    
    right_lines = ["Recent Trade History", "--------------------"]
    for ev in reversed(recent_trade_events[-MAX_TRADE_EVENT_LINES:]):
        pnl_str = f" ({ev.get('net_pips')} pips)" if "net_pips" in ev else ""
        right_lines.append(f"{ev['ts'][11:19]} {ev['event']} {pnl_str}")

    for i in range(max(len(left_lines), len(right_lines))):
        l = left_lines[i] if i < len(left_lines) else ""
        r = right_lines[i] if i < len(right_lines) else ""
        print(f"{l:<60} | {r}")

def run_analyzer():
    global last_timestamp_str, bucket_times, last_snapshot_time
    print(f"Initializing V2 Analyzer for {SYMBOL}...")
    try:
        while True:
            should_render = False
            try:
                quotes = fetch_quotes()
                if not quotes: time.sleep(POLL_INTERVAL); continue
                ts_str = max((q.get("timestamp") or "") for q in quotes)
                for q in quotes:
                    sym = (q.get("code") or "").upper()
                    if sym == SYMBOL:
                        last_raw_prices[sym] = {"bid": round(float(q["bid"]), 5), "ask": round(float(q["ask"]), 5)}
                
                if ts_str != last_timestamp_str:
                    dt = parse_quote_timestamp(ts_str)
                    b_time = get_bucket_time(dt)
                    if b_time not in bucket_times: bucket_times.append(b_time); bucket_times.sort()
                    quote = next((q for q in quotes if q["code"].upper() == SYMBOL), None)
                    if quote:
                        for side in ["bid", "ask"]:
                            p = round(float(quote[side]), 2 if "JPY" in SYMBOL else 4)
                            if b_time not in first_prices[SYMBOL][side]: first_prices[SYMBOL][side][b_time] = p
                            price_data[SYMBOL][side][p][b_time] += 1
                        idx = bucket_times.index(b_time)
                        prior_b = bucket_times[idx-1] if idx > 0 else None
                        m_info = get_bucket_marker(SYMBOL, b_time, prior_b)
                        if m_info and last_trade_state_by_symbol.get(SYMBOL) != m_info["state"]:
                            if should_record_trade_event(SYMBOL, m_info, ts_str):
                                ev = {"ts": ts_str, "symbol": SYMBOL, "event": "OPEN" if m_info["style"]=="open" else "CLOSE", "state": m_info["state"], "price": m_info["price"]}
                                if "net_pips" in m_info: ev["net_pips"] = m_info["net_pips"]
                                recent_trade_events.append(ev); append_trade_signal_log(ev)
                            last_trade_state_by_symbol[SYMBOL] = m_info["state"]
                    last_timestamp_str = ts_str; should_render = True
            except: pass
            if should_render: display_frequency()
            if (time.time() - last_snapshot_time) >= SNAPSHOT_INTERVAL_SECONDS: capture_snapshot()
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt: print("\nStopped.")

if __name__ == "__main__":
    run_analyzer()
