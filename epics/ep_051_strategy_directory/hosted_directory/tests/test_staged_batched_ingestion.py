# Version history:
# 2026-08-28 v1.0.0 - Covers the staged, batched ingestion path (PUB-04):
#   MemoryRepository.begin_snapshot/add_snapshot_batch/finalize_snapshot,
#   the /internal/snapshots/{id}/begin,/batch,/finalize API contract, and
#   sync.publish_snapshot's client-side chunking against a mock transport.

from __future__ import annotations

import httpx
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.contracts import SnapshotEnvelope
from app.main import create_app
from app.repository import MemoryRepository
from sync.export_snapshot import build_snapshot
from sync.publish_snapshot import publish_snapshot


def _envelope(snapshot):
    return SnapshotEnvelope(**snapshot.model_dump(mode="json", include={
        "schema_version", "methodology_version", "snapshot_id",
        "source_watermark", "generated_at", "item_count", "sha256"}))


def test_repository_batched_round_trip_matches_direct_promote(strategy_items, snapshot_kwargs):
    snapshot = build_snapshot(strategy_items, **snapshot_kwargs)
    repository = MemoryRepository()
    repository.begin_snapshot(_envelope(snapshot))
    # Split into two batches to prove chunking reassembles correctly.
    repository.add_snapshot_batch(snapshot.snapshot_id, snapshot.items[:1], [], [])
    repository.add_snapshot_batch(snapshot.snapshot_id, snapshot.items[1:], [], [])
    repository.finalize_snapshot(snapshot.snapshot_id)

    assert repository.current_snapshot().snapshot_id == snapshot.snapshot_id
    assert {item.strategy_id for item in repository.current_snapshot().items} == {item.strategy_id for item in snapshot.items}


def test_finalize_rejects_incomplete_batches(strategy_items, snapshot_kwargs):
    snapshot = build_snapshot(strategy_items, **snapshot_kwargs)
    repository = MemoryRepository()
    repository.begin_snapshot(_envelope(snapshot))
    repository.add_snapshot_batch(snapshot.snapshot_id, snapshot.items[:1], [], [])
    with pytest.raises(ValueError, match="received 1 of 2 declared items"):
        repository.finalize_snapshot(snapshot.snapshot_id)
    assert repository.current_snapshot() is None


def test_batch_before_begin_is_rejected(strategy_items, snapshot_kwargs):
    snapshot = build_snapshot(strategy_items, **snapshot_kwargs)
    repository = MemoryRepository()
    with pytest.raises(KeyError):
        repository.add_snapshot_batch(snapshot.snapshot_id, snapshot.items, [], [])


def test_repeated_batch_is_idempotent(strategy_items, snapshot_kwargs):
    snapshot = build_snapshot(strategy_items, **snapshot_kwargs)
    repository = MemoryRepository()
    repository.begin_snapshot(_envelope(snapshot))
    repository.add_snapshot_batch(snapshot.snapshot_id, snapshot.items, [], [])
    repository.add_snapshot_batch(snapshot.snapshot_id, snapshot.items, [], [])  # retry of the same batch
    repository.finalize_snapshot(snapshot.snapshot_id)
    assert len(repository.current_snapshot().items) == len(snapshot.items)


def _client(repository, token="test-sync-token"):
    settings = Settings(data_backend="memory", sync_token=token)
    return TestClient(create_app(repository=repository, settings=settings))


def test_api_begin_batch_finalize_promotes_and_requires_auth(strategy_items, snapshot_kwargs):
    repository = MemoryRepository()
    client = _client(repository)
    snapshot = build_snapshot(strategy_items, **snapshot_kwargs)
    base = f"/internal/snapshots/{snapshot.snapshot_id}"
    envelope_body = snapshot.model_dump(mode="json", include={"schema_version", "methodology_version",
        "snapshot_id", "source_watermark", "generated_at", "item_count", "sha256"})
    auth = {"Authorization": "Bearer test-sync-token"}

    assert client.post(base + "/begin", json=envelope_body).status_code == 401
    assert client.post(base + "/begin", headers=auth, json=envelope_body).status_code == 202

    batch_body = {"batch_index": 0, "items": [item.model_dump(mode="json") for item in snapshot.items],
                  "intelligence_profiles": [], "return_series": []}
    bad_key = client.post(base + "/batch", headers=auth | {"Idempotency-Key": "wrong"}, json=batch_body)
    assert bad_key.status_code == 400
    good = client.post(base + "/batch", headers=auth | {"Idempotency-Key": f"{snapshot.snapshot_id}:0"}, json=batch_body)
    assert good.status_code == 202

    finalized = client.post(base + "/finalize", headers=auth | {"Idempotency-Key": snapshot.snapshot_id})
    assert finalized.status_code == 202
    assert finalized.json()["status"] == "current"
    assert repository.current_snapshot().snapshot_id == snapshot.snapshot_id


def test_publish_snapshot_client_chunks_into_begin_batch_finalize(strategy_items, snapshot_kwargs):
    snapshot = build_snapshot(strategy_items, **snapshot_kwargs)
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        return httpx.Response(202, json={"accepted": True})

    transport = httpx.MockTransport(handler)
    result = publish_snapshot(snapshot, "https://example.invalid", "tok", transport=transport, batch_size=1)

    assert result == {"accepted": True}
    base = f"/internal/snapshots/{snapshot.snapshot_id}"
    # 2 items with batch_size=1 -> begin, 2 batches, finalize.
    assert calls == [f"{base}/begin", f"{base}/batch", f"{base}/batch", f"{base}/finalize"]
