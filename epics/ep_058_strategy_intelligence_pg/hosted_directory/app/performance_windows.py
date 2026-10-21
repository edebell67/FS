# epics/ep_058_strategy_intelligence_pg/hosted_directory/app/performance_windows.py — per-strategy performance over trading-day windows (today, yesterday, last 5 days, last 10 days, ...), for any requesting agent.
#
# VERSION HISTORY
# v1.1.0 · 2026-10-19 · make_day_fetch (cached strategy-day fetch shared by the API route and the arena provider) and performance_for (several strategies at once).
# v1.0.0 · 2026-10-19 · Initial version: days the daily target (+500 intraday peak) was hit, counted for net and alt net separately and combined; closing net, trades and win rate per window; as-at time, sample size, confidence, caveats and a snapshot id an agent can cite.
"""A strategy's answer to "how have you done?". The primary figure is days-target-hit: the cumulative net (or alt net) reached the daily target (default +500) at any
point intraday. Closing net, trades and win rate are supporting figures. Net and alt net are reported separately and as "either".

The numbers come from the same 5-minute snapshot series the dashboard shows (`build_portfolio_day`), one fetch per trading day. `fetch(model, date_iso)` returns that
payload; the caller supplies it (and its caching), which keeps this module pure and testable."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

DAILY_TARGET = 500.0
MAX_WINDOW_DAYS = 30
DEFAULT_WINDOWS = ("today", "yesterday", "last_5_days", "last_10_days")
_NAMED = {"today": 1, "last_5_days": 5, "last_10_days": 10}
_ND = re.compile(r"^last_(\d{1,2})_days$")


class WindowError(ValueError):
    pass


def trading_days(today: dt.date, count: int) -> list[dt.date]:
    """The `count` most recent weekdays, newest first, starting from `today` (or the last weekday before it when today is a weekend)."""
    out, day = [], today
    while len(out) < count:
        if day.weekday() < 5:
            out.append(day)
        day -= dt.timedelta(days=1)
    return out


def window_days(name: str, today: dt.date) -> list[dt.date]:
    """Trading days of a window, oldest first. 'today', 'yesterday' (the previous trading day), 'last_N_days' (N trading days ending at today)."""
    if name == "yesterday":
        return [trading_days(today, 2)[1]]
    n = _NAMED.get(name)
    if n is None:
        m = _ND.match(name)
        if not m or not 1 <= int(m.group(1)) <= MAX_WINDOW_DAYS:
            raise WindowError(f"unknown window {name!r}: use today, yesterday or last_N_days (N 1..{MAX_WINDOW_DAYS})")
        n = int(m.group(1))
    return sorted(trading_days(today, n))


def _first_hit(series: list[dict], key: str, target: float):
    for p in series:
        if (p.get(key) or 0) >= target:
            return p.get("time")
    return None


def day_stats(date: dt.date, payload: dict | None, target: float) -> dict:
    """One strategy-day from a build_portfolio_day payload; `has_data` False when the strategy has no series that day."""
    models = (payload or {}).get("models") or []
    m = models[0] if models else None
    series = (m or {}).get("series") or []
    if not series:
        return {"date": date.isoformat(), "has_data": False}
    peak_net = max((p.get("net") or 0) for p in series)
    peak_alt = max((p.get("alt_net") or 0) for p in series)
    return {
        "date": date.isoformat(), "has_data": True, "trades": int(m.get("trades") or 0), "wins": int(m.get("wins") or 0),
        "close_net": m.get("cum_net"), "close_alt_net": m.get("cum_alt_net"),
        "peak_net": peak_net, "peak_alt_net": peak_alt,
        "target_hit_net": peak_net >= target, "target_hit_alt_net": peak_alt >= target,
        "first_hit_net": _first_hit(series, "net", target), "first_hit_alt_net": _first_hit(series, "alt_net", target),
        "last_snapshot": series[-1].get("time"),
    }


def _confidence(days_with_data: int) -> str:
    return "high" if days_with_data >= 8 else ("medium" if days_with_data >= 3 else "low")


def build_windows(model: str, today: dt.date, fetch: Callable[[str, str], dict], windows=DEFAULT_WINDOWS, target: float = DAILY_TARGET, workers: int = 4) -> dict:
    spec = {name: window_days(name, today) for name in windows}
    needed = sorted({d for days in spec.values() for d in days})
    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        payloads = dict(zip(needed, ex.map(lambda d: fetch(model, d.isoformat()), needed)))
    per_day = {d: day_stats(d, payloads[d], target) for d in needed}
    out, product, strategy = {}, None, None
    for d in needed:
        mm = ((payloads[d] or {}).get("models") or [None])[0]
        if mm:
            product, strategy = mm.get("product") or product, mm.get("strategy") or strategy
    for name, days in spec.items():
        rows = [per_day[d] for d in days]
        have = [r for r in rows if r["has_data"]]
        net_hits = sum(1 for r in have if r["target_hit_net"])
        alt_hits = sum(1 for r in have if r["target_hit_alt_net"])
        either = sum(1 for r in have if r["target_hit_net"] or r["target_hit_alt_net"])
        trades = sum(r["trades"] for r in have)
        wins = sum(r["wins"] for r in have)
        out[name] = {
            "from": days[0].isoformat(), "to": days[-1].isoformat(), "trading_days": len(days), "days_with_data": len(have),
            "days_target_hit": {"net": net_hits, "alt_net": alt_hits, "either": either},
            "trades": trades, "win_rate_net": round(wins / trades, 4) if trades else None,
            "close_net": round(sum(r["close_net"] or 0 for r in have), 2), "close_alt_net": round(sum(r["close_alt_net"] or 0 for r in have), 2),
            "confidence": _confidence(len(have)), "days": rows,
        }
    as_of_day = max(needed)
    last = per_day[as_of_day].get("last_snapshot")
    caveats = ["Days-target-hit counts days whose cumulative net (or alt net) reached the target at any 5-minute snapshot; closing net is shown separately.",
               "Net and alt net are two sides of the same trades: an agent acting on one side gets that side's count, not the combined 'either' count.",
               "Past performance only; sample sizes are in days_with_data."]
    if today in per_day and per_day[today].get("has_data"):
        caveats.append(f"Today is partial: data to {last}.")
    missing = [d.isoformat() for d in needed if not per_day[d]["has_data"]]
    if missing:
        caveats.append(f"No snapshot data for {', '.join(missing)} (counted as no target hit only where the strategy traded; otherwise excluded from days_with_data).")
    body = {"strategy_id": model, "product": product, "strategy": strategy, "target": target, "windows": out,
            "as_of": f"{as_of_day.isoformat()}T{last}" if last else None, "source": "5-minute model snapshots (tbl_dna_model_summary_snapshots_5min) via build_portfolio_day",
            "caveats": caveats}
    body["snapshot_id"] = "perf-" + hashlib.sha256(json.dumps({k: body[k] for k in ("strategy_id", "target", "windows", "as_of")}, sort_keys=True, default=str).encode()).hexdigest()[:16]
    return body


def make_day_fetch(build_day: Callable[[str, list], dict], today_fn: Callable[[], dt.date] = dt.date.today, today_ttl_s: float = 60.0, max_entries: int = 2000):
    """fetch(model, date_iso) over `build_day(date_iso, [model])` with a cache: past days never change (kept), today is kept for `today_ttl_s` seconds."""
    cache: dict = {}
    lock = threading.Lock()

    def fetch(model: str, date_iso: str) -> dict:
        key = (model.lower(), date_iso)
        past = date_iso < today_fn().isoformat()
        with lock:
            hit = cache.get(key)
        if hit and (past or time.time() - hit[0] < today_ttl_s):
            return hit[1]
        payload = build_day(date_iso, [model])   # ids are stored upper-case (DNA_201700)
        with lock:
            if len(cache) > max_entries:
                cache.clear()
            cache[key] = (time.time(), payload)
        return payload
    return fetch


def performance_for(strategy_ids, fetch, today: dt.date | None = None, windows=DEFAULT_WINDOWS, target: float = DAILY_TARGET) -> dict:
    """{strategy_id: build_windows answer, or None when the strategy has no snapshot data in any requested window}."""
    today = today or dt.date.today()
    out = {}
    for sid in strategy_ids:
        ans = build_windows(sid.upper(), today, fetch, windows, target)
        out[sid] = ans if any(w["days_with_data"] for w in ans["windows"].values()) else None
    return out
