import math
import time

import psycopg2
import psycopg2.extras

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
PROCESS_INTERVAL = 10
WINDOW_SIZE = 3
WINDOW_SECONDS = 300
MODEL_VERSION = "V3_FEATURES_ONLY_20D"
VECTOR_PIP_RANGE = range(-10, 11)
VECTOR_TIME_RANGE = range(-3, 4)
NEAREST_MATCH_COUNT = 5

# Feature weights based on correlation analysis (2026-05-04)
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


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def cosine_similarity(v1, v2):
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_1 = math.sqrt(sum(a * a for a in v1))
    magnitude_2 = math.sqrt(sum(b * b for b in v2))
    if magnitude_1 == 0 or magnitude_2 == 0:
        return 0.0
    return dot_product / (magnitude_1 * magnitude_2)


def get_snapshot_levels(cur, snapshot_id):
    cur.execute(
        """
        SELECT side, price, frequency_count
        FROM frequency_levels
        WHERE snapshot_id = %s
        ORDER BY side, price
        """,
        (snapshot_id,),
    )
    return [(side, float(price), int(count)) for side, price, count in cur.fetchall()]


def get_magnet_price(levels):
    if not levels:
        return None
    best_side, best_price, best_count = max(levels, key=lambda row: (row[2], -row[1]))
    return float(best_price)


def get_snapshot_window(cur, product_id):
    cur.execute(
        """
        SELECT snapshot_id, snapshot_time
        FROM frequency_snapshots
        WHERE product_id = %s
          AND window_seconds = %s
        ORDER BY snapshot_time DESC
        LIMIT %s
        """,
        (product_id, WINDOW_SECONDS, 2 * WINDOW_SIZE + 1),
    )
    rows = cur.fetchall()
    if len(rows) < (2 * WINDOW_SIZE + 1):
        return None
    return list(reversed(rows))


def safe_ratio(numerator, denominator):
    if denominator in (0, None):
        return float(numerator) if numerator not in (None, 0) else 0.0
    return float(numerator) / float(denominator)


def build_live_vector(cur, snapshots, pip_size):
    center_snapshot_id = snapshots[WINDOW_SIZE][0]
    center_levels = get_snapshot_levels(cur, center_snapshot_id)
    candidate_turn_price = get_magnet_price(center_levels)
    if candidate_turn_price is None:
        return None

    normalised_map = {}
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

    for idx, (snapshot_id, snapshot_time) in enumerate(snapshots):
        rel_time = idx - WINDOW_SIZE
        levels = get_snapshot_levels(cur, snapshot_id)
        side_rows = {"BID": [], "ASK": []}
        for side, price, count in levels:
            side_rows[side].append((price, count))

        for side, rows in side_rows.items():
            if not rows:
                continue
            side_total = sum(count for _, count in rows)
            mean = side_total / len(rows)
            variance = sum((count - mean) ** 2 for _, count in rows) / len(rows)
            std_dev = variance ** 0.5

            for price, count in rows:
                rel_pips = int(round((price - candidate_turn_price) / pip_size))
                normalised_frequency = count / side_total if side_total else 0.0
                zscore_frequency = ((count - mean) / std_dev) if std_dev else 0.0
                normalised_map[(rel_time, side, rel_pips)] = normalised_frequency
                total_frequency += count
                weighted_sum += rel_pips * count
                relative_pips_list.append(rel_pips)
                totals_by_time[rel_time] = totals_by_time.get(rel_time, 0) + count
                if rel_pips > 0:
                    total_above += count
                elif rel_pips < 0:
                    total_below += count
                if count > peak_frequency:
                    peak_frequency = count
                    peak_relative_pips = rel_pips

                bucket = frequency_by_time.setdefault(rel_time, {})
                bucket[rel_pips] = bucket.get(rel_pips, 0) + count
                if rel_time not in magnet_freqs or bucket[rel_pips] > magnet_freqs[rel_time]:
                    magnet_freqs[rel_time] = bucket[rel_pips]
                    magnets[rel_time] = rel_pips

    cluster_width = max(relative_pips_list) - min(relative_pips_list) if relative_pips_list else 0
    cluster_skew = safe_ratio(weighted_sum, total_frequency) if total_frequency else 0.0

    magnet_t_minus_3 = magnets.get(-3, 0)
    magnet_t_minus_2 = magnets.get(-2, 0)
    magnet_t_minus_1 = magnets.get(-1, 0)
    magnet_t = magnets.get(0, 0)
    magnet_t_plus_1 = magnets.get(1, 0)
    magnet_t_plus_2 = magnets.get(2, 0)
    magnet_t_plus_3 = magnets.get(3, 0)

    magnet_shift_pre = magnet_t - magnet_t_minus_3
    magnet_shift_post = magnet_t_plus_3 - magnet_t

    failed_probe_pips = min(magnets.get(rel_time, 0) for rel_time in (-3, -2, -1))
    failed_probe_frequency = frequency_by_time.get(-1, {}).get(failed_probe_pips, 0)
    pre_turn_total = sum(totals_by_time.get(rel_time, 0) for rel_time in (-3, -2, -1))
    post_turn_total = sum(totals_by_time.get(rel_time, 0) for rel_time in (1, 2, 3))
    prior_zone_vanish_score = abs(magnet_t_minus_1 - magnet_t_plus_1) / max(cluster_width, 1)
    rebuild_score = safe_ratio(post_turn_total, pre_turn_total)
    reversal_strength_score = abs(magnet_shift_pre) + abs(magnet_shift_post)
    thin_snapshot_score = 1.0 - safe_ratio(totals_by_time.get(3, 0), max(totals_by_time.values()) if totals_by_time else 1)

    # Calculate pattern_quality_score to match feature_processor.py
    pattern_quality_score = max(
        0.0,
        rebuild_score + reversal_strength_score + (1.0 - thin_snapshot_score) - prior_zone_vanish_score,
    )

    # V3: Build weighted feature-only vector (17 dimensions)
    # Order must match feature_processor.py build_pattern_vector_v3
    raw_features = {
        "peak_frequency": float(peak_frequency),
        "peak_relative_pips": float(peak_relative_pips),
        "total_frequency": float(total_frequency),
        "total_frequency_above_turn": float(total_above),
        "total_frequency_below_turn": float(total_below),
        "above_below_ratio": float(safe_ratio(total_above, total_below)),
        "cluster_width_pips": float(cluster_width),
        "cluster_skew": float(cluster_skew),
        "magnet_shift_pre_turn_pips": float(magnet_shift_pre),
        "magnet_shift_post_turn_pips": float(magnet_shift_post),
        "failed_probe_pips": float(failed_probe_pips),
        "failed_probe_frequency": float(failed_probe_frequency),
        "prior_zone_vanish_score": float(prior_zone_vanish_score),
        "rebuild_score": float(rebuild_score),
        "reversal_strength_score": float(reversal_strength_score),
        "thin_snapshot_score": float(thin_snapshot_score),
        "pattern_quality_score": float(pattern_quality_score),
    }

    feature_order = [
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

    vector = []
    for name in feature_order:
        value = raw_features[name]
        weight = FEATURE_WEIGHTS.get(name, 1.0)
        vector.append(value * weight)

    return {
        "candidate_turn_price": candidate_turn_price,
        "vector": vector,
        "magnet_path": [magnet_t_minus_3, magnet_t_minus_2, magnet_t_minus_1, magnet_t, magnet_t_plus_1, magnet_t_plus_2, magnet_t_plus_3],
        "cluster_width": cluster_width,
        "rebuild_score": rebuild_score,
        "reversal_strength_score": reversal_strength_score,
        "thin_snapshot_score": thin_snapshot_score,
        # Additional features for direct scoring
        "cluster_width_pips": cluster_width,
        "magnet_shift_post_turn_pips": magnet_shift_post,
    }


def summarise_matches(matches, expected_turn_type):
    if not matches:
        return {
            "avg_similarity": 0.0,
            "count": 0,
            "next_5m_bias_rate": 0.0,
            "next_10m_bias_rate": 0.0,
            "avg_10m_move": 0.0,
        }

    top_matches = matches[:NEAREST_MATCH_COUNT]
    avg_similarity = sum(match["similarity"] for match in top_matches) / len(top_matches)
    if expected_turn_type == "BOTTOM":
        success_5m = sum(1 for match in top_matches if (match["outcome_5m"] or 0) > 0)
        success_10m = sum(1 for match in top_matches if (match["outcome_10m"] or 0) > 0)
        avg_10m_move = sum((match["outcome_10m"] or 0) for match in top_matches) / len(top_matches)
    else:
        success_5m = sum(1 for match in top_matches if (match["outcome_5m"] or 0) < 0)
        success_10m = sum(1 for match in top_matches if (match["outcome_10m"] or 0) < 0)
        avg_10m_move = sum((-(match["outcome_10m"] or 0)) for match in top_matches) / len(top_matches)

    return {
        "avg_similarity": round(avg_similarity, 8),
        "count": len(top_matches),
        "next_5m_bias_rate": round(success_5m / len(top_matches), 8),
        "next_10m_bias_rate": round(success_10m / len(top_matches), 8),
        "avg_10m_move": round(avg_10m_move, 4),
    }


def classify_confidence(primary_similarity, opposing_similarity):
    """Legacy similarity-based confidence (r = -0.13 with outcomes)."""
    edge = primary_similarity - opposing_similarity
    if primary_similarity >= 0.9 and edge >= 0.2:
        return "HIGH"
    if primary_similarity >= 0.75 and edge >= 0.1:
        return "MEDIUM_HIGH"
    if primary_similarity >= 0.6:
        return "MEDIUM"
    return "LOW"


def compute_predictive_score(features):
    """Direct feature scoring (r = +0.78 with outcomes).

    Based on correlation analysis 2026-05-04:
    - reversal_strength: r = +0.84
    - cluster_width: r = +0.65
    - magnet_shift_post: r = +0.44

    Returns a score where higher = more likely profitable.
    """
    reversal = float(features.get("reversal_strength_score", 0) or 0)
    width = float(features.get("cluster_width_pips", 0) or 0)
    magnet_post = float(features.get("magnet_shift_post_turn_pips", 0) or 0)

    score = (
        reversal * 5.0 +
        width * 4.0 +
        magnet_post * 3.0
    )
    return round(score, 4)


def classify_confidence_by_score(predictive_score):
    """Score-based confidence (replaces similarity-based).

    Thresholds based on observed score distribution.
    """
    if predictive_score >= 80:
        return "SCORE_HIGH"
    if predictive_score >= 50:
        return "SCORE_MEDIUM_HIGH"
    if predictive_score >= 30:
        return "SCORE_MEDIUM"
    return "SCORE_LOW"


def process_latest_snapshot(cur, product_id, product_code):
    snapshots = get_snapshot_window(cur, product_id)
    if not snapshots:
        return None

    latest_snapshot_time = snapshots[-1][1]
    cur.execute(
        """
        SELECT live_pattern_id
        FROM live_pattern_windows
        WHERE product_id = %s AND latest_snapshot_time = %s
        """,
        (product_id, latest_snapshot_time),
    )
    if cur.fetchone():
        return None

    cur.execute("SELECT pip_size FROM products WHERE product_id = %s", (product_id,))
    pip_size = float(cur.fetchone()[0])
    live_vector = build_live_vector(cur, snapshots, pip_size)
    if not live_vector:
        return None

    # Compute direct predictive score (r = +0.78 with outcomes)
    predictive_score = compute_predictive_score(live_vector)
    score_confidence = classify_confidence_by_score(predictive_score)

    cur.execute(
        """
        INSERT INTO live_pattern_windows (
            product_id,
            latest_snapshot_time,
            candidate_turn_price,
            pre_window_snapshots,
            post_window_snapshots
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING live_pattern_id
        """,
        (product_id, latest_snapshot_time, live_vector["candidate_turn_price"], WINDOW_SIZE, WINDOW_SIZE),
    )
    live_pattern_id = cur.fetchone()[0]

    cur.execute(
        """
        INSERT INTO live_pattern_vectors (
            live_pattern_id,
            vector_model_version,
            vector_dimensions,
            feature_vector
        )
        VALUES (%s, %s, %s, %s)
        """,
        (live_pattern_id, MODEL_VERSION, len(live_vector["vector"]), live_vector["vector"]),
    )

    cur.execute(
        """
        SELECT
            pv.turn_id,
            pv.turn_type,
            pv.feature_vector,
            pv.product_id,
            tp.outcome_5m_pips,
            tp.outcome_10m_pips,
            tp.outcome_15m_pips
        FROM pattern_vectors pv
        JOIN turning_points tp ON tp.turn_id = pv.turn_id
        WHERE pv.vector_model_version = %s
        """,
        (MODEL_VERSION,),
    )
    historical_vectors = cur.fetchall()

    grouped = {"BOTTOM": [], "TOP": []}
    inserted_matches = []
    for turn_id, turn_type, feature_vector, matched_product_id, outcome_5m, outcome_10m, outcome_15m in historical_vectors:
        similarity = cosine_similarity(live_vector["vector"], feature_vector)
        match = {
            "turn_id": turn_id,
            "turn_type": turn_type,
            "matched_product_id": matched_product_id,
            "similarity": similarity,
            "outcome_5m": float(outcome_5m or 0),
            "outcome_10m": float(outcome_10m or 0),
            "outcome_15m": float(outcome_15m or 0),
        }
        grouped[turn_type].append(match)
        inserted_matches.append(
            (
                live_pattern_id,
                turn_id,
                matched_product_id,
                turn_type,
                round(similarity, 8),
                round(1.0 - similarity, 8),
                outcome_5m,
                outcome_10m,
                outcome_15m,
            )
        )

    for turn_type in grouped:
        grouped[turn_type].sort(key=lambda item: item["similarity"], reverse=True)

    bottom_summary = summarise_matches(grouped["BOTTOM"], "BOTTOM")
    top_summary = summarise_matches(grouped["TOP"], "TOP")

    if bottom_summary["avg_similarity"] > top_summary["avg_similarity"]:
        candidate_type = "BOTTOM"
        direction_bias = "UP"
        primary = bottom_summary
        opposing = top_summary
    elif top_summary["avg_similarity"] > bottom_summary["avg_similarity"]:
        candidate_type = "TOP"
        direction_bias = "DOWN"
        primary = top_summary
        opposing = bottom_summary
    else:
        candidate_type = "UNKNOWN"
        direction_bias = "UNCLEAR"
        primary = bottom_summary
        opposing = top_summary

    confidence = classify_confidence(primary["avg_similarity"], opposing["avg_similarity"])
    current_state = f"{candidate_type}_BIAS" if candidate_type != "UNKNOWN" else "BALANCED"
    summary = (
        f"{product_code} {candidate_type} bottom_similarity={bottom_summary['avg_similarity']:.4f} "
        f"top_similarity={top_summary['avg_similarity']:.4f} matches={bottom_summary['count'] + top_summary['count']}"
    )

    cur.execute(
        """
        UPDATE live_pattern_windows
        SET
            candidate_type = %s,
            current_state = %s,
            direction_bias = %s,
            bottom_similarity = %s,
            top_similarity = %s,
            nearest_match_count = %s,
            historical_next_5m_bias_rate = %s,
            historical_next_10m_bias_rate = %s,
            historical_avg_10m_move_pips = %s,
            confidence_label = %s,
            summary = %s,
            predictive_score = %s,
            score_confidence_label = %s
        WHERE live_pattern_id = %s
        """,
        (
            candidate_type,
            current_state,
            direction_bias,
            bottom_summary["avg_similarity"],
            top_summary["avg_similarity"],
            primary["count"],
            primary["next_5m_bias_rate"],
            primary["next_10m_bias_rate"],
            primary["avg_10m_move"],
            confidence,
            summary,
            predictive_score,
            score_confidence,
            live_pattern_id,
        ),
    )

    psycopg2.extras.execute_values(
        cur,
        """
        INSERT INTO pattern_similarity_matches (
            live_pattern_id,
            matched_turn_id,
            matched_product_id,
            matched_turn_type,
            similarity_score,
            distance_score,
            matched_outcome_5m_pips,
            matched_outcome_10m_pips,
            matched_outcome_15m_pips
        )
        VALUES %s
        """,
        inserted_matches,
    )

    print(
        f"[{product_code}] candidate_type={candidate_type} direction_bias={direction_bias} "
        f"bottom_similarity={bottom_summary['avg_similarity']:.4f} top_similarity={top_summary['avg_similarity']:.4f} "
        f"predictive_score={predictive_score:.1f} ({score_confidence})"
    )
    return live_pattern_id


def run_engine():
    print("Starting live similarity engine...")
    while True:
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT product_id, product_code FROM products WHERE is_active = TRUE")
            products = cur.fetchall()
            for product_id, product_code in products:
                process_latest_snapshot(cur, product_id, product_code)
            conn.commit()
        except Exception as exc:
            if conn:
                conn.rollback()
            print(f"Engine error: {exc}")
        finally:
            if conn:
                cur.close()
                conn.close()
        time.sleep(PROCESS_INTERVAL)


if __name__ == "__main__":
    run_engine()
