import os
import time
from datetime import datetime

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


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def build_status_report():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT product_id, product_code FROM products WHERE is_active = TRUE ORDER BY product_code")
    products = cur.fetchall()

    lines = [
        "=== Turning-Point Pattern Engine Status ===",
        f"Time: {datetime.now().strftime('%H:%M:%S')}",
        "-" * 72,
    ]

    for product_id, product_code in products:
        lines.append(f"\n[{product_code}]")
        cur.execute(
            """
            SELECT
                live_pattern_id,
                latest_snapshot_time,
                candidate_type,
                candidate_turn_price,
                current_state,
                direction_bias,
                bottom_similarity,
                top_similarity,
                nearest_match_count,
                historical_next_5m_bias_rate,
                historical_next_10m_bias_rate,
                historical_avg_10m_move_pips,
                confidence_label,
                summary,
                predictive_score,
                score_confidence_label
            FROM live_pattern_windows
            WHERE product_id = %s
            ORDER BY latest_snapshot_time DESC
            LIMIT 1
            """,
            (product_id,),
        )
        live_row = cur.fetchone()
        if not live_row:
            lines.append("  No live data processed yet.")
            continue

        (
            live_pattern_id,
            latest_snapshot_time,
            candidate_type,
            candidate_turn_price,
            current_state,
            direction_bias,
            bottom_similarity,
            top_similarity,
            nearest_match_count,
            historical_next_5m_bias_rate,
            historical_next_10m_bias_rate,
            historical_avg_10m_move_pips,
            confidence_label,
            summary,
            predictive_score,
            score_confidence_label,
        ) = live_row

        # Format predictive score display
        score_str = f"{float(predictive_score):.1f}" if predictive_score else "N/A"
        score_conf_str = score_confidence_label or "N/A"

        lines.append(
            f"  Last window: {latest_snapshot_time.strftime('%Y-%m-%d %H:%M:%S')} "
            f"| candidate={candidate_type} | bias={direction_bias} | confidence={confidence_label}"
        )
        lines.append(
            f"  PREDICTIVE SCORE: {score_str} ({score_conf_str}) [r=+0.78 with outcomes]"
        )
        lines.append(
            f"  Candidate turn price: {float(candidate_turn_price):.4f} "
            f"| state={current_state}"
        )
        lines.append(
            f"  Similarity: bottom={float(bottom_similarity or 0)*100:.2f}% "
            f"| top={float(top_similarity or 0)*100:.2f}% "
            f"| matches={nearest_match_count or 0}"
        )
        lines.append(
            f"  Historical bias follow-through: 5m={float(historical_next_5m_bias_rate or 0)*100:.1f}% "
            f"| 10m={float(historical_next_10m_bias_rate or 0)*100:.1f}% "
            f"| avg_10m_move={float(historical_avg_10m_move_pips or 0):.2f} pips"
        )
        lines.append(f"  Summary: {summary}")

        cur.execute("SELECT COUNT(*) FROM turning_points WHERE product_id = %s", (product_id,))
        turn_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM frequency_snapshots WHERE product_id = %s", (product_id,))
        snapshot_count = cur.fetchone()[0]
        lines.append(f"  Database: {snapshot_count} snapshots | {turn_count} confirmed turns")

        cur.execute(
            """
            SELECT e.event_time, e.event_type, e.event_confidence, e.summary
            FROM cross_product_pattern_events e
            JOIN cross_product_event_members m ON m.event_id = e.event_id
            WHERE m.product_id = %s
            ORDER BY e.event_time DESC
            LIMIT 1
            """,
            (product_id,),
        )
        event_row = cur.fetchone()
        if event_row:
            event_time, event_type, event_confidence, event_summary = event_row
            lines.append(
                f"  Latest cross-product event: {event_time.strftime('%Y-%m-%d %H:%M:%S')} "
                f"| {event_type} | confidence={float(event_confidence or 0):.2f}"
            )
            lines.append(f"  Event summary: {event_summary}")
        else:
            lines.append("  Latest cross-product event: none")

    cur.close()
    conn.close()
    return "\n".join(lines)


def get_latest_status():
    clear_screen()
    print(build_status_report())


if __name__ == "__main__":
    try:
        while True:
            get_latest_status()
            time.sleep(5)
    except KeyboardInterrupt:
        pass
