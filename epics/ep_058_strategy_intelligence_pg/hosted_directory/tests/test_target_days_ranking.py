# epics/ep_058_strategy_intelligence_pg/hosted_directory/tests/test_target_days_ranking.py — which strategies hit the daily target on the most days of the last x trading days (app/target_days_ranking.py).
#
# VERSION HISTORY
# v1.0.0 · 2026-10-20 · Initial version: ranking by net / alt_net / either, configurable target and lookback, tie-breaks, validation, the cached day fetch.
import datetime as dt
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import target_days_ranking as tdr  # noqa: E402

FRI = dt.date(2026, 10, 16)


def table(per_day):
    """fetch_day over {date_iso: {strategy: (net_peak, alt_peak)}}; calls are recorded."""
    calls = []

    def fetch(date_iso, product_type):
        calls.append((date_iso, product_type))
        return {name: {"net": n, "alt": a, "models": 28} for name, (n, a) in per_day.get(date_iso, {}).items()}
    fetch.calls = calls
    return fetch


DAYS5 = {  # five trading days ending Fri 16 Oct
    "2026-10-12": {"A": (600, 0), "B": (0, 600), "C": (499.99, 499.99)},
    "2026-10-13": {"A": (600, 0), "B": (0, 600), "C": (500, 100)},
    "2026-10-14": {"A": (600, 0), "B": (0, 600), "C": (0, 0)},
    "2026-10-15": {"A": (100, 0), "B": (0, 600), "C": (0, 0)},
    "2026-10-16": {"A": (100, 600), "B": (100, 0), "C": (0, 0)},
}


def rank(fetch=None, **kw):
    return tdr.rank_by_target_days(FRI, fetch or table(DAYS5), **{"days": 5, **kw})


def counts(out):
    return {r["strategy"]: (r["days_target_hit"]["either"], r["days_target_hit"]["net"], r["days_target_hit"]["alt_net"]) for r in out["ranking"]}


def test_the_return_type_picks_what_is_counted_and_ordered():
    net = rank(return_type="net")
    assert [r["strategy"] for r in net["ranking"]] == ["A", "C", "B"] and counts(net)["A"] == (4, 3, 1) and counts(net)["B"] == (4, 0, 4)   # by net: A 3 days, C 1, B none
    alt = rank(return_type="alt_net")
    assert [r["strategy"] for r in alt["ranking"]][0] == "B" and alt["return_type"] == "alt_net"
    either = rank(return_type="either")
    assert counts(either)["A"] == (4, 3, 1) and either["ranking"][0]["days_target_hit"]["either"] == 4
    assert "net or alt net" in either["question"] and "most days with net peak" in net["question"]


def test_the_target_is_configurable_and_a_day_at_exactly_the_target_counts():
    assert counts(rank(target=500))["C"] == (1, 1, 0)   # 500 counts, 499.99 does not
    assert counts(rank(target=100))["A"][1] == 5 and rank(target=100)["target"] == 100
    assert counts(rank(target=700))["A"] == (0, 0, 0)


def test_the_lookback_is_configurable_and_counts_trading_days_only():
    fetch = table(DAYS5)
    out = rank(fetch, days=3)
    assert out["window"] == {"from": "2026-10-14", "to": "2026-10-16", "trading_days": 3} and sorted(d for d, _ in fetch.calls) == ["2026-10-14", "2026-10-15", "2026-10-16"]
    wide = rank(table(DAYS5), days=10)   # days with no data are not counted against a strategy
    assert wide["window"]["trading_days"] == 10 and counts(wide)["A"] == (4, 3, 1) and {r["strategy"]: r["days_with_data"] for r in wide["ranking"]}["A"] == 5
    weekend = tdr.rank_by_target_days(dt.date(2026, 10, 17), table(DAYS5), days=2)
    assert weekend["window"]["to"] == "2026-10-16"   # a Saturday ends the window on Friday


def test_ties_are_broken_by_the_other_counts_then_the_name():
    data = {"2026-10-16": {"Z": (600, 600), "M": (600, 0), "B": (600, 0)}}
    out = tdr.rank_by_target_days(FRI, table(data), days=1, return_type="net")
    assert [r["strategy"] for r in out["ranking"]] == ["Z", "B", "M"]   # all hit net; Z also hit alt; B before M by name


def test_limit_and_per_day_peaks_are_returned():
    out = rank(limit=2)
    assert len(out["ranking"]) == 2 and out["strategies_considered"] == 3 and out["ranking"][0]["rank"] == 1
    first = out["ranking"][0]
    assert len(first["days"]) == 5 and {"date", "peak_net", "peak_alt_net", "hit_net", "hit_alt_net"} <= set(first["days"][0]) and first["models"] == 28


def test_the_snapshot_id_is_stable_and_changes_with_the_answer():
    a, b = rank(), rank()
    assert a["snapshot_id"] == b["snapshot_id"] and a["snapshot_id"].startswith("rank-")
    assert rank(target=100)["snapshot_id"] != a["snapshot_id"] and rank(return_type="alt_net")["snapshot_id"] != a["snapshot_id"]


@pytest.mark.parametrize("kw", [{"return_type": "side"}, {"product_type": "bonds"}, {"days": 0}, {"days": 31}, {"limit": 0}, {"limit": 101}, {"target": 0}, {"target": -5}])
def test_bad_parameters_are_refused(kw):
    with pytest.raises(tdr.RankingError):
        rank(**kw)


def test_the_day_fetch_caches_past_days_and_refreshes_today(monkeypatch):
    runs = []

    def run_sql(sql, params):
        runs.append(params)
        return [("breakout_2_tp10_sl50", 650.0, -10.0, 28), (None, 1, 1, 1)]   # a row without a strategy name is ignored
    clock = {"t": 1000.0}
    monkeypatch.setattr(tdr.time, "time", lambda: clock["t"])
    fetch = tdr.make_day_fetch(run_sql, today_fn=lambda: dt.date(2026, 10, 20), today_ttl_s=120)
    assert fetch("2026-10-16", "forex") == {"breakout_2_tp10_sl50": {"net": 650.0, "alt": -10.0, "models": 28}}
    fetch("2026-10-16", "forex"); fetch("2026-10-16", "forex")
    assert len(runs) == 1   # a past day is fetched once
    fetch("2026-10-20", "forex"); fetch("2026-10-20", "forex")
    assert len(runs) == 2   # today is cached for the ttl
    clock["t"] += 121
    fetch("2026-10-20", "forex")
    assert len(runs) == 3
    fetch("2026-10-16", "all")
    assert len(runs) == 4 and runs[-1] == ("2026-10-16", "all", "all")   # the product type is part of the key and of the query


def test_past_day_peaks_survive_a_restart_and_today_is_never_persisted():
    import datetime as dt
    import tempfile
    from pathlib import Path
    tmp_path = Path(tempfile.mkdtemp())
    from app import target_days_ranking as tdr
    calls = []
    def run_sql(sql, params):
        calls.append(params[0])
        return [("s1", 600.0, 100.0, 3)]
    path = str(tmp_path / "cache.json")
    today = lambda: dt.date(2026, 10, 21)
    first = tdr.make_day_fetch(run_sql, today_fn=today, persist_path=path)
    first("2026-10-20", "forex"); first("2026-10-21", "forex")
    second = tdr.make_day_fetch(run_sql, today_fn=today, persist_path=path)   # a new process reads the file
    assert second("2026-10-20", "forex") == {"s1": {"net": 600.0, "alt": 100.0, "models": 3}}
    assert calls == ["2026-10-20", "2026-10-21"]   # the past day was not queried again
    second("2026-10-21", "forex")
    assert calls[-1] == "2026-10-21"   # today is recomputed after a restart
    (tmp_path / "cache.json").write_text("not json")
    assert tdr.make_day_fetch(run_sql, today_fn=today, persist_path=path)("2026-10-20", "forex")["s1"]["net"] == 600.0   # an unreadable file is a cold cache
