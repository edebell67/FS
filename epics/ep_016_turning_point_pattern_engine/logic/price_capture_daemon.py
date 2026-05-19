import json
import os
import time
import argparse
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
HTTP_SOURCE_URL = "http://127.0.0.1:8002/api/vw_000_fx_quotes"
POLL_INTERVAL = 1.0 # Fetch frequently to get latest prices
SNAPSHOT_INTERVAL_SECONDS = 5 # Write to file every 5 seconds

# Load config for snapshot storage path
BREAKOUT_CONFIG_PATH = Path(__file__).resolve().parents[3] / "TradeApps" / "breakout" / "fs" / "config.json"
GENERATED_DATA_ROOT = Path("X:\\EDS") # Hardcoded to match user expectation exactly

def fetch_quotes():
    try:
        with urlopen(HTTP_SOURCE_URL, timeout=5) as response:
            payload = json.load(response)
        return payload.get("data", [])
    except:
        return []

def capture_snapshot(prices):
    if not prices: return
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    # Target: TradeApps/breakout/fs/json/live/forex/YYYY-MM-DD/
    snapshot_dir = GENERATED_DATA_ROOT / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex" / date_str
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    snapshot_file = snapshot_dir / "_price_capture.jsonl"
    
    snapshot_data = {"ts": now.isoformat()}
    snapshot_data.update(prices)
    
    try:
        with open(snapshot_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(snapshot_data) + "\n")
        return True
    except OSError as e:
        print(f"File Error: {e}")
        return False

def run_daemon():
    print("--- EPIC 016 PRICE CAPTURE DAEMON ---")
    print(f"Target Root: {GENERATED_DATA_ROOT}")
    print(f"Frequency: {SNAPSHOT_INTERVAL_SECONDS}s")
    print("-------------------------------------")
    
    last_snapshot_time = 0
    last_raw_prices = {}
    
    try:
        while True:
            quotes = fetch_quotes()
            if quotes:
                # Update latest prices for all symbols
                for q in quotes:
                    sym = (q.get("code") or "").upper()
                    last_raw_prices[sym] = {"bid": round(float(q["bid"]), 5), "ask": round(float(q["ask"]), 4 if "JPY" not in sym else 2)}
            
            # Check if it's time to write to the file
            now_time = time.time()
            if (now_time - last_snapshot_time) >= SNAPSHOT_INTERVAL_SECONDS:
                if capture_snapshot(last_raw_prices):
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] Snapshot captured ({len(last_raw_prices)} symbols)")
                    last_snapshot_time = now_time
            
            time.sleep(POLL_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nDaemon stopped by user.")

if __name__ == "__main__":
    run_daemon()
