"""Captures each DNA strategy's CURRENT-DAY net_return rank once per cycle,
building a time series that shows a strategy's journey relative to every
other strategy - not just its own equity curve, but where it stood in the
field at each point in time.

Version history:
- 1.2.0 (2026-08-31): Default cadence 3600s -> 900s (15 min), now that the
  current-day-scoped query (see 1.1.0) is cheap enough to run that often
  without adding meaningfully to database load.
- 1.1.0 (2026-08-31): Changes the ranking window from all-time to current
  day (entry-date cohort, same COALESCE-free `created` convention as
  local_period_strategies() - "Directory periods are entry-date cohorts",
  see app/repository.py). All-time gave every strategy's entire history
  equal weight regardless of when it traded, which wasn't the intended
  read of "position" - and as a side effect, filtering to one day's trades
  instead of scanning the full ~130k-row closed-trade history makes this
  a much cheaper query, which should also stop it queueing behind the
  live trading system's SQL Server memory-grant contention the way the
  full aggregate did.
- 1.0.0 (2026-08-30): Initial hourly rank-position capture into
  dbo.ep051_strategy_rank_history (all-time basis, since changed).
"""
from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import get_settings
from app.repository import sqlserver_connection

RANK_QUERY = """
SET QUOTED_IDENTIFIER ON;
WITH agg AS (
  SELECT CASE WHEN RIGHT(model,2) IN ('_B','_S') THEN LEFT(model,LEN(model)-2) ELSE model END strategy_id,
         SUM(CAST(net_return AS float)) total_net_return, COUNT(*) total_trades
  FROM dbo.combined_trades_closed WITH (NOLOCK)
  WHERE model_ix LIKE 'DNA[_]%' AND net_return IS NOT NULL AND created >= ? AND created < ?
  GROUP BY CASE WHEN RIGHT(model,2) IN ('_B','_S') THEN LEFT(model,LEN(model)-2) ELSE model END
)
SELECT strategy_id, total_net_return, total_trades,
       RANK() OVER (ORDER BY total_net_return DESC) rank_position
FROM agg
OPTION (MAXDOP 1)
"""

INSERT_SQL = """
INSERT INTO dbo.ep051_strategy_rank_history
  (captured_at, strategy_id, total_net_return, total_trades, rank_position)
VALUES (?, ?, ?, ?, ?)
"""


def capture() -> int:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    captured_at = now.replace(microsecond=0, tzinfo=None)
    today_start = datetime(now.year, now.month, now.day)
    today_end = today_start + timedelta(days=1)
    with sqlserver_connection(settings) as connection:
        cursor = connection.cursor()
        cursor.execute(RANK_QUERY, today_start, today_end)
        rows = cursor.fetchall()
        cursor.fast_executemany = True
        cursor.executemany(
            INSERT_SQL,
            [(captured_at, row.strategy_id, row.total_net_return, row.total_trades, row.rank_position) for row in rows],
        )
        connection.commit()
    print(f"captured {len(rows)} strategy rank positions (current day) at {captured_at.isoformat()}", flush=True)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=900)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    while True:
        try:
            capture()
        except Exception as exc:
            print(f"strategy rank capture failed: {exc}", flush=True)
        if args.once:
            return
        time.sleep(max(300, args.interval))


if __name__ == "__main__":
    main()
