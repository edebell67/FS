# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_engine_client_js.py — the browser-side engine client (runner/static/engine_client.js) in Node with a fake XMLHttpRequest.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version: synchronous POST of the request JSON, memo of identical requests, memo bound, errors thrown to the caller, ?engine= override.
import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CLIENT = ROOT / "runner" / "static" / "engine_client.js"
pytestmark = pytest.mark.skipif(not shutil.which("node"), reason="needs node")

HARNESS = r"""
const vm = require('vm'), fs = require('fs');
const src = fs.readFileSync(process.argv[1], 'utf8');
const scenario = JSON.parse(process.argv[2]);
const sent = [];
class FakeXHR { open(m, u, async) { this.m = m; this.u = u; this.async = async; this.h = {}; }
  setRequestHeader(k, v) { this.h[k] = v; }
  send(body) { sent.push({ method: this.m, url: this.u, async: this.async, headers: this.h, body });
    const r = scenario.responses.shift(); this.status = r.status; this.responseText = r.text; } }
const win = {};
const ctx = vm.createContext({ window: win, XMLHttpRequest: FakeXHR, location: { search: scenario.search || '', origin: 'http://page.example' }, URLSearchParams, JSON, Map, Error, String, performance: { now: () => Date.now() }, Date });
vm.runInContext(src, ctx);
const out = { base: win.__engine.base, results: [], errors: [] };
for (const req of scenario.requests) { try { out.results.push(win.__engine.call(req)); } catch (e) { out.errors.push(String(e.message)); } }
out.sent = sent; out.stats = win.__engine.stats;
console.log(JSON.stringify(out));
"""


def run(requests, responses, search=""):
    r = subprocess.run(["node", "-e", HARNESS, str(CLIENT), json.dumps({"requests": requests, "responses": responses, "search": search})], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_posts_json_synchronously_to_the_engine_and_returns_the_parsed_answer():
    out = run([{"fn": "computeSplitTargetSignal", "args": [1, 2]}], [{"status": 200, "text": json.dumps({"ok": [1, 2, 3]})}])
    assert out["results"] == [{"ok": [1, 2, 3]}] and out["errors"] == []
    (call,) = out["sent"]
    assert call["method"] == "POST" and call["url"] == "http://page.example/engine/call" and call["async"] is False
    assert call["headers"]["Content-Type"] == "application/json" and json.loads(call["body"]) == {"fn": "computeSplitTargetSignal", "args": [1, 2]}


def test_identical_requests_are_answered_from_the_memo():
    req = {"fn": "f", "args": [1]}
    out = run([req, req, {"fn": "f", "args": [2]}, req], [{"status": 200, "text": '"a"'}, {"status": 200, "text": '"b"'}])
    assert out["results"] == ["a", "a", "b", "a"] and len(out["sent"]) == 2
    assert out["stats"] == {"calls": 4, "hits": 2, "requests": 2, "ms": out["stats"]["ms"]}


def test_a_failed_call_throws_and_is_not_remembered():
    req = {"fn": "f", "args": []}
    out = run([req, req], [{"status": 422, "text": "bad request: missing global"}, {"status": 200, "text": "1"}])
    assert len(out["errors"]) == 1 and "422" in out["errors"][0] and "missing global" in out["errors"][0]
    assert out["results"] == [1] and len(out["sent"]) == 2


def test_engine_location_can_be_overridden_in_the_url():
    out = run([{"fn": "f"}], [{"status": 200, "text": "null"}], search="?engine=http://127.0.0.1:9999/")
    assert out["base"] == "http://127.0.0.1:9999" and out["sent"][0]["url"] == "http://127.0.0.1:9999/engine/call"


def test_the_memo_is_bounded():
    reqs = [{"fn": "f", "args": [i]} for i in range(300)] + [{"fn": "f", "args": [0]}]
    out = run(reqs, [{"status": 200, "text": str(i)} for i in range(301)])
    assert len(out["sent"]) == 301  # the first request was evicted (256 entries), so asking again hits the engine again
