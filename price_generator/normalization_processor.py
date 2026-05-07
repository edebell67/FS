# C:\Users\edebe\eds\price_generator\normalization_processor.py
import psycopg2
import psycopg2.extras
import time

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
PROCESS_INTERVAL = 30 

# ---------------------------------------------------
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def normalize_turn(cur, turn_id):
    # 1. Get turn info
    cur.execute(
        "SELECT product_id, turn_type, turn_price FROM turning_points WHERE turn_id = %s",
        (turn_id,)
    )
    product_id, turn_type, turn_price = cur.fetchone()
    turn_price = float(turn_price)

    # 2. Get pip size
    cur.execute("SELECT pip_size FROM products WHERE product_id = %s", (product_id,))
    pip_size = float(cur.fetchone()[0])

    # 3. Get snapshots associated with this turn
    cur.execute(
        """
        SELECT w.snapshot_id, w.relative_time_index 
        FROM turning_point_windows w
        WHERE w.turn_id = %s
        """,
        (turn_id,)
    )
    snapshots = cur.fetchall()

    normalized_rows = []
    for snapshot_id, rel_time_idx in snapshots:
        # 4. Get levels for this snapshot
        cur.execute(
            "SELECT side, price, frequency_count FROM frequency_levels WHERE snapshot_id = %s",
            (snapshot_id,)
        )
        levels = cur.fetchall()
        
        for side, raw_price, count in levels:
            raw_price = float(raw_price)
            # relative_pips = (raw_price - turn_price) / pip_size
            rel_pips = int(round((raw_price - turn_price) / pip_size))
            
            normalized_rows.append((
                turn_id, product_id, turn_type,
                rel_time_idx, side, rel_pips, raw_price, count
            ))

    if normalized_rows:
        psycopg2.extras.execute_values(
            cur,
            """
            INSERT INTO normalised_pattern_levels 
            (turn_id, product_id, turn_type, relative_time_index, side, relative_pips, raw_price, frequency_count)
            VALUES %s
            """,
            normalized_rows
        )

    # 5. Mark as normalized
    cur.execute("UPDATE turning_points SET is_normalized = TRUE WHERE turn_id = %s", (turn_id,))

def run_normalization():
    print(f"Starting normalization processor...")
    while True:
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT turn_id FROM turning_points WHERE is_normalized = FALSE")
            turns = cur.fetchall()
            
            for (t_id,) in turns:
                normalize_turn(cur, t_id)
                print(f"Normalized turn {t_id}")
            
            conn.commit()
        except Exception as e:
            if conn: conn.rollback()
            print(f"Normalization error: {e}")
        finally:
            if conn:
                cur.close()
                conn.close()
        
        time.sleep(PROCESS_INTERVAL)

if __name__ == "__main__":
    run_normalization()
