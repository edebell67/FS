# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_runner_server.py — the race runner's HTTP service: launch, list, read, cancel, parallel cap, validation, live refusal, dashboard.
#
# VERSION HISTORY
# v1.1.0 · 2026-10-17 · /engine/call, the engine client script, the engine-client page and the data-service proxy.
# v1.0.0 · 2026-10-17 · Initial version (FastAPI TestClient; races run on a fake data client, no network).
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
from fastapi.testclient import TestClient  # noqa: E402
from runner import RaceManager  # noqa: E402
from runner.server import create_app  # noqa: E402
from test_runner import FakeClient  # noqa: E402


@pytest.fixture()
def api():
    mgr = RaceManager(max_concurrent=5, client_factory=lambda c: FakeClient())
    return TestClient(create_app(mgr)), mgr


BODY = {"name": "t", "start_model": "DNA_1", "add_models": ["DNA_2", "DNA_3"], "date": "2026-10-14"}


def test_health_config_and_dashboard(api):
    c, _ = api
    h = c.get("/healthz").json()
    assert h["ok"] and h["mode"] == "virtual_only" and h["max_concurrent"] == 5
    cfg = c.get("/api/config").json()
    assert cfg["max_concurrent"] == 5 and cfg["default_max_concurrent"] == 5 and cfg["hard_limit"] >= 5
    page = c.get("/dashboard")
    assert page.status_code == 200 and "Virtual Race Dashboard" in page.text and 'name="viewport"' in page.text
    assert c.get("/").status_code == 200


def test_cap_can_be_changed_and_is_validated(api):
    c, mgr = api
    assert c.put("/api/config", json={"max_concurrent": 8}).json() == {"max_concurrent": 8}
    assert mgr.max_concurrent == 8
    assert c.put("/api/config", json={"max_concurrent": 0}).status_code == 422
    assert c.put("/api/config", json={"max_concurrent": 1000}).status_code == 422
    assert c.put("/api/config", json={"max_concurrent": 3, "extra": 1}).status_code == 422


def test_launch_list_read_result(api):
    c, mgr = api
    r = c.post("/api/races", json=BODY)
    assert r.status_code == 201
    rid = r.json()["race_id"]
    assert mgr.wait(30)
    s = c.get(f"/api/races/{rid}").json()
    assert s["state"] == "completed" and s["leader"] == "DNA_2" and s["standings"][0]["model"] == "DNA_2" and s["pct"] == 100.0
    full = c.get(f"/api/races/{rid}/result").json()
    assert full["frames"] == 5 and len(full["board"]) == 5 and "outputs" in full
    lst = c.get("/api/races").json()
    assert lst["counts"]["completed"] == 1 and lst["races"][0]["race_id"] == rid
    assert c.get("/api/races/nope").status_code == 404 and c.get("/api/races/nope/result").status_code == 404


def test_many_launches_are_all_accepted_and_complete(api):
    c, mgr = api
    ids = [c.post("/api/races", json={**BODY, "name": f"r{i}"}).json()["race_id"] for i in range(12)]
    assert len(set(ids)) == 12
    assert mgr.wait(60)
    assert c.get("/api/races").json()["counts"]["completed"] == 12


def test_validation_and_live_refusal(api):
    c, _ = api
    assert c.post("/api/races", json={**BODY, "date": "14/10/2026"}).status_code == 422
    assert c.post("/api/races", json={**BODY, "return_type": "XX"}).status_code == 422
    assert c.post("/api/races", json={**BODY, "bogus": 1}).status_code == 422
    r = c.post("/api/races", json={**BODY, "start_model": "LIVE"})
    assert r.status_code == 422 and "live" in r.json()["detail"].lower()
    assert c.post("/api/races", json={**BODY, "add_models": [f"DNA_{i}" for i in range(25)]}).status_code == 422


def test_cancel(api):
    import threading
    gate = threading.Event()
    mgr = RaceManager(max_concurrent=1, client_factory=lambda c: FakeClient(gate))
    c = TestClient(create_app(mgr))
    a = c.post("/api/races", json=BODY).json()["race_id"]
    b = c.post("/api/races", json=BODY).json()["race_id"]
    time.sleep(0.2)
    assert c.delete(f"/api/races/{b}").json() == {"cancelled": True}
    assert c.delete(f"/api/races/{a}").json() == {"cancelled": True}
    gate.set()
    assert mgr.wait(30)
    assert c.get(f"/api/races/{a}").json()["state"] == "cancelled" and c.get(f"/api/races/{b}").json()["state"] == "cancelled"
    assert c.delete("/api/races/nope").status_code == 404


# ---- the engine contract, the engine-client page and the data-service proxy ----
import json  # noqa: E402
import threading  # noqa: E402
from http.server import BaseHTTPRequestHandler, HTTPServer  # noqa: E402

from engine import core_ported as core  # noqa: E402


def _series(vals):
    return [{"time": f"{h:02d}:00", "net": v, "buy": v, "sell": 0} for h, v in enumerate(vals)]


def test_engine_call_answers_like_the_engine(api):
    c, _ = api
    series = _series([0, 10, 30, 20, 50])
    base = core.base_point(series, 0)
    body = {"fn": "computeTradeOverlaySignals", "args": [series, base], "globals": {"exitThreshold": 0}}
    r = c.post("/engine/call", json=body)
    assert r.status_code == 200 and r.json() == json.loads(json.dumps(core.overlay_signals(series, base, 0.0)))
    r2 = c.post("/engine/call", json={"fn": "computeSplitTargetSignal", "args": [r.json(), series, base], "globals": {"dailyTarget": 0}})
    assert r2.status_code == 200 and r2.json() is None


def test_engine_call_rejects_bad_requests(api):
    c, _ = api
    assert c.post("/engine/call", json={"fn": "nope", "args": []}).status_code == 422
    assert c.post("/engine/call", json={"fn": "computeTradeOverlaySignals", "args": [[], {}], "globals": {}}).status_code == 422   # missing global
    assert c.post("/engine/call", json=[1, 2]).status_code == 422
    assert c.post("/engine/call", json={"fn": "computeTradeOverlaySignals", "args": [1]}).status_code == 422                       # malformed args


def test_engine_client_script_and_thin_page_are_served(api):
    c, _ = api
    js = c.get("/engine/client.js")
    assert js.status_code == 200 and "XMLHttpRequest" in js.text and "/engine/call" in js.text
    page = c.get("/top10_5min_equity_curves_engine_client.html")
    assert page.status_code == 200 and "__engine.call" in page.text and "function computeLeaderRotation(activeModels, metricKey, upToIdx, replaySeries = null)" in page.text


def test_data_service_proxy_forwards_requests_and_failures():
    seen = []

    class Up(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, status, payload, ctype="application/json"):
            data = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):  # noqa: N802
            seen.append(("GET", self.path))
            if self.path.startswith("/api/live_day"):
                self._send(200, {"top_net": [], "path": self.path})
            elif self.path == "/style.css":
                self._send(200, b"body{}", "text/css")
            else:
                self._send(404, {"error": "not found"})

        def do_PUT(self):  # noqa: N802
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            seen.append(("PUT", self.path, body.decode()))
            self._send(200, {"echo": json.loads(body)})

    srv = HTTPServer(("127.0.0.1", 0), Up)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        c = TestClient(create_app(RaceManager(client_factory=lambda cfg: FakeClient()), data_api=f"http://127.0.0.1:{srv.server_port}"))
        r = c.get("/api/live_day?date=2026-10-14&limit=10")
        assert r.status_code == 200 and r.json()["path"] == "/api/live_day?date=2026-10-14&limit=10"
        assert c.get("/style.css").text == "body{}" and c.get("/style.css").headers["content-type"].startswith("text/css")
        assert c.get("/api/unknown").status_code == 404
        put = c.put("/api/scenario_workspace", json={"a": 1})
        assert put.status_code == 200 and put.json() == {"echo": {"a": 1}} and seen[-1] == ("PUT", "/api/scenario_workspace", '{"a":1}')
        assert c.get("/api/races").json()["counts"]["running"] == 0        # the runner's own routes win over the proxy
    finally:
        srv.shutdown()
    dead = TestClient(create_app(RaceManager(), data_api="http://127.0.0.1:9"))
    assert dead.get("/api/live_day").status_code == 502


def test_limit_validation_matches_the_data_service(api):
    c, _ = api
    assert c.post("/api/races", json={**BODY, "limit": 15}).status_code == 422
    assert c.post("/api/races", json={**BODY, "limit": 20}).status_code == 201
    assert c.post("/api/intelligence/report", json={"date": "2026-10-14", "limit": 50}).status_code == 422


def test_delete_finished_race_and_clear_finished(api):
    import threading
    gate = threading.Event()
    mgr = RaceManager(max_concurrent=1, client_factory=lambda c: FakeClient(gate))
    c = TestClient(create_app(mgr))
    a = c.post("/api/races", json=BODY).json()["race_id"]
    time.sleep(0.2)
    assert c.delete(f"/api/races/{a}").json() == {"cancelled": True}  # active: cancel, not remove
    gate.set()
    assert mgr.wait(30)
    assert c.delete(f"/api/races/{a}").json() == {"removed": True}  # finished: removed
    assert c.get(f"/api/races/{a}").status_code == 404
    ids = [c.post("/api/races", json=BODY).json()["race_id"] for _ in range(2)]
    assert mgr.wait(30)
    assert c.delete("/api/races").json() == {"removed": 2}
    assert c.get("/api/races").json()["races"] == [] and all(c.get(f"/api/races/{i}").status_code == 404 for i in ids)


def test_board_endpoint_serves_every_frame(api):
    mgr = RaceManager(max_concurrent=1, client_factory=lambda c: FakeClient())
    c = TestClient(create_app(mgr))
    rid = c.post("/api/races", json=BODY).json()["race_id"]
    assert mgr.wait(30)
    full = c.get(f"/api/races/{rid}/board").json()
    assert full["state"] == "completed" and len(full["board"]) == full["frames"] > 1
    assert full["board"][0]["frame"] == 0 and full["board"][0]["leaders"]
    tail = c.get(f"/api/races/{rid}/board", params={"since": 2}).json()["board"]
    assert tail == full["board"][2:]
    assert c.get("/api/races/nope/board").status_code == 404


def test_the_proxy_builds_its_http_client_once_not_per_request(monkeypatch):
    """Constructing an httpx client loads the CA bundle (0.7-1.8 s) and the proxy runs on the event loop: a client per request froze every engine call behind it."""
    import httpx
    built = []
    real = httpx.AsyncClient.__init__

    def counting(self, *a, **kw):
        built.append(1)
        real(self, *a, **kw)

    monkeypatch.setattr(httpx.AsyncClient, "__init__", counting)
    c = TestClient(create_app(RaceManager(client_factory=lambda cfg: FakeClient()), data_api="http://127.0.0.1:9"))
    for _ in range(3):
        assert c.get("/api/live_day").status_code == 502
    assert len(built) == 1


def test_find_model_calls_go_to_the_fast_api_and_the_served_page_points_at_this_origin(monkeypatch):
    import json
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer

    def serve(tag):
        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):  # noqa: N802
                body = json.dumps({"from": tag, "path": self.path}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        s = HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=s.serve_forever, daemon=True).start()
        return s
    data, fast = serve("data"), serve("fast")
    monkeypatch.setenv("EP057_FAST_API", f"http://127.0.0.1:{fast.server_port}")
    try:
        c = TestClient(create_app(RaceManager(), data_api=f"http://127.0.0.1:{data.server_port}"))
        for path in ("strategy_search", "strategy_search_day", "strategy_search_metrics", "portfolio_day"):
            assert c.get(f"/api/{path}?query=abc").json()["from"] == "fast"
        assert c.get("/api/live_day").json()["from"] == "data"   # everything else still goes to the data service
        page = c.get("/top10_5min_equity_curves_engine_client.html").text
        assert "|| location.origin" in page and "|| 'http://127.0.0.1:8767'" not in page
    finally:
        data.shutdown()
        fast.shutdown()
