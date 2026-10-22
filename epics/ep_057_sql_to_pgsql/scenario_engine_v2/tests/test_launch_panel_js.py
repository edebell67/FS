# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_launch_panel_js.py — the "Virtual race" panel of the engine-client page (runner/static/launch_panel.js) in Node with a fake DOM.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version: the request built from the page's view, selection fallbacks, clamping, rule opt-in, live-portfolio refusal, the page copy carries the panel after the main script.
import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PANEL = ROOT / "runner" / "static" / "launch_panel.js"
pytestmark = pytest.mark.skipif(not shutil.which("node"), reason="needs node")

HARNESS = r"""
const vm = require('vm'), fs = require('fs');
const src = fs.readFileSync(process.argv[1], 'utf8');
const scenario = JSON.parse(process.argv[2]);
class El { constructor(tag) { this.tag = tag; this.children = []; this.style = {}; this._text = ''; this.className = ''; }
  appendChild(c) { this.children.push(c); return c; } replaceChildren(...c) { this.children = c; } remove() { this.removed = true; }
  set textContent(v) { this._text = String(v); } get textContent() { return this._text + this.children.map(c => c.textContent).join(''); }
  querySelectorAll() { return []; } }
const created = [];
const document = { readyState: 'complete', head: new El('head'), body: new El('body'), createElement: t => { const e = new El(t); created.push(e); return e; },
  createTextNode: t => { const e = new El('#text'); e._text = t; return e; }, getElementById: () => null, addEventListener() {} };
const g = { document, window: {}, location: { origin: 'http://runner.example' }, fetch: () => Promise.reject(new Error('no network in this test')), setTimeout, JSON, Math, Set, Number, String, Array, Object, Error, Promise };
Object.assign(g, scenario.globals || {});
if (scenario.globals && scenario.globals.visibleModels) g.visibleModels = new Set(scenario.globals.visibleModels);
const ctx = vm.createContext(g);
// the page's functions are top-level declarations: define them as the page does
vm.runInContext('function getEligibleModels(){ return __models; } function activePortfolioOverlayRule(){ return __rule; }', ctx);
ctx.__models = scenario.models; ctx.__rule = scenario.rule || null;
vm.runInContext(src, ctx);
const api = ctx.window.__virtualRace;
const out = { view: api.currentView() };
if (scenario.form) out.request = api.buildRequest(out.view, scenario.form);
if (scenario.open) { api.openPanel(); out.panelText = document.body.children.filter(c => c.id === 'vr-panel').map(c => c.textContent)[0] || null;
  out.hasLaunch = created.some(e => e.tag === 'button' && e.className === 'vr-go'); }
out.buttons = document.body.children.filter(c => c.id === 'vr-btn').length;
console.log(JSON.stringify(out));
"""

MODELS = [{"model": "DNA_1"}, {"model": "DNA_2"}, {"model": "DNA_3"}]
BASE_GLOBALS = {"currentDate": "2026-10-14", "currentCriteria": "top_net", "currentReturnType": "NET", "splitMode": "ALL_NET", "exitThreshold": 25, "overlayTopX": 2, "dailyTarget": 500,
                "baselineFrameIndex": 0, "currentProductType": "forex", "currentProduct": "all", "currentStrategyFamily": "all", "modelLimit": 10, "activePortfolioName": None,
                "selectedModelIndex": 1, "visibleModels": ["DNA_1", "DNA_2", "DNA_3"], "LIVE_DATE": "2026-10-17"}


def run(**kw):
    scenario = {"models": MODELS, "globals": {**BASE_GLOBALS, **kw.pop("globals", {})}, **kw}
    r = subprocess.run(["node", "-e", HARNESS, str(PANEL), json.dumps(scenario)], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_the_view_reflects_the_page_and_picks_the_selected_strategy():
    v = run()["view"]
    assert v["ids"] == ["DNA_1", "DNA_2", "DNA_3"] and v["selected"] == "DNA_2" and v["date"] == "2026-10-14"
    assert v["scenario"] == "top_net" and v["exitThreshold"] == 25 and v["holdRank"] == 2 and v["productType"] == "forex" and v["limit"] == 10


def test_hidden_models_are_not_candidates_and_the_selection_falls_back():
    v = run(globals={"visibleModels": ["DNA_1", "DNA_3"]})["view"]
    assert v["shown"] == ["DNA_1", "DNA_3"] and v["selected"] == "DNA_1"      # the selected DNA_2 is hidden -> first shown
    assert run(globals={"selectedModelIndex": 99})["view"]["selected"] == "DNA_1"


def test_a_past_date_is_used_and_a_non_date_falls_back_to_the_live_date():
    assert run(globals={"currentDate": "WEEK_OVERALL"})["view"]["date"] == "2026-10-17"


def test_request_building_and_clamping():
    out = run(form={"start": "DNA_2", "competitors": ["DNA_1", "DNA_2", "DNA_3"], "addTop": 40, "date": "2026-10-13", "returnType": "ALT", "scenario": "top_net", "useRule": False},
              globals={"overlayTopX": 9, "modelLimit": 500})
    r = out["request"]
    assert r["start_model"] == "DNA_2" and r["add_models"] == ["DNA_1", "DNA_3"]       # the start strategy is not its own competitor
    assert r["add_scenario_top"] == 19 and r["date"] == "2026-10-13" and r["return_type"] == "ALT"
    assert r["hold_rank"] == 5 and r["limit"] == 50 and r["exit_threshold"] == 25 and r["split_mode"] == "ALL_NET" and "overlay_rule_id" not in r


def test_the_assigned_rule_is_used_only_when_asked_for():
    kw = dict(rule={"id": "r1", "name": "R1"}, globals={"activePortfolioName": "P"})
    on = run(form={"start": "DNA_1", "competitors": [], "useRule": True}, **kw)
    off = run(form={"start": "DNA_1", "competitors": [], "useRule": False}, **kw)
    assert on["view"]["ruleId"] == "r1" and on["request"]["overlay_rule_id"] == "r1" and "overlay_rule_id" not in off["request"]


@pytest.mark.parametrize("portfolio", ["LIVE", "live_alt"])
def test_live_portfolios_cannot_be_raced(portfolio):
    out = run(open=True, globals={"activePortfolioName": portfolio})
    assert "cannot be raced" in out["panelText"] and out["hasLaunch"] is False


def test_an_ordinary_view_gets_a_launch_button_and_one_floating_button():
    out = run(open=True)
    assert out["hasLaunch"] is True and out["buttons"] == 1 and "Virtual race" in out["panelText"]


def test_the_engine_client_page_carries_the_panel_after_the_main_script():
    page = sorted(ROOT.glob("top10_5min_equity_curves_engine_client_v*.html"))[-1].read_text(encoding="utf-8")
    assert page.count("__virtualRace") >= 1 and page.index("function computeLeaderRotation") < page.index("window.__virtualRace")
    import re
    assert len(re.findall(r"<script\b", page)) == page.count("</script>")   # every script tag is closed (the injected blocks are balanced)
