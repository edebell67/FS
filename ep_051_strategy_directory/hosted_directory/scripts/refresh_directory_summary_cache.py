"""Precompute directory evidence datasets outside the web request process."""
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
from app.repository import local_period_strategies, sqlserver_connection

CACHE = ROOT / "runtime" / "directory_summary_cache.json"


def refresh() -> None:
    now = datetime.now(timezone.utc)
    start = datetime.combine(now.date(), datetime.min.time())
    end = start + timedelta(days=1)
    settings = get_settings()
    datasets = {
        "BOTH": local_period_strategies(settings, start, end),
        "BUY": local_period_strategies(settings, start, end, signal="BUY"),
        "SELL": local_period_strategies(settings, start, end, signal="SELL"),
    }
    trades_by_strategy = {}
    trade_sql = """
      SELECT model,guid,product,UPPER(LTRIM(RTRIM(signal))) signal,
             created entry_time,CAST(entry_price AS float) entry_price,
             COALESCE(g_close_time,last_update,created) exit_time,
             CAST(latest_price AS float) exit_price,CAST(net_return AS float) net_return
      FROM dbo.combined_trades_closed WITH (NOLOCK)
      WHERE model_ix LIKE 'DNA[_]%' AND created >= ? AND created < ?
        AND net_return IS NOT NULL
      OPTION(MAXDOP 1,RECOMPILE)
    """
    with closing(sqlserver_connection(settings)) as connection:
        for model,guid,product,signal,entry_time,entry_price,exit_time,exit_price,net_return in connection.cursor().execute(trade_sql,start,end):
            strategy_id=model[:-2] if model.endswith(("_B","_S")) else model
            trades_by_strategy.setdefault(strategy_id,[]).append({
                "guid":str(guid),"product":product,"signal":signal,
                "entry_time":entry_time.isoformat() if entry_time else None,
                "entry_price":float(entry_price) if entry_price is not None else None,
                "exit_time":exit_time.isoformat() if exit_time else None,
                "exit_price":float(exit_price) if exit_price is not None else None,
                "net_return":float(net_return),
            })
    for trades in trades_by_strategy.values():
        trades.sort(key=lambda row:(row.get("entry_time") or "",row.get("guid") or ""))
    payload = {
        "schema_version": "1.0.0",
        "generated_at": now.isoformat(),
        "date_from": start.date().isoformat(),
        "date_to": start.date().isoformat(),
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
