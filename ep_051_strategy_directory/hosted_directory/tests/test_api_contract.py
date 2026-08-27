# Version history:
# 2026-08-27 v1.5.0 Codex - Verifies profitable-strategy count and percentage reconcile across the full filtered result before paging.
# 2026-08-25 v1.4.0 Codex - Verifies full-filter directory summary totals remain independent of pagination.
# 2026-08-24 v1.3.0 Codex - Verifies source product identity is exposed publicly.
# 2026-08-24 v1.2.0 Codex - Adds canonical equity-curve endpoint contract coverage.
# 2026-08-24 v1.1.0 Codex - Adds bounded evidence-period validation.
# 2026-08-23 v1.0.0 Codex - Authenticated ingestion and public API contract tests using fakes.

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app
from app.config import Settings
from app.repository import MemoryRepository
from sync.export_snapshot import build_snapshot


def _client(repository, token="test-sync-token"):
    settings = Settings(data_backend="memory", sync_token=token)
    return TestClient(create_app(repository=repository, settings=settings))


def test_ingestion_requires_bearer_token_and_is_idempotent(
    strategy_items, snapshot_kwargs
):
    repository = MemoryRepository()
    client = _client(repository)
    snapshot = build_snapshot(strategy_items, **snapshot_kwargs)

    payload = snapshot.model_dump(mode="json")
    assert client.post("/internal/snapshots", json=payload).status_code == 401
    assert (
        client.post(
            "/internal/snapshots",
            headers={"Authorization": "Bearer wrong"},
            json=payload,
        ).status_code
        == 401
    )

    headers = {
        "Authorization": "Bearer test-sync-token",
        "Idempotency-Key": snapshot.snapshot_id,
    }
    accepted = client.post("/internal/snapshots", headers=headers, json=payload)
    repeated = client.post("/internal/snapshots", headers=headers, json=payload)
    assert accepted.status_code == 202
    assert repeated.status_code == 202
    assert repeated.json()["snapshot_id"] == snapshot.snapshot_id


def test_ingestion_rejects_mismatched_idempotency_key(strategy_items, snapshot_kwargs):
    repository = MemoryRepository()
    client = _client(repository)
    snapshot = build_snapshot(strategy_items, **snapshot_kwargs)
    response = client.post(
        "/internal/snapshots",
        headers={
            "Authorization": "Bearer test-sync-token",
            "Idempotency-Key": "different-snapshot",
        },
        json=snapshot.model_dump(mode="json"),
    )
    assert response.status_code == 400
    assert repository.current_snapshot() is None


def test_public_directory_contract_supports_search_sort_and_paging(
    strategy_items, snapshot_kwargs
):
    repository = MemoryRepository()
    repository.promote(build_snapshot(strategy_items, **snapshot_kwargs))
    client = _client(repository)

    response = client.get(
        "/api/dna/strategies",
        params={"search": "102002", "sort": "total_net_return", "direction": "desc", "page": 1, "page_size": 10},
    )
    assert response.status_code == 200
    body = response.json()
    assert set(body) >= {"data", "as_of", "basis", "methodology_version", "quality_state"}
    assert body["data"]["total"] == 1
    assert body["data"]["items"][0]["strategy_id"] == "DNA_102002"
    assert body["data"]["items"][0]["product_name"] == "EURUSD"
    profitable = int(body["data"]["items"][0]["total_net_return"] > 0)
    assert body["data"]["summary"] == {
        "strategies": 1,
        "closed_trades": body["data"]["items"][0]["total_trades"],
        "total_net_return": body["data"]["items"][0]["total_net_return"],
        "profitable_strategies": profitable,
        "profitable_percentage": float(profitable * 100),
        "evidence_ready": int(body["data"]["items"][0]["quality_state"] == "VALID"),
        "collecting": int(body["data"]["items"][0]["quality_state"] == "COLLECTING"),
    }
    assert body["methodology_version"] == "1.0.0"
    assert "costs and commission already included" in body["basis"]


def test_directory_summary_covers_full_result_before_paging(strategy_items, snapshot_kwargs):
    repository = MemoryRepository()
    repository.promote(build_snapshot(strategy_items, **snapshot_kwargs))
    body = _client(repository).get(
        "/api/dna/strategies", params={"page_size": 1}
    ).json()["data"]
    assert len(body["items"]) == 1
    assert body["summary"]["strategies"] == body["total"] == len(strategy_items)
    assert body["summary"]["closed_trades"] == sum(item["total_trades"] for item in strategy_items)
    profitable = sum(item["total_trades"] > 0 and item["total_net_return"] > 0 for item in strategy_items)
    assert body["summary"]["profitable_strategies"] == profitable
    assert body["summary"]["profitable_percentage"] == round(profitable / len(strategy_items) * 100, 2)


def test_health_reports_no_snapshot_without_exposing_secrets():
    client = _client(MemoryRepository(), token="do-not-leak")
    response = client.get("/healthz")
    assert response.status_code == 200
    rendered = response.text
    assert "do-not-leak" not in rendered
    assert response.json()["status"] == "ok"


def test_directory_rejects_reversed_date_range_before_querying_source():
    settings = Settings(data_backend="sqlserver", db_server="unused", db_user="unused", db_pass="unused", local_intelligence_cache_path="runtime/__missing_api_contract_cache__.json",allow_synchronous_local_fallback=True)
    client = TestClient(create_app(settings=settings))
    response = client.get("/api/dna/strategies?date_from=2026-08-24&date_to=2026-08-01")
    assert response.status_code == 422
    assert "date_from" in response.json()["detail"]


def test_equity_curve_contract_is_canonical_and_period_aware(monkeypatch):
    import app.main as main_module
    monkeypatch.setattr(main_module, "local_equity_curve", lambda settings, strategy_id, start, end: [
        {"trade_number": 1, "closed_at": "2026-08-02T10:00:00", "net_return": 12.5, "equity": 12.5, "drawdown": 0.0}
    ])
    settings = Settings(data_backend="sqlserver", db_server="unused", db_user="unused", db_pass="unused", local_intelligence_cache_path="runtime/__missing_equity_cache__.json",allow_synchronous_local_fallback=True)
    client = TestClient(create_app(settings=settings))
    response = client.get("/api/dna/strategies/DNA_102001/equity-curve?date_from=2026-08-01&date_to=2026-08-31")
    assert response.status_code == 200
    assert response.json()["strategy_id"] == "DNA_102001"
    assert response.json()["period"] == {"date_from": "2026-08-01", "date_to": "2026-08-31"}
    assert response.json()["points"][0]["equity"] == 12.5
