"""Sandbox reconciler. Versions: 1.1.0 (2026-08-23) fail-closed numeric validation; 1.0.0 initial."""
from collections import defaultdict
import math
import numbers


TERMINAL = {"FILL", "REJECT", "CANCEL"}


def reconcile(intents, events, *, heartbeat_age, heartbeat_limit, killed=False):
    by_id = defaultdict(list)
    alerts = []
    unique_intents = {}
    def valid_number(value, *, nonnegative=True):
        return isinstance(value, numbers.Real) and not isinstance(value, bool) and math.isfinite(value) and (value >= 0 if nonnegative else True)
    if not valid_number(heartbeat_age) or not valid_number(heartbeat_limit):
        alerts.append({"code": "INVALID_NUMERIC"})
    for intent in intents:
        iid = intent["intent_id"]
        if iid in unique_intents and unique_intents[iid] != intent: alerts.append({"code": "INTENT_CONFLICT", "intent_id": iid})
        unique_intents.setdefault(iid, intent)
    seen_events = set()
    for event in events:
        key = (event["intent_id"], event["type"], event.get("event_id"))
        if key in seen_events: continue
        seen_events.add(key); by_id[event["intent_id"]].append(event)
        if event["intent_id"] not in unique_intents: alerts.append({"code": "ORPHAN_EVENT", "intent_id": event["intent_id"]})
    states = {}
    for iid in unique_intents:
        types = [e["type"] for e in by_id[iid]]
        states[iid] = next((x for x in reversed(types) if x in TERMINAL), "ACK" if "ACK" in types else "PENDING")
        if not types: alerts.append({"code": "MISSING_ACK", "intent_id": iid})
    if valid_number(heartbeat_age) and valid_number(heartbeat_limit) and heartbeat_age > heartbeat_limit: alerts.append({"code": "HEARTBEAT_STALE"})
    quantities=[i.get("quantity",0) for i in unique_intents.values()];fills=[e.get("filled_quantity",0) for e in events if e["type"]=="FILL"]
    if not all(valid_number(x) for x in quantities+fills): alerts.append({"code":"INVALID_NUMERIC"})
    else:
        expected=sum(quantities);filled=sum(fills)
        if filled > expected: alerts.append({"code": "POSITION_DRIFT", "expected_max": expected, "observed": filled})
    return {"states": states, "alerts": alerts, "kill_active": killed or any(a["code"] in {"INTENT_CONFLICT", "POSITION_DRIFT", "INVALID_NUMERIC"} for a in alerts)}
