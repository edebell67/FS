# workstreams/WF-104/regime_foundation.py — Objective regime classification and leakage-free temporal joins.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: applies frozen directional/volatility rules with UNKNOWN and availability gates.

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


@dataclass(frozen=True)
class Observation:
    instrument_id: str
    interval_start: datetime
    interval_end: datetime
    available_at: datetime
    directional_state: str
    volatility_state: str
    definition_version: str = "1.0.0"
    quality_state: str = "VALID"


def classify(sma20: float | None, sma50: float | None, natr: float | None, p20: float | None, p80: float | None) -> tuple[str, str]:
    if sma20 is None or sma50 in (None, 0):
        direction = "UNKNOWN"
    else:
        difference = (sma20 - sma50) / sma50
        direction = "TREND_UP" if difference > 0.005 else "TREND_DOWN" if difference < -0.005 else "SIDEWAYS"
    if natr is None or p20 is None or p80 is None:
        volatility = "UNKNOWN"
    else:
        volatility = "HIGH_VOLATILITY" if natr > p80 else "LOW_VOLATILITY" if natr < p20 else "NORMAL_VOLATILITY"
    return direction, volatility


def join_regime(event_time: datetime, instrument_id: str, observations: Iterable[Observation]) -> Observation:
    eligible = sorted((item for item in observations if item.instrument_id == instrument_id and item.available_at <= event_time and item.quality_state == "VALID"), key=lambda item: (item.available_at, item.definition_version))
    if not eligible:
        return Observation(instrument_id, event_time, event_time, event_time, "UNKNOWN", "UNKNOWN", quality_state="MISSING")
    return eligible[-1]


def coverage(observations: Iterable[Observation]) -> dict[str, float | int]:
    rows = list(observations)
    total = len(rows)
    known = sum(1 for row in rows if row.directional_state != "UNKNOWN" and row.volatility_state != "UNKNOWN")
    return {"total": total, "fully_known": known, "coverage": known / total if total else 0.0}

