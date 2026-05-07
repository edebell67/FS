import os
import time
import json
from collections import defaultdict
from datetime import datetime

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
# [V20260502_1255] Add 5-minute time buckets as columns
JSON_SOURCE_PATH = r"z:\algo_forex\prices\forex_price_sim.json"
POLL_INTERVAL = 0.5
BUCKET_MINUTES = 5
MAX_COLUMNS = 6  # Show last 30 minutes (6 buckets)

# ---------------------------------------------------
# Global state
# ---------------------------------------------------
# data[symbol][side][price][bucket_time] = count
# bucket_time is HH:MM string of the interval start
price_data = defaultdict(lambda: {
    "bid": defaultdict(lambda: defaultdict(int)),
    "ask": defaultdict(lambda: defaultdict(int))
})
bucket_times = []
last_timestamp_str = None

# ---------------------------------------------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_bucket_time(dt):
    """Align datetime to the start of the 5-minute bucket."""
    minute = (dt.minute // BUCKET_MINUTES) * BUCKET_MINUTES
    return dt.replace(minute=minute, second=0, microsecond=0).strftime("%H:%M")

def display_frequency():
    clear_screen()
    print(f"--- Price Frequency Analyzer (5-Min Buckets) ---")
    print(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Source: {JSON_SOURCE_PATH}")
    print("-" * 80)

    # Focus on symbols, starting with GBP
    symbols = sorted(price_data.keys())
    if "gbp" in symbols:
        symbols.remove("gbp")
        symbols.insert(0, "gbp")

    # Determine which buckets to show
    recent_buckets = bucket_times[-MAX_COLUMNS:]
    
    for symbol in symbols:
        print(f"\n[{symbol.upper()}]")
        
        for side in ["bid", "ask"]:
            print(f"\n  {side.upper()} Cluster History:")
            
            # Header row
            header = f"    Price    |" + "|".join([f" {b} " for b in recent_buckets])
            print(header)
            print("    " + "-" * len(header))
            
            # Get all unique prices for this symbol/side
            all_prices = sorted(price_data[symbol][side].keys(), reverse=True)
            
            # To keep display manageable, we show a sliding window of prices around the current price
            # but for now, we show all as requested
            for price in all_prices:
                row = f"    {price:.4f} |"
                has_data_in_view = False
                for b in recent_buckets:
                    count = price_data[symbol][side][price].get(b, 0)
                    cell = f" {count:3} " if count > 0 else "  -  "
                    row += f"{cell}|"
                    if count > 0:
                        has_data_in_view = True
                
                if has_data_in_view:
                    print(row)

def run_analyzer():
    global last_timestamp_str, bucket_times
    print(f"Starting analyzer on {JSON_SOURCE_PATH}...")
    
    try:
        while True:
            if not os.path.exists(JSON_SOURCE_PATH):
                time.sleep(1)
                continue

            try:
                with open(JSON_SOURCE_PATH, "r") as f:
                    data = json.load(f)
                
                ts_str = data.get("timestamp")
                
                # Only process if it's a new snapshot
                if ts_str != last_timestamp_str:
                    # Parse timestamp to find its bucket
                    try:
                        dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S.%f")
                    except ValueError:
                        dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                    
                    b_time = get_bucket_time(dt)
                    if b_time not in bucket_times:
                        bucket_times.append(b_time)
                        bucket_times = sorted(bucket_times) # Ensure chronological order
                    
                    prices = data.get("prices", {})
                    for symbol, px in prices.items():
                        for side in ["bid", "ask"]:
                            val_raw = px.get(side)
                            if val_raw is not None:
                                price_pip = round(val_raw, 4)
                                price_data[symbol][side][price_pip][b_time] += 1
                    
                    last_timestamp_str = ts_str
                    display_frequency()

            except (json.JSONDecodeError, PermissionError, IOError):
                pass
            
            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nAnalyzer stopped.")

# ---------------------------------------------------
if __name__ == "__main__":
    run_analyzer()
