"""Captures each DNA strategy's all-time net_return rank once per cycle,
building a time series that shows a strategy's journey relative to every
other strategy - not just its own equity curve, but where it stood in the
field at each point in time.

Version history:
- 1.0.0 (2026-08-30): Initial hourly rank-position capture into
  dbo.ep051_strategy_rank_history.
"""
from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timezone
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
  WHERE model_ix LIKE 'DNA[_]%' AND net_return IS NOT NULL
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
    captured_at = datetime.now(timezone.utc).replace(microsecond=0, tzinfo=None)
    with sqlserver_connection(settings) as connection:
        cursor = connection.cursor()
        cursor.execute(RANK_QUERY)
        rows = cursor.fetchall()
        cursor.fast_executemany = True
        cursor.executemany(
            INSERT_SQL,
            [(captured_at, row.strategy_id, row.total_net_return, row.total_trades, row.rank_position) for row in rows],
        )
        connection.commit()
    print(f"captured {len(rows)} strategy rank positions at {captured_at.isoformat()}", flush=True)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=3600)
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
