"""One-time script to regenerate all pattern vectors with V3 model.

Run this once after updating feature_processor.py to rebuild the
historical pattern library with weighted features.
"""
import psycopg2

DB_CONFIG = {
    "dbname": "pattern_engine",
    "user": "postgres",
    "password": "admin6093",
    "host": "localhost",
    "port": "5432",
}

MODEL_VERSION = "V3_FEATURES_ONLY_20D"

FEATURE_WEIGHTS = {
    "reversal_strength_score": 5.0,
    "pattern_quality_score": 5.0,
    "cluster_width_pips": 4.0,
    "magnet_shift_post_turn_pips": 3.0,
    "cluster_skew": 3.0,
    "peak_relative_pips": 2.5,
    "failed_probe_pips": 2.0,
    "thin_snapshot_score": 1.5,
    "above_below_ratio": 1.0,
    "prior_zone_vanish_score": 1.0,
    "magnet_shift_pre_turn_pips": 1.0,
    "rebuild_score": 1.0,
    "peak_frequency": 0.5,
    "total_frequency": 0.5,
    "total_frequency_above_turn": 0.5,
    "total_frequency_below_turn": 0.5,
    "failed_probe_frequency": 0.5,
}

FEATURE_ORDER = [
    "peak_frequency",
    "peak_relative_pips",
    "total_frequency",
    "total_frequency_above_turn",
    "total_frequency_below_turn",
    "above_below_ratio",
    "cluster_width_pips",
    "cluster_skew",
    "magnet_shift_pre_turn_pips",
    "magnet_shift_post_turn_pips",
    "failed_probe_pips",
    "failed_probe_frequency",
    "prior_zone_vanish_score",
    "rebuild_score",
    "reversal_strength_score",
    "thin_snapshot_score",
    "pattern_quality_score",
]


def build_v3_vector(row):
    """Build weighted V3 vector from feature row."""
    vector = []
    for i, name in enumerate(FEATURE_ORDER):
        value = float(row[i]) if row[i] is not None else 0.0
        weight = FEATURE_WEIGHTS.get(name, 1.0)
        vector.append(value * weight)
    return vector


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Count existing turns with features
    cur.execute("SELECT COUNT(*) FROM pattern_features")
    total = cur.fetchone()[0]
    print(f"Found {total} turns with features")

    # Delete old V3 vectors (if any from previous runs)
    cur.execute(
        "DELETE FROM pattern_vectors WHERE vector_model_version = %s",
        (MODEL_VERSION,)
    )
    deleted = cur.rowcount
    print(f"Deleted {deleted} existing V3 vectors")

    # Get all turns with features
    cur.execute("""
        SELECT
            f.turn_id,
            t.product_id,
            t.turn_type,
            f.peak_frequency,
            f.peak_relative_pips,
            f.total_frequency,
            f.total_frequency_above_turn,
            f.total_frequency_below_turn,
            f.above_below_ratio,
            f.cluster_width_pips,
            f.cluster_skew,
            f.magnet_shift_pre_turn_pips,
            f.magnet_shift_post_turn_pips,
            f.failed_probe_pips,
            f.failed_probe_frequency,
            f.prior_zone_vanish_score,
            f.rebuild_score,
            f.reversal_strength_score,
            f.thin_snapshot_score,
            f.pattern_quality_score
        FROM pattern_features f
        JOIN turning_points t ON t.turn_id = f.turn_id
        ORDER BY f.turn_id
    """)

    rows = cur.fetchall()
    inserted = 0

    for row in rows:
        turn_id = row[0]
        product_id = row[1]
        turn_type = row[2]
        feature_values = row[3:]

        vector = build_v3_vector(feature_values)

        cur.execute("""
            INSERT INTO pattern_vectors (
                turn_id, product_id, turn_type,
                vector_model_version, vector_dimensions, feature_vector
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (turn_id, product_id, turn_type, MODEL_VERSION, len(vector), vector))

        inserted += 1
        if inserted % 50 == 0:
            print(f"  Processed {inserted}/{total} vectors...")

    conn.commit()
    print(f"Inserted {inserted} V3 vectors")

    # Rebuild library profiles
    print("Rebuilding library profiles...")
    cur.execute("DELETE FROM pattern_library_profiles")

    cur.execute("""
        SELECT
            pv.product_id,
            p.product_type,
            pv.turn_type,
            pv.feature_vector
        FROM pattern_vectors pv
        JOIN products p ON p.product_id = pv.product_id
        WHERE pv.vector_model_version = %s
        ORDER BY pv.product_id, pv.turn_type
    """, (MODEL_VERSION,))

    rows = cur.fetchall()
    grouped = {}
    for product_id, product_type, turn_type, feature_vector in rows:
        grouped.setdefault(("PRODUCT_ONLY", product_id, turn_type), []).append(feature_vector)
        grouped.setdefault(("PRODUCT_TYPE", product_type, turn_type), []).append(feature_vector)
        grouped.setdefault(("GLOBAL", None, turn_type), []).append(feature_vector)

    profile_count = 0
    for (scope, scope_value, turn_type), vectors in grouped.items():
        dimensions = len(vectors[0])
        averaged = [
            round(sum(v[i] for v in vectors) / len(vectors), 8)
            for i in range(dimensions)
        ]
        product_id = scope_value if scope == "PRODUCT_ONLY" else None

        cur.execute("""
            INSERT INTO pattern_library_profiles (
                product_id, turn_type, profile_scope,
                sample_count, vector_model_version, average_vector
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (product_id, turn_type, scope, len(vectors), MODEL_VERSION, averaged))
        profile_count += 1

    conn.commit()
    print(f"Created {profile_count} library profiles")

    cur.close()
    conn.close()
    print("Done!")


if __name__ == "__main__":
    main()
