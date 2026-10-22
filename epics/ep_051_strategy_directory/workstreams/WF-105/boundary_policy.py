# workstreams/WF-105/boundary_policy.py — Enforces the Non-DNA research/public separation contract.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: validates lineage envelopes and denies Non-DNA use in public surfaces.

from __future__ import annotations

PUBLIC_SURFACES = {"strategy_directory", "strategy_detail", "portfolio_search", "public_api", "public_cache"}
NON_DNA_DOMAIN = "NON_DNA_RESEARCH"


def authorize_domain(surface: str, data_domain: str, *, role: str) -> bool:
    if data_domain == NON_DNA_DOMAIN:
        return surface not in PUBLIC_SURFACES and role in {"researcher", "research_service", "auditor"}
    return data_domain == "DNA_DIRECTORY"


def validate_research_envelope(payload: dict[str, object]) -> None:
    required = {
        "data_domain": NON_DNA_DOMAIN,
        "research_only": True,
        "warning": "Not DNA strategy performance.",
    }
    for field, expected in required.items():
        if payload.get(field) != expected:
            raise ValueError(f"invalid or missing research lineage field: {field}")
    for field in ("source_window", "methodology_version", "generated_at"):
        if not payload.get(field):
            raise ValueError(f"missing research lineage field: {field}")

