# epics/ep_058_strategy_intelligence_pg/hosted_directory/reports/scenario_return_monitor.py — cross-scenario return leaderboard.
#
# VERSION HISTORY
# v1.0.0 (2026-09-27): Initial version. Pulls every scenario from the EP058 dashboard API (the same data and aggregation
#   the top10_5min_equity_curves.html page's "Select Strategy Scenario / Criteria" picker offers), computes each
#   scenario's current aggregate return and per-strategy breakdown, and ranks scenarios by return - live, from the API,
#   with no UI driving involved. Can run once or loop every N minutes.
"""
Replicates, purely via the EP058 API, what selecting every scenario in the page's
"Select Strategy Scenario / Criteria" picker one at a time would show, then ranks
them by current aggregate return so you can see which scenario is winning right now.

For each scenario id returned by GET /api/scenarios (every id also listed in
GET /api/live_day for the day - Top 10 Net Return, Top 10 Win Rate, Touched #1
Today, Best Performer by Family, Top 5 per family, Top 3 per TP/SL pair, and
every other card in the picker), this calls POST /api/ribbon with that scenario
and the same default view the page opens with (Net Return, full day, no
baseline offset, no win-rate filter) to get:
  - the scenario's aggregate return (summed net/buy/sell delta across its
    matched strategies, same figure as the page's ribbon/header total), and
  - the return of every individual strategy matched by that scenario's criteria
    (per-model net/buy/sell delta, same as one row on the page's ribbon).

Usage:
    python -m reports.scenario_return_monitor                       # one report, stdout summary + JSON/CSV files
    python -m reports.scenario_return_monitor --loop                # repeat every --interval seconds (default 300 = 5 min)
    python -m reports.scenario_return_monitor --date 2026-09-24      # a specific past trading date
    python -m reports.scenario_return_monitor --return-type ALT --min-win-rate 50 --product-type forex

Config (env, all optional):
    EP058_API_BASE      default http://127.0.0.1:8149
    EP058_REPORT_DIR    default runtime/scenario_reports (relative to this file's parent)
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
API_BASE = os.environ.get("EP058_API_BASE", "http://127.0.0.1:8149").rstrip("/")
REPORT_DIR = Path(os.environ.get("EP058_REPORT_DIR", str(HERE.parent / "runtime" / "scenario_reports")))
TIMEOUT = 60


def _get(path: str) -> dict:
    with urllib.request.urlopen(f"{API_BASE}{path}", timeout=TIMEOUT) as resp:
        return json.load(resp)


def _post(path: str, body: dict) -> dict:
    req = urllib.request.Request(f"{API_BASE}{path}", json.dumps(body).encode(), {"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.load(resp)


def fetch_scenario_ids(date: str, product_type: str, product: str, strategy_family: str, limit: int) -> list[str]:
    """Every scenario id the page's picker offers for this day/filter set (GET /api/scenarios)."""
    payload = _get(f"/api/scenarios?date={date}&product_type={product_type}&product={product}"
                   f"&strategy_family={strategy_family}&limit={limit}")
    return payload["available_ids"]


def fetch_scenario_return(scenario: str, common: dict) -> dict | None:
    """One scenario's aggregate return (ribbon total) and every matched strategy's own return (ribbon per-model list)."""
    try:
        return _post("/api/ribbon", {**common, "scenario": scenario})
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        print(f"  ! {scenario}: HTTP {exc.code} {body[:200]}", file=sys.stderr)
        return None
    except urllib.error.URLError as exc:
        print(f"  ! {scenario}: {exc}", file=sys.stderr)
        return None


def build_report(date: str, return_type: str, product_type: str, product: str, strategy_family: str,
                 limit: int, min_win_rate: float, exit_threshold: float = 0.0, daily_target: float = 0.0) -> dict:
    common = {"date": date, "return_type": return_type, "product_type": product_type, "product": product,
              "strategy_family": strategy_family, "limit": limit, "min_win_rate": min_win_rate,
              "baseline_index": 0, "frame_index": -1, "exit_threshold": exit_threshold, "daily_target": daily_target}
    scenario_ids = fetch_scenario_ids(date, product_type, product, strategy_family, limit)
    scenarios = []
    for scenario_id in scenario_ids:
        ribbon = fetch_scenario_return(scenario_id, common)
        if ribbon is None or not ribbon.get("count"):
            continue
        scenarios.append({
            "scenario": scenario_id,
            "strategy_count": ribbon["count"],
            "total_net": round(ribbon["total"]["net"], 2),
            "total_buy": round(ribbon["total"]["buy"], 2),
            "total_sell": round(ribbon["total"]["sell"], 2),
            "base_time": ribbon.get("base_time"),
            "head_time": ribbon.get("head_time"),
            "strategies": sorted(
                ({"model": m["model"], "net": round(m["net"], 2), "buy": round(m["buy"], 2), "sell": round(m["sell"], 2)}
                 for m in ribbon["models"]),
                key=lambda s: -s["net"],
            ),
        })
    scenarios.sort(key=lambda s: -s["total_net"])
    for rank, scenario in enumerate(scenarios, start=1):
        scenario["rank"] = rank
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "date": date, "return_type": return_type, "product_type": product_type, "product": product,
        "strategy_family": strategy_family, "limit": limit, "min_win_rate": min_win_rate,
        "scenario_count": len(scenarios),
        "best_scenario": scenarios[0]["scenario"] if scenarios else None,
        "best_scenario_return": scenarios[0]["total_net"] if scenarios else None,
        "scenarios": scenarios,
    }


def write_report(report: dict, stem: str = "latest") -> tuple[Path, Path]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORT_DIR / f"{stem}.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    csv_path = REPORT_DIR / f"{stem}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["rank", "scenario", "strategy_count", "total_net", "total_buy", "total_sell", "top_strategy", "top_strategy_net"])
        for s in report["scenarios"]:
            top = s["strategies"][0] if s["strategies"] else {}
            writer.writerow([s["rank"], s["scenario"], s["strategy_count"], s["total_net"], s["total_buy"], s["total_sell"],
                             top.get("model", ""), top.get("net", "")])
    # timestamped copy so a --loop run keeps history, not just the latest snapshot
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (REPORT_DIR / f"{ts}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return json_path, csv_path


def print_summary(report: dict, top_n: int = 10) -> None:
    print(f"\n[{report['generated_at']}] {report['date']} · {report['scenario_count']} scenarios "
          f"({report['return_type']}, product_type={report['product_type']}, product={report['product']})")
    print(f"{'#':>3}  {'scenario':<28} {'n':>3}  {'total_net':>12}  {'buy':>10}  {'sell':>10}  top strategy")
    for s in report["scenarios"][:top_n]:
        top = s["strategies"][0]["model"] if s["strategies"] else "-"
        print(f"{s['rank']:>3}  {s['scenario']:<28} {s['strategy_count']:>3}  {s['total_net']:>12,.2f}  "
              f"{s['total_buy']:>10,.2f}  {s['total_sell']:>10,.2f}  {top}")
    if report["best_scenario"]:
        print(f"\nBest right now: {report['best_scenario']} ({report['best_scenario_return']:+,.2f})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--date", default=None, help="YYYY-MM-DD; default = today")
    parser.add_argument("--return-type", choices=["NET", "ALT"], default="NET")
    parser.add_argument("--product-type", choices=["all", "forex", "crypto"], default="all")
    parser.add_argument("--product", default="all")
    parser.add_argument("--strategy-family", default="all",
                        choices=["all", "breakout", "breakout_r", "breakout_rev", "breakout_r_rev"])
    parser.add_argument("--limit", type=int, default=10, choices=[10, 20, 30])
    parser.add_argument("--min-win-rate", type=float, default=0.0, help="Percent 0-100")
    parser.add_argument("--top", type=int, default=10, help="How many scenarios to print (all are still written to file)")
    parser.add_argument("--loop", action="store_true", help="Repeat every --interval seconds instead of running once")
    parser.add_argument("--interval", type=int, default=300, help="Seconds between runs in --loop mode (default 300 = 5 min)")
    args = parser.parse_args()

    date = args.date or datetime.now().strftime("%Y-%m-%d")

    def run_once() -> None:
        report = build_report(date, args.return_type, args.product_type, args.product,
                              args.strategy_family, args.limit, args.min_win_rate)
        json_path, csv_path = write_report(report)
        print_summary(report, args.top)
        print(f"Wrote {json_path} and {csv_path}")

    run_once()
    if not args.loop:
        return 0
    try:
        while True:
            time.sleep(args.interval)
            run_once()
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
