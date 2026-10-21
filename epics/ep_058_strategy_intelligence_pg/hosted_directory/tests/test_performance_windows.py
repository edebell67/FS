# epics/ep_058_strategy_intelligence_pg/hosted_directory/tests/test_performance_windows.py — per-strategy performance windows (app/performance_windows.py).
#
# VERSION HISTORY
# v1.0.0 · 2026-10-19 · Initial version: trading-day windows, day stats, days-target-hit for net / alt net / either, missing days, partial today, stable snapshot id.
import datetime as dt
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import performance_windows as pw  # noqa: E402

MON, TUE, WED, THU, FRI = (dt.date(2026, 10, d) for d in (12, 13, 14, 15, 16))
SAT, TODAY = dt.date(2026, 10, 17), dt.date(2026, 10, 19)


def day(trades, wins, close_net, close_alt, points):
    """A build_portfolio_day-shaped payload; points = [(time, net, alt_net), ...]."""
    return {"models": [{"model": "DNA_1", "product": "gbpeur_c", "strategy": "breakout_2_tp20_sl50", "trades": trades, "wins": wins, "cum_net": close_net, "cum_alt_net": close_alt,
                        "series": [{"time": t, "net": n, "alt_net": a} for t, n, a in points]}]}


def test_trading_days_skip_weekends():
    assert pw.trading_days(TODAY, 3) == [TODAY, FRI, THU]
    assert pw.trading_days(SAT, 1) == [FRI]   # a Saturday asks for the last weekday


def test_windows_are_named_and_bounded():
    assert pw.window_days("today", TODAY) == [TODAY]
    assert pw.window_days("yesterday", TODAY) == [FRI]
    assert pw.window_days("last_5_days", TODAY) == [dt.date(2026, 10, 13), WED, THU, FRI, TODAY]
    assert len(pw.window_days("last_30_days", TODAY)) == 30
    for bad in ("last_31_days", "last_0_days", "week", "last_x_days"):
        with pytest.raises(pw.WindowError):
            pw.window_days(bad, TODAY)


def test_day_stats_report_peaks_and_the_time_the_target_was_first_hit():
    s = pw.day_stats(FRI, day(7, 5, 225.0, -695.0, [("09:00", 100, 0), ("10:30", 520, -50), ("12:00", 225, 600)]), 500)
    assert s["peak_net"] == 520 and s["peak_alt_net"] == 600 and s["target_hit_net"] and s["target_hit_alt_net"]
    assert s["first_hit_net"] == "10:30" and s["first_hit_alt_net"] == "12:00" and s["close_net"] == 225.0 and s["last_snapshot"] == "12:00"
    below = pw.day_stats(FRI, day(2, 1, 10, 10, [("09:00", 499.99, 499)]), 500)
    assert not below["target_hit_net"] and not below["target_hit_alt_net"] and below["first_hit_net"] is None
    exact = pw.day_stats(FRI, day(1, 1, 500, 0, [("09:00", 500, 0)]), 500)
    assert exact["target_hit_net"] and exact["first_hit_net"] == "09:00"   # the target itself counts
    assert pw.day_stats(FRI, {"models": []}, 500) == {"date": "2026-10-16", "has_data": False}
    assert pw.day_stats(FRI, None, 500)["has_data"] is False


def fake_fetch(table):
    calls = []

    def fetch(model, date_iso):
        calls.append(date_iso)
        return table.get(date_iso, {"models": []})
    fetch.calls = calls
    return fetch


def test_windows_count_days_target_hit_for_net_alt_and_either_separately():
    table = {
        "2026-10-19": day(5, 5, 1140, -1520, [("12:00", 1140, -1520)]),            # net hit
        "2026-10-16": day(7, 5, 225, -695, [("10:00", 520, -100), ("23:58", 225, -695)]),   # net hit
        "2026-10-15": day(5, 2, -325, 660, [("10:00", -100, 660)]),                # alt hit
        "2026-10-14": day(22, 6, 500, -2355, [("10:00", 1435, -790)]),             # net hit
        "2026-10-13": day(9, 0, -1680, 345, [("10:00", -515, 920)]),               # alt hit
    }
    f = fake_fetch(table)
    out = pw.build_windows("DNA_1", TODAY, f, ("today", "yesterday", "last_5_days"), 500)
    w5 = out["windows"]["last_5_days"]
    assert w5["days_target_hit"] == {"net": 3, "alt_net": 2, "either": 5} and w5["days_with_data"] == 5 and w5["trades"] == 48
    assert w5["close_net"] == -140.0 and w5["close_alt_net"] == -3565.0 and w5["win_rate_net"] == round(18 / 48, 4)
    assert out["windows"]["today"]["days_target_hit"] == {"net": 1, "alt_net": 0, "either": 1}
    assert out["windows"]["yesterday"]["from"] == "2026-10-16" and out["windows"]["yesterday"]["days_target_hit"]["net"] == 1
    assert sorted(f.calls) == sorted(set(f.calls)) and len(f.calls) == 5   # each day fetched once across all windows
    assert out["product"] == "gbpeur_c" and out["strategy"] == "breakout_2_tp20_sl50" and out["target"] == 500
    assert out["as_of"] == "2026-10-19T12:00" and any("Today is partial" in c for c in out["caveats"])


def test_days_without_data_are_excluded_from_the_sample_and_called_out():
    f = fake_fetch({"2026-10-19": day(1, 1, 600, 0, [("09:00", 600, 0)])})
    out = pw.build_windows("DNA_1", TODAY, f, ("last_5_days",), 500)
    w = out["windows"]["last_5_days"]
    assert w["trading_days"] == 5 and w["days_with_data"] == 1 and w["confidence"] == "low" and w["days_target_hit"]["either"] == 1
    assert any("No snapshot data for" in c for c in out["caveats"])


def test_confidence_follows_the_number_of_days_with_data():
    assert [pw._confidence(n) for n in (0, 2, 3, 7, 8, 30)] == ["low", "low", "medium", "medium", "high", "high"]


def test_snapshot_id_is_stable_for_the_same_answer_and_changes_with_it():
    table = {"2026-10-19": day(1, 1, 600, 0, [("09:00", 600, 0)])}
    a = pw.build_windows("DNA_1", TODAY, fake_fetch(table), ("today",), 500)
    b = pw.build_windows("DNA_1", TODAY, fake_fetch(table), ("today",), 500)
    c = pw.build_windows("DNA_1", TODAY, fake_fetch({"2026-10-19": day(1, 1, 601, 0, [("09:00", 601, 0)])}), ("today",), 500)
    assert a["snapshot_id"] == b["snapshot_id"] and a["snapshot_id"] != c["snapshot_id"] and a["snapshot_id"].startswith("perf-")
