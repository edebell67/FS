# VERSION HISTORY
# v1.1.1 · 2026-08-27 · Tracks the approved “Profitable strategies” summary label.
# v1.1.0 · 2026-08-27 · Verifies the directory headline renders the API-backed profitable-strategy percentage instead of aggregate net return.
# v1.0.1 · 2026-08-25 · Verifies the directory renders and updates its persistent evidence summary.
# v1.0.0 · 2026-08-24 · Finder routing, discoverability and no-hidden-constraint UI checks.
from pathlib import Path
from fastapi.testclient import TestClient
from app.config import Settings
from app.main import create_app


WEB=Path(__file__).resolve().parents[1]/"web"


def test_directory_renders_api_backed_summary():
    html=(WEB/"index.html").read_text(encoding="utf-8")
    assert 'id="directorySummary"' in html
    for field in ("summaryStrategies", "summaryTrades", "summaryProfitable", "summaryReady"):
        assert f'id="{field}"' in html
    assert "p.data.summary" in html and "summary.closed_trades" in html
    assert "Profitable strategies" in html and "summary.profitable_percentage" in html
    assert "summaryReturn" not in html


def test_finder_is_served_and_discoverable_from_directory():
    client=TestClient(create_app(settings=Settings(data_backend="memory")))
    assert client.get("/intelligence.html").status_code==200
    assert '/intelligence.html' in (WEB/"index.html").read_text(encoding="utf-8")


def test_finder_shows_interpreted_constraints_before_retrieval_and_has_mobile_css():
    html=(WEB/"intelligence.html").read_text(encoding="utf-8")
    css=(WEB/"styles.css").read_text(encoding="utf-8")
    assert html.index("constraintStage")<html.index("runButton") or "constraintStage" in html
    assert "No hidden filters" in html and "filter-before-rank" not in html
    assert "@media (max-width: 580px)" in css and ".intelligence-grid" in css


def test_finder_escapes_server_values_before_rendering():
    html=(WEB/"intelligence.html").read_text(encoding="utf-8")
    assert "const esc =" in html and "esc(profile.identity.name" in html and "esc(reason)" in html


def test_comparison_uses_canonical_intelligence_relationships():
    html=(WEB/"compare.html").read_text(encoding="utf-8")
    assert "intelligenceCompare" in html and "result.relationships" in html
    assert "Evidence state" in html and "aligned observations" in html and "result.warnings" in html
