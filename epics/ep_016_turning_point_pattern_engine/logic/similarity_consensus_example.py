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

def get_specific_top_example():
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    cur = conn.cursor()

    # 1. Get the latest live turn with a vector
    cur.execute("""
        SELECT t.turn_id, p.product_code, t.turn_time, t.turn_price, v.feature_vector
        FROM turning_points t
        JOIN products p ON p.product_id = t.product_id
        JOIN pattern_vectors v ON v.turn_id = t.turn_id
        JOIN frequency_snapshots s ON s.product_id = t.product_id AND s.snapshot_time = t.turn_time
        WHERE s.market_mode = 'LIVE' AND t.turn_type = 'TOP'
        ORDER BY t.turn_time DESC
        LIMIT 1
    """)
    target = cur.fetchone()
    
    if not target:
        print("No live tops with vectors found.")
        return

    print(f"Target TOP: {target['product_code']} at {target['turn_time']} (Price: {target['turn_price']})")
    target_vector = target['feature_vector']

    # 2. Find similar historical turns
    cur.execute("""
        SELECT t.turn_id, p.product_code, t.turn_time, t.turn_price, t.outcome_5m_pips, t.outcome_10m_pips, v.feature_vector
        FROM turning_points t
        JOIN products p ON p.product_id = t.product_id
        JOIN pattern_vectors v ON v.turn_id = t.turn_id
        WHERE t.turn_type = 'TOP' AND t.turn_id != %s
    """, (target['turn_id'],))
    
    candidates = cur.fetchall()
    
    matches = []
    for cand in candidates:
        sim = get_cosine_similarity(target_vector, cand['feature_vector'])
        matches.append({
            "product": cand['product_code'],
            "time": cand['turn_time'],
            "similarity": sim,
            "outcome_5m": float(cand['outcome_5m_pips'] or 0),
            "outcome_10m": float(cand['outcome_10m_pips'] or 0)
        })

    # Sort by similarity
    matches.sort(key=lambda x: x['similarity'], reverse=True)

    print("\n=== Top 5 'Similar Shape' Matches ===")
    print(f"{'Product':<12} | {'Similarity':<10} | {'Outcome 5m':<12} | {'Outcome 10m'}")
    print("-" * 60)
    for m in matches[:5]:
        print(f"{m['product']:<12} | {m['similarity']:<10.4f} | {m['outcome_5m']:<12.2f} | {m['outcome_10m']:.2f}")

    # Calculate Consensus
    top_5 = matches[:5]
    avg_sim = sum(m['similarity'] for m in top_5) / 5
    avg_out_5m = sum(m['outcome_5m'] for m in top_5) / 5
    avg_out_10m = sum(m['outcome_10m'] for m in top_5) / 5

    print("\n=== Consensus Assessment ===")
    print(f"Average Shape Similarity: {avg_sim:.4f}")
    print(f"Consensus Outcome (5m):  {avg_out_5m:.2f} pips")
    print(f"Consensus Outcome (10m): {avg_out_10m:.2f} pips")
    
    # 3. Highlight the "Problem" (High shape sim, different outcome)
    # Find a match with high sim but opposite outcome if possible
    outliers = [m for m in matches[:10] if m['outcome_5m'] > 0] # TOPS should be negative outcome
    if outliers:
        print("\n--- Insight: The 'Dynamics' Problem ---")
        print(f"Found {len(outliers)} match(es) in the top 10 similarity results with POSITIVE 5m outcomes.")
        print("Despite high 'Shape Similarity', these historical patterns did NOT reverse immediately.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    get_specific_top_example()
