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


def _pit_state(**kw):
    st = PageState()
    st.live_date = st.current_date = "2026-10-14"
    st.pit_mode = True
    for k, v in kw.items():
        setattr(st, k, v)
    return st


def _pit_run(method, st, stage=None, ctx=None, result=None, args=None):
    req = {"method": method, "args": args or [], "state": st.snapshot(), "hooks": {"maxFrames": 5, "head": "10:00", "eligible": [model(1)], "candidates": [model(1)]}}
    if stage:
        req.update({"stage": stage, "ctx": ctx, "result": result})
    return command.run(req)


def test_the_selection_lookup_plans_then_merges_on_the_pages_current_state():
    st = _pit_state()
    r = _pit_run("refresh_point_in_time_selection", st)
    assert r["await"]["fn"] == "fetchPointInTime" and r["await"]["catch"] and r["await"]["args"][0].startswith("/api/point_in_time_scenario?date=2026-10-14&at=10%3A00")
    assert r["state"]["pit_status"][0] == "Loading as of 10:00…" and r["state"]["pit_request_sequence"] == 1 and r["state"]["pit_requested_key"]
    ok = {"ok": {"status": 200, "payload": {"models": [model(1), model(2)], "at_time": "10:00"}}}
    done = _pit_run("refresh_point_in_time_selection", None, r["stage"], r["ctx"], ok) if False else command.run({"method": "refresh_point_in_time_selection", "stage": r["stage"], "ctx": r["ctx"], "result": ok, "state": r["state"],
                                                                                                         "hooks": {"maxFrames": 5, "head": "10:00", "eligible": [model(1)], "candidates": []}})
    assert done["state"]["pit_status"][0] == "10:00 · 1 selected" and "await" not in done
    assert ["dom", "applySelectedTimeBtn", "classList.remove", ["click-feedback-pending"]] in done["effects"]   # a current answer clears the button's busy look
    err = command.run({"method": "refresh_point_in_time_selection", "stage": r["stage"], "ctx": r["ctx"], "result": {"error": "boom"}, "state": r["state"],
                       "hooks": {"maxFrames": 5, "head": "10:00", "eligible": [], "candidates": []}})
    assert err["state"]["pit_status"][0] == "Lookup failed for 10:00: boom" and err["state"]["pit_requested_key"] == ""
    http = command.run({"method": "refresh_point_in_time_selection", "stage": r["stage"], "ctx": r["ctx"], "result": {"ok": {"status": 500, "payload": {"error": "db"}}}, "state": r["state"],
                        "hooks": {"maxFrames": 5, "head": "10:00", "eligible": [], "candidates": []}})
    assert http["state"]["pit_status"][0] == "Lookup failed for 10:00: db"
    stale_state = {**r["state"], "pit_request_sequence": 7}   # another lookup started while this one was out
    stale = command.run({"method": "refresh_point_in_time_selection", "stage": r["stage"], "ctx": r["ctx"], "result": ok, "state": stale_state,
                         "hooks": {"maxFrames": 5, "head": "10:00", "eligible": [model(1)], "candidates": []}})
    assert "selected" not in stale["state"]["pit_status"][0] and ["dom", "applySelectedTimeBtn", "classList.remove", ["click-feedback-pending"]] not in stale["effects"]


def test_the_selection_lookup_does_nothing_when_it_is_not_needed():
    r = _pit_run("refresh_point_in_time_selection", _pit_state(pit_mode=False))
    assert "await" not in r
    st = _pit_state()
    r1 = _pit_run("refresh_point_in_time_selection", st)
    r2 = _pit_run("refresh_point_in_time_selection", PageState.from_snapshot(r1["state"]))   # same request key again
    assert "await" not in r2


def test_the_hourly_cohort_lookup_branches():
    st = _pit_state(pit_history_near_viewport=True, pit_history_panel_hidden=False)
    r = _pit_run("refresh_point_in_time_history", st)
    assert r["await"]["fn"] == "fetchPointInTimeHours" and r["await"]["catch"] and r["state"]["pit_history_status_text"] == "Building hourly cohorts…"
    hours = {"ok": {"status": 200, "payload": {"hours": [{"hour": "09:00"}, {"hour": "10:00"}]}}}
    ok = command.run({"method": "refresh_point_in_time_history", "stage": r["stage"], "ctx": r["ctx"], "result": hours, "state": r["state"]})
    assert ok["state"]["pit_history_status_text"] == "2 hourly cohorts · select an hour to inspect its strategies" and ["renderPointInTimeHistory"] in ok["effects"]
    bad = command.run({"method": "refresh_point_in_time_history", "stage": r["stage"], "ctx": r["ctx"], "result": {"error": "x"}, "state": r["state"]})
    assert bad["state"]["pit_history_status_text"] == "Hourly cohorts unavailable: x" and bad["state"]["pit_history_key"] == ""
    stale = command.run({"method": "refresh_point_in_time_history", "stage": r["stage"], "ctx": r["ctx"], "result": hours, "state": {**r["state"], "pit_history_sequence": 9}})
    assert stale["state"]["pit_history_status_text"] == "Building hourly cohorts…" and ["renderPointInTimeHistory"] not in stale["effects"]
    gone = command.run({"method": "refresh_point_in_time_history", "stage": r["stage"], "ctx": r["ctx"], "result": {"error": "x"}, "state": {**r["state"], "pit_history_sequence": 9}})
    assert gone["state"]["pit_history_status_text"] == "Building hourly cohorts…"   # a newer request owns the status line
    assert "await" not in _pit_run("refresh_point_in_time_history", _pit_state(pit_history_near_viewport=False))   # panel not near the viewport: nothing to build
    assert "await" not in _pit_run("refresh_point_in_time_history", _pit_state(pit_history_panel_hidden=True))
    assert "await" not in _pit_run("refresh_point_in_time_history", _pit_state(pit_mode=False))


def test_an_automatic_top_one_lookup_reports_its_status_and_schedules_the_next_check_through_the_page():
    st = _pit_state(auto_enabled=True, auto_minutes=15, auto_request_at="10:00")
    r = _pit_run("refresh_point_in_time_selection", st)
    assert r["await"]["fn"] == "fetchPointInTime" and "rank_direction=top" in r["await"]["args"][0] and "rank_position=1" in r["await"]["args"][0]
    ok = {"ok": {"status": 200, "payload": {"models": [model(1)], "at_time": "10:00"}}}
    done = command.run({"method": "refresh_point_in_time_selection", "stage": r["stage"], "ctx": r["ctx"], "result": ok, "state": r["state"],
                        "hooks": {"maxFrames": 5, "head": "10:00", "eligible": [model(1)], "candidates": []}})
    assert "checked 10:00" in done["state"]["auto_status_text"] and ["setTimeout", 0] in done["effects"]
    # an automatic add keeps the chart that is already there (the plan's context carries the retained curves across the page's fetch)
    st2 = _pit_state(auto_enabled=True, auto_minutes=15, auto_request_at="10:00", pit_models=[model(5)])
    r2 = _pit_run("refresh_point_in_time_selection", st2)
    done2 = command.run({"method": "refresh_point_in_time_selection", "stage": r2["stage"], "ctx": r2["ctx"], "result": ok, "state": r2["state"],
                         "hooks": {"maxFrames": 5, "head": "10:00", "eligible": [model(1)], "candidates": []}})
    roles = {m["model"]: m["comparisonRole"] for m in done2["state"]["pit_models"]}
    assert roles.get("M1", "").startswith("selected-time #1") and roles.get("M5") == "retained chart"
    timer = [t for t in done["timers"] if t["op"] == "set"][0]
    assert timer["call"] == "scheduleAutomaticTop1Refresh" and timer["timer"] == "anonymousTimer" and timer["ms"] == 0 and len(timer["args"]) == 1


def test_a_hourly_cohort_answer_for_an_older_context_key_is_ignored():
    st = _pit_state(pit_history_near_viewport=True, pit_history_panel_hidden=False)
    r = _pit_run("refresh_point_in_time_history", st)
    hours = {"ok": {"status": 200, "payload": {"hours": [{"hour": "09:00"}]}}}
    changed = command.run({"method": "refresh_point_in_time_history", "stage": r["stage"], "ctx": r["ctx"], "result": hours, "state": {**r["state"], "pit_history_key": "another|context"}})
    assert changed["state"]["pit_history_status_text"] == "Building hourly cohorts…" and ["renderPointInTimeHistory"] not in changed["effects"]


def test_an_unawaited_lookup_is_planned_in_place_and_handed_to_the_page_as_a_spawn():
    st = _pit_state(selected_time_input="10:05")
    r = command.run({"method": "apply_selected_time", "args": [], "state": st.snapshot(), "hooks": {"maxFrames": 5, "head": "10:05", "eligible": [model(1)], "candidates": []}})
    assert "needsNetwork" not in r and len(r["spawns"]) == 1
    sp = r["spawns"][0]
    assert sp["method"] == "refresh_point_in_time_selection" and sp["fn"] == "fetchPointInTime" and sp["stage"] == "_pit_sel_1"
    assert sp["args"][0].startswith("/api/point_in_time_scenario?date=2026-10-14&at=10%3A05") and sp["ctx"]["explicit"] is True
    assert r["state"]["pit_status"][0].startswith("Finding top") and r["state"]["pit_request_sequence"] >= 1   # the part before the request ran, in place
    ok = {"ok": {"status": 200, "payload": {"models": [model(1)], "at_time": "10:05"}}}
    done = command.run({"method": sp["method"], "stage": sp["stage"], "ctx": sp["ctx"], "result": ok, "state": r["state"], "hooks": {"maxFrames": 5, "head": "10:05", "eligible": [model(1)], "candidates": []}})
    assert "selected" in done["state"]["pit_status"][0] or "Added" in done["state"]["pit_status"][0] or "retained" in done["state"]["pit_status"][0]
    assert command.run({"method": "apply_selected_time", "args": [], "state": _pit_state(pit_mode=False, selected_time_input="bad").snapshot()})["spawns"] == []


def test_no_controller_answers_needs_network_for_a_lookup_any_more():
    from engine.command import STAGE1
    st = _pit_state(auto_enabled=True, auto_minutes=5, auto_next_minute=0, auto_last_minute=-1, selected_time_input="10:05")
    for method, args in (("apply_selected_time", []), ("schedule_point_in_time_selection", []), ("trigger_selected_time_refresh", []), ("schedule_automatic_top1_refresh", ["10:00"]),
                         ("reset_automatic_rank_schedule", []), ("apply_chart_lock", [False, False])):
        assert method in STAGE1
        r = command.run({"method": method, "args": args, "state": st.snapshot(), "hooks": {"maxFrames": 5, "head": "10:05", "eligible": [model(1)], "candidates": [model(1)]}})
        assert "needsNetwork" not in r, method


# ---- step 8: loadModelSearchFromDatabase / loadDeepLinkModelsFromDatabase
def _load_run(method, st, args=None, stage=None, ctx=None, result=None, eligible=None):
    req = {"method": method, "args": args or [], "state": st.snapshot(),
           "hooks": {"maxFrames": 5, "head": "10:00", "eligible": eligible if eligible is not None else [model(1), model(2)], "candidates": []}}
    if stage:
        req.update({"stage": stage, "ctx": ctx, "result": result})
    return command.run(req)


def _search_state(term="M1,M2", **kw):
    st = PageState()
    st.live_date = st.current_date = "2026-10-14"
    st.model_search_input = term
    for k, v in kw.items():
        setattr(st, k, v)
    return st


SEARCH = "load_model_search_from_database"
DEEP = "load_deep_link_models_from_database"


def _answer(method, first, result, **change):
    """The page's answer to the fetch the first stage asked for, merged into the state as it is NOW (optionally changed while the fetch was out)."""
    return _load_run(method, PageState.from_snapshot({**first["state"], **change}), stage=first["stage"], ctx=first["ctx"], result=result)


def test_model_id_search_validates_before_it_asks_the_page_to_fetch():
    r = _load_run(SEARCH, _search_state("201700 201701"), ["201700 201701"])
    assert r["await"]["fn"] == "fetchPortfolioDayBatches" and r["await"]["catch"] and r["await"]["args"] == [[["201700", "201701"]], "2026-10-14"]
    assert r["state"]["model_search_status"] == "Searching 2 model IDs in PostgreSQL…" and r["state"]["search_sequence"] == 1
    one = _load_run(SEARCH, _search_state("DNA_201700"), ["DNA_201700"])   # one ID of five or more digits is a direct search
    assert one["await"]["fn"] == "fetchPortfolioDayBatches" and one["state"]["model_search_status"] == "Searching model IDs and strategy names in PostgreSQL…"
    many = " ".join(str(200000 + i) for i in range(11))
    assert [len(b) for b in _load_run(SEARCH, _search_state(many), [many])["await"]["args"][0]] == [10, 1]   # the day endpoint takes at most ten ids
    for bad_term in ("", "x" * 101):
        bad = _load_run(SEARCH, _search_state(bad_term), [bad_term])
        assert "await" not in bad and bad["state"]["model_search_status"] == "Search by one strategy name, or enter model IDs separated by commas or spaces"
    week = _load_run(SEARCH, _search_state("201700 201701", current_date="WEEK_OVERALL"), ["201700 201701"])
    assert "await" not in week and week["state"]["model_search_status"] == "Choose a single date to search PostgreSQL"


def test_strategy_name_search_asks_the_page_for_the_catalogue_first():
    r = _load_run(SEARCH, _search_state("Breakout 4  TP20"), ["Breakout 4  TP20"])
    assert r["await"]["fn"] == "fetchStrategyCatalog" and r["await"]["catch"] and r["await"]["args"] == ["2026-10-14"]
    assert r["ctx"]["query"] == "breakout_4_tp20" and r["state"]["model_search_status"] == "Searching model IDs and strategy names in PostgreSQL…"
    assert _load_run(SEARCH, _search_state("M1,M2"), ["M1,M2"])["await"]["fn"] == "fetchStrategyCatalog"   # anything that is not a model ID is a name


def _catalogue(n=3, name="breakout_4_tp20_sl50"):
    return {"ok": [{"model": f"DNA_2{i:05d}", "strategy": name} for i in range(n)] + [{"model": "DNA_299999"}]}


def _name_search(term="breakout_4", **state):
    first = _load_run(SEARCH, _search_state(term, **state), [term])
    return first, _answer(SEARCH, first, _catalogue())


def test_strategy_name_matches_by_strategy_or_model_and_then_loads_their_curves():
    first, r = _name_search("breakout_4")
    assert r["await"]["fn"] == "fetchPortfolioDayBatches" and r["await"]["args"] == [[["DNA_200000", "DNA_200001", "DNA_200002"]], "2026-10-14"]
    _, byid = _name_search("dna_2000")   # the model ID is searched too
    assert byid["ctx"]["model_ids"] == ["DNA_200000", "DNA_200001", "DNA_200002"]
    done = _answer(SEARCH, {"state": r["state"], "stage": r["stage"], "ctx": r["ctx"]}, {"ok": [[{"model": "DNA_200001", "series": []}, {"model": "DNA_200000", "series": []}]]})
    assert [m["model"] for m in done["state"]["search_loaded"]] == ["DNA_200000", "DNA_200001"] and done["state"]["model_search_status"] == "2 models match “breakout_4”"
    one = _answer(SEARCH, {"state": r["state"], "stage": r["stage"], "ctx": r["ctx"]}, {"ok": [[{"model": "DNA_200000", "series": []}]]})
    assert one["state"]["model_search_status"] == "1 model match “breakout_4”"


def test_strategy_name_search_shows_the_first_hundred_and_says_so():
    first = _load_run(SEARCH, _search_state("breakout"), ["breakout"])
    r = _answer(SEARCH, first, _catalogue(130))
    ids = r["ctx"]["model_ids"]
    assert len(ids) == 100 and ids[0] == "DNA_200000" and r["ctx"]["truncated"] is True and len(r["await"]["args"][0]) == 10   # 100 ids in ten batches
    exactly = _answer(SEARCH, first, _catalogue(100))
    assert len(exactly["ctx"]["model_ids"]) == 100 and exactly["ctx"]["truncated"] is False
    done = _answer(SEARCH, {"state": r["state"], "stage": r["stage"], "ctx": r["ctx"]}, {"ok": [[{"model": i, "series": []} for i in ids[:10]]] + [[] for _ in range(9)]})
    assert done["state"]["model_search_status"] == "10 models match “breakout” · showing first 100 matches"


def test_strategy_name_with_no_match_clears_the_previous_results():
    first = _load_run(SEARCH, _search_state("zzz_nothing", search_loaded=[{"model": "OLD"}]), ["zzz_nothing"])
    r = _answer(SEARCH, first, _catalogue())
    assert "await" not in r and r["state"]["search_loaded"] == [] and r["state"]["model_search_status"] == "No model ID or strategy name matches “zzz_nothing” for 2026-10-14"
    assert [v for v in r["effects"] if v[0] == "view"] == [["view", "renderCards"], ["view", "drawChart"]]
    empty = _answer(SEARCH, first, {"ok": []})
    assert empty["state"]["search_loaded"] == [] and "No model ID or strategy name matches" in empty["state"]["model_search_status"]


def test_strategy_name_catalogue_failure_and_stale_answers():
    first = _load_run(SEARCH, _search_state("breakout_4"), ["breakout_4"])
    assert _answer(SEARCH, first, {"error": "catalog down"})["state"]["model_search_status"] == "Database search failed: catalog down"
    assert _answer(SEARCH, first, {"error": "x"}, search_sequence=9)["state"]["model_search_status"] == "Searching model IDs and strategy names in PostgreSQL…"
    for change in ({"search_sequence": 9}, {"model_search_input": "breakout_5"}, {"current_date": "2026-10-13"}):
        r = _answer(SEARCH, first, _catalogue(), **change)
        assert "await" not in r and r["state"]["search_loaded"] == [] and r["state"]["model_search_status"] == "Searching model IDs and strategy names in PostgreSQL…", change
    assert "await" in _answer(SEARCH, first, _catalogue(), model_search_input="Breakout 4".replace(" ", "_"))   # the box's whitespace counts as '_' when comparing


def test_model_id_search_merges_the_answer_into_the_pages_current_state():
    first = _load_run(SEARCH, _search_state("DNA_201700", scenario_removed={"dna_201700", "Other"}), ["DNA_201700"])
    r = _answer(SEARCH, first, {"ok": [[{"model": "dna_201700", "series": []}]]})
    assert [m["model"] for m in r["state"]["search_loaded"]] == ["dna_201700"]   # matched case-insensitively
    assert r["state"]["model_search_status"] == "1 model loaded" and r["state"]["frame"] == -1 and r["state"]["selected_model_index"] == 0
    assert r["state"]["scenario_removed"] == ["Other"]   # a searched model is no longer "removed"
    assert [v for v in r["effects"] if v[0] == "view"] == [["view", "updateScrubberUI"], ["view", "updateRibbon"], ["view", "renderCards"], ["view", "drawChart"]]
    missing = _answer(SEARCH, first, {"ok": [[]]})
    assert missing["state"]["model_search_status"] == "No model data found for 2026-10-14: DNA_201700" and missing["state"]["search_loaded"] == []
    assert _answer(SEARCH, first, {"ok": [[]]}, frame=3)["state"]["frame"] == 3   # nothing was found: the replay position is left alone
    bare = _load_run(SEARCH, _search_state("201700"), ["201700"])
    assert _answer(SEARCH, bare, {"ok": [[{"model": "DNA_201700", "series": []}]]})["state"]["search_loaded"] == []   # a bare number is looked up as typed (the page's behaviour)


def test_model_search_in_selected_time_mode_schedules_the_lookup():
    first = _load_run(SEARCH, _search_state("DNA_201700", pit_mode=True), ["DNA_201700"])
    r = _answer(SEARCH, first, {"ok": [[{"model": "DNA_201700", "series": []}]]})
    assert ["setTimeout", 180] in r["effects"]
    off = _answer(SEARCH, _load_run(SEARCH, _search_state("DNA_201700", pit_mode=False), ["DNA_201700"]), {"ok": [[{"model": "DNA_201700", "series": []}]]})
    assert ["setTimeout", 180] not in off["effects"]


def test_model_search_drops_a_stale_or_failed_answer():
    ok = {"ok": [[{"model": "DNA_201700", "series": []}]]}
    first = _load_run(SEARCH, _search_state("DNA_201700"), ["DNA_201700"])
    for change in ({"search_sequence": 9}, {"model_search_input": "DNA_201701"}, {"current_date": "2026-10-13"}):
        r = _answer(SEARCH, first, ok, **change)
        assert r["state"]["search_loaded"] == [] and r["state"]["model_search_status"] == "Searching model IDs and strategy names in PostgreSQL…", change
    assert _answer(SEARCH, first, {"error": "boom"})["state"]["model_search_status"] == "Database search failed: boom"
    assert _answer(SEARCH, first, {"error": "boom"}, search_sequence=9)["state"]["model_search_status"] == "Searching model IDs and strategy names in PostgreSQL…"   # a newer search owns the line


def test_deep_link_load_validates_and_limits_before_it_asks_the_page_to_fetch():
    st = _search_state("")
    one = _load_run(DEEP, st, [["M1"]])
    assert one["await"]["fn"] == "fetchPortfolioDayBatches" and one["await"]["args"] == [[["M1"]], "2026-10-14"]
    assert one["state"]["model_search_status"] == "Loading 1 linked comparison strategy…"
    two = _load_run(DEEP, st, [[" M1 ", "M2", "M1", "bad id"]])
    assert two["await"]["args"][0] == [["M1", "M2"]] and two["state"]["model_search_status"] == "Loading 2 linked comparison strategies…"
    assert len(_load_run(DEEP, st, [[f"D{i}" for i in range(12)]])["await"]["args"][0][0]) == 10
    assert "await" not in _load_run(DEEP, st, [[]]) and "await" not in _load_run(DEEP, st, [None])
    week = _load_run(DEEP, _search_state("", current_date="WEEK_OVERALL"), [["M1"]])
    assert "await" not in week and week["state"]["model_search_status"] == "Choose a single date to load linked comparison models"


def test_deep_link_load_pins_the_models_and_words_the_result():
    first = _load_run(DEEP, _search_state(""), [["M1", "M2", "M3"]])
    ok = {"ok": [[{"model": "M1", "series": []}, {"model": "M2", "color": "#123456", "series": []}, {"model": "", "series": []}, {"model": "M4", "series": []}]]}
    r = _answer(DEEP, first, ok)
    pinned = dict(r["state"]["pinned"])
    assert pinned["M1"]["color"] == "#f59e0b" and pinned["M2"]["color"] == "#123456" and pinned["M4"]["color"] == "#fb7185"   # the palette index counts every returned model
    assert all(v["comparisonRole"] == "pinned comparison" for v in pinned.values()) and "" not in pinned
    assert r["state"]["model_search_status"] == "4 linked comparison strategies added · no data found for M3 · change scenario to compare"
    assert [v for v in r["effects"] if v[0] == "view"][0] == ["view", "updateDateLabelAndTitle"] and sorted(r["state"]["visible"]) == ["M1", "M2"]
    only = _answer(DEEP, first, {"ok": [[{"model": "M1", "series": []}]]}, deep_link_only=True)
    assert only["state"]["model_search_status"] == "Showing 1 selected strategy only · no data found for M2, M3 · choose a scenario to add scenario leaders"
    moved = _answer(DEEP, first, ok, current_date="2026-10-13")
    assert moved["state"]["pinned"] == [] and moved["state"]["model_search_status"] == "Loading 3 linked comparison strategies…"
    assert _answer(DEEP, first, {"error": "x"})["state"]["model_search_status"] == "Could not load linked models: x"
