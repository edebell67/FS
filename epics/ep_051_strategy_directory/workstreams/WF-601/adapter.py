"""Offline-only broker abstraction and deterministic sandbox.

Version history: 1.1.0 (2026-08-23) — finite positive quantity validation.
1.0.0 (2026-08-23) — initial safe adapter contract.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import math
import numbers
from typing import Protocol


class EventType(str, Enum):
    ACK = "ACK"
    FILL = "FILL"
    REJECT = "REJECT"
    CANCEL = "CANCEL"


@dataclass(frozen=True)
class OrderIntent:
    intent_id: str
    strategy_id: str
    instrument_id: str
    side: str
    quantity: float
    order_type: str = "MARKET"


class BrokerAdapter(Protocol):
    def capabilities(self) -> dict: ...
    def submit(self, intent: OrderIntent) -> list[dict]: ...
    def cancel(self, intent_id: str) -> dict: ...


class SandboxAdapter:
    """No network or credential fields; records synthetic events in memory only."""
    def __init__(self, instruments: dict[str, str]):
        self._instruments = dict(instruments)
        self._events: dict[str, list[dict]] = {}

    def capabilities(self) -> dict:
        return {
            "environment": "offline_sandbox",
            "supported": {"order_types": ["MARKET"], "events": [x.value for x in EventType]},
            "unsupported": ["live_accounts", "network_transport", "credential_storage", "withdrawals", "options"],
        }

    def submit(self, intent: OrderIntent) -> list[dict]:
        if intent.intent_id in self._events:
            return self._events[intent.intent_id]
        quantity_valid = isinstance(intent.quantity, numbers.Real) and not isinstance(intent.quantity, bool) and math.isfinite(intent.quantity) and intent.quantity > 0
        if not quantity_valid or intent.side not in {"BUY", "SELL"} or intent.order_type != "MARKET":
            events = [{"type": EventType.REJECT.value, "intent_id": intent.intent_id, "reason": "INVALID_ORDER"}]
        elif intent.instrument_id not in self._instruments:
            events = [{"type": EventType.REJECT.value, "intent_id": intent.intent_id, "reason": "UNSUPPORTED_INSTRUMENT"}]
        else:
            events = [
                {"type": EventType.ACK.value, "intent_id": intent.intent_id, "sandbox_symbol": self._instruments[intent.instrument_id]},
                {"type": EventType.FILL.value, "intent_id": intent.intent_id, "filled_quantity": intent.quantity, "synthetic": True},
            ]
        self._events[intent.intent_id] = events
        return events

    def cancel(self, intent_id: str) -> dict:
        return {"type": EventType.CANCEL.value, "intent_id": intent_id, "synthetic": True}

    def audit_view(self, intent: OrderIntent) -> dict:
        return {"intent": asdict(intent), "events": self._events.get(intent.intent_id, []), "environment": "offline_sandbox"}
