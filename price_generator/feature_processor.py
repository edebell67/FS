# C:\Users\edebe\eds\price_generator\feature_processor.py
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
MODEL_VERSION = "V1"

# ---------------------------------------------------
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def generate_features(cur, turn_id):
    # 1. Get normalized levels for this turn
    cur.execute(
        """
        SELECT relative_time_index, relative_pips, frequency_count, side
        FROM normalised_pattern_levels
        WHERE turn_id = %s
        ORDER BY relative_time_index, relative_pips
        """,
        (turn_id,)
    )
    levels = cur.fetchall()
    if not levels: return

    # 2. Calculate simple features
    # Peak Frequency
    peak_freq = 0
    peak_rel_pips = 0
    total_freq = 0
    freq_above = 0
    freq_below = 0
    
    # Magnet path
    magnets = {} # rel_time -> best_pips
    max_freq_per_time = {} # rel_time -> max_freq

    rel_pips_list = []

    for rel_time, rel_pips, count, side in levels:
        total_freq += count
        if rel_pips > 0: freq_above += count
        elif rel_pips < 0: freq_below += count
        
        if count > peak_freq:
            peak_freq = count
            peak_rel_pips = rel_pips
        
        if rel_time not in max_freq_per_time or count > max_freq_per_time[rel_time]:
            max_freq_per_time[rel_time] = count
            magnets[rel_time] = rel_pips
        
        rel_pips_list.append(rel_pips)

    above_below_ratio = freq_above / freq_below if freq_below > 0 else (freq_above if freq_above > 0 else 1.0)
    cluster_width = max(rel_pips_list) - min(rel_pips_list) if rel_pips_list else 0

    # 3. Construct vector (path of magnets)
    # Window is T-3 to T+3
    vector = []
    for t in range(-3, 4):
        vector.append(float(magnets.get(t, 0))) # Default 0 if missing

    # 4. Save Features
    cur.execute(
        """
        INSERT INTO pattern_features 
        (turn_id, product_id, turn_type, peak_frequency, peak_relative_pips, total_frequency, 
         total_frequency_above_turn, total_frequency_below_turn, above_below_ratio, cluster_width_pips)
        SELECT turn_id, product_id, turn_type, %s, %s, %s, %s, %s, %s, %s
        FROM turning_points WHERE turn_id = %s
        """,
        (peak_freq, peak_rel_pips, total_freq, freq_above, freq_below, above_below_ratio, cluster_width, turn_id)
    )

    # 5. Save Vector
    cur.execute(
        """
        INSERT INTO pattern_vectors (turn_id, product_id, turn_type, vector_model_version, vector_dimensions, feature_vector)
        SELECT turn_id, product_id, turn_type, %s, %s, %s
        FROM turning_points WHERE turn_id = %s
        """,
        (MODEL_VERSION, len(vector), vector, turn_id)
    )

    # 6. Mark as completed
    cur.execute("UPDATE turning_points SET has_features = TRUE WHERE turn_id = %s", (turn_id,))

def run_features():
    print(f"Starting feature processor...")
    while True:
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT turn_id FROM turning_points WHERE is_normalized = TRUE AND has_features = FALSE")
            turns = cur.fetchall()
            
            for (t_id,) in turns:
                generate_features(cur, t_id)
                print(f"Generated features for turn {t_id}")
            
            conn.commit()
        except Exception as e:
            if conn: conn.rollback()
            print(f"Feature processor error: {e}")
        finally:
            if conn:
                cur.close()
                conn.close()
        
        time.sleep(PROCESS_INTERVAL)

if __name__ == "__main__":
    run_features()
