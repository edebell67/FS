import json
import os
import re
import shutil
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

# ---------------------------------------------------
# Configuration & Optimized Parameters
# ---------------------------------------------------
HTTP_SOURCE_URL = "http://127.0.0.1:8002/api/vw_000_fx_quotes"
POLL_INTERVAL = 0.5
SNAPSHOT_INTERVAL_SECONDS = 5
MAX_COLUMNS = 15
ANSI_GREEN = "\033[92m"
ANSI_RED = "\033[91m"
ANSI_BRIGHT = "\033[1m"
ANSI_DIM = "\033[2m"
ANSI_RESET = "\033[0m"
ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")
PRICE_LABEL_WIDTH = 11
MAX_TRADE_EVENT_LINES = 18
TRADE_SIGNAL_LOG_FILE = Path(__file__).resolve().parent / "price_frequency_multi_analyzer_signals.txt"

# [V20260513_1320] Optimized Symbol Configuration
SYMBOL_CONFIGS = {
    "GBPAUD_C": {
        "h": 72, "m": 30, "l": 18, 
        "bucket": 8, "tp": 50.0, "sl": 15.0
    },
    "EURAUD_C": {
        "h": 55, "m": 22, "l": 6, 
        "bucket": 15, "tp": None, "sl": None
    },
    "NZDAUD_C": {
        "h": 15, "m": 14, "l": 7, 
        "bucket": 8, "tp": None, "sl": None
    },
    "CHFCAD_C": {
        "h": 45, "m": 12, "l": 9, 
        "bucket": 8, "tp": None, "sl": None
    },
    "CADJPY_C": {
        "h": 19, "m": 18, "l": 12, 
        "bucket": 10, "tp": 10.0, "sl": 20.0
    }
}

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

def get_bucket_time(dt, bucket_min):
    minute = (dt.minute // bucket_min) * bucket_min
    return dt.replace(minute=minute, second=0, microsecond=0).strftime("%H:%M")

def parse_quote_timestamp(timestamp_str):
    try: return datetime.fromisoformat(timestamp_str).replace(tzinfo=None)
    except ValueError: pass
    try: return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError: return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

def fetch_quotes():
    with urlopen(HTTP_SOURCE_URL, timeout=5) as response:
        payload = json.load(response)
    return payload.get("data", [])

def compute_side_metrics(symbol, side, bucket_time):
    open_price = first_prices[symbol][side].get(bucket_time)
    above_p = 0
    at_open = 0
    below_p = 0
    for price, bucket_counts in price_data[symbol][side].items():
        count = bucket_counts.get(bucket_time, 0)
        if count <= 0 or open_price is None: continue
        if price > open_price: above_p += count
        elif price == open_price: at_open += count
        else: below_p += count
    return {
        "open": open_price, "above": above_p, "at_open": at_open, 
        "below": below_p, "net": above_p - below_p
    }

def classify_state(symbol, bid_m, ask_m, current_open, prior_open):
    conf = SYMBOL_CONFIGS.get(symbol, {"h": 20, "m": 10, "l": 6})
    bid_net = bid_m["net"]
    ask_net = ask_m["net"]
    open_move = None
    if current_open and prior_open:
        if current_open > prior_open: open_move = "higher"
        elif current_open < prior_open: open_move = "lower"
        else: open_move = "flat"

    state = "FLAT"
    if bid_net > 0 and ask_net > 0:
        if bid_net >= conf["h"] and ask_net >= conf["h"]: state = "LONG_HIGH"
        elif bid_net >= conf["m"] and ask_net >= conf["m"]: state = "LONG_MED"
        elif bid_net >= conf["l"] and ask_net >= conf["l"]: state = "LONG_LOW"
    elif bid_net < 0 and ask_net < 0:
        if bid_net <= -conf["h"] and ask_net <= -conf["h"]: state = "SHORT_HIGH"
        elif bid_net <= -conf["m"] and ask_net <= -conf["m"]: state = "SHORT_MED"
        elif bid_net <= -conf["l"] and ask_net <= -conf["l"]: state = "SHORT_LOW"

    if open_move == "higher" and bid_net < 0 and ask_net < 0: state = "EXIT_LONG"
    elif open_move == "lower" and bid_net > 0 and ask_net > 0: state = "EXIT_SHORT"
    return state, open_move

def infer_pip_multiplier(symbol):
    return 100 if "JPY" in str(symbol).upper() else 10000

def get_bucket_marker(symbol, bucket_time, previous_bucket=None):
    bid_metrics = compute_side_metrics(symbol, "bid", bucket_time)
    ask_metrics = compute_side_metrics(symbol, "ask", bucket_time)
    prior_open = first_prices[symbol]["bid"].get(previous_bucket) if previous_bucket else None
    state, _ = classify_state(symbol, bid_metrics, ask_metrics, bid_metrics["open"], prior_open)

    if "LONG" in state:
        return {"state": state, "side": "ask", "style": "open" if "ENTRY" in state else "close", "price": ask_metrics["open"]}
    if "SHORT" in state:
        return {"state": state, "side": "bid", "style": "open" if "ENTRY" in state else "close", "price": bid_metrics["open"]}
    return None

def should_record_trade_event(symbol, marker_info, ts):
    if not marker_info: return False
    style = marker_info.get("style")
    active = active_position_by_symbol.get(symbol)
    
    if style == "open":
        if active: return False
        active_position_by_symbol[symbol] = {
            "dir": "long" if "LONG" in marker_info["state"] else "short",
            "entry_p": marker_info["price"], "ts": ts
        }
        return True
    if style == "close":
        if not active: return False
        mult = infer_pip_multiplier(symbol)
        pnl = (marker_info["price"] - active["entry_p"]) * mult if active["dir"] == "long" else (active["entry_p"] - marker_info["price"]) * mult
        marker_info["net_pips"] = round(pnl, 1)
        marker_info["entry_p"] = active["entry_p"]
        active_position_by_symbol.pop(symbol)
        return True
    return False

def append_trade_signal_log(event):
    line = f"{event['ts']} | {event['symbol']} | {event['event']} | {event['state']} | P={event['price']:.5f}"
    if "net_pips" in event: line += f" | PNL={event['net_pips']}"
    with TRADE_SIGNAL_LOG_FILE.open("a", encoding="utf-8") as fh: fh.write(line + "\n")

def display_frequency(pulse_phase=False):
    clear_screen()
    left_lines = [
        "--- Epic 016 Pattern Engine V2 (Multi-Symbol Optimized) ---",
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "-" * 80,
    ]
    
    for symbol, conf in SYMBOL_CONFIGS.items():
        recent_b = [b for b in bucket_times if b in first_prices[symbol]["bid"]][-MAX_COLUMNS:]
        if not recent_b: continue
        current_b = recent_b[-1]
        prior_b = recent_b[-2] if len(recent_b) > 1 else None
        
        bid_m = compute_side_metrics(symbol, "bid", current_b)
        ask_m = compute_side_metrics(symbol, "ask", current_b)
        state, _ = classify_state(symbol, bid_m, ask_m, bid_m["open"], first_prices[symbol]["bid"].get(prior_b))
        
        left_lines.append(f"\n[{symbol}]  Thresholds: {conf['h']}/{conf['m']}/{conf['l']}  Bucket: {conf['bucket']}m")
        left_lines.append(f"  STATE: {ANSI_BRIGHT}{state}{ANSI_RESET} | BID_NET: {bid_m['net']} | ASK_NET: {ask_m['net']}")
        
        # Simplified cluster view for brevity in multi-mode
        left_lines.append(f"  BID Open: {bid_m['open']:.5f} | Above: {bid_m['above']} | Below: {bid_m['below']}")
        left_lines.append(f"  ASK Open: {ask_m['open']:.5f} | Above: {ask_m['above']} | Below: {ask_m['below']}")

    # Right panel: Trade Signals
    right_lines = ["Recent Signals", "--------------"]
    for ev in reversed(recent_trade_events[-MAX_TRADE_EVENT_LINES:]):
        pnl_str = f" ({ev.get('net_pips')} pips)" if "net_pips" in ev else ""
        right_lines.append(f"{ev['ts'][11:19]} {ev['symbol']} {ev['event']} {pnl_str}")

    terminal_width = shutil.get_terminal_size((120, 30)).columns
    for i in range(max(len(left_lines), len(right_lines))):
        l = left_lines[i] if i < len(left_lines) else ""
        r = right_lines[i] if i < len(right_lines) else ""
        print(f"{l:<60} | {r}")

def run_analyzer():
    global last_timestamp_str, bucket_times, last_pulse_phase, last_snapshot_time
    print("Starting Multi-Symbol Optimized Analyzer...")
    try:
        while True:
            should_render = False
            try:
                quotes = fetch_quotes()
                if not quotes: time.sleep(POLL_INTERVAL); continue
                ts_str = max((q.get("timestamp") or "") for q in quotes)
                for q in quotes:
                    sym = (q.get("code") or "").upper()
                    if sym in SYMBOL_CONFIGS:
                        last_raw_prices[sym] = {"bid": round(float(q["bid"]), 5), "ask": round(float(q["ask"]), 5)}
                
                if ts_str != last_timestamp_str:
                    dt = parse_quote_timestamp(ts_str)
                    for sym, config in SYMBOL_CONFIGS.items():
                        b_time = get_bucket_time(dt, config["bucket"])
                        if b_time not in bucket_times: bucket_times.append(b_time); bucket_times.sort()
                        
                        quote = next((q for q in quotes if q["code"].upper() == sym), None)
                        if quote:
                            for side in ["bid", "ask"]:
                                p = round(float(quote[side]), 2 if "JPY" in sym else 4)
                                if b_time not in first_prices[sym][side]: first_prices[sym][side][b_time] = p
                                price_data[sym][side][p][b_time] += 1
                                
                            # Trade Detection
                            prior_b = bucket_times[bucket_times.index(b_time)-1] if bucket_times.index(b_time) > 0 else None
                            m_info = get_bucket_marker(sym, b_time, prior_b)
                            if m_info and last_trade_state_by_symbol.get(sym) != m_info["state"]:
                                if should_record_trade_event(sym, m_info, ts_str):
                                    ev = {"ts": ts_str, "symbol": sym, "event": "OPEN" if m_info["style"]=="open" else "CLOSE", "state": m_info["state"], "price": m_info["price"]}
                                    if "net_pips" in m_info: ev["net_pips"] = m_info["net_pips"]
                                    recent_trade_events.append(ev)
                                    append_trade_signal_log(ev)
                                last_trade_state_by_symbol[sym] = m_info["state"]

                    last_timestamp_str = ts_str
                    should_render = True
            except: pass
            
            if should_render: display_frequency()
            if (time.time() - last_snapshot_time) >= SNAPSHOT_INTERVAL_SECONDS: capture_snapshot()
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt: print("\nStopped.")

if __name__ == "__main__":
    run_analyzer()
