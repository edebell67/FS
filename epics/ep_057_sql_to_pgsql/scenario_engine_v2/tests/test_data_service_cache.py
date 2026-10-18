# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_data_service_cache.py — the data service's short-lived response cache (dashboards_and_uis/top10_live_server.py).
#
# VERSION HISTORY
# v1.0.0 · 2026-10-18 · Initial version: single flight, failure not cached, expiry, copies, live_switch_candidates never cached, live execution keeps calling the builder.
"""No database needed: the builders are replaced by counters."""
import sys
import threading
import time
from pathlib import Path

import pytest

DS = Path(__file__).resolve().parents[2] / "dashboards_and_uis"
sys.path.insert(0, str(DS))
srv = pytest.importorskip("top10_live_server")


@pytest.fixture(autouse=True)
def clean():
    srv._RESPONSE_CACHE.clear()
    srv._RESPONSE_KEY_LOCKS.clear()
    yield
    srv._RESPONSE_CACHE.clear()


def test_identical_concurrent_requests_share_one_build():
    calls, gate = [], threading.Event()

    def build():
        calls.append(1)
        gate.wait(5)
        return {"models": [1, 2, 3]}
    out = []
    ts = [threading.Thread(target=lambda: out.append(srv._cached_single_flight(("k",), 60, build))) for _ in range(6)]
    [t.start() for t in ts]
    time.sleep(0.2)
    gate.set()
    [t.join() for t in ts]
    assert len(calls) == 1 and len(out) == 6 and all(o == {"models": [1, 2, 3]} for o in out)


def test_a_failure_is_not_cached_and_the_key_can_be_built_again():
    n = {"i": 0}

    def build():
        n["i"] += 1
        if n["i"] == 1:
            raise RuntimeError("db down")
        return {"ok": n["i"]}
    with pytest.raises(RuntimeError):
        srv._cached_single_flight(("f",), 60, build)
    assert srv._cached_single_flight(("f",), 60, build) == {"ok": 2}
    assert srv._cached_single_flight(("f",), 60, build) == {"ok": 2}   # now cached


def test_entries_expire_and_callers_get_their_own_copy():
    n = {"i": 0}

    def build():
        n["i"] += 1
        return {"models": [n["i"]]}
    a = srv._cached_single_flight(("e",), 0.2, build)
    a["models"].append("mutated")
    assert srv._cached_single_flight(("e",), 0.2, build) == {"models": [1]}   # the cached value was not touched by the caller
    time.sleep(0.3)
    assert srv._cached_single_flight(("e",), 0.2, build) == {"models": [2]}   # expired: rebuilt


def test_the_cache_is_bounded():
    for i in range(srv.RESPONSE_CACHE_ENTRIES + 10):
        srv._cached_single_flight(("b", i), 60, lambda i=i: {"i": i})
    assert len(srv._RESPONSE_CACHE) <= srv.RESPONSE_CACHE_ENTRIES


def test_live_switch_candidates_is_never_cached_and_live_execution_keeps_the_uncached_builder(monkeypatch):
    calls = []
    monkeypatch.setattr(srv, "build_point_in_time_scenario", lambda *a, **k: calls.append(a) or {"models": []})
    today = srv.dt.date.today().isoformat()
    srv.cached_point_in_time_scenario(today, "10:00", "live_switch_candidates", "NET")
    srv.cached_point_in_time_scenario(today, "10:00", "live_switch_candidates", "NET")
    assert len(calls) == 2   # every call reaches the builder: live portfolio switching must see fresh data
    srv.cached_point_in_time_scenario(today, "10:00", "top_net", "NET")
    srv.cached_point_in_time_scenario(today, "10:00", "top_net", "NET")
    assert len(calls) == 3   # an ordinary scenario is cached
    app_src = (DS / "top10_live_app.py").read_text(encoding="utf-8")
    assert app_src.count('"live_switch_candidates"') >= 2 and "cached_point_in_time_scenario, date_str, at_time, \"live_switch_candidates\"" not in app_src
