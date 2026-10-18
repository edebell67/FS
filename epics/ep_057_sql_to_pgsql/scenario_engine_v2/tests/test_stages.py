# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_stages.py — the engine stages of the staged controllers (engine/page.py STAGES), branch by branch.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-18 · Initial version: the branches the differential harness cannot reach reliably (intermediate flags during an await, the failure branch of a page-awaited load, the live-portfolio hand-off, page flags).
"""The differential harness (tools/diff_page_js_vs_py.py, wrapper mode) compares the final result with the original page's. These tests pin what is only visible in between: what a stage returns
(the Await the page must perform and what it carries back) and the state it leaves while the page awaits."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import command  # noqa: E402
from engine.data_client import DataClient  # noqa: E402
from engine.page import STAGES, Await, Page  # noqa: E402
from engine.page_state import PageState  # noqa: E402


def model(i):
    return {"model": f"M{i}", "product": "gbp", "series": [{"time": "10:00", "net": float(i)}]}


def page(**state):
    st = PageState()
    st.live_date, st.current_date = "2026-10-14", "2026-10-14"
    for k, v in state.items():
        setattr(st, k, v)
    cl = DataClient(None, "", live_date=st.live_date)
    return st, Page(st, cl, max_frames=lambda: 5, head_time=lambda: None, eligible=lambda: [model(1), model(2)], candidates=lambda: [model(1)], flags=state.get("_flags"))


def test_every_stage_method_exists_and_is_resumable_by_name():
    st, pg = page()
    from engine.page import STAGE_METHODS
    for name, methods in STAGES.items():
        for m in methods:
            assert callable(getattr(pg, m)), (name, m)
            assert m in STAGE_METHODS


def test_run_stage_refuses_a_name_that_is_not_a_stage():
    st, pg = page()
    try:
        pg.run_stage("refresh_live_data", "__init__", [], {}, None)
    except ValueError as e:
        assert "not a stage method" in str(e)
    else:
        raise AssertionError("an arbitrary method was run")


def test_switch_date_failed_portfolio_load_empties_the_models():
    st, pg = page(portfolio_models=[model(3)])
    ctx = {"seq": 1, "date": "2026-10-14", "skip": False, "refresh": False, "hist": False}
    pg._switch_3(ctx, {"error": "db down"})
    assert st.portfolio_models == []
    st, pg = page(portfolio_models=[model(3)])
    pg._switch_3(ctx, {"ok": True})
    assert st.portfolio_models == [model(3)]


def test_refresh_active_portfolio_view_marks_itself_in_flight_while_the_page_awaits():
    st, pg = page(active_portfolio="P", portfolios={"P": ["M1"]})
    aw = pg._refresh_view_0()
    assert isinstance(aw, Await) and aw.fn == "loadPortfolioData" and aw.catch
    assert st.live_refresh_in_flight is True
    assert pg._refresh_view_0() is None   # an overlapping call returns at once


def test_refresh_active_portfolio_view_clears_the_flag_on_failure_and_on_a_stale_answer():
    st, pg = page(active_portfolio="P", portfolios={"P": ["M1"]})
    aw = pg._refresh_view_0()
    pg._refresh_view_1(aw.ctx, {"error": "x"})
    assert st.live_refresh_in_flight is False
    aw = pg._refresh_view_0()
    st.active_portfolio = "Other"   # the user switched tabs while it loaded
    pg._refresh_view_1(aw.ctx, {"ok": True})
    assert st.live_refresh_in_flight is False and st.effects.count(["view", "renderCards"]) == 0


def test_refresh_live_data_hands_a_live_portfolio_to_the_page_and_resumes_after_it():
    st, pg = page(active_portfolio="LIVE", portfolios={"LIVE": ["M1"]})
    ctx = {"seq": 1, "req": [], "target_date": "2026-10-14", "skip": False, "scenario": "top_net", "on_target": True, "was_at_end": True, "prev": []}
    aw = pg._refresh_live_after_data(ctx, None)
    assert aw.fn == "syncLivePortfolioScreenState" and aw.args == ["2026-10-14"] and aw.next == "_refresh_live_after_sync" and not aw.catch
    # the sync already loaded a new model: no second load
    st.portfolio_models = [model(1)]
    assert pg._refresh_live_after_sync(ctx, True) is None and ["view", "renderCards"] in st.effects
    # nothing new: the engine asks the page to load
    aw = pg._refresh_live_after_sync(ctx, False)
    assert aw.fn == "loadPortfolioData" and aw.catch and aw.next == "_refresh_live_after_load"


def test_refresh_live_data_armed_live_mode_follows_the_newest_frame():
    st, pg = page(active_portfolio="P", portfolios={"P": ["M1"]}, frame=0, portfolio_models=[model(1)])
    pg.flags = {"liveArmed": True}
    st.live_date = "2026-10-14"
    pg._refresh_live_after_load({"target_date": "2026-10-14"}, {"ok": True})
    assert st.frame == 4   # max frames 5 -> the last frame
    st.frame = 0
    pg.flags = {}
    pg._refresh_live_after_load({"target_date": "2026-10-14"}, {"ok": True})
    assert st.frame == 0
    st.frame = 0
    pg.flags = {"liveArmed": True}
    pg._refresh_live_after_load({"target_date": "2026-10-13"}, {"ok": True})   # armed, but not the live date
    assert st.frame == 0


def test_a_failed_live_day_fetch_shows_the_offline_badge_with_its_arguments_only_if_still_the_newest():
    st, pg = page()
    aw = pg._refresh_live_0()
    assert aw.fn == "fetchLiveDay" and aw.catch and aw.args[0].startswith("/api/live_day?date=2026-10-14")
    pg._refresh_live_1(aw.ctx, {"error": "down"})
    assert st.effects[-1] == ["view", "setLiveBadge"] and st.view_args[len(st.effects) - 1] == ["Live: offline", "err"]
    st2, pg2 = page()
    aw = pg2._refresh_live_0()
    st2.live_refresh_sequence += 1   # a newer request started
    pg2._refresh_live_1(aw.ctx, {"error": "down"})
    assert ["view", "setLiveBadge"] not in st2.effects


def test_the_command_layer_carries_an_await_its_stage_and_the_view_arguments():
    st = PageState()
    st.live_date, st.current_date = "2026-10-14", "2026-10-14"
    r = command.run({"method": "refresh_live_data", "args": [None, False], "state": st.snapshot()})
    assert r["await"]["fn"] == "fetchLiveDay" and r["await"]["catch"] is True and r["stage"] == "_refresh_live_1"
    r2 = command.run({"method": "refresh_live_data", "stage": r["stage"], "ctx": r["ctx"], "result": {"error": "down"}, "state": r["state"]})
    assert r2["viewArgs"] and list(r2["viewArgs"].values())[0] == ["Live: offline", "err"] and "await" not in r2
