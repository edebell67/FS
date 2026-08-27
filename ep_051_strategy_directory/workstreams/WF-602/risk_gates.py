"""Offline preview gates. Versions: 1.1.0 (2026-08-23) finite/range validation; 1.0.0 initial."""
from dataclasses import dataclass, asdict
import math
import numbers


@dataclass(frozen=True)
class Preview:
    run_id: str
    environment: str
    confirmed: bool
    paused: bool
    killed: bool
    projected_exposure: float
    exposure_limit: float
    daily_loss: float
    daily_loss_limit: float
    data_age_seconds: int
    staleness_limit_seconds: int
    duplicate_intent: bool
    reference_price: float
    preview_price: float
    price_tolerance_fraction: float


def evaluate(preview: Preview) -> dict:
    failures = []
    numeric = (preview.projected_exposure, preview.exposure_limit, preview.daily_loss, preview.daily_loss_limit, preview.data_age_seconds, preview.staleness_limit_seconds, preview.reference_price, preview.preview_price, preview.price_tolerance_fraction)
    if any(not isinstance(value, numbers.Real) or isinstance(value, bool) or not math.isfinite(value) for value in numeric):
        failures.append("INVALID_NUMERIC")
    if preview.exposure_limit < 0 or preview.daily_loss_limit < 0 or preview.data_age_seconds < 0 or preview.staleness_limit_seconds < 0 or preview.reference_price <= 0 or preview.preview_price <= 0 or preview.price_tolerance_fraction < 0:
        failures.append("INVALID_RANGE")
    if preview.environment != "offline_sandbox": failures.append("LIVE_ENVIRONMENT_FORBIDDEN")
    if not preview.confirmed: failures.append("CONFIRMATION_REQUIRED")
    if preview.paused: failures.append("PAUSED")
    if preview.killed: failures.append("KILL_SWITCH")
    if preview.projected_exposure > preview.exposure_limit: failures.append("EXPOSURE_LIMIT")
    if abs(preview.daily_loss) > preview.daily_loss_limit: failures.append("LOSS_LIMIT")
    if preview.data_age_seconds > preview.staleness_limit_seconds: failures.append("STALE_DATA")
    if preview.duplicate_intent: failures.append("DUPLICATE_INTENT")
    if "INVALID_NUMERIC" not in failures and "INVALID_RANGE" not in failures:
        deviation = abs(preview.preview_price - preview.reference_price) / preview.reference_price
        if deviation > preview.price_tolerance_fraction: failures.append("PRICE_DEVIATION")
    return {"allowed": not failures, "failures": failures, "preview": asdict(preview), "action": "SIMULATE_ONLY" if not failures else "BLOCK"}
