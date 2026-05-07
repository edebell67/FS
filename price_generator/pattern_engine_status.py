# C:\Users\edebe\eds\price_generator\pattern_engine_status.py
import psycopg2
import time
import os
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

# ---------------------------------------------------
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_latest_status():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. Get products
    cur.execute("SELECT product_id, product_code FROM products WHERE is_active = TRUE")
    products = cur.fetchall()
    
    clear_screen()
    print(f"=== Turning-Point Pattern Engine Status ===")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 50)
    
    for p_id, p_code in products:
        print(f"\n[{p_code}]")
        
        # Latest live pattern
        cur.execute(
            """
            SELECT live_pattern_id, latest_snapshot_time, candidate_turn_price 
            FROM live_pattern_windows 
            WHERE product_id = %s 
            ORDER BY latest_snapshot_time DESC LIMIT 1
            """,
            (p_id,)
        )
        row = cur.fetchone()
        if not row:
            print("  No live data processed yet.")
            continue
            
        lp_id, ts, price = row
        print(f"  Last window: {ts.strftime('%H:%M:%S')} (Price: {price:.4f})")
        
        # Matches
        cur.execute(
            """
            SELECT matched_turn_type, AVG(similarity_score), COUNT(*)
            FROM pattern_similarity_matches
            WHERE live_pattern_id = %s
            GROUP BY matched_turn_type
            """,
            (lp_id,)
        )
        matches = cur.fetchall()
        if matches:
            for m_type, avg_sim, count in matches:
                print(f"  - {m_type} Similarity: {avg_sim*100:.1f}% (Matches: {count})")
        else:
            print("  - No historical matches found (>70%).")
            
        # Database Stats
        cur.execute("SELECT COUNT(*) FROM turning_points WHERE product_id = %s", (p_id,))
        turn_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM frequency_snapshots WHERE product_id = %s", (p_id,))
        snap_count = cur.fetchone()[0]
        print(f"  Database: {snap_count} snapshots, {turn_count} confirmed turns.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    try:
        while True:
            get_latest_status()
            time.sleep(5)
    except KeyboardInterrupt:
        pass
