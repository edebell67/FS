# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_twophase.py — begin / finish (engine/twophase.py) gives the same result as running the controller in one go.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-18 · Initial version: refresh_live_data.
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import data_client as dc, twophase  # noqa: E402
from engine.page import Page  # noqa: E402
from engine.page_state import PageState  # noqa: E402

PAYLOAD = {"products": ["eurusd", "gbpusd"], "top_net": [{"model": "DNA_1", "series": [{"time": "10:00", "pnl": 1.0}, {"time": "10:05", "pnl": 2.0}], "rank": 1}], "tp_sl_scenarios": []}


def _state(**kw):
    st = PageState()
    st.live_date, st.current_date, st.product = "2026-10-14", "2026-10-14", "eurusd"
    for k, v in kw.items():
        setattr(st, k, v)
    return st


def _direct(st, transport, args):
    cl = dc.DataClient(transport, "", live_date=st.live_date)
    page = Page(st, cl)
    page.refresh_live_data(*args)
    return st.snapshot(), st.effects


def _twophase(st, responses, args):
    snap = st.snapshot()
    b = twophase.run({"method": "refresh_live_data", "phase": "begin", "args": args, "state": snap})
    got = {}
    for _ in range(5):
        for u in b["requests"]:
            got[u] = responses(u)
        f = twophase.run({"method": "refresh_live_data", "phase": "finish", "ctx": b["ctx"], "responses": got, "state": b["state"]})
        if f.get("done"):
            return f, b
        b = {**b, "requests": f["need"]}
    raise AssertionError("never finished")


def test_begin_names_the_live_day_request_and_bumps_the_sequence():
    b = twophase.run({"method": "refresh_live_data", "phase": "begin", "args": [], "state": _state().snapshot()})
    assert len(b["requests"]) == 1 and "/api/live_day?date=2026-10-14" in b["requests"][0]
    assert b["state"]["live_refresh_sequence"] == 1 and b["ctx"]["seq"] == 1


def test_finish_matches_the_one_go_run():
    url_of = lambda st: dc.DataClient(None, "", live_date=st.live_date).live_day_url("2026-10-14", st.product_type, st.product, st.strategy_family, st.model_limit, st.current_criteria, st.return_type)  # noqa: E731
    st = _state()
    url = url_of(st)
    d_state, d_effects = _direct(copy.deepcopy(st), lambda u: (200, PAYLOAD) if u == url else (404, {}), [])
    f, _ = _twophase(_state(), lambda u: [200, PAYLOAD], [])
    assert f["state"] == d_state and f["effects"] == d_effects


def test_offline_answer_gives_the_offline_badge_like_the_one_go_run():
    def boom(u):
        raise ConnectionError("down")
    st = _state()
    d_state, d_effects = _direct(copy.deepcopy(st), boom, [])
    f, _ = _twophase(_state(), lambda u: {"error": "down"}, [])
    assert f["state"] == d_state and f["effects"] == d_effects


def test_a_newer_request_makes_the_answer_stale():
    b = twophase.run({"method": "refresh_live_data", "phase": "begin", "args": [], "state": _state().snapshot()})
    newer = copy.deepcopy(b["state"])
    newer["live_refresh_sequence"] += 1   # the page started another refresh while this one was in flight
    f = twophase.run({"method": "refresh_live_data", "phase": "finish", "ctx": b["ctx"], "responses": {b["requests"][0]: [200, PAYLOAD]}, "state": newer})
    assert f["done"] and f["ret"] is None and f["state"]["live_refresh_sequence"] == newer["live_refresh_sequence"]
