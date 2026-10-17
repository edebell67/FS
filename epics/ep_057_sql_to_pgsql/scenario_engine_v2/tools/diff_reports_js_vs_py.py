# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/diff_reports_js_vs_py.py — differential test of the report fetchers: loadHourlyReport (request + error text) vs engine/reports.py.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version: loadHourlyReport (form defaults -> URL, success payload, error message with / without a server message).
"""Usage: python diff_reports_js_vs_py.py [--cases N]. The page function runs with stub form controls and a recording fetch; compared: the URL requested, the payload kept, the error shown."""
import json
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import data_client as dc  # noqa: E402
from engine import reports  # noqa: E402

PAGE = ROOT / "top10_5min_equity_curves_source_v2.65.32.html"
INVENTORY = ROOT / "inventory_v2.65.32" / "inventory.json"
EXTRA = r"""
var __calls = [];
globalThis.API_BASE = 'http://api';
globalThis.HOURLY_REPORT_FAMILIES = [['breakout', 'Breakout']];
globalThis.syncHourlyProducts = () => {}; globalThis.renderHourlyRows = () => {}; globalThis.hourlyMoney = () => ''; globalThis.hourlyTone = () => '';
globalThis.hourlyIntervalLabel = () => 'Hourly';
async function __hourly(fx, name, c) {
  __calls = [];
  globalThis.fetch = async (url) => { const u = String(url); __calls.push(u); const r = fx[u] || { status: 404, payload: { error: 'not found' } };
    return { ok: r.status >= 200 && r.status < 300, status: r.status, json: async () => r.payload }; };
  const els = {};
  globalThis.document = { getElementById: id => els[id] || (els[id] = { innerHTML: '', textContent: '' }) };
  globalThis.hourlyReportRequest = 0; globalThis.hourlyReportPayload = null; globalThis.hourlyReportSummary = { innerHTML: '' };
  globalThis.hourlyProductType = { value: c.pt }; globalThis.hourlyProduct = { value: c.p }; globalThis.hourlyInterval = { value: c.iv };
  globalThis.hourlyReportInterval = c.ri; globalThis.hourlyReportDate = c.rd; globalThis.LIVE_DATE = c.live; globalThis.hourlyReportFamily = c.fam;
  await loadHourlyReport();
  const m = /Report unavailable: (.*)<\/span>/.exec(els.hourlyReportState.innerHTML);
  return { calls: __calls, error: m ? m[1] : null, payload: globalThis.hourlyReportPayload };
}
"""


def good_payload(c):
    return {"date": "2026-10-14", "product_type": "forex", "product": "all", "family": "breakout", "interval_minutes": 60, "summary": {"closed_trades": 3},
            "products": ["gbp"], "generated_at": "2026-10-14T12:00:00", "rows": [1, 2]}


def make_case(rng):
    return {"pt": rng.choice(["", "forex", "crypto"]), "p": rng.choice(["", "gbp", "a b&c", "EUR"]), "iv": rng.choice(["", "30", "0", "abc", "15.5", " 5 "]),
            "ri": rng.choice([60, "15", 0, None, 120]), "rd": rng.choice(["", "2026-10-14", None]), "live": "2026-10-15", "fam": rng.choice(["breakout", "breakout_r", "x y"]),
            "mode": rng.choice(["ok", "ok", "err", "errplain", "missing"])}


def run_python(case):
    cl = dc.DataClient(None, "http://api")
    url = f"http://api/api/hourly_family_report?{dc.url_search_params(reports.hourly_report_params(report_date=case['rd'], live_date=case['live'], product_type_value=case['pt'], product_value=case['p'], family=case['fam'], interval_value=case['iv'], report_interval=case['ri']))}"
    fx = {}
    if case["mode"] == "ok":
        fx[url] = {"status": 200, "payload": good_payload(case)}
    elif case["mode"] == "err":
        fx[url] = {"status": 400, "payload": {"error": "bad family"}}
    elif case["mode"] == "errplain":
        fx[url] = {"status": 500, "payload": {}}
    cl.transport = lambda u: ((fx[u]["status"], fx[u]["payload"]) if u in fx else (404, {"error": "not found"}))
    r = reports.load_hourly_report(cl, report_date=case["rd"], live_date=case["live"], product_type_value=case["pt"], product_value=case["p"],
                                   family=case["fam"], interval_value=case["iv"], report_interval=case["ri"])
    return {"calls": [r["url"]], "error": None if r["ok"] else r["error"], "payload": r.get("payload")}, fx


def diff(a, b, path=""):
    if a == b:
        return None
    return f"{path}: py {json.dumps(a)[:200]} vs js {json.dumps(b)[:200]}"


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", type=int, default=300)
    ns = ap.parse_args()
    rng = random.Random(3)
    cases, expected = [], {}
    for i in range(ns.cases):
        case = make_case(rng)
        exp, fx = run_python(case)
        cases.append({"id": i + 1, "call": "__hourly", "args": [fx, "loadHourlyReport", case]})
        expected[i + 1] = exp
    spec = {"page": str(PAGE), "inventory": str(INVENTORY), "functions": ["loadHourlyReport"], "extra": EXTRA, "cases": cases}
    with tempfile.TemporaryDirectory() as td:
        sp = Path(td) / "c.json"
        sp.write_text(json.dumps(spec), encoding="utf-8")
        r = subprocess.run(["node", str(ROOT / "tools" / "js_runner.js"), str(sp)], capture_output=True, text=True, encoding="utf-8", timeout=600)
    if r.returncode != 0:
        print("NODE FAILED:", r.stderr[-1500:])
        sys.exit(2)
    res = {x["id"]: x for x in json.loads(r.stdout)}
    ok, bad, jserr = 0, [], 0
    for cid, exp in expected.items():
        x = res[cid]
        if not x["ok"]:
            jserr += 1
            bad.append(f"case {cid}: JS error {x['error']}")
            continue
        d = diff(exp, x["result"])
        if d:
            bad.append(f"case {cid}: {d}")
        else:
            ok += 1
    print(f"load_hourly_report                 cases={ns.cases:4d} pass={ok:4d} fail={ns.cases - ok - jserr:4d} js_error={jserr}")
    for b in bad[:5]:
        print("     ", b)
    sys.exit(1 if ok != ns.cases else 0)


if __name__ == "__main__":
    main()
