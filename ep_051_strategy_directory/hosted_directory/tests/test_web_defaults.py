# Version history:
# 2026-08-27 v1.1.0 - Current day is the approved default; cover shared screen styling.
# 2026-08-24 v1.0.0 Codex - Verifies directory entry defaults align with the requested ranking and period.

from pathlib import Path


def test_directory_defaults_to_current_day_and_net_return_descending():
    html = (Path(__file__).parents[1] / "web" / "index.html").read_text(encoding="utf-8")
    assert 'value="total_net_return" selected' in html
    assert 'value="desc" selected' in html
    assert 'DnaPeriod.setPreset("today")' in html


def test_all_accessible_screens_load_shared_responsive_theme():
    web = Path(__file__).parents[1] / "web"
    for name in ("index", "search", "strategy", "intelligence", "regimes", "account", "compare", "builder"):
        html = (web / f"{name}.html").read_text(encoding="utf-8")
        assert '/assets/tech-principle-theme.css' in html
        assert 'name="viewport"' in html
    css = (web / "tech-principle-theme.css").read_text(encoding="utf-8")
    assert '[hidden]{display:none!important}' in css
    assert '@media(max-width:760px)' in css
    assert 'html[data-theme="dark"]' in css


def test_day_shift_controls_are_safe_for_shared_strategy_pages():
    web = Path(__file__).parents[1] / "web"
    index = (web / "index.html").read_text(encoding="utf-8")
    shared_period_script = (web / "period-filter.js").read_text(encoding="utf-8")
    strategy = (web / "strategy.html").read_text(encoding="utf-8")

    assert 'id="dayBack"' in index
    assert 'id="dayForward"' in index
    assert "window.dayBack.addEventListener" in shared_period_script
    assert "window.dayForward.addEventListener" in shared_period_script
    assert "dayBack.addEventListener" not in shared_period_script.replace("window.dayBack.addEventListener", "")
    assert "dayForward.addEventListener" not in shared_period_script.replace("window.dayForward.addEventListener", "")
    assert "globalThis.DnaPeriod" in shared_period_script
    assert "/assets/period-filter.js" in strategy


def test_shared_theme_asset_is_served():
    from fastapi.testclient import TestClient
    from app.main import create_app
    from app.config import Settings
    client = TestClient(create_app(settings=Settings(data_backend="memory")))
    response = client.get('/assets/tech-principle-theme.css')
    assert response.status_code == 200
    assert 'text/css' in response.headers['content-type']
