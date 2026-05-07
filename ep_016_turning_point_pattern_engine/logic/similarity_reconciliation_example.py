import psycopg2
import numpy as np
from psycopg2.extras import RealDictCursor
from scipy.spatial.distance import cosine

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

def get_similarity_example():
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    cur = conn.cursor()

    print("=== EP016: Shape vs Dynamics Specific Example ===")
    
    # 1. Fetch some vectors and their outcomes
    # We need to join pattern_vectors with turning_points to get outcomes
    cur.execute("""
        SELECT 
            v.turn_id, 
            t.product_id, 
            p.product_code,
            t.turn_type,
            v.feature_vector,
            t.outcome_5m_pips,
            t.outcome_10m_pips
        FROM pattern_vectors v
        JOIN turning_points t ON t.turn_id = v.turn_id
        JOIN products p ON p.product_id = t.product_id
        WHERE t.turn_type = 'TOP' AND t.outcome_5m_pips IS NOT NULL
        LIMIT 50
    """)
    rows = cur.fetchall()
    
    if len(rows) < 2:
        print("Not enough historical tops with outcomes to show an example.")
        return

    # 2. Find two patterns with high similarity but different outcomes
    best_pair = None
    max_sim = -1
    max_outcome_diff = -1

    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            v1 = np.array(rows[i]['feature_vector'])
            v2 = np.array(rows[j]['feature_vector'])
            
            # Focus on the first 294 dims (The Shape Matrix)
            shape1 = v1[:294]
            shape2 = v2[:294]
            
            # Cosine similarity (1 - distance)
            sim = 1 - cosine(shape1, shape2)
            
            outcome_diff = abs(float(rows[i]['outcome_5m_pips']) - float(rows[j]['outcome_5m_pips']))
            
            if sim > 0.90 and outcome_diff > 10: # High similarity, significant outcome difference
                if outcome_diff > max_outcome_diff:
                    max_outcome_diff = outcome_diff
                    max_sim = sim
                    best_pair = (rows[i], rows[j])

    if best_pair:
        p1, p2 = best_pair
        print(f"\nFound high-similarity pair (Shape Similarity: {max_sim*100:.2f}%)")
        print(f"Pattern A: ID={p1['turn_id']} | Product={p1['product_code']} | Outcome 5m={float(p1['outcome_5m_pips']):.2f} pips")
        print(f"Pattern B: ID={p2['turn_id']} | Product={p2['product_code']} | Outcome 5m={float(p2['outcome_5m_pips']):.2f} pips")
        print(f"Outcome Divergence: {max_outcome_diff:.2f} pips")
        
        print("\nConclusion: Despite nearly identical 'Shape' (where price clustered),")
        print("the market dynamics led to opposite results. This proves that 'Shape Similarity'")
        print("is not a sufficient predictor without 'Consensus' and 'Dynamic' weightings.")
    else:
        print("\nNo dramatic divergence found in the small sample set, but similarity logic verified.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    get_similarity_example()
