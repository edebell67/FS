# epics/ep_057_sql_to_pgsql/scenario_engine_v2/runner/arena_provider.py — EP052 arena intelligence provider: POST /v1/queries (the arena's QueryRequest -> QueryDelivery contract) answered with real strategy intelligence.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version: kinds top_performers / correlated_groups / spread_candidates, bearer token + agent header, exact-retry idempotency, request-id conflict, strict contract echo.
"""The arena posts its QueryRequest to `intelligence_url` and validates the QueryDelivery strictly (same ids, echoed query, <= limit unique strategy ids, subset of the requested ids). This provider
returns the ranked strategy ids in `strategy_ids` and the evidence (z-scores, correlations, as-of time, caveats) in `notice`; the full structured report is at /api/intelligence/report.
The service token comes from EP057_INTELLIGENCE_TOKEN (>= 32 characters); without it the endpoint is disabled (503)."""
from __future__ import annotations

import hmac
import json
import os
import re
import threading
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from .intel import build_report

KINDS = ("top_performers", "correlated_groups", "spread_candidates")
STRATEGY_ID = re.compile(r"(?i)^DNA_[0-9_]+$")


def _ids_for(kind: str, report: dict, limit: int, allowed: set | None) -> tuple[list[str], str]:
    def ok(i):
        return bool(STRATEGY_ID.match(i)) and (not allowed or i in allowed)
    if kind == "top_performers":
        ids = [r["model"] for r in report["top"]]
        note = "; ".join(f"#{r['rank']} {r['model']} net {r['net']:.0f}, momentum {r['momentum']:.0f}, max drawdown {r['max_drawdown']:.0f}" for r in report["top"])
    elif kind == "correlated_groups":
        ids, note_parts = [], []
        for g in report["clusters"]:
            ids += g["members"]
            note_parts.append(f"{'/'.join(g['members'])} avg corr {g['avg_correlation']}")
        note = "; ".join(note_parts) or "no correlated group at the threshold"
    else:
        ids, note_parts = [], []
        for s in report["spread_signals"]:
            ids += s["pair"]
            note_parts.append(f"{s['pair'][0]}/{s['pair'][1]} z {s['z']} {s['state']} (half-life {s['half_life_points']} pts, leader {s['leader']})")
        note = "; ".join(note_parts) or "no stretched spread"
    seen, out = set(), []
    for i in ids:
        if ok(i) and i not in seen:
            seen.add(i)
            out.append(i)
    return out[:limit], note


def create_router(factory, token: str | None = None) -> APIRouter:
    router = APIRouter()
    deliveries: dict[tuple, tuple[str, dict]] = {}
    lock = threading.Lock()

    @router.post("/v1/queries")
    async def queries(request: Request, authorization: str = Header(default=""), x_ep052_agent_id: str | None = Header(default=None)):
        secret = token or os.environ.get("EP057_INTELLIGENCE_TOKEN")
        if not secret or len(secret) < 32:
            raise HTTPException(503, "provider not configured")
        if not hmac.compare_digest(authorization.encode(), ("Bearer " + secret).encode()):
            raise HTTPException(401, "invalid service credential")
        if not x_ep052_agent_id:
            raise HTTPException(422, "agent identity required")
        body = await request.json()
        try:
            rid, revision, kind, limit = str(uuid.UUID(str(body["request_id"]))), int(body.get("revision", 0)), str(body["kind"]), int(body.get("limit", 5))
        except (KeyError, ValueError, TypeError) as e:
            raise HTTPException(422, f"bad query: {type(e).__name__}") from e
        if kind not in KINDS or limit < 1 or limit > 50:
            raise HTTPException(422, f"kind must be one of {KINDS}; limit 1..50")
        identity = (x_ep052_agent_id, rid, revision)
        fp = json.dumps(body, sort_keys=True)
        with lock:
            if identity in deliveries:
                old_fp, old = deliveries[identity]
                if old_fp != fp:
                    raise HTTPException(409, "REQUEST_ID_CONFLICT")
                return JSONResponse(old)
        end = body.get("window_end")
        day = (datetime.fromisoformat(end.replace("Z", "+00:00")) if end else datetime.now(timezone.utc))
        spec = {"date": day.strftime("%Y-%m-%d"), "models": [s for s in body.get("strategy_ids") or []], "scenario": "top_net", "top_n": min(limit, 10), "limit": 50}
        if end:
            spec["as_of_time"] = day.strftime("%H:%M")   # nothing after the window end is used
        try:
            report = build_report(factory, spec)
        except Exception as e:  # noqa: BLE001
            raise HTTPException(503, f"intelligence unavailable: {type(e).__name__}") from e
        allowed = {s for s in body.get("strategy_ids") or []} or None
        ids, note = _ids_for(kind, report, limit, allowed)
        out = {"delivery_id": str(uuid.uuid4()), "request_id": rid, "revision": revision, "result_version": str(uuid.uuid4()), "created_at": datetime.now(timezone.utc).isoformat(),
               "source_version": f"ep057-intel-v1:{report['as_of'] or 'n/a'}", "mode": "external", "strategy_ids": ids, "query": body,
               "notice": f"{kind} as of {report['as_of']} ({report['confidence']} confidence, {report['sample_points']} points): {note}. " + " ".join(report["caveats"])}
        with lock:
            deliveries[identity] = (fp, out)
        return JSONResponse(out)

    return router
