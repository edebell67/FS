# Version history:
# 2026-08-30 v1.0.0 - Covers period_items() on MemoryRepository and the
#   /api/dna/strategies date_from/date_to path on the hosted (postgres)
#   backend, which previously 501'd unconditionally for any date filter -
#   the actual blocker once PUB-04 got a real publish landing (evidence_end
#   advanced, but every period-scoped view - Current day/week/month, the
#   default page load - still failed).

from __future__ import annotations

from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.repository import MemoryRepository
from sync.export_snapshot import build_snapshot


def _snapshot_with_trades(strategy_items, snapshot_kwargs):
    # Items must reconcile exactly against return_series (Snapshot.verified()
    # checks this on promote) - built directly here rather than reusing the
    # shared strategy_items fixture, whose stats describe different trades.
    items = [
        {"strategy_id": "DNA_102001", "descriptive_name": None, "product_name": "GBPUSD", "market": "FX",
         "status": "active", "total_trades": 2, "wins": 1, "losses": 1, "breakevens": 0,
         "total_net_return": 2.0, "win_rate": 0.5, "profit_factor": 5 / 3, "max_drawdown_money": -3.0,
         "evidence_start": "2026-08-01T00:00:00Z", "evidence_end": "2026-08-10T01:00:00Z", "quality_state": "COLLECTING"},
        {"strategy_id": "DNA_102002", "descriptive_name": None, "product_name": "EURUSD", "market": "FX",
         "status": "active", "total_trades": 1, "wins": 1, "losses": 0, "breakevens": 0,
         "total_net_return": 1.0, "win_rate": 1.0, "profit_factor": None, "max_drawdown_money": 0.0,
         "evidence_start": "2026-08-01T00:00:00Z", "evidence_end": "2026-08-01T02:00:00Z", "quality_state": "COLLECTING"},
    ]
    series = [
        {"strategy_id": "DNA_102001", "trade_id": "t1", "trade_number": 1,
         "opened_at": "2026-08-01T00:00:00Z", "observed_at": "2026-08-01T01:00:00Z",
         "net_return": 5.0, "cumulative_net_return": 5.0, "drawdown": 0.0},
        {"strategy_id": "DNA_102001", "trade_id": "t2", "trade_number": 2,
         "opened_at": "2026-08-10T00:00:00Z", "observed_at": "2026-08-10T01:00:00Z",
         "net_return": -3.0, "cumulative_net_return": 2.0, "drawdown": -3.0},
        {"strategy_id": "DNA_102002", "trade_id": "t3", "trade_number": 1,
         "opened_at": "2026-08-01T00:00:00Z", "observed_at": "2026-08-01T02:00:00Z",
         "net_return": 1.0, "cumulative_net_return": 1.0, "drawdown": 0.0},
    ]
    return build_snapshot(items, return_series=series, **snapshot_kwargs)


def test_memory_repository_period_items_filters_by_close_time(strategy_items, snapshot_kwargs):
    snapshot = _snapshot_with_trades(strategy_items, snapshot_kwargs)
    repository = MemoryRepository()
    repository.promote(snapshot)

    start = datetime(2026, 8, 1, tzinfo=timezone.utc)
    end = datetime(2026, 8, 2, tzinfo=timezone.utc)
    rows = repository.period_items(start, end)

    by_id = {row["strategy_id"]: row for row in rows}
    assert set(by_id) == {"DNA_102001", "DNA_102002"}
    assert by_id["DNA_102001"]["total_trades"] == 1
    assert by_id["DNA_102001"]["total_net_return"] == 5.0
    assert by_id["DNA_102002"]["total_trades"] == 1


def test_memory_repository_period_items_respects_canonical_strategy(strategy_items, snapshot_kwargs):
    snapshot = _snapshot_with_trades(strategy_items, snapshot_kwargs)
    repository = MemoryRepository()
    repository.promote(snapshot)
    rows = repository.period_items(canonical_strategy="DNA_102001")
    assert {row["strategy_id"] for row in rows} == {"DNA_102001"}
    assert rows[0]["total_trades"] == 2


def _client(repository, token="test-sync-token"):
    settings = Settings(data_backend="memory", sync_token=token)
    return TestClient(create_app(repository=repository, settings=settings))


def test_api_period_query_no_longer_501s_on_hosted_backend(strategy_items, snapshot_kwargs):
    snapshot = _snapshot_with_trades(strategy_items, snapshot_kwargs)
    repository = MemoryRepository()
    repository.promote(snapshot)
    client = _client(repository)

    response = client.get("/api/dna/strategies", params={"date_from": "2026-08-01", "date_to": "2026-08-01"})
    assert response.status_code == 200
    body = response.json()["data"]
    assert body["total"] == 2

    # A signal filter combined with a period still can't be answered hosted -
    # the trade-level data model carries no per-trade signal - so this stays
    # a clean 501 rather than silently ignoring the filter.
    signalled = client.get("/api/dna/strategies", params={"date_from": "2026-08-01", "date_to": "2026-08-01", "signal": "BUY"})
    assert signalled.status_code == 501
