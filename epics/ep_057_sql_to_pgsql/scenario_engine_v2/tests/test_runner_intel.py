# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_runner_intel.py — intelligence endpoints and watches (proactive events) over fake data.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version.
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
from fastapi.testclient import TestClient  # noqa: E402
from runner import RaceManager  # noqa: E402
from runner.intel import MAX_WATCHES_PER_AGENT, WatchRegistry  # noqa: E402
from runner.server import create_app  # noqa: E402
from test_intelligence import curves  # noqa: E402


class Data:
    """A data source whose curves can be swapped between evaluations."""

    def __init__(self):
        self.models = curves(120)

    def factory(self, spec):
        outer = self
        assert spec.get("limit", 10) in (10, 20, 30), "the real data service only serves 10, 20 or 30 strategies"

        class C:
            portfolio_models, criteria_data = [], {}

            def fetch_portfolio_data(self, *a, **k):
                self.portfolio_models = outer.models

            def refresh_live_data(self, date, **k):
                self.criteria_data = {"top_net": {date: outer.models}}
                return {"ok": True, "scenario": "top_net", "url": "fake"}
        return C()


@pytest.fixture()
def env():
    data = Data()
    reg = WatchRegistry(data.factory)
    app = create_app(RaceManager(), client_factory=data.factory, watches=reg)
    return TestClient(app), data, reg


BODY = {"date": "2026-10-14", "window": 40, "corr_threshold": 0.5}


def test_report_endpoint_returns_decision_evidence(env):
    c, _, _ = env
    r = c.post("/api/intelligence/report", json=BODY).json()
    assert r["strategies"] == 3 and len(r["top"]) == 3 and r["confidence"] in ("medium", "high") and r["caveats"] and r["as_of"]
    assert any(set(g["members"]) == {"A", "B"} for g in r["clusters"]) or r["spread_signals"] is not None


def test_report_as_of_time_never_looks_ahead(env):
    c, _, _ = env
    early = c.post("/api/intelligence/report", json={**BODY, "as_of_time": "05:00"}).json()
    assert early["as_of"] <= "05:00" and early["sample_points"] == 61   # 00:00 .. 05:00 at 5-minute spacing


def test_validation(env):
    c, _, _ = env
    assert c.post("/api/intelligence/report", json={"date": "x"}).status_code == 422
    assert c.post("/api/intelligence/report", json={**BODY, "as_of_time": "5pm"}).status_code == 422
    assert c.post("/api/intelligence/report", json={**BODY, "extra": 1}).status_code == 422


def test_watches_queue_events_only_on_change_and_agents_pull_them(env):
    c, data, _ = env
    w = c.post("/api/intelligence/watches", json={"agent": "agent-1", "spec": BODY, "top_change": True, "spread_z": 1.5}).json()
    wid = w["watch_id"]
    first = c.post(f"/api/intelligence/watches/{wid}/evaluate").json()["new_events"]
    again = c.post(f"/api/intelligence/watches/{wid}/evaluate").json()["new_events"]
    assert again == 0                                                       # nothing new, nothing queued
    data.models = [m for m in reversed(data.models)]                        # same curves, different order: top set unchanged
    assert c.post(f"/api/intelligence/watches/{wid}/evaluate").json()["new_events"] == 0
    from test_intelligence import model
    data.models = data.models + [model("D", [x * 5 for x in range(120)])]  # a new leader: the top 3 changes
    assert c.post(f"/api/intelligence/watches/{wid}/evaluate").json()["new_events"] >= 1
    events = c.get("/api/intelligence/events", params={"agent": "agent-1"}).json()["events"]
    assert any(e["kind"] == "top_change" for e in events) and all(e["caveats"] and e["as_of"] for e in events)
    assert len(events) >= first + 1
    assert c.get("/api/intelligence/events", params={"agent": "agent-1"}).json()["events"] == []   # pulled once, cleared
    assert c.get("/api/intelligence/events", params={"agent": "agent-2"}).json()["events"] == []   # other agents see nothing


def test_watch_limits_and_deletion(env):
    c, _, _ = env
    ids = [c.post("/api/intelligence/watches", json={"agent": "a", "spec": BODY}).json()["watch_id"] for _ in range(MAX_WATCHES_PER_AGENT)]
    assert c.post("/api/intelligence/watches", json={"agent": "a", "spec": BODY}).status_code == 422
    assert c.delete(f"/api/intelligence/watches/{ids[0]}").json() == {"removed": True}
    assert c.delete(f"/api/intelligence/watches/{ids[0]}").status_code == 404
    assert c.post("/api/intelligence/watches/nope/evaluate").status_code == 404
