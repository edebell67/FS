# epics/ep_058_strategy_intelligence_pg/hosted_directory/app/dashboard_api.py — Top10 dashboard endpoints.
#
# VERSION HISTORY
# v1.1.0 · 2026-09-26 · Adds an endpoint for every function that was client-side only on the page: scenarios, scenario_candidates,
#   ribbon, replay_frame, overlay_signals, leader_rotation, multi_split_rotation and server-side named portfolios.
# v1.0.0 · 2026-09-26 · Same paths and payloads as ep_057 top10_live_app.py so top10_5min_equity_curves.html can point at this service.
"""Read-only dashboard endpoints backed by PostgreSQL tradedb (settings.source_database_url); portfolios live in SQLite."""
from __future__ import annotations

import datetime as dt
import json
import os
import sqlite3
import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from . import dashboard_engine as eng
from . import dashboard_queries as q

NO_STORE = {"Cache-Control": "no-store"}
MAX_PORTFOLIO_MODELS = 10
SCENARIO_CATALOGUE = json.loads((Path(__file__).parent / "scenarios_catalogue.json").read_text(encoding="utf-8")) + [
    {"id": "touched_rank_one", "name": "Touched #1 Today", "badge": "Intraday Leaders"},
    {"id": "family_leaders", "name": "Best Performer by Family", "badge": "Cross-Family Leaders"},
    {"id": "top5_breakout", "name": "Top 5 · Breakout"}, {"id": "top5_breakout_r", "name": "Top 5 · Breakout R"},
    {"id": "top5_breakout_rev", "name": "Top 5 · Breakout Rev"}, {"id": "top5_breakout_r_rev", "name": "Top 5 · Breakout R Rev"},
    {"id": "top3_tp{N}_sl{M}", "name": "Top 3 by TP/SL pair (ids from /api/scenarios tp_sl_scenarios)"},
]


def _date(value):
    value = value or dt.date.today().isoformat()
    if not q.DATE_RE.fullmatch(value):
        raise HTTPException(400, "date must be YYYY-MM-DD")
    return value


async def _run(fn, *args):
    try:
        return JSONResponse(await run_in_threadpool(fn, *args), headers=NO_STORE)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=500, headers=NO_STORE)


class EngineRequest(BaseModel):
    """Everything the page holds as UI state, as explicit parameters."""
    date: str | None = None
    scenario: str = "top_net"
    models: str | None = Field(None, description="csv of model ids (a portfolio); overrides scenario")
    return_type: str = Field("NET", pattern="^(NET|ALT)$")
    product_type: str = "all"
    product: str = "all"
    strategy_family: str = "all"
    limit: int = 10
    min_win_rate: float = 0.0
    baseline_index: int | None = None
    baseline_time: str | None = Field(None, description="HH:MM; resolves baseline_index on the longest series")
    frame_index: int = Field(-1, description="replay head; -1 = end of series")
    exit_threshold: float = 0.0
    daily_target: float = 500.0
    model: str | None = Field(None, description="overlay_signals: which model (default: first eligible)")
    visible_models: str | None = Field(None, description="csv subset of models to include (model curve toggles)")


class PortfolioBody(BaseModel):
    models: list[str] = Field(default_factory=list, max_length=MAX_PORTFOLIO_MODELS)


class MergeBody(BaseModel):
    name: str
    sources: list[str]


class SimilarBody(BaseModel):
    name: str
    date: str | None = None
    model: str
    group: str


class PortfolioStore:
    """Named portfolios (max ten unique strategies each), SQLite-backed, per owner key."""

    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._path, self._lock = str(path), threading.Lock()
        with self._conn() as c:
            c.execute("CREATE TABLE IF NOT EXISTS portfolios(owner TEXT, name TEXT, models TEXT, PRIMARY KEY(owner,name))")

    def _conn(self):
        return sqlite3.connect(self._path)

    @staticmethod
    def _clean(models):
        out = list(dict.fromkeys(m.strip() for m in models if m and m.strip()))
        if len(out) > MAX_PORTFOLIO_MODELS:
            raise ValueError(f"a portfolio holds at most {MAX_PORTFOLIO_MODELS} strategies")
        return out

    @staticmethod
    def _get(c, owner, name):
        row = c.execute("SELECT models FROM portfolios WHERE owner=? AND name=?", (owner, name)).fetchone()
        return json.loads(row[0]) if row else None

    def put(self, owner, name, models):
        models = self._clean(models)
        with self._lock, self._conn() as c:
            c.execute("INSERT INTO portfolios VALUES(?,?,?) ON CONFLICT(owner,name) DO UPDATE SET models=excluded.models",
                      (owner, name, json.dumps(models)))
        return {"name": name, "models": models}

    def list(self, owner):
        with self._conn() as c:
            return {"portfolios": {n: json.loads(m) for n, m in c.execute("SELECT name, models FROM portfolios WHERE owner=?", (owner,))}}

    def add(self, owner, name, models):
        with self._conn() as c:
            cur = self._get(c, owner, name) or []
        return self.put(owner, name, cur + list(models))

    def remove(self, owner, name, model):
        with self._conn() as c:
            cur = self._get(c, owner, name)
        if cur is None:
            raise ValueError(f"no portfolio {name!r}")
        return self.put(owner, name, [m for m in cur if m != model])

    def delete(self, owner, name):
        with self._lock, self._conn() as c:
            c.execute("DELETE FROM portfolios WHERE owner=? AND name=?", (owner, name))
        return {"deleted": name}

    def merge(self, owner, name, sources):
        merged = []
        with self._conn() as c:
            for s in sources:
                got = self._get(c, owner, s)
                if got is None:
                    raise ValueError(f"no portfolio {s!r}")
                merged += got
        return self.put(owner, name, merged)


def _dataset_key(scenario: str, return_type: str) -> str:
    metric_aware = scenario == "family_leaders" or scenario.startswith("top5_") or scenario.startswith("top3_tp")
    return f"{scenario}_{'alt' if str(return_type).upper() == 'ALT' else 'net'}" if metric_aware else scenario


def resolve_models(req: EngineRequest) -> list[dict]:
    """The model set the page would show: explicit portfolio list, else the day's scenario, filtered like getEligibleModels."""
    date = _date(req.date)
    keys = eng.metric_keys(req.return_type)
    if req.models:
        data = q.build_portfolio_day(date, [m.strip() for m in req.models.split(",") if m.strip()])
        models = [m for m in data["models"]
                  if float(m.get(keys["winRateKey"]) or m.get("win_rate") or 0) >= req.min_win_rate]
        return sorted(models, key=lambda m: (-float(m.get(keys["cumNetKey"]) or 0), str(m["model"])))
    ptype, prod = q.normalize_product_type(req.product_type), q.normalize_product(req.product)
    fam = q.normalize_strategy_family(req.strategy_family)
    live = q.build_live_day(date, ptype, prod, fam, q.normalize_model_limit(req.limit))
    key = _dataset_key(req.scenario, req.return_type)
    if not isinstance(live.get(key), list):
        raise ValueError(f"unknown scenario {req.scenario!r}")
    return eng.scenario_candidates(live[key], return_type=req.return_type, min_win_rate=req.min_win_rate,
                                   product_type=ptype, product=prod, strategy_family=fam,
                                   dedicated_family_scenario=req.scenario.startswith("top5_"))


def _prepare(req: EngineRequest):
    models = resolve_models(req)
    if req.visible_models:
        vis = {m.strip() for m in req.visible_models.split(",")}
        models = [m for m in models if m["model"] in vis]
    return models, eng.resolve_baseline_index(models, req.baseline_index, req.baseline_time)


def _head(models, frame_index):
    longest = max((len(m["series"]) for m in models), default=1)
    return longest - 1 if frame_index < 0 else min(frame_index, longest - 1)


def install(app: FastAPI, source_database_url: str | None) -> None:
    if not source_database_url:
        return
    q.DSN = source_database_url
    store = PortfolioStore(Path(os.environ.get("EP058_PORTFOLIO_DB", "runtime/dashboard_portfolios.sqlite")))

    # --- query endpoints (identical paths/payloads to the ep_057 server) ---------------------
    @app.get("/api/live_day")
    async def live_day(date: str | None = None, product_type: str = "all", product: str = "all",
                       strategy_family: str = "all", limit: int = 10):
        return await _run(q.build_live_day, _date(date), q.normalize_product_type(product_type),
                          q.normalize_product(product), q.normalize_strategy_family(strategy_family),
                          q.normalize_model_limit(limit))

    @app.get("/api/hourly_family_report")
    async def hourly_family_report(date: str | None = None, product_type: str = "all",
                                   product: str = "all", family: str = "all"):
        return await _run(q.build_hourly_family_report, _date(date), q.normalize_product_type(product_type),
                          q.normalize_product(product), q.normalize_strategy_family(family))

    @app.get("/api/portfolio_day")
    async def portfolio_day(models: str = Query(..., min_length=1), date: str | None = None):
        return await _run(q.build_portfolio_day, _date(date), models.split(","))

    @app.get("/api/similar_strategies")
    async def similar_strategies(model: str = Query(..., min_length=1), date: str | None = None):
        return await _run(q.build_similar_strategies, _date(date), model)

    @app.get("/api/strategy_catalog")
    async def strategy_catalog(date: str | None = None):
        return await _run(q.build_strategy_catalog, _date(date))

    @app.get("/api/model_trades")
    async def model_trades(model: str = Query(..., min_length=1), date_from: str = Query(..., alias="from"),
                           date_to: str | None = Query(None, alias="to"), product_type: str = "all",
                           product: str = "all"):
        return await _run(q.build_model_trades, model, _date(date_from), _date(date_to or date_from),
                          q.normalize_product_type(product_type), q.normalize_product(product))

    # --- functions that were client-side only on the page ------------------------------------
    @app.get("/api/scenarios")
    async def scenarios(date: str | None = None, product_type: str = "all", product: str = "all",
                        strategy_family: str = "all", limit: int = 10):
        """SCENARIOS_CATALOGUE plus the day's dynamic scenario ids (top5_<family>, top3_tp<N>_sl<M>)."""
        def build():
            live = q.build_live_day(_date(date), q.normalize_product_type(product_type), q.normalize_product(product),
                                    q.normalize_strategy_family(strategy_family), q.normalize_model_limit(limit))
            return {"catalogue": SCENARIO_CATALOGUE, "tp_sl_scenarios": live["tp_sl_scenarios"],
                    "available_ids": sorted(k for k, v in live.items() if isinstance(v, list)),
                    "products": live["products"], "metric_aware": ["family_leaders", "top5_*", "top3_tp*"]}
        return await _run(build)

    @app.post("/api/scenario_candidates")
    async def scenario_candidates(req: EngineRequest):
        """getScenarioCandidates / getEligibleModels: the model list (with series) the page would display."""
        return await _run(lambda: {"models": resolve_models(req)})

    @app.post("/api/ribbon")
    async def ribbon(req: EngineRequest):
        """updateRibbon: summed and per-model delta net/buy/sell from baseline to replay head."""
        def build():
            models, b = _prepare(req)
            return eng.ribbon(models, return_type=req.return_type, baseline_index=b, frame_index=req.frame_index) | {"baseline_index": b}
        return await _run(build)

    @app.post("/api/replay_frame")
    async def replay_frame(req: EngineRequest):
        """Replay / baseline / scrubber: per-model base and head point plus frame count."""
        def build():
            models, b = _prepare(req)
            return {"baseline_index": b, "frame_index": req.frame_index,
                    "max_frames": max((len(m["series"]) for m in models), default=1),
                    "models": [{"model": m["model"], "base": eng.base_point(m["series"], b),
                                "head": eng.head_point(m["series"], req.frame_index)} for m in models]}
        return await _run(build)

    @app.post("/api/overlay_signals")
    async def overlay_signals(req: EngineRequest):
        """Tri-split B/S/X overlay for one model: signals, paired trades (with flip result), daily-target hit."""
        def build():
            models, b = _prepare(req)
            m = next((x for x in models if x["model"] == req.model), models[0] if models else None)
            if m is None:
                return {"model": None, "signals": [], "trades": [], "targetSignal": None}
            series = eng.mapped_series(m, req.return_type)
            head = len(series) - 1 if req.frame_index < 0 else min(req.frame_index, len(series) - 1)
            sub = series[min(b, head): head + 1]
            base = eng.base_point(series, b)
            sigs = eng.overlay_signals(sub, base, req.exit_threshold)
            trades = eng.pair_overlay_trades(sigs, sub, base)
            return {"model": m["model"], "baseline_index": b, "signals": sigs, "trades": trades,
                    "summary": {"count": len(trades), "wins": sum(1 for t in trades if t["pnl"] > 0),
                                "total": sum(t["pnl"] for t in trades),
                                "flip_total": sum(t.get("flipPnl") or 0 for t in trades)},
                    "targetSignal": eng.split_target_signal(sigs, sub, base, req.daily_target)}
        return await _run(build)

    @app.post("/api/leader_rotation")
    async def leader_rotation(req: EngineRequest):
        """Total Net leader rotation across the visible strategies (ALL_NET mode B/X signals)."""
        def build():
            models, b = _prepare(req)
            return eng.leader_rotation(models, eng.metric_keys(req.return_type)["netKey"], _head(models, req.frame_index),
                                       baseline_index=b, exit_threshold=req.exit_threshold,
                                       daily_target=req.daily_target) | {"baseline_index": b}
        return await _run(build)

    @app.post("/api/multi_split_rotation")
    async def multi_split_rotation(req: EngineRequest):
        """Multi-Split rotation across every visible strategy's Buy and Sell side."""
        def build():
            models, b = _prepare(req)
            return eng.multi_split_rotation(models, eng.metric_keys(req.return_type), _head(models, req.frame_index),
                                            baseline_index=b, exit_threshold=req.exit_threshold,
                                            daily_target=req.daily_target) | {"baseline_index": b}
        return await _run(build)

    # --- named portfolios (localStorage on the page; server-side here) -----------------------
    @app.get("/api/portfolios")
    async def portfolios_list(owner: str = "default"):
        return await _run(store.list, owner)

    @app.put("/api/portfolios/{name}")
    async def portfolios_put(name: str, body: PortfolioBody, owner: str = "default"):
        return await _run(store.put, owner, name, body.models)

    @app.delete("/api/portfolios/{name}")
    async def portfolios_delete(name: str, owner: str = "default"):
        return await _run(store.delete, owner, name)

    @app.post("/api/portfolios/{name}/models")
    async def portfolios_add(name: str, body: PortfolioBody, owner: str = "default"):
        return await _run(store.add, owner, name, body.models)

    @app.delete("/api/portfolios/{name}/models/{model}")
    async def portfolios_remove(name: str, model: str, owner: str = "default"):
        return await _run(store.remove, owner, name, model)

    @app.post("/api/portfolio_merge")
    async def portfolios_merge(body: MergeBody, owner: str = "default"):
        return await _run(store.merge, owner, body.name, body.sources)

    @app.post("/api/portfolio_from_similar")
    async def portfolios_from_similar(body: SimilarBody, owner: str = "default"):
        """createSimilarPortfolio: portfolio from a same-product comparison group of a model."""
        def build():
            sim = q.build_similar_strategies(_date(body.date), body.model)
            groups = {k: v for k, v in sim.items() if isinstance(v, list)}
            if body.group not in groups:
                raise ValueError(f"unknown comparison group {body.group!r}; available: {sorted(groups)}")
            return store.put(owner, body.name, [g["model"] if isinstance(g, dict) else g for g in groups[body.group]])
        return await _run(build)


CATALOGUE = {
    "enabled_when": "SOURCE_DATABASE_URL is set",
    "endpoints": {
        "GET /api/live_day": "date, product_type(all|forex|crypto), product, strategy_family, limit(10|20|30) -> every scenario's model list with 5-min curves",
        "GET /api/portfolio_day": "date, models=csv (max 10) -> 5-min curves for a named portfolio",
        "GET /api/similar_strategies": "date, model -> same-product comparisons by family, window, TP, SL",
        "GET /api/strategy_catalog": "date -> active models with parsed family/window/tp/sl",
        "GET /api/model_trades": "model, from, to, product_type, product -> closed+open trades with summary",
        "GET /api/hourly_family_report": "date, product_type, product, family -> hourly exits by family and side",
        "GET /api/scenarios": "scenario catalogue + the day's dynamic ids (top5_*, top3_tp*_sl*)",
        "POST /api/scenario_candidates": "EngineRequest -> getScenarioCandidates/getEligibleModels (win-rate, product, family filters)",
        "POST /api/ribbon": "EngineRequest -> summed/per-model delta net/buy/sell baseline->head",
        "POST /api/replay_frame": "EngineRequest -> base/head points per model, max_frames (replay, baseline, scrubber)",
        "POST /api/overlay_signals": "EngineRequest(model) -> tri-split B/S/X signals, paired trades, flip result, daily-target hit",
        "POST /api/leader_rotation": "EngineRequest -> Total Net leader rotation signals/trades/target",
        "POST /api/multi_split_rotation": "EngineRequest -> Multi-Split buy/sell rotation signals/trades/target",
        "GET|PUT|DELETE /api/portfolios[/{name}]": "named portfolios (max 10 strategies), plus POST /{name}/models, DELETE /{name}/models/{model}",
        "POST /api/portfolio_merge": "{name, sources[]} -> de-duplicated merge",
        "POST /api/portfolio_from_similar": "{name, date, model, group} -> portfolio from a comparison group",
    },
    "engine_request_fields": list(EngineRequest.model_fields),
    "ui_only": ["theme", "collapse/expand sections", "chart drawing/tooltips", "trades-modal column sorting", "scrubber speed"],
}
