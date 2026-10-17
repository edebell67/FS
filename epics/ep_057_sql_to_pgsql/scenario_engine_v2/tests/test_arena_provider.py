# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tests/test_arena_provider.py — the EP052 arena's own contracts and IntelligenceClient against the runner's /v1/queries provider.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version.
import sys
import uuid
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
ARENA = ROOT.parent.parent / "ep_052_strategy_directory_agentic_trade_arena" / "lean_delivery" / "app" / "src"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
from fastapi.testclient import TestClient  # noqa: E402
from runner import RaceManager  # noqa: E402
from runner.server import create_app  # noqa: E402
from test_intelligence import curves  # noqa: E402
from test_runner_intel import Data  # noqa: E402

TOKEN = "t" * 40
HEAD = {"Authorization": "Bearer " + TOKEN, "X-EP052-Agent-ID": str(uuid.uuid4())}


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("EP057_INTELLIGENCE_TOKEN", TOKEN)
    data = Data()
    data.models = [{**m, "model": f"DNA_{i}"} for i, m in enumerate(curves(120), start=1)]   # DNA_1 (A), DNA_2 (B), DNA_3 (C)
    return TestClient(create_app(RaceManager(), client_factory=data.factory))


def body(kind="top_performers", **kw):
    return {"request_id": str(uuid.uuid4()), "revision": 0, "kind": kind, "strategy_ids": [], "limit": 3, **kw}


def test_auth_and_identity_are_required(client, monkeypatch):
    assert client.post("/v1/queries", json=body()).status_code == 401
    assert client.post("/v1/queries", json=body(), headers={"Authorization": "Bearer wrong" + "x" * 40, "X-EP052-Agent-ID": "a"}).status_code == 401
    assert client.post("/v1/queries", json=body(), headers={"Authorization": "Bearer " + TOKEN}).status_code == 422
    monkeypatch.delenv("EP057_INTELLIGENCE_TOKEN")
    assert client.post("/v1/queries", json=body(), headers=HEAD).status_code == 503


def test_each_kind_returns_ranked_ids_with_evidence(client):
    top = client.post("/v1/queries", json=body(), headers=HEAD).json()
    assert top["mode"] == "external" and len(top["strategy_ids"]) == 3 and "momentum" in top["notice"] and "evidence, not advice" in top["notice"]
    grp = client.post("/v1/queries", json=body("correlated_groups"), headers=HEAD).json()
    assert grp["strategy_ids"][:2] == ["DNA_1", "DNA_2"] or grp["strategy_ids"] == []
    assert client.post("/v1/queries", json=body("nonsense"), headers=HEAD).status_code == 422
    assert client.post("/v1/queries", json=body(limit=0), headers=HEAD).status_code == 422


def test_requested_ids_limit_and_window_are_respected(client):
    d = client.post("/v1/queries", json=body(strategy_ids=["DNA_1", "DNA_3"], limit=1), headers=HEAD).json()
    assert len(d["strategy_ids"]) == 1 and set(d["strategy_ids"]) <= {"DNA_1", "DNA_3"}
    early = client.post("/v1/queries", json=body(window_end="2026-10-14T05:00:00+00:00"), headers=HEAD).json()
    assert "as of 05:00" in early["notice"] and early["source_version"].endswith("05:00")


def test_exact_retry_returns_the_same_delivery_and_changed_content_conflicts(client):
    b = body()
    a = client.post("/v1/queries", json=b, headers=HEAD).json()
    again = client.post("/v1/queries", json=b, headers=HEAD).json()
    assert a["delivery_id"] == again["delivery_id"]
    assert client.post("/v1/queries", json={**b, "limit": 2}, headers=HEAD).status_code == 409
    other = {**HEAD, "X-EP052-Agent-ID": str(uuid.uuid4())}
    assert client.post("/v1/queries", json=b, headers=other).json()["delivery_id"] != a["delivery_id"]


def test_the_arenas_own_client_accepts_the_delivery(client):
    pytest.importorskip("httpx")
    if not ARENA.exists():
        pytest.skip("arena source not present")
    sys.path.insert(0, str(ARENA))
    import httpx
    from lean_exchange.contracts import QueryRequest
    from lean_exchange.intelligence_client import IntelligenceClient

    def handler(request):
        r = client.post("/v1/queries", content=request.content, headers={k: v for k, v in request.headers.items() if k.lower() in ("authorization", "x-ep052-agent-id", "content-type")})
        return httpx.Response(r.status_code, content=r.content, headers={"content-type": "application/json"})

    class Settings:
        provider_timeout_seconds = 5
        intelligence_url = "http://provider.test/v1/queries"
        intelligence_mode = "external"
    q = QueryRequest(request_id=uuid.uuid4(), kind="top_performers", limit=3)
    result = IntelligenceClient(Settings(), token=TOKEN, transport=httpx.MockTransport(handler)).query(HEAD["X-EP052-Agent-ID"], q)
    assert result.mode == "external" and 1 <= len(result.strategy_ids) <= 3 and result.query == q


def test_the_limit_caps_groups_that_hold_more_ids(client):
    full = client.post("/v1/queries", json=body("correlated_groups", limit=3), headers=HEAD).json()
    capped = client.post("/v1/queries", json=body("correlated_groups", limit=1), headers=HEAD).json()
    assert len(full["strategy_ids"]) >= 2 and len(capped["strategy_ids"]) == 1
