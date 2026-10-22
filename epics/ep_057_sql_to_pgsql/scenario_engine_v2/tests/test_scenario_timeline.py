# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_scenario_timeline.py — time-consistent scenarios (dashboards_and_uis/scenario_timeline.py).
#
# VERSION HISTORY
# v1.0.0 · 2026-10-22 · Initial version: bucket labels, interval building (joins, drops, re-entry, open end), caching of finished days, incremental ranking of today.
"""No database needed: the ranking cursor is a fake that answers from a table of snapshots."""
import datetime as dt
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "dashboards_and_uis"))
tl = pytest.importorskip("scenario_timeline")


def ts(hhmmss: str, day="2026-10-20") -> dt.datetime:
    return dt.datetime.fromisoformat(f"{day} {hhmmss}")


def test_a_snapshot_is_labelled_with_the_next_five_minute_bucket_like_the_chart_series():
    assert tl.bucket_label(ts("00:01:30")) == "00:05"
    assert tl.bucket_label(ts("03:05:00")) == "03:05"
    assert tl.bucket_label(ts("03:05:01")) == "03:10"
    assert tl.bucket_label(ts("23:58:40")) == "23:55"   # capped, as the chart's time axis is


def members_for(table):
    stamps = sorted(table)
    return stamps, {s: table[s] for s in stamps}


def test_a_strategy_is_shown_only_while_it_is_in_the_top_n_and_its_replacement_starts_when_it_drops_out():
    # dna_1 leads 01:00-03:00 and drops out at 03:05, dna_11 replaces it from 03:05
    table = {}
    for minute in range(60, 200, 5):
        t = f"2026-10-20T{minute // 60:02d}:{minute % 60:02d}:00"
        table[t] = ["DNA_1", "DNA_2"] if minute <= 180 else ["DNA_11", "DNA_2"]
    stamps, members = members_for(table)
    order, intervals = tl.intervals_from_members(stamps, members, open_ended_last=False)
    assert order == ["DNA_1", "DNA_2", "DNA_11"]
    assert intervals["DNA_1"] == [{"start": "01:00", "end": "03:05"}]   # last drawn point 03:00, end exclusive
    assert intervals["DNA_11"] == [{"start": "03:05", "end": "03:20"}]  # a finished day: the last point drawn is 03:15, end exclusive
    assert intervals["DNA_2"] == [{"start": "01:00", "end": "03:20"}]


def test_a_strategy_that_leaves_and_comes_back_gets_two_intervals():
    stamps = [f"2026-10-20T10:{m:02d}:00" for m in range(0, 30, 5)]
    members = {stamps[0]: ["A"], stamps[1]: ["A"], stamps[2]: ["B"], stamps[3]: ["A"], stamps[4]: ["A"], stamps[5]: ["A"]}
    _order, intervals = tl.intervals_from_members(stamps, members, open_ended_last=True)
    assert intervals["A"] == [{"start": "10:00", "end": "10:10"}, {"start": "10:15", "end": "24:00"}]
    assert intervals["B"] == [{"start": "10:10", "end": "10:15"}]


def test_a_run_reaching_the_newest_snapshot_stays_open_while_the_day_is_running():
    stamps = ["2026-10-21T00:01:30", "2026-10-21T00:06:30"]
    members = {s: ["A"] for s in stamps}
    open_end = tl.intervals_from_members(stamps, members, open_ended_last=True)[1]["A"]
    closed = tl.intervals_from_members(stamps, members, open_ended_last=False)[1]["A"]
    assert open_end == [{"start": "00:05", "end": "24:00"}]
    assert closed == [{"start": "00:05", "end": "00:15"}]


class FakeCursor:
    """Answers RANK_SQL from {iso stamp: [models in rank order]}; counts the calls and remembers the lower bound each time."""
    def __init__(self, table):
        self.table, self.calls, self.rows = table, [], []

    def execute(self, sql, params):
        after, _d1, _d2, ids, limit = params
        self.calls.append(after)
        scores = getattr(self, "scores", {})
        self.rows = [(dt.datetime.fromisoformat(s), m, rank + 1, scores.get((s, m), 100.0 - rank)) for s in sorted(self.table) if dt.datetime.fromisoformat(s) > dt.datetime.fromisoformat(after)
                     for rank, m in enumerate([x for x in self.table[s] if x in ids][:limit])]

    def fetchall(self):
        return self.rows


@pytest.fixture()
def cache_dir(monkeypatch):
    path = Path(tempfile.mkdtemp())
    monkeypatch.setattr(tl, "CACHE_DIR", path)
    tl._MEMORY.clear()
    yield path
    tl._MEMORY.clear()


def test_a_finished_day_is_ranked_once_and_then_served_from_the_cache(cache_dir):
    table = {f"2026-10-20T10:{m:02d}:00": ["A", "B"] for m in range(0, 30, 5)}
    cur = FakeCursor(table)
    first = tl.leader_schedule(cur, "2026-10-20", "top_net", 2, ["A", "B", "C"], "u1", today_iso="2026-10-21")
    again = tl.leader_schedule(cur, "2026-10-20", "top_net", 2, ["A", "B", "C"], "u1", today_iso="2026-10-21")
    assert first == again and len(cur.calls) == 1
    tl._MEMORY.clear()   # a restart: the file answers
    assert tl.leader_schedule(cur, "2026-10-20", "top_net", 2, ["A", "B", "C"], "u1", today_iso="2026-10-21") == first and len(cur.calls) == 1


def test_today_is_ranked_incrementally_and_the_newest_cached_snapshot_is_ranked_again(cache_dir):
    table = {f"2026-10-21T09:{m:02d}:00": ["A"] for m in (0, 5, 10)}
    cur = FakeCursor(table)
    tl.leader_schedule(cur, "2026-10-21", "top_net", 1, ["A", "B"], "u1", today_iso="2026-10-21")
    table["2026-10-21T09:15:00"] = ["B"]   # a new snapshot arrives
    table["2026-10-21T09:10:00"] = ["B"]   # and the newest cached one had been captured half-written
    _order, intervals = tl.leader_schedule(cur, "2026-10-21", "top_net", 1, ["A", "B"], "u1", today_iso="2026-10-21")
    assert cur.calls[1] == "2026-10-21T09:05:00"   # re-ranks from the one before the newest cached stamp, not from midnight
    assert intervals["A"] == [{"start": "09:00", "end": "09:10"}] and intervals["B"] == [{"start": "09:10", "end": "24:00"}]


def test_a_day_cached_while_it_was_running_is_completed_after_it_ends(cache_dir):
    table = {"2026-10-20T23:50:00": ["A"], "2026-10-20T23:55:00": ["A"]}
    cur = FakeCursor({"2026-10-20T23:50:00": ["A"]})
    tl.leader_schedule(cur, "2026-10-20", "top_net", 1, ["A"], "u1", today_iso="2026-10-20")   # cached during the day
    cur.table = table   # the last snapshot landed afterwards
    _o, iv = tl.leader_schedule(cur, "2026-10-20", "top_net", 1, ["A"], "u1", today_iso="2026-10-21")
    assert len(cur.calls) == 2 and iv["A"] == [{"start": "23:50", "end": "24:00"}]   # the late snapshot is included
    again = tl.leader_schedule(cur, "2026-10-20", "top_net", 1, ["A"], "u1", today_iso="2026-10-21")
    assert len(cur.calls) == 2 and again[1]["A"] == iv["A"]   # now final


def test_unknown_scenarios_are_refused():
    with pytest.raises(ValueError):
        tl.leader_schedule(None, "2026-10-20", "top_win", 10, [], "u")



def test_plan_recognises_the_catalogue_scenarios_and_their_cohort_sizes():
    assert tl.plan("top_net", 10)["groups"] == [("top_net", None, 10)] and tl.plan("NET_RETURN", 7)["score"] == "net"
    assert tl.plan("top_alt_net", 10)["score"] == "alt" and tl.plan("top_buy_sell_net", 10)["score"] == "buy_sell"
    assert tl.plan("top5_breakout_r_rev_alt", 10) == {"score": "alt", "groups": [("top5_breakout_r_rev_alt", ("family", "breakout_r_rev"), 5)]}
    assert tl.plan("top5_breakout_net", 3)["groups"][0][2] == 3   # never more than the page's model limit
    assert tl.plan("top3_tp5_sl20_alt", 10) == {"score": "alt", "groups": [("top3_tp5_sl20_alt", ("tp_sl", 5, 20), 3)]}
    leaders = tl.plan("family_leaders_net", 10)
    assert [g[1] for g in leaders["groups"]] == [("family", f) for f in tl.FAMILY_ORDER] and {g[2] for g in leaders["groups"]} == {1}
    for other in ("top_win", "touched_rank_one_30m", "strongest_three", "weakening_selection", "top3_momentum_net", ""):
        assert tl.plan(other, 10) is None and other not in tl.TIMELINE_SCENARIOS
    assert "top5_breakout_net" in tl.TIMELINE_SCENARIOS


def test_a_family_scenario_ranks_only_that_familys_strategies_and_leaders_merge_the_four_families(cache_dir):
    stats = [{"model": "B1", "strategy": "breakout_2_tp5_sl20"}, {"model": "R1", "strategy": "breakout_R_2_tp5_sl20"}, {"model": "X1", "strategy": "other"}]
    family_of = lambda s: "breakout" if (s or "").startswith("breakout_2") else ("breakout_r" if (s or "").startswith("breakout_R") else "unknown")
    tp_sl_of = lambda s: (5, 20) if s and "tp5_sl20" in s else None
    seen_universes = []

    class Cur(FakeCursor):
        def execute(self, sql, params):
            seen_universes.append(sorted(params[3]))
            super().execute(sql, params)
    table = {"2026-10-20T10:00:00": ["B1", "R1", "X1"], "2026-10-20T10:05:00": ["B1", "R1", "X1"]}
    cur = Cur(table)
    order, iv = tl.scenario_schedule(cur, "2026-10-20", "top5_breakout_net", 10, stats, family_of, tp_sl_of, "all", today_iso="2026-10-21")
    assert order == ["B1"] and seen_universes == [["B1"]] and iv["B1"] == [{"start": "10:00", "end": "10:10"}]
    order, iv = tl.scenario_schedule(cur, "2026-10-20", "family_leaders_net", 10, stats, family_of, tp_sl_of, "all", today_iso="2026-10-21")
    assert order == ["B1", "R1"] and set(iv) == {"B1", "R1"}   # one leader per family that has strategies; the empty families are skipped
    order, _iv = tl.scenario_schedule(cur, "2026-10-20", "top3_tp5_sl20_net", 10, stats, family_of, tp_sl_of, "all", today_iso="2026-10-21")
    assert order == ["B1", "R1"]
