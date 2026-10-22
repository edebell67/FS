# Version history:
# 2026-08-24 v1.1.0 Codex - Adds source product identity to public strategy fixtures.
# 2026-08-23 v1.0.0 Codex - Shared infrastructure-free EP051 test fixtures.

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone

import pytest


@pytest.fixture
def strategy_items() -> list[dict]:
    """Representative aggregate rows; no raw trades or database are required."""
    return [
        {
            "strategy_id": "DNA_102001",
            "descriptive_name": None,
            "product_name": "GBPUSD",
            "market": "FX",
            "status": "active",
            "total_trades": 12,
            "wins": 7,
            "losses": 4,
            "breakevens": 1,
            "total_net_return": 18.25,
            "win_rate": 7 / 12,
            "profit_factor": 1.72,
            "max_drawdown_money": -4.5,
            "evidence_start": "2025-01-01T00:00:00Z",
            "evidence_end": "2025-12-31T00:00:00Z",
            "quality_state": "VALID",
        },
        {
            "strategy_id": "DNA_102002",
            "descriptive_name": "Range Break",
            "product_name": "EURUSD",
            "market": "FX",
            "status": "active",
            "total_trades": 8,
            "wins": 3,
            "losses": 5,
            "breakevens": 0,
            "total_net_return": -2.75,
            "win_rate": 3 / 8,
            "profit_factor": 0.88,
            "max_drawdown_money": -8.0,
            "evidence_start": "2025-02-01T00:00:00Z",
            "evidence_end": "2025-11-30T00:00:00Z",
            "quality_state": "VALID",
        },
    ]


@pytest.fixture
def snapshot_kwargs() -> dict:
    return {
        "source_watermark": datetime.now(timezone.utc).isoformat(),
    }


@pytest.fixture
def copied_items(strategy_items: list[dict]) -> list[dict]:
    return deepcopy(strategy_items)
