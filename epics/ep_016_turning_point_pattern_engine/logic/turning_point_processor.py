import time
from dataclasses import dataclass
from datetime import timedelta

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
WINDOW_SIZE = 3
SNAPSHOT_WINDOW_SECONDS = 300
CONFIRMATION_PIPS = 5


@dataclass
class SnapshotSummary:
    snapshot_id: int
    snapshot_time: object
    magnet_price: float
    weighted_price: float
    total_frequency: int
    level_count: int


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_pip_size(cur, product_id):
    cur.execute("SELECT pip_size FROM products WHERE product_id = %s", (product_id,))
    row = cur.fetchone()
    return float(row[0]) if row else 0.0001


def get_snapshot_summary(cur, snapshot_id):
    cur.execute(
        """
        SELECT
            price,
            frequency_count
        FROM frequency_levels
        WHERE snapshot_id = %s
        ORDER BY frequency_count DESC, price ASC
        """,
        (snapshot_id,),
    )
    rows = cur.fetchall()
    if not rows:
        return None

    total_frequency = sum(int(count) for _, count in rows)
    weighted_sum = sum(float(price) * int(count) for price, count in rows)
    magnet_price = float(rows[0][0])
    weighted_price = weighted_sum / total_frequency if total_frequency else magnet_price
    return magnet_price, weighted_price, total_frequency, len(rows)


def load_product_snapshots(cur, product_id):
    cur.execute(
        """
        SELECT snapshot_id, snapshot_time
        FROM frequency_snapshots
        WHERE product_id = %s
          AND window_seconds = %s
        ORDER BY snapshot_time ASC
        """,
        (product_id, SNAPSHOT_WINDOW_SECONDS),
    )
    rows = cur.fetchall()
    summaries = []
    for snapshot_id, snapshot_time in rows:
        summary = get_snapshot_summary(cur, snapshot_id)
        if not summary:
            continue
        magnet_price, weighted_price, total_frequency, level_count = summary
        summaries.append(
            SnapshotSummary(
                snapshot_id=snapshot_id,
                snapshot_time=snapshot_time,
                magnet_price=magnet_price,
                weighted_price=weighted_price,
                total_frequency=total_frequency,
                level_count=level_count,
            )
        )
    return summaries


def get_confirmation_delay(post_prices, center_price, pip_size, direction):
    threshold = CONFIRMATION_PIPS * pip_size
    for idx, price in enumerate(post_prices, start=1):
        move = price - center_price
        if direction == "BOTTOM" and move >= threshold:
            return idx
        if direction == "TOP" and move <= -threshold:
            return idx
    return None


def compute_turn_move_metrics(window, pip_size, turn_type, confirmation_delay_snapshots):
    center_idx = WINDOW_SIZE
    magnet_prices = [summary.magnet_price for summary in window]
    pre_prices = magnet_prices[:center_idx]
    post_prices = magnet_prices[center_idx + 1 :]
    center_price = magnet_prices[center_idx]

    if turn_type == "BOTTOM":
        move_into_turn_pips = round((max(pre_prices) - center_price) / pip_size, 4)
        confirmation_move_pips = round(
            (post_prices[confirmation_delay_snapshots - 1] - center_price) / pip_size,
            4,
        )
    else:
        move_into_turn_pips = round((center_price - min(pre_prices)) / pip_size, 4)
        confirmation_move_pips = round(
            (center_price - post_prices[confirmation_delay_snapshots - 1]) / pip_size,
            4,
        )

    local_window_range_pips = round((max(magnet_prices) - min(magnet_prices)) / pip_size, 4)
    return move_into_turn_pips, confirmation_move_pips, local_window_range_pips


def evaluate_turn_candidate(window, pip_size):
    center_idx = WINDOW_SIZE
    center = window[center_idx]
    magnet_prices = [summary.magnet_price for summary in window]
    pre_prices = magnet_prices[:center_idx]
    post_prices = magnet_prices[center_idx + 1 :]
    threshold = CONFIRMATION_PIPS * pip_size

    center_price = center.magnet_price
    pre_average = sum(pre_prices) / len(pre_prices)
    post_average = sum(post_prices) / len(post_prices)

    bottom_confirm_delay = get_confirmation_delay(post_prices, center_price, pip_size, "BOTTOM")
    if (
        center_price == min(magnet_prices)
        and center_price <= min(pre_prices)
        and post_prices[-1] >= center_price + threshold
        and post_average > center_price
        and pre_average > center_price
        and bottom_confirm_delay is not None
    ):
        return "BOTTOM", center_price, bottom_confirm_delay

    top_confirm_delay = get_confirmation_delay(post_prices, center_price, pip_size, "TOP")
    if (
        center_price == max(magnet_prices)
        and center_price >= max(pre_prices)
        and post_prices[-1] <= center_price - threshold
        and post_average < center_price
        and pre_average < center_price
        and top_confirm_delay is not None
    ):
        return "TOP", center_price, top_confirm_delay

    return None


def find_snapshot_at_or_after(snapshots, target_time):
    for snapshot in snapshots:
        if snapshot.snapshot_time >= target_time:
            return snapshot
    return None


def compute_outcomes(center_snapshot, future_snapshots, turn_price, turn_type, pip_size):
    outcome_minutes = (5, 10, 15, 30)
    outcome_values = {}
    for minutes in outcome_minutes:
        target_time = center_snapshot.snapshot_time + timedelta(minutes=minutes)
        matched = find_snapshot_at_or_after(future_snapshots, target_time)
        if not matched:
            outcome_values[minutes] = None
            continue
        raw_move = (matched.magnet_price - turn_price) / pip_size
        outcome_values[minutes] = round(raw_move, 4)

    ten_minute_cutoff = center_snapshot.snapshot_time + timedelta(minutes=10)
    ten_minute_snapshots = [
        snapshot for snapshot in future_snapshots if snapshot.snapshot_time <= ten_minute_cutoff
    ]
    if ten_minute_snapshots:
        moves = [(snapshot.magnet_price - turn_price) / pip_size for snapshot in ten_minute_snapshots]
        if turn_type == "BOTTOM":
            max_favourable = round(max(moves), 4)
            max_adverse = round(min(moves), 4)
        else:
            max_favourable = round(max((-move for move in moves)), 4)
            max_adverse = round(max(moves), 4)
    else:
        max_favourable = None
        max_adverse = None

    return outcome_values, max_favourable, max_adverse


def save_turn(cur, product_id, turn_type, confirmation_delay_snapshots, pip_size, window, all_snapshots):
    center_idx = WINDOW_SIZE
    center_snapshot = window[center_idx]
    turn_time = center_snapshot.snapshot_time
    turn_price = center_snapshot.magnet_price

    cur.execute(
        """
        SELECT turn_id
        FROM turning_points
        WHERE product_id = %s AND turn_time = %s AND turn_type = %s
        """,
        (product_id, turn_time, turn_type),
    )
    if cur.fetchone():
        return False

    confirmation_delay_minutes = confirmation_delay_snapshots * int(SNAPSHOT_WINDOW_SECONDS / 60)
    move_into_turn_pips, confirmation_move_pips, local_window_range_pips = compute_turn_move_metrics(
        window=window,
        pip_size=pip_size,
        turn_type=turn_type,
        confirmation_delay_snapshots=confirmation_delay_snapshots,
    )
    future_snapshots = [snapshot for snapshot in all_snapshots if snapshot.snapshot_time > turn_time]
    outcomes, max_favourable, max_adverse = compute_outcomes(
        center_snapshot=center_snapshot,
        future_snapshots=future_snapshots,
        turn_price=turn_price,
        turn_type=turn_type,
        pip_size=pip_size,
    )

    cur.execute(
        """
        INSERT INTO turning_points (
            product_id,
            turn_time,
            turn_type,
            turn_price,
            confirmation_method,
            confirmation_delay_snapshots,
            confirmation_delay_minutes,
            move_into_turn_pips,
            confirmation_move_pips,
            local_window_range_pips,
            outcome_5m_pips,
            outcome_10m_pips,
            outcome_15m_pips,
            outcome_30m_pips,
            max_favourable_10m_pips,
            max_adverse_10m_pips
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING turn_id
        """,
        (
            product_id,
            turn_time,
            turn_type,
            turn_price,
            f"MagnetWindow{WINDOW_SIZE}_Threshold{CONFIRMATION_PIPS}",
            confirmation_delay_snapshots,
            confirmation_delay_minutes,
            move_into_turn_pips,
            confirmation_move_pips,
            local_window_range_pips,
            outcomes[5],
            outcomes[10],
            outcomes[15],
            outcomes[30],
            max_favourable,
            max_adverse,
        ),
    )
    turn_id = cur.fetchone()[0]

    for idx, snapshot in enumerate(window):
        relative_idx = idx - WINDOW_SIZE
        cur.execute(
            """
            INSERT INTO turning_point_windows (turn_id, snapshot_id, relative_time_index)
            VALUES (%s, %s, %s)
            """,
            (turn_id, snapshot.snapshot_id, relative_idx),
        )

    print(
        f"Detected {turn_type} for product {product_id} at {turn_time} "
        f"(Price: {turn_price:.4f}, delay_snapshots={confirmation_delay_snapshots}, "
        f"move_into_turn_pips={move_into_turn_pips:.1f}, "
        f"confirmation_move_pips={confirmation_move_pips:.1f}, "
        f"local_window_range_pips={local_window_range_pips:.1f})"
    )
    return True


def backfill_missing_turn_move_metrics(cur, product_id, snapshots):
    snapshot_map = {snapshot.snapshot_id: snapshot for snapshot in snapshots}
    pip_size = get_pip_size(cur, product_id)

    cur.execute(
        """
        SELECT turn_id, turn_type, confirmation_delay_snapshots
        FROM turning_points
        WHERE product_id = %s
          AND (
            move_into_turn_pips IS NULL
            OR confirmation_move_pips IS NULL
            OR local_window_range_pips IS NULL
          )
        ORDER BY turn_id
        """,
        (product_id,),
    )
    turns = cur.fetchall()
    updated = 0
    for turn_id, turn_type, confirmation_delay_snapshots in turns:
        cur.execute(
            """
            SELECT snapshot_id, relative_time_index
            FROM turning_point_windows
            WHERE turn_id = %s
            ORDER BY relative_time_index
            """,
            (turn_id,),
        )
        window_rows = cur.fetchall()
        if len(window_rows) != (2 * WINDOW_SIZE + 1):
            continue
        try:
            window = [snapshot_map[snapshot_id] for snapshot_id, _ in window_rows]
        except KeyError:
            continue

        move_into_turn_pips, confirmation_move_pips, local_window_range_pips = compute_turn_move_metrics(
            window=window,
            pip_size=pip_size,
            turn_type=turn_type,
            confirmation_delay_snapshots=int(confirmation_delay_snapshots),
        )
        cur.execute(
            """
            UPDATE turning_points
            SET
                move_into_turn_pips = %s,
                confirmation_move_pips = %s,
                local_window_range_pips = %s
            WHERE turn_id = %s
            """,
            (
                move_into_turn_pips,
                confirmation_move_pips,
                local_window_range_pips,
                turn_id,
            ),
        )
        updated += 1
    return updated


def process_product_turns(cur, product_id, product_code):
    snapshots = load_product_snapshots(cur, product_id)
    if len(snapshots) < (2 * WINDOW_SIZE + 1):
        return 0

    updated = backfill_missing_turn_move_metrics(cur, product_id, snapshots)
    if updated:
        print(f"[{product_code}] backfilled_turn_move_metrics={updated}")

    pip_size = get_pip_size(cur, product_id)
    detected = 0
    for center_idx in range(WINDOW_SIZE, len(snapshots) - WINDOW_SIZE):
        window = snapshots[center_idx - WINDOW_SIZE : center_idx + WINDOW_SIZE + 1]
        result = evaluate_turn_candidate(window, pip_size)
        if not result:
            continue
        turn_type, _, confirmation_delay = result
        if save_turn(cur, product_id, turn_type, confirmation_delay, pip_size, window, snapshots):
            detected += 1
    if detected:
        print(f"[{product_code}] detected_turns={detected}")
    return detected


def run_processor():
    print("Starting turning point processor...")
    while True:
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("SELECT product_id, product_code FROM products WHERE is_active = TRUE")
            products = cur.fetchall()

            for product_id, product_code in products:
                process_product_turns(cur, product_id, product_code)

            conn.commit()
        except Exception as exc:
            if conn:
                conn.rollback()
            print(f"Processor error: {exc}")
        finally:
            if conn:
                cur.close()
                conn.close()

        time.sleep(PROCESS_INTERVAL)


if __name__ == "__main__":
    run_processor()
