"""Pure validation and attribution policy for public waitlist registrations."""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
MAX_SOURCE_LENGTH = 80
MAX_DETAIL_LENGTH = 500
MAX_PATH_LENGTH = 240


class ValidationError(ValueError):
    """The public registration payload cannot be accepted."""


@dataclass(frozen=True)
class Registration:
    email: str
    discovery_source: str
    source_detail: str | None
    utm_source: str | None
    utm_medium: str | None
    utm_campaign: str | None
    utm_content: str | None
    landing_path: str | None
    referrer: str | None


def _text(value: Any, limit: int) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return text[:limit]


def normalize_registration(payload: dict[str, Any]) -> Registration:
    if _text(payload.get("company"), MAX_DETAIL_LENGTH):
        raise ValidationError("submission rejected")
    if payload.get("consent") is not True:
        raise ValidationError("email consent is required")

    email = _text(payload.get("email"), 254)
    if not email or not EMAIL_RE.fullmatch(email):
        raise ValidationError("valid email is required")

    discovery_source = _text(payload.get("discoverySource"), MAX_SOURCE_LENGTH)
    if not discovery_source:
        raise ValidationError("lead source is required")

    return Registration(
        email=email.lower(),
        discovery_source=discovery_source.lower(),
        source_detail=_text(payload.get("sourceDetail"), MAX_DETAIL_LENGTH),
        utm_source=_text(payload.get("utmSource"), MAX_SOURCE_LENGTH),
        utm_medium=_text(payload.get("utmMedium"), MAX_SOURCE_LENGTH),
        utm_campaign=_text(payload.get("utmCampaign"), MAX_SOURCE_LENGTH),
        utm_content=_text(payload.get("utmContent"), MAX_SOURCE_LENGTH),
        landing_path=_text(payload.get("landingPath"), MAX_PATH_LENGTH),
        referrer=_text(payload.get("referrer"), MAX_PATH_LENGTH),
    )
