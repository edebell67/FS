import time
import json
from pathlib import Path
from urllib.parse import urlparse
import psycopg2
import psycopg2.extras
from urllib.request import urlopen
from collections import defaultdict
from datetime import datetime, timedelta

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
BREAKOUT_CONFIG_PATH = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\config.json")
DB_CONFIG = {
    "dbname": "pattern_engine",
    "user": "postgres",
    "password": "admin6093",
    "host": "localhost",
    "port": "5432"
}
POLL_INTERVAL = 0.5  # Seconds to poll API
SNAPSHOT_INTERVAL = 300  # Seconds to write a snapshot to DB

# ---------------------------------------------------
# Global state
# ---------------------------------------------------
# Current window accumulation: window_data[symbol][side][price] = count
window_data = defaultdict(lambda: {
    "BID": defaultdict(int),
    "ASK": defaultdict(int)
})
last_timestamp_str = None
current_bucket_start = None
current_bucket_quote_count = 0
current_bucket_source_timestamp = None
product_map = {}  # symbol -> product_id

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def load_breakout_config():
    return json.loads(BREAKOUT_CONFIG_PATH.read_text(encoding="utf-8"))

def get_market_mode():
    try:
        config = load_breakout_config()
        run_mode = str(config.get("run_mode", "sim")).strip().upper()
        return "LIVE" if run_mode == "LIVE" else "SIM"
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return "SIM"

def get_config_run_mode_key():
    return "live" if get_market_mode() == "LIVE" else "sim"

def get_active_price_source():
    try:
        config = load_breakout_config()
        endpoints_by_mode = config.get("endpoints") or {}
        endpoint_candidates = endpoints_by_mode.get(get_config_run_mode_key()) or []
        fx_endpoint = next(
            (endpoint for endpoint in endpoint_candidates if "vw_000_fx_quotes" in endpoint),
            None,
        )
        if not fx_endpoint:
            raise ValueError("FX endpoint missing from config")
        source_name = Path(urlparse(fx_endpoint).path).name
        return fx_endpoint, source_name
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        fallback_url = "http://127.0.0.1:8002/api/vw_000_fx_quotes_sim"
        fallback_source_name = "vw_000_fx_quotes_sim"
        return fallback_url, fallback_source_name

def fetch_latest_prices():
    api_source_url, _ = get_active_price_source()
    with urlopen(api_source_url, timeout=5) as response:
        return json.load(response)

def parse_quote_timestamp(timestamp_str):
    return datetime.fromisoformat(timestamp_str).replace(tzinfo=None)

def get_bucket_start(timestamp_value):
    bucket_minute = (timestamp_value.minute // 5) * 5
    return timestamp_value.replace(minute=bucket_minute, second=0, microsecond=0)

def get_bucket_end(bucket_start):
    return bucket_start + timedelta(seconds=SNAPSHOT_INTERVAL)

def get_product_id(cursor, symbol):
    symbol = symbol.upper()
    if symbol in product_map:
        return product_map[symbol]
    
    cursor.execute("SELECT product_id FROM products WHERE product_code = %s", (symbol,))
    row = cursor.fetchone()
    if row:
        product_map[symbol] = row[0]
        return row[0]
    
    # If not found, insert a default entry
    cursor.execute(
        "INSERT INTO products (product_code, product_type) VALUES (%s, 'FX') RETURNING product_id",
        (symbol,)
    )
    new_id = cursor.fetchone()[0]
    product_map[symbol] = new_id
    return new_id

def write_snapshot_to_db(snapshot_time, source_timestamp, quote_count):
    global window_data
    
    if not window_data:
        return

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        market_mode = get_market_mode()
        _, source_name = get_active_price_source()
        
        for symbol, sides in window_data.items():
            product_id = get_product_id(cur, symbol)
            window_end_time = get_bucket_end(snapshot_time)
            bucket_label = snapshot_time.strftime("%Y-%m-%d %H:%M")
            
            # 1. Insert snapshot
            cur.execute(
                """
                INSERT INTO frequency_snapshots (
                    product_id,
                    snapshot_time,
                    window_start_time,
                    window_end_time,
                    source_name,
                    source_timestamp,
                    market_mode,
                    bucket_label,
                    quote_count,
                    window_seconds
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (product_id, window_start_time, window_seconds)
                DO UPDATE SET
                    snapshot_time = EXCLUDED.snapshot_time,
                    window_end_time = EXCLUDED.window_end_time,
                    source_name = EXCLUDED.source_name,
                    source_timestamp = EXCLUDED.source_timestamp,
                    market_mode = EXCLUDED.market_mode,
                    bucket_label = EXCLUDED.bucket_label,
                    quote_count = EXCLUDED.quote_count
                RETURNING snapshot_id
                """,
                (
                    product_id,
                    snapshot_time,
                    snapshot_time,
                    window_end_time,
                    source_name,
                    source_timestamp,
                    market_mode,
                    bucket_label,
                    quote_count,
                    SNAPSHOT_INTERVAL,
                )
            )
            snapshot_id = cur.fetchone()[0]
            cur.execute("DELETE FROM frequency_levels WHERE snapshot_id = %s", (snapshot_id,))
            
            # 2. Insert frequency levels
            levels = []
            for side in ["BID", "ASK"]:
                for price, count in sides[side].items():
                    levels.append((snapshot_id, side, price, count))
            
            if levels:
                psycopg2.extras.execute_values(
                    cur,
                    "INSERT INTO frequency_levels (snapshot_id, side, price, frequency_count) VALUES %s",
                    levels
                )
        
        conn.commit()
        print(
            f"[{snapshot_time.strftime('%H:%M:%S')}] Saved snapshot for {len(window_data)} products. "
            f"source_timestamp={source_timestamp.strftime('%H:%M:%S')} quote_count={quote_count} market_mode={market_mode}"
        )
        
        # Reset window
        window_data = defaultdict(lambda: {"BID": defaultdict(int), "ASK": defaultdict(int)})

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error writing to DB: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

def run_writer():
    global current_bucket_quote_count, current_bucket_source_timestamp, current_bucket_start, last_timestamp_str
    api_source_url, source_name = get_active_price_source()
    
    print(f"Starting DB writer for {api_source_url}...")
    print(f"Resolved source_name={source_name} market_mode={get_market_mode()}")
    print(f"Snapshot interval: {SNAPSHOT_INTERVAL} seconds.")
    
    try:
        while True:
            try:
                data = fetch_latest_prices()
                quotes = data.get("data", [])
                if not quotes:
                    time.sleep(POLL_INTERVAL)
                    continue

                ts_str = max((quote.get("timestamp") or "") for quote in quotes)
                
                # Only process if it's a new update
                if ts_str != last_timestamp_str:
                    quote_timestamp = parse_quote_timestamp(ts_str)
                    bucket_start = get_bucket_start(quote_timestamp)

                    if current_bucket_start is None:
                        current_bucket_start = bucket_start
                        current_bucket_source_timestamp = quote_timestamp
                        current_bucket_quote_count = len(quotes)
                    elif bucket_start > current_bucket_start:
                        write_snapshot_to_db(
                            current_bucket_start,
                            current_bucket_source_timestamp or quote_timestamp,
                            current_bucket_quote_count,
                        )
                        current_bucket_start = bucket_start
                        current_bucket_source_timestamp = quote_timestamp
                        current_bucket_quote_count = len(quotes)
                    else:
                        current_bucket_source_timestamp = quote_timestamp
                        current_bucket_quote_count += len(quotes)

                    for quote in quotes:
                        symbol = (quote.get("code") or "").upper()
                        if not symbol:
                            continue

                        for side in ["bid", "ask"]:
                            val_raw = quote.get(side)
                            if val_raw is not None:
                                price_pip = round(val_raw, 4)
                                window_data[symbol][side.upper()][price_pip] += 1
                    
                    last_timestamp_str = ts_str

            except (json.JSONDecodeError, OSError, TimeoutError, ValueError):
                pass
            
            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nDB writer stopped.")
        print("Partial current bucket discarded on stop to preserve exact 5-minute block semantics.")

if __name__ == "__main__":
    run_writer()
