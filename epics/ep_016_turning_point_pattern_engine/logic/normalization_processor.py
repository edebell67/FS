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
PROCESS_INTERVAL = 30


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def compute_zscores(rows):
    if not rows:
        return {}
    mean = sum(row["frequency_count"] for row in rows) / len(rows)
    variance = sum((row["frequency_count"] - mean) ** 2 for row in rows) / len(rows)
    std_dev = variance ** 0.5
    if std_dev == 0:
        return {idx: 0.0 for idx, _ in enumerate(rows)}
    return {
        idx: round((row["frequency_count"] - mean) / std_dev, 8)
        for idx, row in enumerate(rows)
    }


def normalize_turn(cur, turn_id):
    cur.execute(
        """
        SELECT product_id, turn_type, turn_price
        FROM turning_points
        WHERE turn_id = %s
        """,
        (turn_id,),
    )
    product_id, turn_type, turn_price = cur.fetchone()
    turn_price = float(turn_price)

    cur.execute("SELECT pip_size FROM products WHERE product_id = %s", (product_id,))
    pip_size = float(cur.fetchone()[0])

    cur.execute(
        """
        SELECT snapshot_id, relative_time_index
        FROM turning_point_windows
        WHERE turn_id = %s
        ORDER BY relative_time_index ASC
        """,
        (turn_id,),
    )
    snapshots = cur.fetchall()

    cur.execute("DELETE FROM normalised_pattern_levels WHERE turn_id = %s", (turn_id,))
    normalized_rows = []
    for snapshot_id, rel_time_idx in snapshots:
        cur.execute(
            """
            SELECT side, price, frequency_count
            FROM frequency_levels
            WHERE snapshot_id = %s
            ORDER BY side, price
            """,
            (snapshot_id,),
        )
        raw_levels = cur.fetchall()
        side_rows = {"BID": [], "ASK": []}
        for side, raw_price, count in raw_levels:
            side_rows[side].append(
                {
                    "side": side,
                    "raw_price": float(raw_price),
                    "frequency_count": int(count),
                }
            )

        for side, rows in side_rows.items():
            if not rows:
                continue
            total_count = sum(row["frequency_count"] for row in rows)
            zscores = compute_zscores(rows)
            for idx, row in enumerate(rows):
                rel_pips = int(round((row["raw_price"] - turn_price) / pip_size))
                normalized_rows.append(
                    (
                        turn_id,
                        product_id,
                        turn_type,
                        rel_time_idx,
                        side,
                        rel_pips,
                        row["raw_price"],
                        row["frequency_count"],
                        round(row["frequency_count"] / total_count, 8) if total_count else 0.0,
                        zscores[idx],
                    )
                )

    if normalized_rows:
        psycopg2.extras.execute_values(
            cur,
            """
            INSERT INTO normalised_pattern_levels (
                turn_id,
                product_id,
                turn_type,
                relative_time_index,
                side,
                relative_pips,
                raw_price,
                frequency_count,
                normalised_frequency,
                zscore_frequency
            )
            VALUES %s
            """,
            normalized_rows,
        )

    cur.execute("UPDATE turning_points SET is_normalized = TRUE WHERE turn_id = %s", (turn_id,))


def run_normalization():
    print("Starting normalization processor...")
    while True:
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("SELECT turn_id FROM turning_points WHERE is_normalized = FALSE ORDER BY turn_id")
            turns = cur.fetchall()
            for (turn_id,) in turns:
                normalize_turn(cur, turn_id)
                print(f"Normalized turn {turn_id}")

            conn.commit()
        except Exception as exc:
            if conn:
                conn.rollback()
            print(f"Normalization error: {exc}")
        finally:
            if conn:
                cur.close()
                conn.close()

        time.sleep(PROCESS_INTERVAL)


if __name__ == "__main__":
    run_normalization()
