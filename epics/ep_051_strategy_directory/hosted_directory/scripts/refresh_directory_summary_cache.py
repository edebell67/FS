"""Precompute directory evidence datasets outside the web request process.

Version history:
- 3.0.0 (2026-08-28): SQL does the processing, Python does a dumb read.
  The v2.0.0 incremental design (in-memory Python state, watermarked
  queries) was the wrong tool for the job - state held in a Python
  process's memory is fragile (lost on every restart, which happened
  repeatedly this session), single-consumer, and duplicates aggregation
  logic that SQL Server already does robustly for thousands of trades via
  the existing stored procedures. Replaced with: a real SQL Server table
  (dbo.ep051_directory_daily_summary) maintained incrementally by a
  trigger (trg_ep051_combined_trades_closed_update_daily_summary) the
  instant each trade closes, covering every one of the 39 procedures that
  write to combined_trades_closed with zero Python involvement. This
  script's only job now is to read that table plus today's raw trade
  ledger and write the JSON file - no aggregation, no watermark, no
  state to lose on restart. Backfilled and reconciled once (15,010 trades,
  net return matched the raw source to the cent) before cutting over.
- 2.0.1 (2026-08-28): Includes nullable alt_net_return in cached ledger rows.
- 2.0.0 (2026-08-28): Incremental refresh (in-memory Python state - since
  replaced, see 3.0.0).
- 1.0.0 (2026-08-24): Original full-rescan-every-cycle version.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import get_settings
from app.repository import sqlserver_connection

CACHE = ROOT / "runtime" / "directory_summary_cache.json"

# Maintained incrementally by trg_ep051_combined_trades_closed_update_daily_summary.
# This is a plain read of already-aggregated totals - no GROUP BY, no sort,
# no memory grant risk.
SUMMARY_SQL = """
  SELECT strategy_id, signal_group, descriptive_name, product, total_trades,
         wins, losses, breakevens, total_net_return, gross_profit, gross_loss,
         evidence_start, evidence_end
  FROM dbo.ep051_directory_daily_summary WITH (NOLOCK)
  WHERE trade_date = ?
"""

# The per-trade ledger still comes straight from the source table. Filtered
# to today only (a few thousand rows, not the ~106k full-history figure that
# caused the original slowness), so this remains a cheap sequential read.
TRADE_SQL = """
  SELECT model,guid,product,strategy_name,UPPER(LTRIM(RTRIM(signal))) signal,
         created entry_time,CAST(entry_price AS float) entry_price,
         COALESCE(g_close_time,last_update,created) exit_time,
         CAST(latest_price AS float) exit_price,CAST(net_return AS float) net_return,
         CAST(alt_net_return AS float) alt_net_return
  FROM dbo.combined_trades_closed WITH (NOLOCK)
  WHERE model_ix LIKE 'DNA[_]%' AND created >= ? AND created < ?
    AND net_return IS NOT NULL
  OPTION(MAXDOP 1,RECOMPILE)
"""


def canonical_strategy_id(model: str) -> str:
    return model[:-2] if model.endswith(("_B", "_S")) else model


def fetch_summary(cursor, today):
    datasets = {"BOTH": [], "BUY": [], "SELL": []}
    rows = cursor.execute(SUMMARY_SQL, today)
    for (strategy_id, signal_group, descriptive_name, product, total_trades,
         wins, losses, breakevens, total_net_return, gross_profit, gross_loss,
         evidence_start, evidence_end) in rows:
        bucket = datasets.get(signal_group)
        if bucket is None:
            continue
        bucket.append({
            "strategy_id": strategy_id, "descriptive_name": descriptive_name,
            "product_name": product, "total_trades": total_trades,
            "wins": wins, "losses": losses, "breakevens": breakevens,
            "total_net_return": total_net_return,
            "win_rate": wins / total_trades if total_trades else 0.0,
            "profit_factor": gross_profit / gross_loss if gross_loss else None,
            "max_drawdown_money": None, "market": "FX", "status": "active",
            "quality_state": "VALID" if total_trades >= 30 else "COLLECTING",
            "evidence_start": evidence_start, "evidence_end": evidence_end,
        })
    for bucket in datasets.values():
        bucket.sort(key=lambda row: row["strategy_id"])
    return datasets


def fetch_trades_by_strategy(cursor, start, end):
    trades_by_strategy: dict[str, list[dict]] = {}
    rows = cursor.execute(TRADE_SQL, start, end)
    for (model, guid, product, strategy_name, signal, entry_time, entry_price,
         exit_time, exit_price, net_return, alt_net_return) in rows:
        strategy_id = canonical_strategy_id(model)
        trades_by_strategy.setdefault(strategy_id, []).append({
            "guid": str(guid), "product": product, "signal": signal,
            "entry_time": entry_time.isoformat() if entry_time else None,
            "entry_price": float(entry_price) if entry_price is not None else None,
            "exit_time": exit_time.isoformat() if exit_time else None,
            "exit_price": float(exit_price) if exit_price is not None else None,
            "net_return": float(net_return),
            "alt_net_return": float(alt_net_return) if alt_net_return is not None else None,
        })
    for trades in trades_by_strategy.values():
        trades.sort(key=lambda row: (row.get("entry_time") or "", row.get("guid") or ""))
    return trades_by_strategy


def refresh() -> None:
    now = datetime.now(timezone.utc)
    today = now.date()
    start = datetime.combine(today, datetime.min.time())
    end = start + timedelta(days=1)
    settings = get_settings()
    # One connection, two reads - halves the connection-establishment cost
    # (the dominant cost under current SQL Server contention, not the
    # queries themselves) compared to opening a fresh connection per read.
    with closing(sqlserver_connection(settings)) as connection:
        cursor = connection.cursor()
        datasets = fetch_summary(cursor, today)
        trades_by_strategy = fetch_trades_by_strategy(cursor, start, end)
    payload = {
        "schema_version": "1.0.0",
        "generated_at": now.isoformat(),
        "date_from": today.isoformat(),
        "date_to": today.isoformat(),
        "datasets": datasets,
        "trades_by_strategy": trades_by_strategy,
    }
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    temporary = CACHE.with_suffix(f".{os.getpid()}.tmp")
    temporary.write_text(json.dumps(payload, default=str, separators=(",", ":")), encoding="utf-8")
    os.replace(temporary, CACHE)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=180)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    while True:
        try:
            refresh()
        except Exception as exc:
            print(f"directory cache refresh failed: {exc}", flush=True)
        if args.once:
            return
        time.sleep(max(30, args.interval))


if __name__ == "__main__":
    main()
