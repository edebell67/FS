# epics/ep_057_sql_to_pgsql/dashboards_and_uis/scenario_timeline_pool.py — time-consistent win-rate / pool / momentum scenarios (as-of every 5-minute snapshot).
#
# VERSION HISTORY
# v1.1.0 · 2026-10-22 · Filter closed-trade evidence by the selected product type and product so historical win-rate members match the active market scope.
# v1.0.1 · 2026-10-22 · a day's first pass reads the closed trades once (it took 5 minutes with one query per snapshot).
# v1.0.0 · 2026-10-22 · Initial version: top_win, strongest_three, relative_value, market_move, opposite_cluster, strengthening_cluster, repair_negative, weakening_selection and top3_momentum_{net,alt}, each decided at every snapshot with the catalogue's own rules over the figures known at that snapshot (cumulative net from the snapshot, trades and win rate from the closed trades up to it).
"""The scenarios that need more than a ranking of snapshot values.

`top10_live_server._requested_scenario_ids` defines them over end-of-day figures. Here the same definitions are evaluated at every snapshot with what was known then:
net / alt net from the snapshot, trades and wins from the closed trades whose last_update is at or before it, the intraday peak from the snapshots so far, the trailing-hour
change from the last hour of snapshots. All scenarios share one pass over the day, are cached together (one JSON file per day / universe / limit / display metric) and a
running day is extended from the persisted counters, so only new snapshots are processed.

Rounding: net and alt net to the cent, win rate to 0.1, exactly as the day statistics round them (half away from zero, computed on floats)."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import os
import re
import threading
from pathlib import Path

from scenario_timeline import bucket_label, intervals_from_members

ALGORITHM = "p2"
CACHE_DIR = Path(os.environ.get("SCENARIO_TIMELINE_CACHE", Path(__file__).resolve().parent / "scenario_timeline_cache"))
MIN_SCENARIO_MODELS = 2   # fewer qualifying models -> the scenario falls back to top net (as the catalogue does)
MOMENTUM_WINDOW_MINUTES = 60

POOL_SCENARIOS = frozenset({
    "top_win", "WIN_RATE", "strongest_three", "relative_value", "market_move", "opposite_cluster", "strengthening_cluster", "repair_negative",
    "weakening_selection", "top3_momentum_net", "top3_momentum_alt",
})

SNAPSHOT_SQL = "SELECT model, cum_net, cum_alt_net FROM tbl_dna_model_summary_snapshots_5min WHERE snapshot_timestamp = %s"
STAMPS_SQL = """SELECT DISTINCT snapshot_timestamp FROM tbl_dna_model_summary_snapshots_5min
                WHERE snapshot_timestamp > %s AND snapshot_timestamp >= %s::date AND snapshot_timestamp < %s::date + INTERVAL '1 day' ORDER BY 1"""
EVENTS_SQL = """SELECT c.model, c.last_update, (c.net_return > 0), (c.alt_net_return > 0) FROM combined_trades_closed c
                WHERE c.created >= %s::date AND c.created < %s::date + INTERVAL '1 day'
                  AND c.last_update > %s AND c.last_update <= %s
                  AND (%s = 'all' OR LOWER(TRIM(c.product_type)) = %s)
                  AND (%s = 'all' OR LOWER(TRIM(c.product)) = %s)
                ORDER BY c.last_update"""

_LOCK = threading.Lock()
_MEMORY: dict[tuple, dict] = {}


def is_pool_scenario(scenario) -> bool:
    return isinstance(scenario, str) and scenario in POOL_SCENARIOS


def round_half_up(value: float, digits: int) -> float:
    scale = 10 ** digits
    return math.copysign(math.floor(abs(value) * scale + 0.5 + 1e-9) / scale, value)


def _tp_pips(stat: dict) -> float:
    return (stat.get("target_profit") or 0) / 10


def pick_members(rows: list[dict], history: dict, limit: int, display_metric: str) -> dict[str, list[str]]:
    """Every pool scenario's members at one snapshot. `rows` are the models known at it (dicts with model, net, alt, trades, win_rate, strategy, target_profit, peak);
    `history` has the momentum figures {"net": {model: change}, "alt": {...}}. Pure: no database."""
    big = max(limit, limit * 5)
    by_net = sorted(rows, key=lambda s: (-s["net"], -s["win_rate"], s["model"]))
    top_net = by_net[:big]
    winners = sorted((s for s in rows if s["win_rate"] >= 50), key=lambda s: (-s["win_rate"], -s["net"], s["model"]))[:big]
    top_win = winners or top_net
    pool, seen = [], set()
    for s in top_net + winners:
        if s["model"] not in seen:
            seen.add(s["model"])
            pool.append(s)
    value_key = "alt" if str(display_metric).lower() in {"alt", "alt_net"} else "net"

    def choose(models, count=limit):
        selected = list(models)[:max(count, count * 5)]
        return selected if len(selected) >= MIN_SCENARIO_MODELS else top_net

    def drawdown(s):
        return s["peak"] - s["net_raw"]

    lists = {
        "top_win": top_win,
        "WIN_RATE": top_win,
        "strongest_three": sorted(pool, key=lambda s: -s["net"])[:max(3, min(15, limit * 5))],
        "relative_value": choose(sorted((s for s in pool if s["win_rate"] >= 85), key=lambda s: -s["win_rate"])),
        "market_move": choose(s for s in pool if _tp_pips(s) >= 10),
        "opposite_cluster": choose(s for s in pool if 3 <= _tp_pips(s) <= 5),
        "strengthening_cluster": choose(s for s in pool if (s.get("strategy") or "").startswith("breakout_R_")),
        "repair_negative": choose(s for s in pool if s["win_rate"] == 100 and s["net"] > 0),
        "weakening_selection": choose(sorted((s for s in pool if drawdown(s) > 0), key=lambda s: (-s["trades"], -drawdown(s), s["model"]))),
    }
    out: dict[str, list[str]] = {}
    for scenario, stats in lists.items():
        result_limit = min(3, limit) if scenario == "strongest_three" else limit
        distinct, signatures = [], set()
        for s in stats:
            signature = round_half_up(s[value_key], 2)
            if signature in signatures:
                continue
            signatures.add(signature)
            distinct.append(s["model"])
            if len(distinct) >= min(result_limit, len(stats)):
                break
        out[scenario] = distinct
    by_model = {s["model"]: s for s in rows}
    for metric, scenario in (("net", "top3_momentum_net"), ("alt", "top3_momentum_alt")):
        candidates = sorted(((change, end, by_model[m]["win_rate"], m) for m, (change, end) in history[metric].items() if m in by_model),
                            key=lambda row: (-row[0], -row[1], -row[2], row[3]))
        picked, scores = [], set()
        for change, _end, _win, model in candidates:
            score = round_half_up(change, 2)
            if score in scores:
                continue
            scores.add(score)
            picked.append(model)
            if len(picked) >= min(3, limit):
                break
        out[scenario] = picked
    return out


def _cache_file(key: tuple) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", "pool_" + "_".join(str(part) for part in key) + f"_{ALGORITHM}")
    return CACHE_DIR / (safe + ".json")


def _load(key: tuple) -> dict:
    with _LOCK:
        if key in _MEMORY:
            return _MEMORY[key]
    entry = {"stamps": [], "members": {}, "state": None, "complete": False}
    try:
        raw = json.loads(_cache_file(key).read_text(encoding="utf-8"))
        if isinstance(raw.get("stamps"), list) and isinstance(raw.get("members"), dict):
            entry = raw
    except (OSError, ValueError):
        pass
    with _LOCK:
        _MEMORY[key] = entry
    return entry


def _save(key: tuple, entry: dict) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = _cache_file(key).with_suffix(".tmp")
        tmp.write_text(json.dumps(entry), encoding="utf-8")
        tmp.replace(_cache_file(key))
    except OSError:
        pass


def _fresh_state() -> dict:
    return {"trades": {}, "wins": {}, "peak": {}, "events_until": None}


def _momentum(ring: list[tuple[int, dict, dict]], minute: int, nets: dict, alts: dict) -> dict:
    """Trailing-hour change per model: the latest figure minus the one at the newest earlier snapshot at least an hour back (the day's first snapshot when the day is
    younger than that), the catalogue's own anchor rule."""
    cutoff = minute - MOMENTUM_WINDOW_MINUTES
    anchor = None
    for entry in reversed(ring):
        if entry[0] <= cutoff:
            anchor = entry
            break
    if anchor is None:
        anchor = ring[0]
    return {"net": {m: (v - anchor[1].get(m, v), v) for m, v in nets.items()}, "alt": {m: (v - anchor[2].get(m, v), v) for m, v in alts.items()}}


def day_schedule(cur, date_str: str, stats: list[dict], limit: int, display_metric: str, universe: str,
                 today_iso: str | None = None, product_type: str = "all", product: str = "all") -> dict[str, dict]:
    """Extends the cached pass over `date_str` with the snapshots it has not seen and returns {scenario: {"order": [...], "intervals": {...}}}."""
    today_iso = today_iso or dt.date.today().isoformat()
    metric = "alt" if str(display_metric).lower() in {"alt", "alt_net"} else "net"
    key = (date_str, universe, int(limit), metric)
    entry = _load(key)
    meta = {s["model"]: s for s in stats}
    if not (entry.get("complete") and date_str < today_iso):
        cur.execute(STAMPS_SQL, (entry["stamps"][-1] if entry["stamps"] else f"{date_str} 00:00:00", date_str, date_str))
        new_stamps = [row[0] for row in cur.fetchall()]
        if new_stamps:
            _extend(cur, entry, date_str, new_stamps, meta, int(limit), metric,
                    final_day=(date_str < today_iso), product_type=product_type, product=product)
            _save(key, entry)
        elif date_str < today_iso and entry["stamps"]:
            entry["complete"] = True
            _save(key, entry)
    out = {}
    for scenario, by_stamp in entry["members"].items():
        out[scenario] = dict(zip(("order", "intervals"), intervals_from_members(entry["stamps"], by_stamp, open_ended_last=(date_str >= today_iso))))
    return out


def _extend(cur, entry: dict, date_str: str, new_stamps: list, meta: dict, limit: int, metric: str,
            final_day: bool, product_type: str, product: str) -> None:
    state = entry.get("state") or _fresh_state()
    trades, wins, peak = state["trades"], state["wins"], state["peak"]
    stamps_done = list(entry["stamps"])
    members = entry["members"]
    for scenario in list(POOL_SCENARIOS):
        members.setdefault(scenario, {})
    # the momentum anchor needs the last hour of snapshots: re-read it for a resumed day
    ring: list[tuple[int, dict, dict]] = []
    if stamps_done:
        for stamp in stamps_done[-14:]:
            cur.execute(SNAPSHOT_SQL, (stamp,))
            rows = [r for r in cur.fetchall() if r[0] in meta]
            ring.append((_minute_of(stamp), {r[0]: float(r[1] or 0) for r in rows}, {r[0]: float(r[2] or 0) for r in rows}))
    previous_rows = len(ring[-1][1]) if ring else 0
    # many new snapshots (a day's first pass): read the closed trades once and advance through them; a refresh asks per snapshot
    batch_events, pointer = None, 0
    if len(new_stamps) > 3:
        last_stamp = new_stamps[-1] if isinstance(new_stamps[-1], dt.datetime) else dt.datetime.fromisoformat(str(new_stamps[-1]))
        cur.execute(EVENTS_SQL, (date_str, date_str, state["events_until"] or f"{date_str} 00:00:00", last_stamp,
                                 product_type, product_type, product, product))
        batch_events = cur.fetchall()
    for index, ts in enumerate(new_stamps):
        stamp = ts if isinstance(ts, dt.datetime) else dt.datetime.fromisoformat(str(ts))
        cur.execute(SNAPSHOT_SQL, (stamp,))
        snap = [r for r in cur.fetchall() if r[0] in meta]
        newest = index == len(new_stamps) - 1
        if newest and not final_day and previous_rows and len(snap) < 0.9 * previous_rows:
            break   # the snapshot is still being written: take it on the next refresh
        if batch_events is not None:
            due = []
            while pointer < len(batch_events) and batch_events[pointer][1] <= stamp:
                due.append(batch_events[pointer])
                pointer += 1
        else:
            cur.execute(EVENTS_SQL, (date_str, date_str, state["events_until"] or f"{date_str} 00:00:00", stamp,
                                     product_type, product_type, product, product))
            due = cur.fetchall()
        for model, _last_update, win, _alt_win in due:
            trades[model] = trades.get(model, 0) + 1
            if win:
                wins[model] = wins.get(model, 0) + 1
        state["events_until"] = stamp.isoformat()
        nets = {r[0]: float(r[1] or 0) for r in snap}
        alts = {r[0]: float(r[2] or 0) for r in snap}
        for model, value in nets.items():
            if value > peak.get(model, -1e18):
                peak[model] = value
        minute = _minute_of(stamp.isoformat())
        ring.append((minute, nets, alts))
        if len(ring) > 14:
            ring.pop(0)
        rows = []
        for model, net_raw in nets.items():
            count = trades.get(model, 0)
            if not count:
                continue   # the day statistics list only models that have closed a trade
            info = meta[model]
            rows.append({"model": model, "net_raw": net_raw, "net": round_half_up(net_raw, 2), "alt": round_half_up(alts[model], 2), "trades": count,
                         "win_rate": round_half_up(wins.get(model, 0) / count * 100, 1), "strategy": info.get("strategy"),
                         "target_profit": info.get("target_profit"), "peak": peak.get(model, net_raw)})
        picked = pick_members(rows, _momentum(ring, minute, {m: nets[m] for m in nets if trades.get(m)}, {m: alts[m] for m in alts if trades.get(m)}), limit, metric)
        for scenario, ids in picked.items():
            members[scenario][stamp.isoformat()] = ids
        stamps_done.append(stamp.isoformat())
        previous_rows = len(snap)
    entry["stamps"] = stamps_done
    entry["state"] = state
    if final_day and stamps_done:
        entry["complete"] = True


def _minute_of(stamp: str) -> int:
    stamp = dt.datetime.fromisoformat(stamp) if not isinstance(stamp, dt.datetime) else stamp
    return stamp.hour * 60 + stamp.minute


def scenario_schedule(cur, date_str: str, scenario: str, stats: list[dict], limit: int, display_metric: str, universe_prefix: str,
                      today_iso: str | None = None, product_type: str = "all", product: str = "all") -> tuple[list[str], dict[str, list[dict]]]:
    """The scenario's (models in first-appearance order, leader_intervals by model); the pass is shared by every pool scenario of the same day and filters."""
    scenario = "top_win" if scenario == "WIN_RATE" else scenario
    digest = hashlib.sha1(",".join(sorted(s["model"] for s in stats)).encode()).hexdigest()[:10]
    schedules = day_schedule(cur, date_str, stats, limit, display_metric,
                             f"{universe_prefix}-{product_type}-{product}-{len(stats)}-{digest}",
                             today_iso, product_type, product)
    picked = schedules.get(scenario)
    if picked is None:
        raise ValueError(f"no snapshot timeline for scenario {scenario}")
    return picked["order"], picked["intervals"]
