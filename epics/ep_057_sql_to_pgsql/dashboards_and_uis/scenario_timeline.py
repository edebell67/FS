# epics/ep_057_sql_to_pgsql/dashboards_and_uis/scenario_timeline.py — who was in a scenario's top N at every 5-minute snapshot, as per-model leader_intervals.
#
# VERSION HISTORY
# v1.1.0 · 2026-10-22 · Strategies with the same P&L (to the cent) at a snapshot count once, as the catalogue's "distinct outcomes" rule does (grouped in the query: the lowest model id represents a group), so each snapshot has up to N distinct lines; early in the day there can be fewer.
# v1.0.0 · 2026-10-22 · Initial version: Top Net and Top Alt Net. A strategy's curve is shown only while it is in the top N at the snapshot (its line starts at its real cumulative value when it joins and stops when it drops out), so a chart looks the same whenever it is viewed.
"""Time-consistent scenarios.

A scenario such as "Top 10 Net Return" used to take the top N at the moment the chart was opened and draw those curves from midnight, so the same chart looked
different at 03:00 and at 13:00. Here the membership is evaluated at every snapshot: `members[ts]` = the N strategies with the highest score at that snapshot. A
strategy's `leader_intervals` are the runs of consecutive snapshots in which it was a member: `{"start": "HH:MM", "end": "HH:MM"}` with `end` exclusive, in the same
five-minute bucket labels the chart series use (a snapshot at 00:01:30 is the 00:05 point). The page draws a point only inside one of the intervals.

Past snapshots never change, so the membership is kept (memory and a JSON file per day / scenario / universe) and only snapshots newer than the last cached one are
ranked. The newest cached snapshot is always re-ranked in case it was still being written."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import threading
from pathlib import Path

ALGORITHM = "d2"   # part of every cache file name: bump when the membership rule changes so older files are never reused
CACHE_DIR = Path(os.environ.get("SCENARIO_TIMELINE_CACHE", Path(__file__).resolve().parent / "scenario_timeline_cache"))

# scenario id -> SQL expression ranking a snapshot row (higher is better)
SCORES = {
    "top_net": "x.cum_net",
    "NET_RETURN": "x.cum_net",
    "top_alt_net": "x.cum_alt_net",
}
TIMELINE_SCENARIOS = frozenset(SCORES)

RANK_SQL = """
    WITH stamps AS (
        SELECT DISTINCT snapshot_timestamp AS ts FROM tbl_dna_model_summary_snapshots_5min
        WHERE snapshot_timestamp > %s AND snapshot_timestamp >= %s::date AND snapshot_timestamp < %s::date + INTERVAL '1 day'
    )
    SELECT st.ts, t.model, t.rn, t.cents FROM stamps st
    CROSS JOIN LATERAL (
        SELECT g.model, g.cents, ROW_NUMBER() OVER (ORDER BY g.cents DESC NULLS LAST, g.model) AS rn
        FROM (
            SELECT ROUND(({score})::numeric, 2) AS cents, MIN(x.model) AS model
            FROM tbl_dna_model_summary_snapshots_5min x
            WHERE x.snapshot_timestamp = st.ts AND x.model = ANY(%s)
            GROUP BY 1
        ) g
        ORDER BY g.cents DESC NULLS LAST, g.model
        LIMIT %s
    ) t
    ORDER BY st.ts, t.rn
"""

_LOCK = threading.Lock()
_MEMORY: dict[tuple, dict] = {}   # key -> {"stamps": [iso...], "members": {iso: [model, ...]}}


def bucket_label(ts: dt.datetime) -> str:
    """The chart's label for a snapshot: rounded UP to the next five minutes (00:01:30 -> 00:05), capped at 23:55."""
    minutes = ts.hour * 60 + ts.minute + (1 if ts.second or ts.microsecond else 0)
    bucket = min(1435, ((minutes + 4) // 5) * 5)
    return f"{bucket // 60:02d}:{bucket % 60:02d}"


def _minutes(label: str) -> int:
    return int(label[:2]) * 60 + int(label[3:5])


def _label(minutes: int) -> str:
    return "24:00" if minutes >= 1440 else f"{minutes // 60:02d}:{minutes % 60:02d}"


def universe_key(product_type: str, product: str, family: str, ids: list[str]) -> str:
    digest = hashlib.sha1(",".join(sorted(ids)).encode()).hexdigest()[:10]
    return f"{product_type}-{product}-{family}-{len(ids)}-{digest}"


def intervals_from_members(stamps: list[str], members: dict[str, list[str]], open_ended_last: bool) -> tuple[list[str], dict[str, list[dict]]]:
    """-> (models in order of first appearance, {model: [{"start", "end"}]}). `stamps` are ISO timestamps in time order; a run that reaches the newest stamp is
    open-ended ("24:00") while the day is still running."""
    labels = [bucket_label(dt.datetime.fromisoformat(ts)) for ts in stamps]
    runs: dict[str, list[list[int]]] = {}   # model -> [[first_index, last_index], ...]
    order: list[str] = []
    previous: set[str] = set()
    for index, ts in enumerate(stamps):
        current = set(members.get(ts, []))
        for model in members.get(ts, []):
            if model not in runs:
                runs[model] = []
                order.append(model)
            if model in previous and runs[model] and runs[model][-1][1] == index - 1:
                runs[model][-1][1] = index
            else:
                runs[model].append([index, index])
        previous = current
    intervals: dict[str, list[dict]] = {}
    last_index = len(stamps) - 1
    for model, model_runs in runs.items():
        out = []
        for first, last in model_runs:
            start = _minutes(labels[first])
            if last >= last_index:
                end = 1440 if open_ended_last else _minutes(labels[last]) + 5
            else:
                end = _minutes(labels[last + 1])
            if end <= start:
                end = start + 5
            out.append({"start": _label(start), "end": _label(end)})
        intervals[model] = out
    return order, intervals


def _cache_file(key: tuple) -> Path:
    date_str, scenario, limit, universe = key
    return CACHE_DIR / f"{date_str}_{scenario}_{limit}_{universe}_{ALGORITHM}.json"


def _load(key: tuple) -> dict:
    with _LOCK:
        if key in _MEMORY:
            return _MEMORY[key]
    entry = {"stamps": [], "members": {}}
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


def leader_schedule(cur, date_str: str, scenario: str, limit: int, universe_ids: list[str], universe: str,
                    today_iso: str | None = None) -> tuple[list[str], dict[str, list[dict]]]:
    """The scenario's members at every snapshot of `date_str` as (models in first-appearance order, leader_intervals by model). Ranks only snapshots newer than
    the cached ones (the newest cached one again), so after the first load of a day a refresh costs a few hundred milliseconds."""
    if scenario not in SCORES:
        raise ValueError(f"no snapshot timeline for scenario {scenario}")
    today_iso = today_iso or dt.date.today().isoformat()
    key = (date_str, scenario, int(limit), universe)
    entry = _load(key)
    stamps: list[str] = entry["stamps"]
    after = stamps[-2] if len(stamps) >= 2 else f"{date_str} 00:00:00"
    if entry.get("complete") and date_str < today_iso:
        pass   # a finished day that was ranked after it ended: nothing can change
    else:
        cur.execute(RANK_SQL.format(score=SCORES[scenario]), (after, date_str, date_str, list(universe_ids), int(limit)))
        rows = cur.fetchall()
        by_stamp: dict[str, list[str]] = {}
        for ts, model, _rn, _cents in rows:
            by_stamp.setdefault(ts.isoformat(), []).append(model)
        if by_stamp:
            with _LOCK:
                merged = {ts: models for ts, models in entry["members"].items() if ts < min(by_stamp)}
                merged.update(by_stamp)
                entry["members"] = merged
                entry["stamps"] = sorted(merged)
        if date_str < today_iso and entry["stamps"]:
            entry["complete"] = True   # ranked after the day ended: the last snapshot is final
        _save(key, entry)
    return intervals_from_members(entry["stamps"], entry["members"], open_ended_last=(date_str >= today_iso))
