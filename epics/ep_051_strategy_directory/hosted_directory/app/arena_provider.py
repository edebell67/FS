"""EP052 Lean Exchange intelligence provider - the real implementation of the
contract ep_052's IntelligenceClient/simulated_intelligence.py already define
and validate against (GET /v1/contracts/intelligence on the arena). Replaces
simulated_intelligence.py's random selection with actual ranked queries
against this directory's own StrategyQuery/basis_profiles engine, gated by
the same Authorization: Bearer <service token> + X-EP052-Agent-ID header
pair the arena's client already sends - the arena's own owner/agent/
connection model is the identity system; this only verifies the arena
itself is a trusted caller and logs which of its agents triggered each query.

VERSION HISTORY
v1.0.0 - Initial real provider: kind-dispatched ranking, durable idempotent
deliveries (mirrors simulated_intelligence.py's SQLite receipt table so a
retried request_id/revision replays the same result instead of re-billing).
"""
from __future__ import annotations
from contextlib import closing
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Literal
from uuid import UUID, uuid4
import hmac, json, sqlite3

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field, model_validator

StrategyId = Field(pattern=r"^DNA_[0-9]+$")

# Recognized `kind` values and which profile metric they rank by. `kind` is
# free text in the contract (no enum enforced) - an unrecognized value falls
# back to quality_score rather than erroring, same tolerant spirit as the
# simulated provider ignoring kind entirely, but ours actually uses it when
# it understands it and says so either way in `notice`.
KIND_METRICS = {
    "top_performers": ("metrics", "total_return"),
    "best_return": ("metrics", "total_return"),
    "net_return": ("metrics", "total_return"),
    "high_win_rate": ("metrics", "win_rate"),
    "win_rate": ("metrics", "win_rate"),
    "low_drawdown": ("metrics", "max_drawdown"),
    "safe": ("metrics", "max_drawdown"),
    "quality": ("score", "quality_score"),
    "quality_score": ("score", "quality_score"),
}
DEFAULT_KIND = "quality"


class ArenaQueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: UUID
    revision: int = Field(default=0, ge=0)
    kind: str = Field(min_length=1, max_length=128)
    strategy_ids: list[str] = Field(default_factory=list, max_length=1000)
    window_start: datetime | None = None
    window_end: datetime | None = None
    limit: int = Field(default=5, gt=0)

    @model_validator(mode="after")
    def valid_window(self):
        for value in (self.window_start, self.window_end):
            if value is not None and value.tzinfo is None:
                raise ValueError("Query timestamps require timezone")
        if self.window_start and self.window_end and self.window_start > self.window_end:
            raise ValueError("Query start must not follow end")
        return self


class ArenaQueryDelivery(BaseModel):
    model_config = ConfigDict(extra="forbid")
    delivery_id: UUID
    request_id: UUID
    revision: int = Field(ge=0)
    result_version: UUID
    created_at: datetime
    source_version: str
    mode: Literal["simulated_random", "external"]
    strategy_ids: list[str]
    query: ArenaQueryRequest
    notice: str


def _fingerprint(request: ArenaQueryRequest) -> str:
    return sha256(json.dumps(request.model_dump(mode="json"), sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _metric_value(profile: dict, path: tuple[str, str]) -> float | None:
    section, key = path
    if section == "score":
        return profile.get("score", {}).get(key)
    return profile.get("metrics", {}).get(key, {}).get("value")


def select_strategies(request: ArenaQueryRequest, universe_fn, cfg) -> tuple[list[str], str]:
    """Resolve one ArenaQueryRequest against the real directory: builds the
    candidate pool for [window_start, window_end) via basis_profiles (or the
    full since-inception pool when no window is given), ranks by whatever
    `kind` maps to, restricts to request.strategy_ids when given, and caps
    at request.limit. Returns (strategy_ids, notice)."""
    metric_path = KIND_METRICS.get(request.kind.lower())
    fallback = metric_path is None
    if fallback:
        metric_path = KIND_METRICS[DEFAULT_KIND]
    profiles = universe_fn(request.window_start, request.window_end)
    if profiles is None:
        raise HTTPException(503, "EXTERNAL_PROVIDER_UNAVAILABLE")
    if request.strategy_ids:
        requested = set(request.strategy_ids)
        profiles = [p for p in profiles if p["identity"]["strategy_id"] in requested]
    reverse = metric_path[1] != "max_drawdown"  # drawdown: closer to zero (less negative) is better -> descending still correct since values are <=0
    ranked = sorted(profiles, key=lambda p: (_metric_value(p, metric_path) if _metric_value(p, metric_path) is not None else float("-inf")), reverse=reverse)
    selected = [p["identity"]["strategy_id"] for p in ranked[:request.limit]]
    window_note = f" within [{request.window_start.isoformat() if request.window_start else 'inception'}, {request.window_end.isoformat() if request.window_end else 'now'})"
    if fallback:
        notice = f"kind '{request.kind}' is not a recognized ranking; ranked by quality_score{window_note} instead. Recognized kinds: {sorted(KIND_METRICS)}."
    else:
        notice = f"Ranked by {'/'.join(metric_path)}{window_note}, {len(profiles)} strategies eligible, {len(selected)} returned."
    return selected, notice


def install(app: FastAPI, cfg, universe_fn):
    """Mount POST /v1/queries and GET /v1/deliveries/{id} on `app`, matching
    ep_052's IntelligenceClient contract exactly. `universe_fn(start,end)`
    must return a list of profile dicts (or None if unavailable) bounded to
    that window - the caller supplies this so this module stays independent
    of main.py's specific profile-cache plumbing."""
    db_path = Path(cfg.arena_deliveries_path)
    db_path = db_path if db_path.is_absolute() else Path(__file__).resolve().parents[1] / db_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(db_path)) as db:
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("""CREATE TABLE IF NOT EXISTS deliveries (
            delivery_id TEXT PRIMARY KEY, agent_id TEXT NOT NULL, request_id TEXT NOT NULL,
            revision INTEGER NOT NULL, fingerprint TEXT NOT NULL, payload TEXT NOT NULL,
            UNIQUE(agent_id,request_id,revision))""")
        db.commit()

    def arena_actor(authorization: str = Header(default=""), x_ep052_agent_id: UUID | None = Header(default=None)) -> str:
        token = cfg.ep052_intelligence_token
        if not token:
            raise HTTPException(503, "EP052 intelligence provider is not configured")
        if not hmac.compare_digest(authorization.encode(), ("Bearer " + token).encode()):
            raise HTTPException(401, "Invalid service credential")
        if x_ep052_agent_id is None:
            raise HTTPException(422, "Trusted caller must supply its authenticated agent identity")
        return str(x_ep052_agent_id)

    @app.post("/v1/queries", response_model=ArenaQueryDelivery)
    def arena_query(request: ArenaQueryRequest, agent_id: str = Depends(arena_actor)):
        if request.limit > cfg.intelligence_max_query_results:
            raise HTTPException(422, "Configured query result limit exceeded")
        identity = (agent_id, str(request.request_id), request.revision)
        request_hash = _fingerprint(request)

        def existing(db):
            row = db.execute("SELECT fingerprint,payload FROM deliveries WHERE agent_id=? AND request_id=? AND revision=?", identity).fetchone()
            if row:
                if row[0] != request_hash:
                    raise HTTPException(409, "REQUEST_ID_CONFLICT")
                return ArenaQueryDelivery.model_validate_json(row[1])
            return None

        with closing(sqlite3.connect(db_path)) as db:
            recovered = existing(db)
            if recovered:
                return recovered

        selected, notice = select_strategies(request, universe_fn, cfg)
        result = ArenaQueryDelivery(delivery_id=uuid4(), request_id=request.request_id, revision=request.revision,
                                     result_version=uuid4(), created_at=datetime.now(timezone.utc),
                                     source_version="dna-strategy-directory-1.0.0", mode="external",
                                     strategy_ids=selected, query=request, notice=notice)
        with closing(sqlite3.connect(db_path, timeout=15)) as db:
            try:
                db.execute("BEGIN IMMEDIATE")
                recovered = existing(db)
                if recovered:
                    return recovered
                db.execute("INSERT INTO deliveries VALUES (?,?,?,?,?,?)",
                           (str(result.delivery_id), *identity, request_hash, result.model_dump_json()))
                db.commit()
            finally:
                if db.in_transaction:
                    db.rollback()
        return result

    @app.get("/v1/deliveries/{delivery_id}", response_model=ArenaQueryDelivery)
    def arena_recover(delivery_id: UUID, agent_id: str = Depends(arena_actor)):
        with closing(sqlite3.connect(db_path)) as db:
            row = db.execute("SELECT payload FROM deliveries WHERE delivery_id=? AND agent_id=?",
                              (str(delivery_id), agent_id)).fetchone()
        if not row:
            raise HTTPException(404, "Delivery not found")
        return ArenaQueryDelivery.model_validate_json(row[0])
