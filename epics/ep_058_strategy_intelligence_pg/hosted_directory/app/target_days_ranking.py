# epics/ep_058_strategy_intelligence_pg/hosted_directory/app/target_days_ranking.py — which strategies reached the daily target on the most days of the last x trading days.
#
# VERSION HISTORY
# v1.2.0 · 2026-10-21 · Past-day peaks persist to a JSON file (survive restarts; keyed by day and product type, independent of target / return type) and `prewarm` fills the window in the background, so the Target leaders modal no longer pays 44-90 s per cold load; 4 workers.
# v1.1.0 · 2026-10-20 · return_type (net | alt_net | either) replaces side; target and lookback (days) are parameters.
# v1.0.0 · 2026-10-20 · Initial version: per-strategy-name daily peaks (sum of cum_net / cum_alt_net over every model of that strategy at each 5-minute snapshot, then the day's maximum), days-target-hit for net, alt net and either, ranked.
"""The question: "get the best performing strategy in the last x days (criteria = max count of days with net >= target OR alt net >= target)".

A *strategy* here is a strategy name (`breakout_2_tp10_sl50`) aggregated over all the models that run it (one per product), the level of the table that prompted this. For every trading day
the day's peak is the maximum, over the day's 5-minute snapshots, of the sum of the strategy's models' cumulative net (and, separately, alt net). A day counts as a hit when that peak reaches
the target. `return_type` picks what the ranking counts: `net`, `alt_net`, or `either`; the other counts are returned too and break ties.

`fetch_day(date_iso, product_type)` returns {strategy: {"net": peak, "alt": peak, "models": count}} and is supplied by the caller (with its caching), which keeps this module pure."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from .performance_windows import DAILY_TARGET, MAX_WINDOW_DAYS, trading_days

RETURN_TYPES = ("net", "alt_net", "either")   # which return the target is tested against: net, alt net, or a day counts when either reached it
PRODUCT_TYPES = ("forex", "crypto", "all")

PEAKS_SQL = """
    WITH bounds AS (SELECT %s::date AS day), per_time AS (
        SELECT TRIM(pf.strategy_name) AS strategy, s.snapshot_timestamp,
               SUM(s.cum_net) AS net, SUM(s.cum_alt_net) AS alt, COUNT(*) AS models
        FROM tbl_dna_model_summary_snapshots_5min s
        JOIN product_forex pf ON pf.model = s.model
        CROSS JOIN bounds b
        WHERE s.snapshot_timestamp >= b.day
          AND s.snapshot_timestamp < b.day + INTERVAL '1 day'
          AND (%s = 'all' OR LOWER(TRIM(pf.product_type)) = %s)
          AND pf.strategy_name IS NOT NULL
        GROUP BY 1, 2
    )
    SELECT strategy, MAX(net), MAX(alt), MAX(models) FROM per_time GROUP BY strategy;
"""


class RankingError(ValueError):
    pass


def make_day_fetch(run_sql: Callable[[str, tuple], list], today_fn: Callable[[], dt.date] = dt.date.today, today_ttl_s: float = 120.0, max_entries: int = 200,
                   persist_path: str | None = None):
    """fetch_day(date_iso, product_type) over `run_sql(sql, params) -> rows`; past days never change (kept, and written to `persist_path` when given), today is kept for `today_ttl_s` seconds."""
    cache: dict = {}
    lock = threading.Lock()
    if persist_path and os.path.exists(persist_path):
        try:
            with open(persist_path, encoding="utf-8") as fh:
                for k, v in json.load(fh).items():
                    day, _, ptype = k.partition("|")
                    cache[(day, ptype)] = (0.0, v)
        except (OSError, ValueError):
            cache.clear()   # an unreadable file is only a cold cache

    def save() -> None:
        if not persist_path:
            return
        today_iso = today_fn().isoformat()
        with lock:
            past = {f"{d}|{p}": v[1] for (d, p), v in cache.items() if d < today_iso}
        tmp = persist_path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(past, fh)
            os.replace(tmp, persist_path)
        except OSError:
            pass

    def fetch(date_iso: str, product_type: str) -> dict:
        key = (date_iso, product_type)
        past = date_iso < today_fn().isoformat()
        with lock:
            hit = cache.get(key)
        if hit and (past or time.time() - hit[0] < today_ttl_s):
            return hit[1]
        rows = run_sql(PEAKS_SQL, (date_iso, product_type, product_type))
        out = {str(r[0]): {"net": float(r[1] or 0), "alt": float(r[2] or 0), "models": int(r[3] or 0)} for r in rows if r[0]}
        with lock:
            if len(cache) > max_entries:
                cache.clear()
            cache[key] = (time.time(), out)
        if past:
            save()
        return out
    return fetch


def rank_by_target_days(today: dt.date, fetch_day: Callable[[str, str], dict], days: int = 20, target: float = DAILY_TARGET, return_type: str = "net",
                        limit: int = 10, product_type: str = "forex", workers: int = 4) -> dict:
    """`today` is the last day of the window; `days` the lookback in trading days; `target` the money the day's peak must reach; `return_type` net | alt_net | either."""
    if return_type not in RETURN_TYPES:
        raise RankingError(f"return_type must be one of {RETURN_TYPES}")
    if target <= 0:
        raise RankingError("target must be above zero")
    if product_type not in PRODUCT_TYPES:
        raise RankingError(f"product_type must be one of {PRODUCT_TYPES}")
    if not 1 <= days <= MAX_WINDOW_DAYS:
        raise RankingError(f"days must be 1..{MAX_WINDOW_DAYS}")
    if not 1 <= limit <= 100:
        raise RankingError("limit must be 1..100")
    window = sorted(trading_days(today, days))
    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        per_day = dict(zip(window, ex.map(lambda d: fetch_day(d.isoformat(), product_type), window)))
    strategies: dict[str, dict] = {}
    for d in window:
        for name, peak in per_day[d].items():
            row = strategies.setdefault(name, {"strategy": name, "days_with_data": 0, "hit_net": 0, "hit_alt": 0, "hit_either": 0, "models": 0, "days": []})
            net_hit, alt_hit = peak["net"] >= target, peak["alt"] >= target
            row["days_with_data"] += 1
            row["hit_net"] += net_hit
            row["hit_alt"] += alt_hit
            row["hit_either"] += net_hit or alt_hit
            row["models"] = max(row["models"], peak["models"])
            row["days"].append({"date": d.isoformat(), "peak_net": round(peak["net"], 2), "peak_alt_net": round(peak["alt"], 2), "hit_net": net_hit, "hit_alt_net": alt_hit})
    primary = {"either": "hit_either", "net": "hit_net", "alt_net": "hit_alt"}[return_type]
    ordered = sorted(strategies.values(), key=lambda r: (-r[primary], -r["hit_either"], -r["hit_net"], -r["hit_alt"], r["strategy"]))
    ranking = [{"rank": i + 1, "strategy": r["strategy"], "days_target_hit": {"either": r["hit_either"], "net": r["hit_net"], "alt_net": r["hit_alt"]},
                "days_with_data": r["days_with_data"], "models": r["models"], "days": r["days"]} for i, r in enumerate(ordered[:limit])]
    last_day = window[-1]
    caveats = ["A strategy is a strategy name aggregated over all its models (one per product); the day's peak is the highest sum of their cumulative net (or alt net) at any 5-minute snapshot.",
               "Net and alt net are two sides of the same trades; 'either' counts a day if either side reached the target, an agent trading one side gets that side's count (return_type net or alt_net).",
               "Past performance only; days_with_data is the sample size per strategy."]
    if last_day == today:
        caveats.append("Today is partial and counts only the snapshots so far.")
    body = {"question": f"best performing strategy in the last {days} trading days (most days with {'net or alt net' if return_type == 'either' else return_type} peak >= {target:g})",
            "window": {"from": window[0].isoformat(), "to": last_day.isoformat(), "trading_days": len(window)}, "target": target, "return_type": return_type, "lookback_days": days, "product_type": product_type,
            "strategies_considered": len(strategies), "ranking": ranking, "caveats": caveats,
            "source": "5-minute model snapshots (tbl_dna_model_summary_snapshots_5min) joined to product_forex.strategy_name"}
    body["snapshot_id"] = "rank-" + hashlib.sha256(json.dumps({k: body[k] for k in ("window", "target", "return_type", "product_type", "ranking")}, sort_keys=True, default=str).encode()).hexdigest()[:16]
    return body


def prewarm(today: dt.date, fetch_day: Callable[[str, str], dict], product_types=("forex", "all"), days: int = 20, workers: int = 4) -> None:
    """Fills the day cache for the default window so the first modal open is instant; failures are ignored (the request path retries)."""
    for ptype in product_types:
        try:
            with ThreadPoolExecutor(max_workers=workers) as ex:
                list(ex.map(lambda d: fetch_day(d.isoformat(), ptype), trading_days(today, days)))
        except Exception:   # noqa: BLE001 - a warm-up must never take the service down
            continue
