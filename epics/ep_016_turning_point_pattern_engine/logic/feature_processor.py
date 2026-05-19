import time

import psycopg2

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
PROCESS_INTERVAL = 30
MODEL_VERSION = "V3_FEATURES_ONLY_20D"
MODEL_VERSION_LEGACY = "V2_PATTERN_LIBRARY_306D"
VECTOR_PIP_RANGE = range(-10, 11)
VECTOR_TIME_RANGE = range(-3, 4)

# Feature weights based on correlation analysis (2026-05-04)
# Higher weight = stronger correlation with profitable outcomes
FEATURE_WEIGHTS = {
    "reversal_strength_score": 5.0,   # r = +0.84
    "pattern_quality_score": 5.0,      # r = +0.84
    "cluster_width_pips": 4.0,         # r = +0.65
    "magnet_shift_post_turn_pips": 3.0, # r = +0.44
    "cluster_skew": 3.0,               # r = +0.44
    "peak_relative_pips": 2.5,         # r = +0.41
    "failed_probe_pips": 2.0,          # r = +0.29
    "thin_snapshot_score": 1.5,        # r = +0.16
    "above_below_ratio": 1.0,          # r = -0.13
    "prior_zone_vanish_score": 1.0,    # r = -0.09
    "magnet_shift_pre_turn_pips": 1.0, # r = -0.08
    "rebuild_score": 1.0,              # r = -0.05
    "peak_frequency": 0.5,             # r = -0.41 (negative predictor, downweight)
    "total_frequency": 0.5,
    "total_frequency_above_turn": 0.5,
    "total_frequency_below_turn": 0.5,
    "failed_probe_frequency": 0.5,     # r = -0.28
}


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def safe_ratio(numerator, denominator):
    if denominator in (0, None):
        return float(numerator) if numerator not in (None, 0) else 0.0
    return float(numerator) / float(denominator)


def build_pattern_vector_v3(cur, turn_id):
    """Build weighted feature-only vector (V3 model).

    Drops the 294-dimension frequency matrix that was drowning out
    the predictive features. Uses only engineered features with
    weights based on correlation analysis.
    """
    cur.execute(
        """
        SELECT
            peak_frequency,
            peak_relative_pips,
            total_frequency,
            total_frequency_above_turn,
            total_frequency_below_turn,
            above_below_ratio,
            cluster_width_pips,
            cluster_skew,
            magnet_shift_pre_turn_pips,
            magnet_shift_post_turn_pips,
            failed_probe_pips,
            failed_probe_frequency,
            prior_zone_vanish_score,
            rebuild_score,
            reversal_strength_score,
            thin_snapshot_score,
            pattern_quality_score
        FROM pattern_features
        WHERE turn_id = %s
        """,
        (turn_id,),
    )
    row = cur.fetchone()
    if not row:
        return None

    feature_names = [
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

    # Build weighted vector
    vector = []
    for i, name in enumerate(feature_names):
        value = float(row[i]) if row[i] is not None else 0.0
        weight = FEATURE_WEIGHTS.get(name, 1.0)
        vector.append(value * weight)

    return vector


def build_pattern_vector(cur, turn_id):
    """Legacy V2 vector builder - kept for backward compatibility."""
    cur.execute(
        """
        SELECT relative_time_index, side, relative_pips, normalised_frequency
        FROM normalised_pattern_levels
        WHERE turn_id = %s
        """,
        (turn_id,),
    )
    normalized_rows = cur.fetchall()
    normalised_map = {
        (rel_time, side, rel_pips): float(normalised_frequency or 0.0)
        for rel_time, side, rel_pips, normalised_frequency in normalized_rows
    }

    vector = []
    for rel_time in VECTOR_TIME_RANGE:
        for rel_pips in VECTOR_PIP_RANGE:
            vector.append(normalised_map.get((rel_time, "BID", rel_pips), 0.0))
            vector.append(normalised_map.get((rel_time, "ASK", rel_pips), 0.0))

    cur.execute(
        """
        SELECT
            peak_frequency,
            peak_relative_pips,
            total_frequency,
            total_frequency_above_turn,
            total_frequency_below_turn,
            above_below_ratio,
            cluster_width_pips,
            cluster_skew,
            magnet_shift_pre_turn_pips,
            magnet_shift_post_turn_pips,
            failed_probe_pips,
            failed_probe_frequency
        FROM pattern_features
        WHERE turn_id = %s
        """,
        (turn_id,),
    )
    feature_row = cur.fetchone()
    if feature_row:
        vector.extend(float(value or 0.0) for value in feature_row)
    return vector


def build_library_profiles(cur):
    cur.execute("DELETE FROM pattern_library_profiles")

    cur.execute(
        """
        SELECT
            pv.product_id,
            p.product_type,
            pv.turn_type,
            pv.feature_vector
        FROM pattern_vectors pv
        JOIN products p ON p.product_id = pv.product_id
        WHERE pv.vector_model_version = %s
        ORDER BY pv.product_id, pv.turn_type
        """,
        (MODEL_VERSION,),
    )
    rows = cur.fetchall()
    if not rows:
        return 0

    grouped = {}
    for product_id, product_type, turn_type, feature_vector in rows:
        grouped.setdefault(("PRODUCT_ONLY", product_id, turn_type), []).append(feature_vector)
        grouped.setdefault(("PRODUCT_TYPE", product_type, turn_type), []).append(feature_vector)
        grouped.setdefault(("GLOBAL", None, turn_type), []).append(feature_vector)

    inserted = 0
    for (scope, scope_value, turn_type), vectors in grouped.items():
        dimensions = len(vectors[0])
        averaged = [
            round(sum(vector[idx] for vector in vectors) / len(vectors), 8)
            for idx in range(dimensions)
        ]
        if scope == "PRODUCT_ONLY":
            product_id = scope_value
        else:
            product_id = None

        cur.execute(
            """
            INSERT INTO pattern_library_profiles (
                product_id,
                turn_type,
                profile_scope,
                sample_count,
                vector_model_version,
                average_vector
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (product_id, turn_type, scope, len(vectors), MODEL_VERSION, averaged),
        )
        inserted += 1
    return inserted


def generate_features(cur, turn_id):
    cur.execute(
        """
        SELECT
            relative_time_index,
            relative_pips,
            frequency_count,
            side,
            normalised_frequency,
            zscore_frequency
        FROM normalised_pattern_levels
        WHERE turn_id = %s
        ORDER BY relative_time_index, side, relative_pips
        """,
        (turn_id,),
    )
    levels = cur.fetchall()
    if not levels:
        return

    peak_frequency = 0
    peak_relative_pips = 0
    total_frequency = 0
    total_above = 0
    total_below = 0
    weighted_sum = 0.0
    relative_pips_list = []

    frequency_by_time = {}
    magnets = {}
    magnet_freqs = {}
    totals_by_time = {}
    total_normalised_by_time = {}

    for rel_time, rel_pips, count, side, normalised_frequency, zscore_frequency in levels:
        count = int(count)
        relative_pips = int(rel_pips)
        total_frequency += count
        weighted_sum += relative_pips * count
        relative_pips_list.append(relative_pips)
        totals_by_time[rel_time] = totals_by_time.get(rel_time, 0) + count
        total_normalised_by_time[rel_time] = total_normalised_by_time.get(rel_time, 0.0) + float(normalised_frequency or 0.0)

        if relative_pips > 0:
            total_above += count
        elif relative_pips < 0:
            total_below += count

        if count > peak_frequency:
            peak_frequency = count
            peak_relative_pips = relative_pips

        bucket = frequency_by_time.setdefault(rel_time, {})
        bucket[relative_pips] = bucket.get(relative_pips, 0) + count
        if rel_time not in magnet_freqs or bucket[relative_pips] > magnet_freqs[rel_time]:
            magnet_freqs[rel_time] = bucket[relative_pips]
            magnets[rel_time] = relative_pips

    above_below_ratio = round(safe_ratio(total_above, total_below), 8)
    cluster_width = max(relative_pips_list) - min(relative_pips_list) if relative_pips_list else 0
    cluster_skew = round(safe_ratio(weighted_sum, total_frequency), 8) if total_frequency else 0.0

    magnet_t_minus_3 = magnets.get(-3, 0)
    magnet_t_minus_2 = magnets.get(-2, 0)
    magnet_t_minus_1 = magnets.get(-1, 0)
    magnet_t = magnets.get(0, 0)
    magnet_t_plus_1 = magnets.get(1, 0)
    magnet_t_plus_2 = magnets.get(2, 0)
    magnet_t_plus_3 = magnets.get(3, 0)

    magnet_shift_pre = round(magnet_t - magnet_t_minus_3, 4)
    magnet_shift_post = round(magnet_t_plus_3 - magnet_t, 4)

    cur.execute("SELECT turn_type FROM turning_points WHERE turn_id = %s", (turn_id,))
    turn_type = cur.fetchone()[0]
    if turn_type == "BOTTOM":
        failed_probe_pips = min(
            magnets.get(rel_time, 0)
            for rel_time in (-3, -2, -1)
        )
    else:
        failed_probe_pips = max(
            magnets.get(rel_time, 0)
            for rel_time in (-3, -2, -1)
        )
    failed_probe_frequency = frequency_by_time.get(-1, {}).get(failed_probe_pips, 0)

    pre_turn_total = sum(totals_by_time.get(rel_time, 0) for rel_time in (-3, -2, -1))
    post_turn_total = sum(totals_by_time.get(rel_time, 0) for rel_time in (1, 2, 3))
    pre_turn_norm = sum(total_normalised_by_time.get(rel_time, 0.0) for rel_time in (-3, -2, -1))
    post_turn_norm = sum(total_normalised_by_time.get(rel_time, 0.0) for rel_time in (1, 2, 3))

    prior_zone_vanish_score = round(
        abs(magnet_t_minus_1 - magnet_t_plus_1) / max(cluster_width, 1),
        8,
    )
    rebuild_score = round(safe_ratio(post_turn_total, pre_turn_total), 8)
    reversal_strength_score = round(
        abs(magnet_shift_pre) + abs(magnet_shift_post),
        8,
    )
    thin_snapshot_score = round(
        1.0 - safe_ratio(totals_by_time.get(3, 0), max(totals_by_time.values()) if totals_by_time else 1),
        8,
    )
    pattern_quality_score = round(
        max(
            0.0,
            rebuild_score + reversal_strength_score + (1.0 - thin_snapshot_score) - prior_zone_vanish_score,
        ),
        8,
    )

    cur.execute("DELETE FROM pattern_features WHERE turn_id = %s", (turn_id,))
    cur.execute("DELETE FROM pattern_vectors WHERE turn_id = %s", (turn_id,))

    cur.execute(
        """
        INSERT INTO pattern_features (
            turn_id,
            product_id,
            turn_type,
            peak_frequency,
            peak_relative_pips,
            total_frequency,
            total_frequency_above_turn,
            total_frequency_below_turn,
            above_below_ratio,
            cluster_width_pips,
            cluster_skew,
            magnet_relative_pips_t_minus_3,
            magnet_relative_pips_t_minus_2,
            magnet_relative_pips_t_minus_1,
            magnet_relative_pips_t,
            magnet_relative_pips_t_plus_1,
            magnet_relative_pips_t_plus_2,
            magnet_relative_pips_t_plus_3,
            magnet_shift_pre_turn_pips,
            magnet_shift_post_turn_pips,
            failed_probe_pips,
            failed_probe_frequency,
            prior_zone_vanish_score,
            rebuild_score,
            reversal_strength_score,
            thin_snapshot_score,
            pattern_quality_score
        )
        SELECT
            turn_id,
            product_id,
            turn_type,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        FROM turning_points
        WHERE turn_id = %s
        """,
        (
            peak_frequency,
            peak_relative_pips,
            total_frequency,
            total_above,
            total_below,
            above_below_ratio,
            cluster_width,
            cluster_skew,
            magnet_t_minus_3,
            magnet_t_minus_2,
            magnet_t_minus_1,
            magnet_t,
            magnet_t_plus_1,
            magnet_t_plus_2,
            magnet_t_plus_3,
            magnet_shift_pre,
            magnet_shift_post,
            failed_probe_pips,
            failed_probe_frequency,
            prior_zone_vanish_score,
            rebuild_score,
            reversal_strength_score,
            thin_snapshot_score,
            pattern_quality_score,
            turn_id,
        ),
    )

    # Build V3 weighted feature-only vector (17 dimensions)
    vector = build_pattern_vector_v3(cur, turn_id)
    if vector:
        cur.execute(
            """
            INSERT INTO pattern_vectors (
                turn_id,
                product_id,
                turn_type,
                vector_model_version,
                vector_dimensions,
                feature_vector
            )
            SELECT turn_id, product_id, turn_type, %s, %s, %s
            FROM turning_points
            WHERE turn_id = %s
            """,
            (MODEL_VERSION, len(vector), vector, turn_id),
        )

    cur.execute("UPDATE turning_points SET has_features = TRUE WHERE turn_id = %s", (turn_id,))


def run_features():
    print("Starting feature processor...")
    while True:
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute(
                """
                SELECT turn_id
                FROM turning_points
                WHERE is_normalized = TRUE
                  AND has_features = FALSE
                ORDER BY turn_id
                """
            )
            turns = cur.fetchall()
            for (turn_id,) in turns:
                generate_features(cur, turn_id)
                print(f"Generated features for turn {turn_id}")

            if turns:
                profile_count = build_library_profiles(cur)
                print(f"Built pattern library profiles: {profile_count}")

            conn.commit()
        except Exception as exc:
            if conn:
                conn.rollback()
            print(f"Feature processor error: {exc}")
        finally:
            if conn:
                cur.close()
                conn.close()

        time.sleep(PROCESS_INTERVAL)


if __name__ == "__main__":
    run_features()
