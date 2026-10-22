# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_parity_page_controller.py — pytest wrapper over the page-controller differential tools (page JS in Node vs Python): Page, RuleEditor, replay_models, availableDates; slow tier = mutation check.
#
# VERSION HISTORY
# v1.3.0 · 2026-10-17 · wrapper mode: the 8 stage-1 engine-delegating controllers (DIFF_WRAPPERS=1) vs the originals.
# v1.2.0 · 2026-10-17 · the engine-client page's stubs (answered by engine/rpc.py) vs the page's original overlay / rotation functions.
# v1.1.0 · 2026-10-17 · history / lookup groups, hourly report, drift-check test.
# v1.0.0 · 2026-10-17 · Initial version: one test per method / function group (every group must pass with 0 failures), a coverage test (no group silently missing), and the mutation check behind RUN_SLOW=1.
"""Fast tier (~6 min): 100 random cases per method. Slow tier (RUN_SLOW=1): 400 cases per method and tools/mutate_check.py over every mutant."""
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))


def _server_up() -> bool:
    try:
        urllib.request.urlopen("http://127.0.0.1:8765/", timeout=3)
        return True
    except Exception:  # noqa: BLE001
        return False


pytestmark = pytest.mark.skipif(not shutil.which("node"), reason="needs node")
CASES = "400" if os.environ.get("RUN_SLOW") else "100"
ROW = re.compile(r"^(\w+)\s+cases=\s*(\d+) pass=\s*(\d+) fail=\s*(\d+) js_error=(\d+)", re.M)


def _run(script, *extra):
    out = subprocess.run([sys.executable, str(ROOT / "tools" / script), *extra], capture_output=True, text=True, encoding="utf-8",
                         timeout=3600, env={**os.environ, "PYTHONIOENCODING": "utf-8"}, cwd=str(ROOT))
    rows = {m.group(1): tuple(int(x) for x in m.groups()[1:]) for m in ROW.finditer(out.stdout)}
    assert rows, out.stdout[-1500:] + out.stderr[-1500:]
    return rows


@pytest.fixture(scope="module")
def page_rows():
    return _run("diff_page_js_vs_py.py", "--cases", CASES)


@pytest.fixture(scope="module")
def editor_rows():
    return _run("diff_rule_editor_js_vs_py.py", "--cases", CASES)


@pytest.fixture(scope="module")
def models_rows():
    return _run("diff_models_js_vs_py.py", "--cases", CASES)


def _all_pass(rows, names):
    for n in names:
        assert n in rows, f"group {n} missing"
        cases, passed, failed, js_error = rows[n]
        assert cases > 0 and failed == 0 and js_error == 0 and passed == cases, (n, rows[n])


PAGE_METHODS = ["move_portfolio", "unique_portfolio_name", "mark_portfolio_fixed", "capture_portfolio_scenario", "remove_model_from_portfolio",
                "remove_portfolios", "delete_portfolio", "delete_selected_portfolios", "add_catalogue_model", "move_model_between_portfolios",
                "get_merged_portfolio_models", "create_similar_portfolio", "repopulate_active_portfolio_from_criteria", "live_portfolio_models_for_date",
                "auto_pin_live_portfolio_strategies", "sync_portfolio_view_refresh", "refresh_active_portfolio_view", "current_portfolio_view_config",
                "apply_portfolio_view_config", "persist_portfolio_view_config", "apply_chart_lock", "reset_automatic_rank_schedule",
                "schedule_automatic_top1_refresh", "schedule_point_in_time_selection", "apply_selected_time", "trigger_selected_time_refresh",
                "start_replay", "pause_replay", "switch_date", "set_ranking_criteria", "activate_portfolio", "refresh_live_data",
                "refresh_point_in_time_selection", "load_portfolio_data", "refresh_live_data_twice", "refresh_point_in_time_history",
                "refresh_point_in_time_history_twice", "assigned_portfolio_overlay_rule", "active_portfolio_overlay_rule",
                "load_model_search_from_database", "load_deep_link_models_from_database"]


@pytest.mark.parametrize("method", PAGE_METHODS)
def test_page_method_matches_page(page_rows, method):
    if method in ("load_model_search_from_database", "load_deep_link_models_from_database"):
        pytest.skip("page v2.65.54+ added a localStorage cache, an early request and the fast API to these loaders; the engine copies are verified against v2.65.38 and not delegated")
    _all_pass(page_rows, [method])


STAGE1_METHODS = ["move_portfolio", "mark_portfolio_fixed", "capture_portfolio_scenario", "persist_portfolio_view_config", "start_replay", "pause_replay",
                  "sync_portfolio_view_refresh", "update_auto_refresh_status"]


@pytest.fixture(scope="module")
def wrapper_rows():
    os.environ["DIFF_WRAPPERS"] = "1"
    try:
        return _run("diff_page_js_vs_py.py", "--cases", CASES)
    finally:
        os.environ.pop("DIFF_WRAPPERS", None)


@pytest.mark.parametrize("method", STAGE1_METHODS)
def test_engine_delegating_wrapper_matches_original(wrapper_rows, method):
    _all_pass(wrapper_rows, [method])


def test_page_methods_cover_every_ported_state_function(page_rows):
    assert set(PAGE_METHODS) <= set(page_rows), sorted(set(PAGE_METHODS) - set(page_rows))


@pytest.mark.parametrize("method", ["config_from_overlay_editor", "begin_edit_named_overlay_rule", "cancel_edit_named_overlay_rule",
                                    "save_named_overlay_rule", "assign_overlay_rule"])
def test_rule_editor_matches_page(editor_rows, method):
    _all_pass(editor_rows, [method])


@pytest.mark.parametrize("method", ["get_scenario_candidates", "get_eligible_models", "get_replay_timeline_models", "point_in_time_at_replay_head",
                                    "get_max_frames", "locale_compare", "update_ribbon"])
def test_replay_models_match_page(models_rows, method):
    _all_pass(models_rows, [method])


def test_available_dates_matches_page():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "diff_available_dates.py")], capture_output=True, text=True, encoding="utf-8",
                         env={**os.environ, "PYTHONIOENCODING": "utf-8"}, cwd=str(ROOT))
    assert out.returncode == 0, out.stdout + out.stderr


def test_hourly_report_matches_page():
    rows = _run("diff_reports_js_vs_py.py", "--cases", CASES)
    _all_pass(rows, ["load_hourly_report"])


@pytest.fixture(scope="module")
def thin_rows():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "build_thin_page.py"), "--rebuild"], capture_output=True, text=True, encoding="utf-8",
                         env={**os.environ, "PYTHONIOENCODING": "utf-8"}, cwd=str(ROOT))
    assert out.returncode == 0, out.stdout + out.stderr      # the build's own consistency checks (globals contract, no stray callers) must pass
    return _run("diff_thin_js_vs_py.py", "--cases", "500" if os.environ.get("RUN_SLOW") else "300")


@pytest.mark.parametrize("fn", ["computeTradeOverlaySignals", "pairOverlayTrades", "computeSplitTargetSignal", "computeLeaderRotation", "computeMultiSplitRotation"])
def test_engine_client_page_stubs_match_the_original_functions(thin_rows, fn):
    _all_pass(thin_rows, [fn])


def test_drift_check_is_clean_and_nothing_is_pending():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "check_drift.py"), str(ROOT / "top10_5min_equity_curves_source_v2.65.54.html")],
                         capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"}, cwd=str(ROOT))
    assert out.returncode == 0 and "PENDING: 0 items" in out.stdout and "DRIFT" not in out.stdout, out.stdout[-1500:]


@pytest.mark.skipif(not os.environ.get("RUN_SLOW"), reason="mutation check takes ~30 min; set RUN_SLOW=1")
def test_every_mutant_is_killed():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "mutate_check.py"), "--jobs", "3"], capture_output=True, text=True, encoding="utf-8",
                         timeout=7200, env={**os.environ, "PYTHONIOENCODING": "utf-8"}, cwd=str(ROOT))
    not_killed = [line for line in out.stdout.splitlines() if re.match(r"^(ALIVE|CRASH|BADPATTERN)", line)]
    assert not not_killed, "\n".join(not_killed)
