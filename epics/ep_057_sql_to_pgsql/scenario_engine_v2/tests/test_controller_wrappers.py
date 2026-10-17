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


def test_play_and_pause_keep_the_dom_shell_lines():
    for name in ("startReplay", "pauseReplay"):
        w = cw.wrapper(name, BODY)
        assert "playIcon.className" in w and "playBtnText.textContent" in w and "playBtn.classList.add" in w and "other()" not in w


def test_persist_sends_no_argument_when_called_without_one():
    assert "arguments.length === 0 || arguments[0] === undefined ? [] : [name]" in cw.wrapper("persistPortfolioViewConfig", "")


def test_wrapper_returns_the_engine_value_and_replays_in_order():
    w = cw.wrapper("movePortfolio", "")
    assert "return res.ret;" in w and "__engineReplay(res.effects" in w
