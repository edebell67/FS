import psycopg2
from psycopg2.extras import RealDictCursor
import numpy as np

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
DB_CONFIG = {
    "dbname": "pattern_engine",
    "user": "postgres",
    "password": "admin6093",
    "host": "localhost",
    "port": "5432",
}

def get_cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def run_specific_example():
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    cur = conn.cursor()

    # 1. Pick a recent LIVE TOP
    cur.execute("""
        SELECT t.turn_id, p.product_code, t.turn_time, t.turn_price, v.feature_vector
        FROM turning_points t
        JOIN products p ON p.product_id = t.product_id
        JOIN frequency_snapshots s ON s.product_id = t.product_id AND s.snapshot_time = t.turn_time
        JOIN pattern_vectors v ON v.turn_id = t.turn_id
        WHERE s.market_mode = 'LIVE' AND t.turn_type = 'TOP'
        ORDER BY t.turn_time DESC
        LIMIT 1
    """)
    live_top = cur.fetchone()

    if not live_top:
        print("No LIVE tops with vectors found.")
        return

    print(f"Target Pattern: {live_top['product_code']} @ {live_top['turn_time']} (Price: {live_top['turn_price']})")
    
    # 2. Find most similar historical patterns (excluding self)
    cur.execute("""
        SELECT t.turn_id, p.product_code, t.turn_time, t.turn_type, t.outcome_10m_pips, v.feature_vector
        FROM turning_points t
        JOIN products p ON p.product_id = t.product_id
        JOIN pattern_vectors v ON v.turn_id = t.turn_id
        WHERE t.turn_id != %s
    """, (live_top['turn_id'],))
    historical_candidates = cur.fetchall()

    matches = []
    target_vec = live_top['feature_vector']
    
    for cand in historical_candidates:
        sim = get_cosine_similarity(target_vec, cand['feature_vector'])
        matches.append({
            "product": cand['product_code'],
            "time": cand['turn_time'],
            "type": cand['turn_type'],
            "similarity": sim,
            "outcome_10m": cand['outcome_10m_pips']
        })

    # Sort by similarity
    matches.sort(key=lambda x: x['similarity'], reverse=True)

    print("\n=== Top 3 Matches (Shape Similarity) ===")
    print(f"{'Rank':<4} | {'Product':<10} | {'Type':<8} | {'Sim %':<10} | {'Outcome (10m)'}")
    print("-" * 60)
    for i, m in enumerate(matches[:3]):
        print(f"{i+1:<4} | {m['product']:<10} | {m['type']:<8} | {m['similarity']*100:.2f}% | {float(m['outcome_10m'] or 0):.2f} pips")

    cur.close()
    conn.close()

if __name__ == "__main__":
    run_specific_example()
