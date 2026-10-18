# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_thin_boundary.py — item 15: what logic is left in the generated thin page is exactly the documented boundary.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-18 · Initial version.
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_thin_boundary as cb  # noqa: E402


def test_the_built_page_is_current():
    """The committed thin page is what the generator produces from the source page and the engine's wrappers today (nothing hand-edited, nothing stale)."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "page.html"
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "build_thin_page.py"), "--out", str(out)], capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT))
        assert r.returncode == 0, r.stdout[-400:] + r.stderr[-400:]
        assert out.read_text(encoding="utf-8") == cb.BUILT.read_text(encoding="utf-8"), "the committed thin page is stale: run python tools/build_thin_page.py --rebuild"


def test_only_the_documented_logic_is_left_in_the_page():
    r = cb.analyse()
    assert r["problems"] == [], r["problems"]
    assert r["fallback_copies"] == ["activatePortfolio"]   # a LIVE / LIVE_ALT tab places orders: the engine refuses it and the page runs its own copy
    assert len(r["delegated"]) >= 30 and len(r["removed_to_engine_calls"]) == 12


def test_a_stray_controller_would_be_reported(monkeypatch):
    """The check can fail: pretend an extra controller is meant to be delegated, or one of the documented in-page functions to be gone."""
    monkeypatch.setitem(cb.BOUNDARY, "movePortfolio", "pretend it stays")   # it is delegated, so it is NOT unchanged in the page
    assert any("movePortfolio" in p for p in cb.analyse()["problems"])
    monkeypatch.delitem(cb.BOUNDARY, "movePortfolio")
    monkeypatch.setattr(cb, "FALLBACK_COPIES", {"activatePortfolio", "somethingElse"})
    assert any("fallback copies" in p for p in cb.analyse()["problems"])
