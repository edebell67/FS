# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_parity_js_vs_py.py — pytest wrapper over tools/diff_js_vs_py.py (page JS in Node vs Python engine, real API data).
#
# VERSION HISTORY
# v1.7.0 · 2026-10-17 · engine_overlay needs >= 472 cases (Engine.eligible now de-duplicates like the page's getScenarioCandidates).
# v1.6.0 · 2026-10-17 · data_pitsel group.
# v1.5.0 · 2026-10-17 · data_* groups.
# v1.4.0 · 2026-10-17 · Adds utils_auto and utils_search groups.
# v1.3.0 · 2026-10-16 · Fast tier (--skip-rules) vs slow tier (RUN_SLOW=1) with the assigned overlay-rule groups; targets the v2.65.31 snapshot.
# v1.2.0 · 2026-10-16 · Runs against the v2.65.27 snapshot + its inventory; adds Engine-class rotation/overlay groups and a drift test on the live page.
# v1.1.0 · 2026-10-16 · Rotation groups are now hard assertions (the strict xfail markers were removed once they passed); adds the extended-grid groups.
# v1.0.0 · 2026-10-16 · Initial version: metric keys + overlay are hard assertions; leader / multi-split rotation are strict xfail until ported (they flip to a failure once they pass, forcing the marker's removal).
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8765"


def _server_up():
    try:
        urllib.request.urlopen(BASE + "/api/scenario_workspace", timeout=5)
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not (shutil.which("node") and _server_up()), reason="needs node and the :8765 server")


SNAPSHOT = ROOT / "top10_5min_equity_curves_source_v2.65.32.html"
INVENTORY = ROOT / "inventory_v2.65.32" / "inventory.json"


def _run(extra):
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "diff_js_vs_py.py"), str(SNAPSHOT), "--inventory", str(INVENTORY), *extra],
                         capture_output=True, text=True, encoding="utf-8", timeout=6000,
                         env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    rows = {}
    for m in re.finditer(r"^(\w+)\s+cases=\s*(\d+) pass=\s*(\d+) fail=\s*(\d+) js_error=(\d+)", out.stdout, re.M):
        rows[m.group(1)] = tuple(int(x) for x in m.groups()[1:])
    assert rows, out.stdout + out.stderr
    return rows


@pytest.fixture(scope="module")
def results():
    """Fast tier (~4 min): everything except the assigned-rule groups."""
    return _run(["--skip-rules"])


@pytest.fixture(scope="module")
def rule_results():
    """Slow tier (~35 min): the assigned-rule groups on real and synthetic data. Run with RUN_SLOW=1."""
    if not os.environ.get("RUN_SLOW"):
        pytest.skip("slow tier: set RUN_SLOW=1")
    return _run([])


def test_metric_keys_match(results):
    cases, ok, fail, err = results["metric_keys"]
    assert ok == cases


def test_overlay_signals_trades_target_match(results):
    cases, ok, fail, err = results["overlay"]
    assert cases >= 300 and ok == cases


def test_leader_rotation_matches(results):
    cases, ok, fail, err = results["leader_rotation"]
    assert cases >= 72 and ok == cases


def test_multi_split_rotation_matches(results):
    cases, ok, fail, err = results["multi_split_rotation"]
    assert cases >= 72 and ok == cases


def test_leader_rotation_extended_grid_matches(results):
    """rank hold 1-3, NET/ALT, selected-time late-joining models."""
    cases, ok, fail, err = results["leader_rotation_ext"]
    assert cases >= 288 and ok == cases


def test_multi_split_rotation_extended_grid_matches(results):
    cases, ok, fail, err = results["multi_split_rotation_ext"]
    assert cases >= 288 and ok == cases


def test_engine_class_rotation_matches_page(results):
    """Engine.rotation (eligible list, replay series, baseline, head all derived by the Engine) vs the page JS."""
    cases, ok, fail, err = results["engine_rotation"]
    assert cases >= 192 and ok == cases


def test_engine_class_overlay_matches_page(results):
    cases, ok, fail, err = results["engine_overlay"]
    # 472 = 59 eligible models x 8 configs: the page de-duplicates equal rounded returns (2026-10-13 ALT: 10 -> 9), the old port did not (480)
    assert cases >= 472 and ok == cases


def test_no_drift_between_live_page_and_verified_ports():
    """A DRIFT line means the live page changed a function whose port was verified (or added/removed functions):
    re-run the differential test, then tools/rebase_map.py. Pending ports are reported by the tool but are not drift."""
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "check_drift.py")], capture_output=True, text=True,
                         encoding="utf-8", timeout=120)
    drift = [l for l in out.stdout.splitlines() if l.startswith("DRIFT")]
    assert not drift, "; ".join(drift)


# ---- slow tier: assigned overlay-rule path (page v2.65.31 has the eligibility filter fixed; the oracle needs no patch) ----
def _all_pass(rows, group, minimum):
    cases, ok, fail, err = rows[group]
    assert cases >= minimum and ok == cases, f"{group}: {ok}/{cases} pass"


def test_rule_leader_matches(rule_results):
    _all_pass(rule_results, "rule_leader", 168)


def test_rule_multi_split_matches(rule_results):
    _all_pass(rule_results, "rule_multi_split", 168)


def test_rule_loading_matches(rule_results):
    _all_pass(rule_results, "rule_loading", 6)


def test_rule_synthetic_leader_matches(rule_results):
    """negatively / positively correlated copies, mixed strategy families, dense source trades incl. open trades."""
    _all_pass(rule_results, "rule_syn_leader", 108)


def test_rule_synthetic_multi_split_matches(rule_results):
    _all_pass(rule_results, "rule_syn_multi_split", 108)


def test_rule_partial_cache_matches(rule_results):
    _all_pass(rule_results, "rule_partial_cache", 6)


def test_engine_class_with_rule_matches_page(rule_results):
    _all_pass(rule_results, "engine_rule", 12)


# ---- fast tier: small page helpers (clock, search terms, request options, selected-time leaders, step / seek, return-type rules) ----
def test_helper_clock_matches_page(results):
    _all_pass(results, "utils_clock", 300)


def test_helper_text_matches_page(results):
    _all_pass(results, "utils_text", 60)


def test_helper_state_matches_page(results):
    _all_pass(results, "utils_state", 3000)


def test_helper_frames_match_page(results):
    _all_pass(results, "utils_frames", 100)


def test_helper_auto_top1_refresh_matches_page(results):
    _all_pass(results, "utils_auto", 3000)


def test_helper_exact_search_matches_page(results):
    _all_pass(results, "utils_search", 100)


# ---- fast tier: the data layer (DataClient) against the page's own fetchers on a recording fetch stub ----
def test_data_live_matches_page(results):
    _all_pass(results, "data_live", 240)


def test_data_portfolio_matches_page(results):
    _all_pass(results, "data_portfolio", 340)


def test_data_search_and_deep_link_match_page(results):
    _all_pass(results, "data_search", 80)


def test_data_catalogue_and_rules_match_page(results):
    _all_pass(results, "data_catalog", 31)


def test_data_trades_and_historical_match_page(results):
    _all_pass(results, "data_trades", 97)


def test_selected_time_cohort_matches_page(results):
    """The page's refreshPointInTimeSelection (request, merge of leaders / history / pinned / searched models, colours, roles,
    status texts, failure handling, early exits) vs selected_time.refresh_point_in_time_selection."""
    _all_pass(results, "data_pitsel", 1400)
