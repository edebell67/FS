from collections import Counter
from datetime import timedelta
import time

import psycopg2
import psycopg2.extras

DB_CONFIG = {
    "dbname": "pattern_engine",
    "user": "postgres",
    "password": "admin6093",
    "host": "localhost",
    "port": "5432",
}
PROCESS_INTERVAL = 30
MAX_LAG_MINUTES = 15


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def load_turns(cur):
    cur.execute(
        """
        SELECT turn_id, product_id, turn_time, turn_type
        FROM turning_points
        ORDER BY product_id, turn_time
        """
    )
    rows = cur.fetchall()
    turns_by_product = {}
    for turn_id, product_id, turn_time, turn_type in rows:
        turns_by_product.setdefault(product_id, []).append(
            {
                "turn_id": turn_id,
                "turn_time": turn_time,
                "turn_type": turn_type,
            }
        )
    return turns_by_product


def build_relationships(cur):
    cur.execute("DELETE FROM product_relationships")
    turns_by_product = load_turns(cur)
    product_ids = sorted(turns_by_product)
    inserted = 0

    for product_a in product_ids:
        for product_b in product_ids:
            if product_a == product_b:
                continue

            same_direction_total = 0
            inverse_direction_total = 0
            lag_counter = Counter()

            for turn_a in turns_by_product.get(product_a, []):
                for turn_b in turns_by_product.get(product_b, []):
                    lag_minutes = int((turn_b["turn_time"] - turn_a["turn_time"]).total_seconds() / 60)
                    if abs(lag_minutes) > MAX_LAG_MINUTES:
                        continue

                    if turn_a["turn_type"] == turn_b["turn_type"]:
                        same_direction_total += 1
                        if lag_minutes > 0:
                            lag_counter[lag_minutes] += 1
                    else:
                        inverse_direction_total += 1

            sample_count = same_direction_total + inverse_direction_total
            if sample_count == 0:
                continue

            same_direction_rate = round(same_direction_total / sample_count, 8)
            inverse_direction_rate = round(inverse_direction_total / sample_count, 8)

            if same_direction_total:
                cur.execute(
                    """
                    INSERT INTO product_relationships (
                        product_a_id,
                        product_b_id,
                        relationship_type,
                        best_lag_minutes,
                        same_direction_rate,
                        inverse_direction_rate,
                        lead_lag_confidence,
                        sample_count
                    )
                    VALUES (%s, %s, 'SAME_DIRECTION', %s, %s, %s, %s, %s)
                    """,
                    (
                        product_a,
                        product_b,
                        0,
                        same_direction_rate,
                        inverse_direction_rate,
                        same_direction_rate,
                        sample_count,
                    ),
                )
                inserted += 1

            if inverse_direction_total:
                cur.execute(
                    """
                    INSERT INTO product_relationships (
                        product_a_id,
                        product_b_id,
                        relationship_type,
                        best_lag_minutes,
                        same_direction_rate,
                        inverse_direction_rate,
                        lead_lag_confidence,
                        sample_count
                    )
                    VALUES (%s, %s, 'INVERSE_DIRECTION', %s, %s, %s, %s, %s)
                    """,
                    (
                        product_a,
                        product_b,
                        0,
                        same_direction_rate,
                        inverse_direction_rate,
                        inverse_direction_rate,
                        sample_count,
                    ),
                )
                inserted += 1

            if lag_counter:
                best_lag_minutes, lag_support = lag_counter.most_common(1)[0]
                lead_lag_confidence = round(lag_support / same_direction_total, 8)
                cur.execute(
                    """
                    INSERT INTO product_relationships (
                        product_a_id,
                        product_b_id,
                        relationship_type,
                        best_lag_minutes,
                        same_direction_rate,
                        inverse_direction_rate,
                        lead_lag_confidence,
                        sample_count
                    )
                    VALUES (%s, %s, 'LEADER_FOLLOWER', %s, %s, %s, %s, %s)
                    """,
                    (
                        product_a,
                        product_b,
                        best_lag_minutes,
                        same_direction_rate,
                        inverse_direction_rate,
                        lead_lag_confidence,
                        same_direction_total,
                    ),
                )
                inserted += 1
    return inserted


def detect_live_events(cur):
    cur.execute("DELETE FROM cross_product_event_members")
    cur.execute("DELETE FROM cross_product_pattern_events")

    cur.execute(
        """
        SELECT DISTINCT ON (lw.product_id)
            lw.live_pattern_id,
            lw.product_id,
            lw.latest_snapshot_time,
            lw.candidate_type,
            lw.direction_bias,
            lw.bottom_similarity,
            lw.top_similarity,
            lw.confidence_label
        FROM live_pattern_windows lw
        ORDER BY lw.product_id, lw.latest_snapshot_time DESC
        """
    )
    latest_live_rows = cur.fetchall()
    latest_live_by_product = {
        row[1]: {
            "live_pattern_id": row[0],
            "product_id": row[1],
            "latest_snapshot_time": row[2],
            "candidate_type": row[3],
            "direction_bias": row[4],
            "bottom_similarity": float(row[5] or 0.0),
            "top_similarity": float(row[6] or 0.0),
            "confidence_label": row[7],
        }
        for row in latest_live_rows
    }

    cur.execute(
        """
        SELECT
            product_a_id,
            product_b_id,
            relationship_type,
            best_lag_minutes,
            lead_lag_confidence
        FROM product_relationships
        WHERE relationship_type = 'LEADER_FOLLOWER'
        ORDER BY product_a_id, product_b_id
        """
    )
    relationships = cur.fetchall()
    inserted_events = 0
    for product_a, product_b, relationship_type, best_lag_minutes, confidence in relationships:
        live_a = latest_live_by_product.get(product_a)
        live_b = latest_live_by_product.get(product_b)
        if not live_a or not live_b:
            continue
        if live_a["candidate_type"] != live_b["candidate_type"]:
            continue
        if live_a["candidate_type"] not in ("BOTTOM", "TOP"):
            continue
        observed_lag = int((live_b["latest_snapshot_time"] - live_a["latest_snapshot_time"]).total_seconds() / 60)
        if observed_lag != best_lag_minutes:
            continue

        event_type = "LEADER_FOLLOWER_SIGNAL"
        summary = (
            f"product {product_a} led product {product_b} by {best_lag_minutes} minutes "
            f"with {live_a['candidate_type']} bias"
        )
        cur.execute(
            """
            INSERT INTO cross_product_pattern_events (
                event_time,
                primary_product_id,
                primary_live_pattern_id,
                event_type,
                event_confidence,
                summary
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING event_id
            """,
            (
                live_b["latest_snapshot_time"],
                product_b,
                live_b["live_pattern_id"],
                event_type,
                confidence,
                summary,
            ),
        )
        event_id = cur.fetchone()[0]
        inserted_events += 1

        event_members = [
            (
                event_id,
                product_b,
                live_b["live_pattern_id"],
                live_b["candidate_type"],
                live_b["bottom_similarity"],
                live_b["top_similarity"],
                live_b["direction_bias"],
                0,
                "PRIMARY",
            ),
            (
                event_id,
                product_a,
                live_a["live_pattern_id"],
                live_a["candidate_type"],
                live_a["bottom_similarity"],
                live_a["top_similarity"],
                live_a["direction_bias"],
                -best_lag_minutes,
                "LEADER",
            ),
        ]
        psycopg2.extras.execute_values(
            cur,
            """
            INSERT INTO cross_product_event_members (
                event_id,
                product_id,
                live_pattern_id,
                candidate_turn_type,
                bottom_similarity,
                top_similarity,
                direction_bias,
                lag_minutes_from_primary,
                role
            )
            VALUES %s
            """,
            event_members,
        )
    return inserted_events


def run_engine():
    print("Starting cross-product relationship engine...")
    while True:
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            relationship_count = build_relationships(cur)
            event_count = detect_live_events(cur)
            conn.commit()
            print(
                f"cross_product_relationships={relationship_count} "
                f"cross_product_events={event_count}"
            )
        except Exception as exc:
            if conn:
                conn.rollback()
            print(f"Cross-product engine error: {exc}")
        finally:
            if conn:
                cur.close()
                conn.close()

        time.sleep(PROCESS_INTERVAL)


if __name__ == "__main__":
    run_engine()
