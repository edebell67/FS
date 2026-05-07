# C:\Users\edebe\eds\price_generator\price_frequency_db_writer.py
import os
import time
import json
import psycopg2
from collections import defaultdict
from datetime import datetime

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
JSON_SOURCE_PATH = r"z:\algo_forex\prices\forex_price_sim.json"
DB_CONFIG = {
    "dbname": "pattern_engine",
    "user": "postgres",
    "password": "admin6093",
    "host": "localhost",
    "port": "5432"
}
POLL_INTERVAL = 0.5  # Seconds to poll JSON
SNAPSHOT_INTERVAL = 60  # Seconds to write a snapshot to DB

# ---------------------------------------------------
# Global state
# ---------------------------------------------------
# Current window accumulation: window_data[symbol][side][price] = count
window_data = defaultdict(lambda: {
    "BID": defaultdict(int),
    "ASK": defaultdict(int)
})
last_timestamp_str = None
last_snapshot_time = time.time()
product_map = {}  # symbol -> product_id

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

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

def write_snapshot_to_db():
    global window_data, last_snapshot_time
    
    if not window_data:
        return

    now = datetime.now()
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        for symbol, sides in window_data.items():
            product_id = get_product_id(cur, symbol)
            
            # 1. Insert snapshot
            cur.execute(
                "INSERT INTO frequency_snapshots (product_id, snapshot_time, window_seconds) VALUES (%s, %s, %s) RETURNING snapshot_id",
                (product_id, now, SNAPSHOT_INTERVAL)
            )
            snapshot_id = cur.fetchone()[0]
            
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
        print(f"[{now.strftime('%H:%M:%S')}] Saved snapshot for {len(window_data)} products.")
        
        # Reset window
        window_data = defaultdict(lambda: {"BID": defaultdict(int), "ASK": defaultdict(int)})
        last_snapshot_time = time.time()

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error writing to DB: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

def run_writer():
    global last_timestamp_str
    import psycopg2.extras # For execute_values
    
    print(f"Starting DB writer for {JSON_SOURCE_PATH}...")
    print(f"Snapshot interval: {SNAPSHOT_INTERVAL} seconds.")
    
    try:
        while True:
            # Check if it's time for a snapshot
            if time.time() - last_snapshot_time >= SNAPSHOT_INTERVAL:
                write_snapshot_to_db()

            if not os.path.exists(JSON_SOURCE_PATH):
                time.sleep(1)
                continue

            try:
                with open(JSON_SOURCE_PATH, "r") as f:
                    data = json.load(f)
                
                ts_str = data.get("timestamp")
                
                # Only process if it's a new update
                if ts_str != last_timestamp_str:
                    prices = data.get("prices", {})
                    for symbol, px in prices.items():
                        for side in ["bid", "ask"]:
                            val_raw = px.get(side)
                            if val_raw is not None:
                                price_pip = round(val_raw, 4)
                                window_data[symbol][side.upper()][price_pip] += 1
                    
                    last_timestamp_str = ts_str

            except (json.JSONDecodeError, PermissionError, IOError):
                pass
            
            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nDB writer stopped.")
        # Attempt to write final snapshot
        write_snapshot_to_db()

if __name__ == "__main__":
    run_writer()
