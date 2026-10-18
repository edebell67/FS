# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_controller_wrappers.py — checks the generated browser wrappers for what the differential harness cannot see (the stored VALUE, the DOM shell, the argument shapes).
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version.
"""The harness stubs localStorage.setItem(key) and does not model the DOM, so these assertions pin the generated JS text."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import controller_wrappers as cw  # noqa: E402

BODY = "      playIcon.className = 'x';\n      playBtnText.textContent = 'Pause';\n      playBtn.classList.add('a');\n      other();"


def test_storage_keys_write_the_matching_config():
    h = cw.helper_block({js: "let" for _py, js, _k, _d in cw.FIELDS if js not in cw.DERIVED})
    assert "'strategyDirectoryPortfolioViewV1': () => localStorage" not in h  # the effect handler stores, the mapping gives the value
    assert "'strategyDirectoryPortfolioViewV1': () => JSON.stringify(portfolioViewConfigs)" in h
    assert "'strategyDirectoryMainViewV1': () => JSON.stringify(mainScenarioViewConfig)" in h


def test_engine_is_sent_the_criteria_buckets_it_reads():
    h = cw.helper_block({js: "let" for _py, js, _k, _d in cw.FIELDS if js not in cw.DERIVED})
    assert "[key, 'top_net'].forEach" in h


def test_play_and_pause_dom_writes_come_from_the_engine_as_dom_effects():
    """The play button's look is no longer copied into the wrapper: the engine emits it as 'dom' effects and the page replays them."""
    import sys
    sys.path.insert(0, str(ROOT))
    from engine import command
    from engine.page_state import PageState
    st = PageState()
    st.current_date = "2026-10-14"
    r = command.run({"method": "pause_replay", "args": [], "state": st.snapshot(), "hooks": {"maxFrames": 10, "head": "10:00", "eligible": [], "candidates": []}})
    dom = [e for e in r["effects"] if e[0] == "dom"]
    assert ["dom", "playIcon", "set", ["textContent", "▶"]] in dom and ["dom", "playBtnText", "set", ["textContent", "Play"]] in dom
    assert "other()" not in cw.wrapper("pauseReplay", BODY)


def test_persist_sends_no_argument_when_called_without_one():
    assert "arguments.length === 0 || arguments[0] === undefined ? [] : [name]" in cw.wrapper("persistPortfolioViewConfig", "")


def test_wrapper_returns_the_engine_value_and_replays_in_order():
    w = cw.wrapper("movePortfolio", "")
    assert "return res.ret;" in w and "__engineReplay(res.effects" in w


def test_engine_names_the_timers_it_starts_and_clears():
    """The harness stubs setTimeout and cannot see which page timer variable holds the handle, so pin the engine's named timer operations here."""
    sys.path.insert(0, str(ROOT))
    from engine import command
    from engine.page_state import PageState
    st = PageState()
    st.pit_mode, st.current_date = True, "2026-10-14"
    r = command.run({"method": "apply_chart_lock", "args": [True, False], "state": st.snapshot(), "hooks": {"maxFrames": 10, "head": "10:00", "eligible": [], "candidates": []}})
    ops = r["timers"]
    assert ops[-1] == {"op": "set", "timer": "pointInTimeDebounceTimer", "ms": 180, "call": "refreshPointInTimeSelection", "args": ["10:00"], "at": ops[-1]["at"]}
    assert r["effects"][ops[-1]["at"]] == ["setTimeout", 180] and r["effects"][ops[0]["at"]] == ["clearTimeout"]


def test_the_point_in_time_fetch_targets_report_the_real_http_status():
    """The engine decides from the status and payload: a target that always said 200 would hide every HTTP failure of a lookup."""
    h = cw.helper_block({js: "let" for _py, js, _k, _d in cw.FIELDS if js not in cw.DERIVED})
    for name in ("fetchPointInTime", "fetchPointInTimeHours"):
        line = next(l for l in h.split("\n") if l.strip().startswith(name + ":") or (name + ": async") in l)
        assert "status: response.status" in line and "cache: 'no-store'" in line and "await response.json()" in line
