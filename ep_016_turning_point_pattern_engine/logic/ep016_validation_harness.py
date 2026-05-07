import sys

import psycopg2

DB_CONFIG = {
    "dbname": "pattern_engine",
    "user": "postgres",
    "password": "admin6093",
    "host": "localhost",
    "port": "5432",
}


def require(condition, message):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {message}")
    if not condition:
        raise AssertionError(message)


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM frequency_snapshots
        WHERE window_seconds = 300
          AND window_start_time IS NOT NULL
          AND window_end_time IS NOT NULL
          AND source_name IS NOT NULL
          AND source_timestamp IS NOT NULL
          AND bucket_label IS NOT NULL
        """
    )
    require(cur.fetchone()[0] > 0, "300-second snapshots store explicit window/source metadata")

    cur.execute(
        """
        SELECT COUNT(*)
        FROM turning_points
        WHERE confirmation_delay_snapshots IS NOT NULL
          AND confirmation_delay_minutes IS NOT NULL
          AND outcome_5m_pips IS NOT NULL
          AND outcome_10m_pips IS NOT NULL
        """
    )
    require(cur.fetchone()[0] >= 2, "turn detection populated delay and outcome fields")

    cur.execute(
        """
        SELECT COUNT(*)
        FROM normalised_pattern_levels
        WHERE normalised_frequency IS NOT NULL
          AND zscore_frequency IS NOT NULL
        """
    )
    require(cur.fetchone()[0] > 0, "normalized pattern rows include normalized frequency and z-score")

    cur.execute("SELECT COUNT(*) FROM pattern_features")
    require(cur.fetchone()[0] >= 2, "pattern features are populated")

    cur.execute(
        """
        SELECT COUNT(*)
        FROM pattern_vectors
        WHERE vector_model_version = 'V2_PATTERN_LIBRARY_306D'
          AND vector_dimensions = 306
        """
    )
    require(cur.fetchone()[0] >= 2, "historical vectors use the 306-dimensional V2 model")

    cur.execute("SELECT COUNT(*) FROM pattern_library_profiles")
    require(cur.fetchone()[0] > 0, "pattern library profiles are populated")

    cur.execute(
        """
        SELECT COUNT(*)
        FROM live_pattern_windows
        WHERE candidate_type IS NOT NULL
          AND direction_bias IS NOT NULL
          AND bottom_similarity IS NOT NULL
          AND top_similarity IS NOT NULL
          AND confidence_label IS NOT NULL
        """
    )
    require(cur.fetchone()[0] >= 2, "live pattern windows persist richer scoring fields")

    cur.execute("SELECT COUNT(*) FROM product_relationships")
    require(cur.fetchone()[0] > 0, "cross-product historical relationships are populated")

    cur.execute("SELECT COUNT(*) FROM cross_product_pattern_events")
    require(cur.fetchone()[0] > 0, "cross-product live events are populated")

    cur.execute("SELECT COUNT(*) FROM cross_product_event_members")
    require(cur.fetchone()[0] >= 2, "cross-product event members are populated")

    cur.close()
    conn.close()
    print("EP016 validation harness: PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"EP016 validation harness: FAIL ({exc})")
        sys.exit(1)
