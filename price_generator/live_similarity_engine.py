# C:\Users\edebe\eds\price_generator\live_similarity_engine.py
import psycopg2
import psycopg2.extras
import time
import math
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
PROCESS_INTERVAL = 10
WINDOW_SIZE = 3 # Matches historical window (T-3 to T+3)
MODEL_VERSION = "V1"

# ---------------------------------------------------
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def cosine_similarity(v1, v2):
    if not v1 or not v2 or len(v1) != len(v2):
        return 0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0
    return dot_product / (mag1 * mag2)

def get_magnet_price(cur, snapshot_id):
    cur.execute(
        "SELECT price FROM frequency_levels WHERE snapshot_id = %s ORDER BY frequency_count DESC LIMIT 1",
        (snapshot_id,)
    )
    row = cur.fetchone()
    return float(row[0]) if row else None

def process_latest_snapshot(cur, product_id, product_code):
    # 1. Get last 2*WINDOW_SIZE + 1 snapshots
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

    snapshots = rows[::-1] # [S0, S1, S2, S3, S4, S5, S6] where S6 is latest
    latest_snapshot_id = snapshots[-1][0]
    latest_snapshot_time = snapshots[-1][1]

    # Check if we already processed this snapshot for this product
    cur.execute(
        "SELECT live_pattern_id FROM live_pattern_windows WHERE product_id = %s AND latest_snapshot_time = %s",
        (product_id, latest_snapshot_time)
    )
    if cur.fetchone():
        return

    # 2. Candidate turn is at index WINDOW_SIZE (the middle of our rolling window)
    candidate_turn_idx = WINDOW_SIZE
    candidate_snapshot_id = snapshots[candidate_turn_idx][0]
    candidate_price = get_magnet_price(cur, candidate_snapshot_id)
    if candidate_price is None: return

    # 3. Vectorise (Magnet path relative to candidate price)
    cur.execute("SELECT pip_size FROM products WHERE product_id = %s", (product_id,))
    pip_size = float(cur.fetchone()[0])

    vector = []
    for i in range(len(snapshots)):
        s_id = snapshots[i][0]
        px = get_magnet_price(cur, s_id)
        if px is None: 
            vector.append(0.0)
        else:
            rel_pips = (px - candidate_price) / pip_size
            vector.append(float(rel_pips))

    # 4. Save Live Pattern Window
    cur.execute(
        """
        INSERT INTO live_pattern_windows (product_id, latest_snapshot_time, candidate_turn_price, pre_window_snapshots, post_window_snapshots)
        VALUES (%s, %s, %s, %s, %s) RETURNING live_pattern_id
        """,
        (product_id, latest_snapshot_time, candidate_price, WINDOW_SIZE, WINDOW_SIZE)
    )
    live_pattern_id = cur.fetchone()[0]

    # 5. Save Live Vector
    cur.execute(
        """
        INSERT INTO live_pattern_vectors (live_pattern_id, vector_model_version, vector_dimensions, feature_vector)
        VALUES (%s, %s, %s, %s)
        """,
        (live_pattern_id, MODEL_VERSION, len(vector), vector)
    )

    # 6. Compare with Historical Vectors
    cur.execute(
        """
        SELECT turn_id, turn_type, feature_vector, product_id
        FROM pattern_vectors
        WHERE vector_model_version = %s
        """,
        (MODEL_VERSION,)
    )
    hist_vectors = cur.fetchall()
    
    matches = []
    for h_turn_id, h_turn_type, h_vector, h_product_id in hist_vectors:
        sim = cosine_similarity(vector, h_vector)
        if sim > 0.7: # Threshold for match
            matches.append((live_pattern_id, h_turn_id, h_product_id, h_turn_type, sim))
    
    if matches:
        psycopg2.extras.execute_values(
            cur,
            """
            INSERT INTO pattern_similarity_matches 
            (live_pattern_id, matched_turn_id, matched_product_id, matched_turn_type, similarity_score)
            VALUES %s
            """,
            matches
        )
        print(f"[{product_code}] Found {len(matches)} historical matches for latest window.")

def run_engine():
    print(f"Starting live similarity engine...")
    while True:
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT product_id, product_code FROM products WHERE is_active = TRUE")
            products = cur.fetchall()
            
            for p_id, p_code in products:
                process_latest_snapshot(cur, p_id, p_code)
            
            conn.commit()
        except Exception as e:
            if conn: conn.rollback()
            print(f"Engine error: {e}")
        finally:
            if conn:
                cur.close()
                conn.close()
        
        time.sleep(PROCESS_INTERVAL)

if __name__ == "__main__":
    run_engine()
