# Version history:
# 2026-08-30 v1.0.0 - Covers the hosted (postgres) per-strategy trade-ledger
# endpoint (/api/dna/strategies/{id}/trades), which previously 501'd
# unconditionally for any non-sqlserver backend. Extends
# IntelligenceReturnPoint with optional product/signal/entry_price/
# exit_price so the hosted ledger can show what the local SQL Server view
# always could; old snapshots without these fields still validate (all
# default to None).

from __future__ import annotations

from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.repository import MemoryRepository
from sync.export_snapshot import build_snapshot


def _snapshot_with_priced_trades(snapshot_kwargs):
    items = [
        {"strategy_id": "DNA_301001", "descriptive_name": None, "product_name": "GBPAUD_S", "market": "FX",
         "status": "active", "total_trades": 2, "wins": 1, "losses": 1, "breakevens": 0,
         "total_net_return": 65.0, "win_rate": 0.5, "profit_factor": 115 / 50, "max_drawdown_money": -50.0,
         "evidence_start": "2026-08-27T13:35:47Z", "evidence_end": "2026-08-28T22:01:37Z", "quality_state": "COLLECTING"},
    ]
    series = [
        {"strategy_id": "DNA_301001", "trade_id": "guid-2", "trade_number": 1,
         "opened_at": "2026-08-27T13:35:47Z", "observed_at": "2026-08-27T22:05:12Z",
         "net_return": -50.0, "cumulative_net_return": -50.0, "drawdown": -50.0,
         "product": "gbpaud_s", "signal": "BUY", "entry_price": 0.63885, "exit_price": 0.6384},
        {"strategy_id": "DNA_301001", "trade_id": "guid-1", "trade_number": 2,
         "opened_at": "2026-08-28T16:07:13Z", "observed_at": "2026-08-28T22:01:37Z",
         "net_return": 115.0, "cumulative_net_return": 65.0, "drawdown": 0.0,
         "product": "gbpaud_s", "signal": "SELL", "entry_price": 0.63895, "exit_price": 0.6378},
    ]
    return build_snapshot(items, return_series=series, **snapshot_kwargs)


def test_memory_repository_current_closed_trades_returns_prices(snapshot_kwargs):
    snapshot = _snapshot_with_priced_trades(snapshot_kwargs)
    repository = MemoryRepository()
    repository.promote(snapshot)
    rows = repository.current_closed_trades("DNA_301001")
    assert len(rows) == 2
    assert rows[0]["guid"] == "guid-2"
    assert rows[0]["signal"] == "BUY"
    assert rows[0]["entry_price"] == 0.63885
    assert rows[0]["exit_price"] == 0.6384
    assert rows[1]["guid"] == "guid-1"
    assert rows[1]["product"] == "gbpaud_s"
    assert rows[1]["net_return"] == 115.0


def test_memory_repository_current_closed_trades_filters_by_close_time(snapshot_kwargs):
    snapshot = _snapshot_with_priced_trades(snapshot_kwargs)
    repository = MemoryRepository()
    repository.promote(snapshot)
    start = datetime(2026, 8, 28, tzinfo=timezone.utc)
    end = datetime(2026, 8, 29, tzinfo=timezone.utc)
    rows = repository.current_closed_trades("DNA_301001", start, end)
    assert len(rows) == 1
    assert rows[0]["guid"] == "guid-1"


def _client(repository, token="test-sync-token"):
    settings = Settings(data_backend="memory", sync_token=token)
    return TestClient(create_app(repository=repository, settings=settings))


def test_api_trade_ledger_no_longer_501s_on_hosted_backend(snapshot_kwargs):
    snapshot = _snapshot_with_priced_trades(snapshot_kwargs)
    repository = MemoryRepository()
    repository.promote(snapshot)
    client = _client(repository)
    response = client.get("/api/dna/strategies/DNA_301001/trades")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert body["items"][1]["entry_price"] == 0.63895
    assert body["items"][1]["exit_price"] == 0.6378
