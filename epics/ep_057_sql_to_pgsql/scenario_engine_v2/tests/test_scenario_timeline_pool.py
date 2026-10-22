# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_scenario_timeline_pool.py — win-rate / pool / momentum scenarios decided at every snapshot (dashboards_and_uis/scenario_timeline_pool.py).
#
# VERSION HISTORY
# v1.0.0 · 2026-10-22 · Initial version: the selection rules (pure), rounding, and the pass over a day with a fake cursor (as-of trades, resume, finished-day cache, partial snapshot).
"""No database needed."""
import datetime as dt
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "dashboards_and_uis"))
pool = pytest.importorskip("scenario_timeline_pool")


def row(model, net, win_rate, trades=10, strategy="breakout_2_tp5_sl20", target_profit=50, peak=None):
    return {"model": model, "net": net, "net_raw": net, "alt": net, "trades": trades, "win_rate": win_rate, "strategy": strategy,
            "target_profit": target_profit, "peak": net if peak is None else peak}


NO_MOMENTUM = {"net": {}, "alt": {}}


def test_rounding_is_half_away_from_zero_to_the_requested_digits():
    assert pool.round_half_up(2.345, 2) == 2.35
    assert pool.round_half_up(-2.345, 2) == -2.35
    assert pool.round_half_up(66.65, 1) == 66.7
    assert pool.round_half_up(0.0, 2) == 0.0


def test_top_win_takes_models_at_or_above_50_percent_ordered_by_win_rate_then_net_and_falls_back_to_top_net():
    rows = [row("A", 100, 60), row("B", 200, 60), row("C", 50, 90), row("D", 500, 40)]
    assert pool.pick_members(rows, NO_MOMENTUM, 10, "net")["top_win"] == ["C", "B", "A"]
    assert pool.pick_members([row("D", 500, 40), row("E", 100, 10)], NO_MOMENTUM, 10, "net")["top_win"] == ["D", "E"]   # nobody qualifies: top net


def test_each_scenario_applies_its_own_predicate_to_the_pool_and_falls_back_to_top_net_when_fewer_than_two_qualify():
    rows = [row("A", 100, 100, strategy="breakout_R_2_tp5_sl20", target_profit=40), row("B", 90, 90, strategy="breakout_2_tp3_sl9", target_profit=100),
            row("C", 80, 50, strategy="breakout_2_tp9_sl9", target_profit=30), row("D", 70, 20, target_profit=50)]
    picked = pool.pick_members(rows, NO_MOMENTUM, 10, "net")
    assert picked["relative_value"] == ["A", "B"]                          # win rate >= 85, best first
    assert picked["opposite_cluster"] == ["A", "C", "D"]                   # 3 to 5 pips of take-profit, in pool order
    assert picked["market_move"] == ["A", "B", "C", "D"]                   # only B has 10+ pips: fewer than two, so top net
    assert picked["strengthening_cluster"] == ["A", "B", "C", "D"]         # only A is a breakout_R_ strategy
    assert picked["repair_negative"] == ["A", "B", "C", "D"]               # only A has a 100% win rate with a profit


def test_duplicate_pnl_counts_once_and_strongest_three_shows_three():
    rows = [row("A", 100, 60), row("B", 100, 70), row("C", 90, 60), row("D", 80, 60), row("E", 70, 60)]
    picked = pool.pick_members(rows, NO_MOMENTUM, 10, "net")
    assert picked["strongest_three"] == ["B", "C", "D"]        # A has B's P&L
    assert picked["top_win"] == ["B", "C", "D", "E"]


def test_weakening_selection_needs_a_drawdown_and_orders_by_trades_then_drawdown():
    rows = [row("A", 50, 60, trades=30, peak=80), row("B", 90, 60, trades=30, peak=90), row("C", 40, 60, trades=40, peak=45), row("D", 30, 60, trades=5, peak=70)]
    assert pool.pick_members(rows, NO_MOMENTUM, 10, "net")["weakening_selection"] == ["C", "A", "D"]


def test_momentum_picks_the_three_best_trailing_hour_changes_and_skips_equal_scores():
    rows = [row(m, 10, 50) for m in "ABCDE"]
    history = {"net": {"A": (5.0, 10), "B": (5.0, 20), "C": (4.0, 10), "D": (3.0, 10), "E": (2.0, 10)}, "alt": {}}
    assert pool.pick_members(rows, history, 10, "net")["top3_momentum_net"] == ["B", "C", "D"]   # A has B's score; B has the higher end value


class FakeDay:
    """A cursor over a tiny day: snapshots {stamp: {model: (net, alt)}} and closed-trade events [(model, last_update, win, alt_win)]."""
    def __init__(self, snaps, events):
        self.snaps, self.events, self.calls, self.rows = snaps, events, 0, []

    def execute(self, sql, params):
        self.calls += 1
        norm = lambda value: str(value).replace("T", " ")
        if "snapshot_timestamp = %s" in sql:
            stamp_key = params[0] if isinstance(params[0], dt.datetime) else dt.datetime.fromisoformat(str(params[0]))   # the database accepts ISO text too
            self.rows = [(m, v[0], v[1]) for m, v in self.snaps.get(stamp_key, {}).items()]
        elif "DISTINCT snapshot_timestamp" in sql:
            self.rows = [(s,) for s in sorted(self.snaps) if norm(s) > norm(params[0])]
        else:
            self.rows = [(m, lu, w, a) for m, lu, w, a in self.events if norm(params[2]) < norm(lu) <= norm(params[3])]

    def fetchall(self):
        return self.rows


def stamp(h, m):
    return dt.datetime(2026, 10, 20, h, m, 0)


@pytest.fixture()
def cache_dir(monkeypatch):
    path = Path(tempfile.mkdtemp())
    monkeypatch.setattr(pool, "CACHE_DIR", path)
    pool._MEMORY.clear()
    yield path
    pool._MEMORY.clear()


STATS = [{"model": m, "strategy": "breakout_2_tp5_sl20", "target_profit": 50} for m in ("A", "B", "C")]


def day():
    snaps = {stamp(10, 0): {"A": (10.0, 1.0), "B": (5.0, 1.0), "C": (0.0, 0.0)},
             stamp(10, 5): {"A": (20.0, 2.0), "B": (30.0, 2.0), "C": (0.0, 0.0)},
             stamp(10, 10): {"A": (15.0, 2.0), "B": (40.0, 2.0), "C": (1.0, 0.0)}}
    events = [("A", stamp(9, 55), True, True), ("B", stamp(9, 59), True, True), ("B", stamp(10, 3), False, False), ("C", stamp(10, 7), False, False)]
    return snaps, events


def test_a_day_is_ranked_with_the_trades_known_at_each_snapshot(cache_dir):
    snaps, events = day()
    schedules = pool.day_schedule(FakeDay(snaps, events), "2026-10-20", STATS, 10, "net", "u1", today_iso="2026-10-21")
    top_win = pool._load(("2026-10-20", "u1", 10, "net"))["members"]["top_win"]
    assert top_win[stamp(10, 0).isoformat()] == ["A", "B"]    # C has closed no trade yet: it is not in the statistics
    assert top_win[stamp(10, 5).isoformat()] == ["A", "B"]    # B has won 1 of 2 trades: 50%, still at the 50% line
    assert top_win[stamp(10, 10).isoformat()] == ["A", "B"]   # C's one trade lost: 0%, below the line
    assert set(schedules) >= {"top_win", "relative_value", "weakening_selection", "top3_momentum_net"}
    assert schedules["top_win"]["order"] == ["A", "B"] and schedules["top_win"]["intervals"]["A"] == [{"start": "10:00", "end": "10:15"}]


def test_a_finished_day_is_served_from_the_cache_and_a_running_day_resumes_from_its_counters(cache_dir):
    snaps, events = day()
    cur = FakeDay(snaps, events)
    first = pool.day_schedule(cur, "2026-10-20", STATS, 10, "net", "u1", today_iso="2026-10-21")
    used = cur.calls
    assert pool.day_schedule(cur, "2026-10-20", STATS, 10, "net", "u1", today_iso="2026-10-21") == first and cur.calls == used   # nothing asked of the database
    pool._MEMORY.clear()   # a restart: the file answers
    assert pool.day_schedule(FakeDay(snaps, events), "2026-10-20", STATS, 10, "net", "u1", today_iso="2026-10-21") == first
    # today: two snapshots first, the third arrives later and is added without starting over
    early = {k: v for k, v in snaps.items() if k < stamp(10, 10)}
    running = FakeDay(early, events)
    pool.day_schedule(running, "2026-10-20", STATS, 10, "net", "u2", today_iso="2026-10-20")
    running.snaps = snaps
    resumed = pool.day_schedule(running, "2026-10-20", STATS, 10, "net", "u2", today_iso="2026-10-20")
    fresh = pool.day_schedule(FakeDay(snaps, events), "2026-10-20", STATS, 10, "net", "u3", today_iso="2026-10-20")
    assert resumed == fresh


def test_a_snapshot_that_is_still_being_written_is_left_for_the_next_refresh(cache_dir):
    snaps, events = day()
    snaps[stamp(10, 10)] = {"A": (15.0, 2.0)}   # 1 of 3 models written so far
    pool.day_schedule(FakeDay(snaps, events), "2026-10-20", STATS, 10, "net", "u4", today_iso="2026-10-20")
    assert pool._load(("2026-10-20", "u4", 10, "net"))["stamps"] == [stamp(10, 0).isoformat(), stamp(10, 5).isoformat()]
