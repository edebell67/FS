# C:\Users\edebe\eds\price_generator\turning_point_processor.py
import psycopg2
import time
from datetime import datetime

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
DB_CONFIG = {
    "dbname": "pattern_engine",
    "user": "postgres",
    "password": "admin6093",
    "host": "localhost",
    "port": "5432"
}
PROCESS_INTERVAL = 30  # Seconds to check for new turns
WINDOW_SIZE = 3        # Number of snapshots before and after to check (T-3 to T+3)
CONFIRMATION_PIPS = 5  # Min move to confirm a turn (pips)

# ---------------------------------------------------
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_magnet_price(cur, snapshot_id):
    """Returns the price with the highest frequency in a snapshot."""
    cur.execute(
        "SELECT price FROM frequency_levels WHERE snapshot_id = %s ORDER BY frequency_count DESC LIMIT 1",
        (snapshot_id,)
    )
    row = cur.fetchone()
    return row[0] if row else None

def process_product_turns(cur, product_id, product_code):
    # 1. Get recent snapshots that haven't been processed for turns yet
    # For simplicity, we just look at the last N+1 snapshots and try to label the one at index - (N+1)
    cur.execute(
        """
        SELECT snapshot_id, snapshot_time 
        FROM frequency_snapshots 
        WHERE product_id = %s 
        ORDER BY snapshot_time DESC 
        LIMIT %s
        """,
        (product_id, 2 * WINDOW_SIZE + 1)
    )
    rows = cur.fetchall()
    if len(rows) < 2 * WINDOW_SIZE + 1:
        return

    # rows are in DESC order: [T+3, T+2, T+1, T, T-1, T-2, T-3]
    # We want to check if T is a turning point.
    snapshots = rows[::-1] # [T-3, T-2, T-1, T, T+1, T+2, T+3]
    
    magnet_prices = []
    for s_id, s_time in snapshots:
        px = get_magnet_price(cur, s_id)
        if px is None: return
        magnet_prices.append(float(px))

    # T is at index WINDOW_SIZE
    t_idx = WINDOW_SIZE
    t_price = magnet_prices[t_idx]
    t_id = snapshots[t_idx][0]
    t_time = snapshots[t_idx][1]

    # Check for BOTTOM
    is_bottom = True
    for i in range(len(magnet_prices)):
        if i == t_idx: continue
        if magnet_prices[i] < t_price:
            is_bottom = False
            break
    
    # Confirmation: T+3 must be at least K pips higher than T
    # Assume 1 pip = 0.0001 for now, or get from products table
    cur.execute("SELECT pip_size FROM products WHERE product_id = %s", (product_id,))
    pip_size = float(cur.fetchone()[0])
    
    if is_bottom:
        if (magnet_prices[-1] - t_price) >= (CONFIRMATION_PIPS * pip_size):
            save_turn(cur, product_id, t_time, 'BOTTOM', t_price, snapshots)
            return

    # Check for TOP
    is_top = True
    for i in range(len(magnet_prices)):
        if i == t_idx: continue
        if magnet_prices[i] > t_price:
            is_top = False
            break
            
    if is_top:
        if (t_price - magnet_prices[-1]) >= (CONFIRMATION_PIPS * pip_size):
            save_turn(cur, product_id, t_time, 'TOP', t_price, snapshots)
            return

def save_turn(cur, product_id, turn_time, turn_type, turn_price, snapshots):
    try:
        # Check if already exists
        cur.execute(
            "SELECT turn_id FROM turning_points WHERE product_id = %s AND turn_time = %s AND turn_type = %s",
            (product_id, turn_time, turn_type)
        )
        if cur.fetchone():
            return

        cur.execute(
            """
            INSERT INTO turning_points (product_id, turn_time, turn_type, turn_price, confirmation_method)
            VALUES (%s, %s, %s, %s, %s) RETURNING turn_id
            """,
            (product_id, turn_time, turn_type, turn_price, f'Magnet Window {WINDOW_SIZE}')
        )
        turn_id = cur.fetchone()[0]

        # Save windows
        for i, (s_id, s_time) in enumerate(snapshots):
            relative_idx = i - WINDOW_SIZE
            cur.execute(
                "INSERT INTO turning_point_windows (turn_id, snapshot_id, relative_time_index) VALUES (%s, %s, %s)",
                (turn_id, s_id, relative_idx)
            )
        
        print(f"Detected {turn_type} for product {product_id} at {turn_time} (Price: {turn_price})")
    except Exception as e:
        print(f"Error saving turn: {e}")

def run_processor():
    print(f"Starting turning point processor...")
    while True:
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT product_id, product_code FROM products WHERE is_active = TRUE")
            products = cur.fetchall()
            
            for p_id, p_code in products:
                process_product_turns(cur, p_id, p_code)
            
            conn.commit()
        except Exception as e:
            if conn: conn.rollback()
            print(f"Processor error: {e}")
        finally:
            if conn:
                cur.close()
                conn.close()
        
        time.sleep(PROCESS_INTERVAL)

if __name__ == "__main__":
    run_processor()
