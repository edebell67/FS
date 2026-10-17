# epics/ep_057_sql_to_pgsql/scenario_engine_v2/runner/server.py — HTTP service for the virtual race runner (port 8766): launch races, watch them, change the parallel cap, serve the dashboard.
#
# VERSION HISTORY
# v1.3.0 · 2026-10-17 · /api/intelligence/report, watches and events (proactive intelligence for agents).
# v1.2.0 · 2026-10-17 · add_scenario_top.
# v1.1.0 · 2026-10-17 · POST /engine/call, /engine/client.js, the engine-client page route and a same-origin proxy to the data service (/api/*, static assets).
# v1.0.0 · 2026-10-17 · Initial version: /api/races (POST / GET / GET id / DELETE id), /api/config (GET / PUT), /healthz, /dashboard; CORS for the scenario page; virtual only.
"""Run: python -m runner.server   (EP057_RUNNER_PORT, EP057_MAX_RACES, EP057_DATA_API). Races are read-only and virtual: the service has no write transport and refuses live portfolios."""
from __future__ import annotations

import json
import math
import os
import subprocess
import time
from dataclasses import fields
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from engine import rpc

from .intel import WatchRegistry, build_report, default_factory
from .manager import DEFAULT_MAX_CONCURRENT, HARD_LIMIT, RaceManager
from .race import RaceConfig

HERE = Path(__file__).resolve().parent
ENGINE_ROOT = HERE.parent
DATA_API = os.environ.get("EP057_DATA_API", "http://127.0.0.1:8765")
PAGE_ORIGINS = ["http://127.0.0.1:8765", "http://localhost:8765"]


class RaceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field("race", max_length=80)
    start_model: str | None = Field(None, max_length=80)
    add_models: list[str] = Field(default_factory=list, max_length=19)
    add_scenario_top: int = Field(0, ge=0, le=19)
    scenario: str = Field("top_net", max_length=80)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    product_type: str = "all"
    product: str = "all"
    strategy_family: str = "all"
    return_type: str = Field("NET", pattern="^(NET|ALT)$")
    limit: int = Field(10, ge=1, le=50)
    split_mode: str = Field("ALL_NET", pattern="^(ALL_NET|BUY_NET|SELL_NET|TRI_SPLIT|MULTI_SPLIT)$")
    baseline_index: int = Field(0, ge=0)
    exit_threshold: float = 0.0
    daily_target: float = 500.0
    hold_rank: int = Field(1, ge=1, le=5)
    overlay_rule_id: str | None = Field(None, max_length=120)
    max_frames: int | None = Field(None, ge=1)

    def to_config(self) -> RaceConfig:
        data = self.model_dump()
        data["add_models"] = tuple(data["add_models"])
        data["api_base"] = DATA_API
        return RaceConfig(**{k: v for k, v in data.items() if k in {f.name for f in fields(RaceConfig)}})


class ConfigRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    max_concurrent: int = Field(..., ge=1, le=HARD_LIMIT)


def build_sha() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=HERE, capture_output=True, text=True, timeout=5).stdout.strip() or "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


def _clean(value):
    """JSON has no NaN / Infinity: they become null (what JSON.stringify does in the page)."""
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if isinstance(value, dict):
        return {k: _clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_clean(v) for v in value]
    return value


HOP = {"connection", "keep-alive", "transfer-encoding", "content-encoding", "content-length", "host", "upgrade", "te", "trailer", "proxy-authorization"}


def thin_page_path() -> Path | None:
    built = sorted(ENGINE_ROOT.glob("top10_5min_equity_curves_engine_client_v*.html"))
    return built[-1] if built else None


class IntelRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    models: list[str] = Field(default_factory=list, max_length=20)
    scenario: str = Field("top_net", max_length=80)
    return_type: str = Field("NET", pattern="^(NET|ALT)$")
    limit: int = Field(10, ge=1, le=50)
    as_of_time: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")
    top_n: int = Field(3, ge=1, le=10)
    window: int = Field(48, ge=8, le=500)
    corr_threshold: float = Field(0.7, ge=0, le=1)
    z_hi: float = Field(1.5, ge=0.5, le=6)


class WatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    agent: str = Field(..., min_length=1, max_length=80)
    spec: IntelRequest
    top_change: bool = True
    spread_z: float | None = Field(2.0, ge=0.5, le=6)


def create_app(manager: RaceManager | None = None, data_api: str | None = None, client_factory=None, watches: WatchRegistry | None = None) -> FastAPI:
    mgr = manager or RaceManager()
    upstream = (data_api or DATA_API).rstrip("/")
    factory = client_factory or default_factory(upstream)
    registry = watches or WatchRegistry(factory)
    app = FastAPI(title="EP057 virtual race runner", version="1.1.0")
    app.add_middleware(CORSMiddleware, allow_origins=PAGE_ORIGINS + ["http://127.0.0.1:8766", "http://localhost:8766"], allow_methods=["GET", "POST", "PUT", "DELETE"],
                       allow_headers=["Content-Type"])
    started = time.time()
    sha = build_sha()

    @app.get("/healthz")
    def healthz():
        return {"ok": True, "build_sha": sha, "uptime_s": round(time.time() - started, 1), "mode": "virtual_only", **mgr.counts()}

    @app.get("/api/config")
    def get_config():
        return {"max_concurrent": mgr.max_concurrent, "default_max_concurrent": DEFAULT_MAX_CONCURRENT, "hard_limit": HARD_LIMIT, "data_api": DATA_API}

    @app.put("/api/config")
    def put_config(req: ConfigRequest):
        return {"max_concurrent": mgr.set_max_concurrent(req.max_concurrent)}

    @app.post("/api/races", status_code=201)
    def start_race(req: RaceRequest):
        try:
            race = mgr.submit(req.to_config())
        except Exception as e:  # noqa: BLE001 - validation / live refusal
            raise HTTPException(422, f"{type(e).__name__}: {e}") from e
        return race.summary()

    @app.post("/api/intelligence/report")
    def intelligence_report(req: IntelRequest):
        try:
            return build_report(factory, req.model_dump())
        except Exception as e:  # noqa: BLE001
            raise HTTPException(502, f"{type(e).__name__}: {e}") from e

    @app.post("/api/intelligence/watches", status_code=201)
    def add_watch(req: WatchRequest):
        try:
            return registry.add(req.agent, req.spec.model_dump(), {"top_change": req.top_change, "spread_z": req.spread_z})
        except ValueError as e:
            raise HTTPException(422, str(e)) from e

    @app.delete("/api/intelligence/watches/{watch_id}")
    def delete_watch(watch_id: str):
        if not registry.remove(watch_id):
            raise HTTPException(404, "watch not found")
        return {"removed": True}

    @app.post("/api/intelligence/watches/{watch_id}/evaluate")
    def evaluate_watch(watch_id: str):
        if watch_id not in registry.watches:
            raise HTTPException(404, "watch not found")
        return {"new_events": len(registry.evaluate(watch_id))}

    @app.get("/api/intelligence/events")
    def pull_events(agent: str, clear: bool = True):
        return {"agent": agent, "events": registry.pull(agent, clear)}

    @app.get("/api/races")
    def list_races():
        return {"counts": mgr.counts(), "races": mgr.list()}

    @app.get("/api/races/{race_id}")
    def get_race(race_id: str):
        race = mgr.get(race_id)
        if race is None:
            raise HTTPException(404, "race not found")
        out = race.summary()
        if race.result is not None:
            out["standings"] = race.result["final"]["standings"]
            out["lead_changes"] = race.result["final"]["lead_changes"]
            out["rotation_net"] = race.result["final"]["rotation_net"]
        return out

    @app.get("/api/races/{race_id}/result")
    def get_result(race_id: str):
        race = mgr.get(race_id)
        if race is None:
            raise HTTPException(404, "race not found")
        if race.result is None:
            return JSONResponse({"state": race.progress.state, "result": None}, status_code=202)
        return race.result

    @app.delete("/api/races/{race_id}")
    def cancel_race(race_id: str):
        if mgr.get(race_id) is None:
            raise HTTPException(404, "race not found")
        return {"cancelled": mgr.cancel(race_id)}

    @app.get("/")
    @app.get("/dashboard")
    def dashboard():
        return FileResponse(HERE / "static" / "dashboard.html", media_type="text/html")

    # ---- the engine contract for the browser copy of the scenario page (engine/rpc.py) ----
    @app.post("/engine/call")
    async def engine_call(request: Request):
        try:
            req = await request.json()
            if not isinstance(req, dict):
                raise rpc.RpcError("request must be a JSON object")
            return JSONResponse(_clean(rpc.dispatch(req)))
        except rpc.RpcError as e:
            raise HTTPException(422, str(e)) from e
        except (KeyError, IndexError, TypeError, ValueError) as e:
            raise HTTPException(422, f"bad request: {type(e).__name__}: {e}") from e

    @app.get("/engine/client.js")
    def engine_client_js():
        return FileResponse(HERE / "static" / "engine_client.js", media_type="application/javascript")

    @app.get("/top10_5min_equity_curves_engine_client.html")
    def thin_page():
        path = thin_page_path()
        if path is None:
            raise HTTPException(404, "no engine-client page has been built (python tools/build_thin_page.py)")
        return FileResponse(path, media_type="text/html", headers={"Cache-Control": "no-store"})

    # ---- same-origin access to the data service (it only allows the 'null' origin for CORS) ----
    async def forward(request: Request, path: str) -> Response:
        target = f"{upstream}/{path}"
        headers = {k: v for k, v in request.headers.items() if k.lower() not in HOP}
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                r = await client.request(request.method, target, params=request.query_params, content=await request.body(), headers=headers)
        except httpx.HTTPError as e:
            raise HTTPException(502, f"data service unavailable: {type(e).__name__}") from e
        return Response(content=r.content, status_code=r.status_code, headers={k: v for k, v in r.headers.items() if k.lower() not in HOP})

    @app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], include_in_schema=False)
    async def proxy_api(request: Request, path: str):
        return await forward(request, f"api/{path}")

    @app.get("/{path:path}", include_in_schema=False)
    async def proxy_static(request: Request, path: str):
        return await forward(request, path)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("EP057_RUNNER_PORT", "8766")))
