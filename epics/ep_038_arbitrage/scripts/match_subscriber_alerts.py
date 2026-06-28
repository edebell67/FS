from pathlib import Path
from datetime import datetime
import csv

ROOT = Path(__file__).resolve().parents[1]
SPREADS = ROOT / "data" / "live_spread_board.csv"
SUBS = ROOT / "data" / "subscriber_preferences.csv"
ALERTS = ROOT / "data" / "alert_events.csv"
ACTIVE_STATES = {"DISCOVERED", "WATCHING", "LIVE", "COOLING"}
RISK_ORDER = {"low": 1, "medium": 2, "medium-high": 3, "high": 4, "very-high": 5}


def split_filter(value):
    return {part.strip().lower() for part in (value or "").split("|") if part.strip()}


def fnum(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def risk_ok(spread_risk, max_risk):
    if not max_risk:
        return True
    return RISK_ORDER.get((spread_risk or "").lower(), 99) <= RISK_ORDER.get(max_risk.lower(), 99)


def matches(sub, spread):
    if sub.get("status") != "active":
        return False, "subscriber inactive"
    if spread.get("state") not in ACTIVE_STATES:
        return False, "spread not active"

    cats = split_filter(sub.get("category_filters"))
    if cats and spread.get("category", "").lower() not in cats:
        return False, "category mismatch"

    if fnum(spread.get("gross_spread_pct")) < fnum(sub.get("min_gross_spread_pct")):
        return False, "spread pct below threshold"
    if fnum(spread.get("gross_spread_amount")) < fnum(sub.get("min_gross_spread_value")):
        return False, "spread value below threshold"
    if fnum(spread.get("confidence_score")) < fnum(sub.get("min_confidence_score")):
        return False, "confidence below threshold"
    if not risk_ok(spread.get("risk_score"), sub.get("max_risk_score")):
        return False, "risk above threshold"

    if (sub.get("time_sensitive_only") or "").lower() == "yes":
        if spread.get("time_sensitive") != "yes" or spread.get("expiry_value_status") == "expired":
            return False, "not active time-sensitive"
        expiry_window = fnum(sub.get("expiry_window_hours"), 0)
        if expiry_window and fnum(spread.get("hours_to_expiry"), 999999) > expiry_window:
            return False, "outside expiry window"

    return True, "matched"


def main():
    with SPREADS.open(encoding="utf-8", newline="") as f:
        spreads = list(csv.DictReader(f))
    with SUBS.open(encoding="utf-8", newline="") as f:
        subscribers = list(csv.DictReader(f))

    alert_headers = ["alert_id", "subscriber_id", "spread_id", "trigger_type", "triggered_at", "delivery_channel", "delivery_status", "message_summary", "user_clicked", "notes"]
    existing = []
    if ALERTS.exists():
        with ALERTS.open(encoding="utf-8", newline="") as f:
            existing = list(csv.DictReader(f))
    existing_keys = {(row.get("subscriber_id"), row.get("spread_id"), row.get("trigger_type")) for row in existing}

    new_alerts = []
    now = datetime.now().isoformat(timespec="seconds")
    for sub in subscribers:
        for spread in spreads:
            ok, reason = matches(sub, spread)
            if not ok:
                continue
            trigger = "preferred_spread_available"
            if spread.get("time_sensitive") == "yes" and fnum(spread.get("hours_to_expiry"), 999999) <= 24:
                trigger = "preferred_spread_expiring_within_24h"
            key = (sub["subscriber_id"], spread["spread_id"], trigger)
            if key in existing_keys:
                continue
            value = spread.get("gross_spread_amount") or "unknown"
            pct = spread.get("gross_spread_pct") or "unknown"
            hours = spread.get("hours_to_expiry") or "unknown"
            summary = f"{spread['category']} match: {spread['item_name']} — £{value} gross spread, {pct}%, expiry {hours}h, confidence {spread.get('confidence_score')}/100."
            new_alerts.append({
                "alert_id": f"ALERT-{len(existing)+len(new_alerts)+1:04d}",
                "subscriber_id": sub["subscriber_id"],
                "spread_id": spread["spread_id"],
                "trigger_type": trigger,
                "triggered_at": now,
                "delivery_channel": sub.get("email_or_channel", "demo"),
                "delivery_status": "would_send_no_delivery",
                "message_summary": summary,
                "user_clicked": "",
                "notes": "Local MVP match only; no notification sent. Research information only; no profit guaranteed.",
            })

    with ALERTS.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=alert_headers)
        w.writeheader()
        w.writerows(existing + new_alerts)

    print(f"Matched {len(new_alerts)} new alert event(s); total stored {len(existing)+len(new_alerts)}")


if __name__ == "__main__":
    main()
