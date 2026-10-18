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


def _chain(method, args, state, results):
    """Drive a staged controller through the command layer the way the page does; `results` maps an awaited function name to the result the page reports."""
    r = command.run({"method": method, "args": args, "state": state})
    seen = []
    while "await" in r:
        aw = r["await"]
        seen.append((aw["fn"], bool(aw.get("fire")), bool(aw.get("sync")), aw.get("handle"), aw.get("attach")))
        r = command.run({"method": method, "stage": r["stage"], "ctx": r["ctx"], "result": results.get(aw["fn"]), "state": r["state"]})
    return seen, r


def test_a_live_portfolio_is_refused_so_the_page_runs_its_own_copy():
    st = PageState()
    st.live_date = st.current_date = "2026-10-14"
    st.portfolios = {"LIVE": ["M1"], "LIVE_ALT": ["M1"]}
    for name in ("LIVE", "live", "LIVE_ALT"):
        assert command.run({"method": "activate_portfolio", "args": [name], "state": st.snapshot()}) == {"needsNetwork": True}


def test_activating_a_portfolio_starts_two_page_requests_and_attaches_a_continuation_to_each():
    st = PageState()
    st.live_date = st.current_date = "2026-10-14"
    st.portfolios = {"P": ["M1"]}
    seen, last = _chain("activate_portfolio", ["P"], st.snapshot(), {})
    assert seen == [("loadOverlayRuleLibrary", True, False, "rules", None), ("applyPortfolioViewConfig", False, True, None, None),
                    ("loadPortfolioData", True, False, "load", None), ("__attach", False, False, None, "_act_load_done"), ("__attach", False, False, None, "_act_rules_done")]
    assert last["state"]["active_portfolio"] == "P"


def test_the_load_continuation_branches():
    st, pg = page(active_portfolio="P", portfolios={"P": ["M1"]}, portfolio_models=[model(1)])
    ctx = {"name": "P", "saved_replay": "", "saved_selection": "", "activation_date": "2026-10-14", "activation_key": "M1"}
    pg._act_load_done(ctx, {"error": "db down"})
    assert st.effects[-1] == ["view", "setLiveBadge"] and st.view_args[len(st.effects) - 1] == ["Portfolio: unavailable", "err"]
    n = len(st.effects)
    pg._act_load_done({**ctx, "activation_date": "2026-10-13"}, {"error": "db down"})   # the date moved on: no badge
    assert len(st.effects) == n
    pg._act_load_done(ctx, {"ok": None})   # the load did not fetch: nothing to paint
    assert len(st.effects) == n
    pg._act_load_done({**ctx, "activation_key": "M9"}, {"ok": True})   # the portfolio's members changed meanwhile
    assert len(st.effects) == n
    pg._act_load_done(ctx, {"ok": True})   # a real final paint
    assert ["view", "renderCards"] in st.effects and st.view_args[max(i for i, e in enumerate(st.effects) if e == ["view", "setLiveBadge"])] == ["Portfolio · P", "ok"]


def test_the_rules_continuation_branches():
    st, pg = page(active_portfolio="P")
    pg._act_rules_done({"name": "P"}, {"error": "x"})
    assert st.effects == []
    pg._act_rules_done({"name": "Other"}, {"ok": None})
    assert st.effects == []
    pg._act_rules_done({"name": "P"}, {"ok": None})
    assert st.effects == [["view", "syncAssignedOverlayRuleUI"], ["view", "drawChart"]]


def test_create_similar_portfolio_closes_the_modal_and_awaits_the_page_activation():
    st = PageState()
    st.live_date = st.current_date = "2026-10-14"
    st.similar_payload = {"groups": {"family": [{"model": "M1"}, {"model": "M2"}]}, "reference": {"product": "gbp", "window": 5, "tp": 3, "sl": 5}}
    r = command.run({"method": "create_similar_portfolio", "args": ["family"], "state": st.snapshot()})
    assert r["await"]["fn"] == "activatePortfolio" and r["await"]["args"] == ["GBP Family W5 T3 S5"] and r["stage"] == "_similar_1"
    assert ["dom", "similarStrategyModal", "call", ["close"]] in r["effects"]
    done = command.run({"method": "create_similar_portfolio", "stage": r["stage"], "ctx": r["ctx"], "result": None, "state": r["state"]})
    assert done["ret"] is None and "await" not in done


def test_remove_portfolios_hands_the_view_config_to_the_page():
    st = PageState()
    st.live_date = st.current_date = "2026-10-14"
    st.portfolios = {"P": ["M1"]}
    st.active_portfolio = "P"
    seen, last = _chain("remove_portfolios", [["P"]], st.snapshot(), {})
    assert [x[0] for x in seen] == ["applyPortfolioViewConfig", "refreshLiveData", "switchDate"]
    assert last["state"]["active_portfolio"] is None and last["state"]["portfolios"] == []


def test_activation_first_stage_state_pit_preference_and_chart_lock_before_live():
    base = {"portfolios": {"P": ["M1"]}, "portfolio_scenario_configs": {"P": {"criteria": "top_net"}}, "portfolio_view_configs": {"P": {"chartLockBeforeLive": True}}}
    st, pg = page(**base, pit_selection_preference=True, auto_context="stale", auto_request_at="10:05", pending_explicit_time="10:00", explicit_refresh=True)
    ctx = pg._act_0("P").ctx
    pg._act_1(ctx, None)
    assert st.pit_mode is True and st.pit_models == [] and st.chart_lock_before_live is True and st.active_portfolio == "P"
    assert (st.auto_context, st.auto_request_at, st.pending_explicit_time, st.explicit_refresh) == ("", None, None, False)   # a new portfolio starts with no auto-add / selected-time request pending
    st, pg = page(**base, pit_selection_preference=False)
    pg._act_1(pg._act_0("P").ctx, None)
    assert st.pit_mode is False and st.pit_models is None
    st, pg = page(portfolios={"P": ["M1"]})   # no saved view: no 'chart lock before live', no dynamic scenario
    pg._act_1(pg._act_0("P").ctx, None)
    assert st.chart_lock_before_live is None and st.pit_mode is False


def test_activation_render_guard_and_saved_selection_time():
    st, pg = page(active_portfolio="P", portfolios={"P": ["M1"]}, portfolio_models=[model(1)])
    ctx = {"name": "P", "saved_replay": "", "saved_selection": "10:15", "activation_date": "2026-10-14", "activation_key": "M1"}
    pg._act_render({**ctx, "activation_date": "2026-10-13"}, True)   # the date moved on: nothing is painted
    assert st.effects == []
    pg._act_render({**ctx, "name": "Other"}, True)                   # another tab is active: nothing is painted
    assert st.effects == []
    pg._act_render(ctx, True)
    assert st.selected_time_input == "10:15" and ["view", "drawChart"] in st.effects
    st2, pg2 = page(active_portfolio="P", portfolios={"P": ["M1"]}, portfolio_models=[model(1)])
    pg2._act_render({**ctx, "saved_selection": "bad"}, True)         # only HH:MM is a saved selection time
    assert st2.selected_time_input != "bad" and st2.selected_time_input != "10:15"


def test_ranking_loading_badge_uses_the_scenario_name_when_the_page_knows_one():
    st = PageState()
    st.live_date = st.current_date = "2026-10-14"
    r = command.run({"method": "set_ranking_criteria", "args": ["top_win"], "state": st.snapshot(), "scenarioNames": {"top_win": "Best win rate"}})
    badge = [v for k, v in r["viewArgs"].items() if v and v[0].startswith("Loading")]
    assert badge == [["Loading Best win rate · keeping current chart visible", "idle"]]
    r = command.run({"method": "set_ranking_criteria", "args": ["top_win"], "state": st.snapshot(), "scenarioNames": {}})
    assert [v for v in r["viewArgs"].values() if v[0].startswith("Loading")] == [["Loading top_win · keeping current chart visible", "idle"]]
