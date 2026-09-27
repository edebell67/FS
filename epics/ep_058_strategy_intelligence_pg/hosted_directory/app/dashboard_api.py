# epics/ep_058_strategy_intelligence_pg/hosted_directory/app/dashboard_api.py — Top10 dashboard endpoints.
#
# VERSION HISTORY
# v1.4.0 · 2026-09-27 · Adds GET /api/point_in_time_scenario_hours (cohort at every completed clock-hour, for the page's hourly-cohort history list).
# v1.3.0 · 2026-09-27 · Adds GET /api/point_in_time_scenario (as-of replay selection) and interval_minutes on hourly_family_report, matching ep_057's point-in-time / hourly-column-panel additions.
# v1.2.0 · 2026-09-27 · Typed OpenAPI responses, parameter docs/enums, GET /api/coverage; fixes portfolio_from_similar (groups are nested, keyed by dimension).
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
from . import dashboard_models as m
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

DATE_DOC = "Trading date YYYY-MM-DD (server local date; defaults to today). Data exists only for dates listed by GET /api/coverage."
PT_DOC = {"description": "Product type filter", "json_schema_extra": {"enum": ["all", "forex", "crypto"]}}
FAM_DOC = {"description": "Strategy family filter", "json_schema_extra": {"enum": ["all", "breakout", "breakout_r", "breakout_rev", "breakout_r_rev"]}}
LIMIT_DOC = {"description": "Models per scenario", "json_schema_extra": {"enum": [10, 20, 30]}}


def _ok(model):
    return {200: {"model": model}}


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
    scenario: str = Field("top_net", description="Scenario id from GET /api/scenarios (top_net, top_alt_net, top_win, touched_rank_one, family_leaders, top5_<family>, top3_tp<N>_sl<M>, ...); metric-aware ids are resolved to _net/_alt from return_type")
    models: str | None = Field(None, description="csv of model ids (a portfolio); overrides scenario")
    return_type: str = Field("NET", pattern="^(NET|ALT)$", description="NET = actual net_return; ALT = counterfactual reversed trades")
    product_type: str = Field("all", description="all | forex | crypto")
    product: str = Field("all", description="Product code, e.g. gbp, eth")
    strategy_family: str = Field("all", description="all | breakout | breakout_r | breakout_rev | breakout_r_rev")
    limit: int = Field(10, description="10, 20 or 30 models per scenario")
    min_win_rate: float = Field(0.0, description="Percent 0-100 (the page's win-rate slider)")
    baseline_index: int | None = Field(None, description="Frame index of the baseline; 0 or null = session start (zero at 00:00)")
    baseline_time: str | None = Field(None, description="HH:MM; resolves baseline_index on the longest series")
    frame_index: int = Field(-1, description="replay head; -1 = end of series")
    exit_threshold: float = Field(0.0, description="USD; overlay exits when a side's delta falls below this (e.g. -50)")
    daily_target: float = Field(500.0, description="USD; first point where overlay P&L reaches it is flagged type T; 0 disables")
    model: str | None = Field(None, description="overlay_signals: which model (default: first eligible)")
    visible_models: str | None = Field(None, description="csv subset of models to include (model curve toggles)")


class PortfolioBody(BaseModel):
    models: list[str] = Field(default_factory=list, max_length=MAX_PORTFOLIO_MODELS)


class MergeBody(BaseModel):
    name: str
    sources: list[str]


class SimilarBody(BaseModel):
    name: str | None = Field(None, description="Portfolio name; auto-named like the page if omitted")
    date: str | None = None
    model: str
    dimension: str = Field(description="family | window | tp | sl")


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
    @app.get("/api/live_day", response_model=None, responses=_ok(m.LiveDayResponse), summary="All scenarios for a day",
             description="Every scenario's model list (top_net, top_alt_net, top_win, touched_rank_one, family_leaders_*, top5_<family>_*, top3_tp<N>_sl<M>_*, ...) with 5-minute cumulative curves. Payload is large (MBs); scenario ids are extra keys - list them via GET /api/scenarios. Money is USD; *_alt_* is the counterfactual reversed trade.")
    async def live_day(date: str | None = Query(None, description=DATE_DOC), product_type: str = Query("all", **PT_DOC),
                       product: str = Query("all", description="Product code within the type, e.g. gbp, eth; must exist for the type"),
                       strategy_family: str = Query("all", **FAM_DOC), limit: int = Query(10, **LIMIT_DOC)):
        return await _run(q.build_live_day, _date(date), q.normalize_product_type(product_type),
                          q.normalize_product(product), q.normalize_strategy_family(strategy_family),
                          q.normalize_model_limit(limit))

    @app.get("/api/hourly_family_report", response_model=None, responses=_ok(m.HourlyFamilyReportResponse), summary="Time-bucketed entries/exits by side",
             description="Per bucket and side: trades opened, open at bucket end, closed, win counts, totals (USD). For today's current bucket the row is partial (is_incomplete_hour). Bucket size is interval_minutes (10, 30, 60, or 180); exit_hour is the bucket start HH:MM.")
    async def hourly_family_report(date: str | None = Query(None, description=DATE_DOC), product_type: str = Query("all", **PT_DOC),
                                   product: str = Query("all", description="Product code"), family: str = Query("all", **FAM_DOC),
                                   interval_minutes: int = Query(60, description="Bucket size in minutes", json_schema_extra={"enum": [10, 30, 60, 180]})):
        return await _run(q.build_hourly_family_report, _date(date), q.normalize_product_type(product_type),
                          q.normalize_product(product), q.normalize_strategy_family(family), interval_minutes)

    @app.get("/api/point_in_time_scenario", response_model=None, responses=_ok(m.PointInTimeScenarioResponse), summary="Scenario cohort as of a past time-of-day",
             description="Re-runs a scenario's selection using only evidence available at or before `at` (HH:MM) on `date` - the cohort you would actually have picked at that moment - then returns each selected model's full-day curve so its actual later performance can be assessed. Distinct from `baseline_index`/`frame_index` on the other endpoints, which replay a fixed, end-of-day-selected cohort from an earlier point; this re-selects the cohort itself as of that time.")
    async def point_in_time_scenario(date: str | None = Query(None, description=DATE_DOC),
                                     at: str = Query(..., pattern=r"^\d{2}:\d{2}$", description="Cutoff time-of-day, HH:MM"),
                                     scenario: str = Query("top_net", description="Scenario id, as in EngineRequest.scenario"),
                                     return_type: str = Query("NET", pattern="^(NET|ALT)$"),
                                     product_type: str = Query("all", **PT_DOC), product: str = Query("all", description="Product code"),
                                     strategy_family: str = Query("all", **FAM_DOC), limit: int = Query(10, **LIMIT_DOC),
                                     min_win_rate: float = Query(0.0, description="Percent 0-100")):
        return await _run(q.build_point_in_time_scenario, _date(date), at, scenario, return_type,
                          q.normalize_product_type(product_type), q.normalize_product(product),
                          q.normalize_strategy_family(strategy_family), q.normalize_model_limit(limit), min_win_rate)

    @app.get("/api/portfolio_day", response_model=None, responses=_ok(m.PortfolioDayResponse), summary="Curves for an explicit model list")
    async def portfolio_day(models: str = Query(..., min_length=1, description="Comma-separated model ids, e.g. dna_301680,dna_301686 (max 10)"),
                            date: str | None = Query(None, description=DATE_DOC)):
        return await _run(q.build_portfolio_day, _date(date), models.split(","))

    @app.get("/api/similar_strategies", response_model=None, responses=_ok(m.SimilarStrategiesResponse), summary="Same-product comparison groups",
             description="For a model, the same-product strategies varying exactly one dimension: family, window, tp or sl.")
    async def similar_strategies(model: str = Query(..., min_length=1, description="Model id"), date: str | None = Query(None, description=DATE_DOC)):
        return await _run(q.build_similar_strategies, _date(date), model)

    @app.get("/api/strategy_catalog", response_model=None, responses=_ok(m.StrategyCatalogResponse), summary="Active models with parsed dimensions")
    async def strategy_catalog(date: str | None = Query(None, description=DATE_DOC)):
        return await _run(q.build_strategy_catalog, _date(date))

    @app.get("/api/model_trades", response_model=None, responses=_ok(m.ModelTradesResponse), summary="Closed and open trades for a model over a date range")
    async def model_trades(model: str = Query(..., min_length=1), date_from: str = Query(..., alias="from"),
                           date_to: str | None = Query(None, alias="to"), product_type: str = "all",
                           product: str = "all"):
        return await _run(q.build_model_trades, model, _date(date_from), _date(date_to or date_from),
                          q.normalize_product_type(product_type), q.normalize_product(product))

    @app.get("/api/model_trades_summary", response_model=None, responses=_ok(m.ModelTradesSummaryResponse), summary="Trades-modal summary chips")
    async def model_trades_summary(model: str = Query(..., min_length=1), date_from: str = Query(..., alias="from"),
                                   date_to: str | None = Query(None, alias="to"), product_type: str = "all",
                                   product: str = "all"):
        """Trades-modal summary chips: trades, open, win rate, closed net, closed alt net (computed client-side on the page)."""
        def build():
            data = q.build_model_trades(model, _date(date_from), _date(date_to or date_from),
                                        q.normalize_product_type(product_type), q.normalize_product(product))
            trades = data["trades"]
            closed = [t for t in trades if t.get("status") == "closed"]
            wins = sum(1 for t in closed if (t.get("net_return") or 0) > 0)
            return {"model": model, "from": data["from"], "to": data["to"], "trades": len(trades),
                    "open": len(trades) - len(closed), "win_rate": round(wins / len(closed) * 100, 1) if closed else None,
                    "closed_net": sum(t.get("net_return") or 0 for t in closed),
                    "closed_alt_net": sum(t.get("alt_net_return") or 0 for t in closed)}
        return await _run(build)

    # --- functions that were client-side only on the page ------------------------------------
    @app.get("/api/scenarios", response_model=None, responses=_ok(m.ScenariosResponse), summary="Scenario catalogue and the day's dynamic scenario ids")
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

    @app.post("/api/scenario_candidates", response_model=None, responses=_ok(m.ScenarioCandidatesResponse), summary="Models the page would display (getEligibleModels)")
    async def scenario_candidates(req: EngineRequest):
        """getScenarioCandidates / getEligibleModels: the model list (with series) the page would display."""
        return await _run(lambda: {"models": resolve_models(req)})

    @app.post("/api/ribbon", response_model=None, responses=_ok(m.RibbonResponse), summary="Summed delta net/buy/sell from baseline to replay head")
    async def ribbon(req: EngineRequest):
        """updateRibbon: summed and per-model delta net/buy/sell from baseline to replay head."""
        def build():
            models, b = _prepare(req)
            return eng.ribbon(models, return_type=req.return_type, baseline_index=b, frame_index=req.frame_index) | {"baseline_index": b}
        return await _run(build)

    @app.post("/api/replay_frame", response_model=None, responses=_ok(m.ReplayFrameResponse), summary="Replay/baseline points per model")
    async def replay_frame(req: EngineRequest):
        """Replay / baseline / scrubber: per-model base and head point plus frame count."""
        def build():
            models, b = _prepare(req)
            return {"baseline_index": b, "frame_index": req.frame_index,
                    "max_frames": max((len(m["series"]) for m in models), default=1),
                    "models": [{"model": m["model"], "base": eng.base_point(m["series"], b),
                                "head": eng.head_point(m["series"], req.frame_index)} for m in models]}
        return await _run(build)

    @app.post("/api/overlay_signals", response_model=None, responses=_ok(m.OverlayResponse), summary="Tri-split B/S/X overlay for one model")
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

    @app.post("/api/leader_rotation", response_model=None, responses=_ok(m.RotationResponse), summary="Total Net leader rotation")
    async def leader_rotation(req: EngineRequest):
        """Total Net leader rotation across the visible strategies (ALL_NET mode B/X signals)."""
        def build():
            models, b = _prepare(req)
            return eng.leader_rotation(models, eng.metric_keys(req.return_type)["netKey"], _head(models, req.frame_index),
                                       baseline_index=b, exit_threshold=req.exit_threshold,
                                       daily_target=req.daily_target) | {"baseline_index": b}
        return await _run(build)

    @app.post("/api/multi_split_rotation", response_model=None, responses=_ok(m.RotationResponse), summary="Multi-Split buy/sell rotation")
    async def multi_split_rotation(req: EngineRequest):
        """Multi-Split rotation across every visible strategy's Buy and Sell side."""
        def build():
            models, b = _prepare(req)
            return eng.multi_split_rotation(models, eng.metric_keys(req.return_type), _head(models, req.frame_index),
                                            baseline_index=b, exit_threshold=req.exit_threshold,
                                            daily_target=req.daily_target) | {"baseline_index": b}
        return await _run(build)

    # --- named portfolios (localStorage on the page; server-side here) -----------------------
    @app.get("/api/point_in_time_scenario_hours", response_model=None, responses=_ok(m.PointInTimeScenarioHoursResponse), summary="Scenario cohort at every completed clock-hour",
             description="Batch form of /api/point_in_time_scenario: the selected cohort re-computed at each completed clock-hour cutoff (00:00, 01:00, ...) through the day, each with rank/model/strategy/trades/win_rate/net only (no curves - call point_in_time_scenario or model_trades for detail on one hour/model).")
    async def point_in_time_scenario_hours(date: str | None = Query(None, description=DATE_DOC),
                                           scenario: str = Query("top_net", description="Scenario id, as in EngineRequest.scenario"),
                                           return_type: str = Query("NET", pattern="^(NET|ALT)$"),
                                           product_type: str = Query("all", **PT_DOC), product: str = Query("all", description="Product code"),
                                           strategy_family: str = Query("all", **FAM_DOC), limit: int = Query(10, **LIMIT_DOC),
                                           min_win_rate: float = Query(0.0, description="Percent 0-100")):
        return await _run(q.build_point_in_time_scenario_hours, _date(date), scenario, return_type,
                          q.normalize_product_type(product_type), q.normalize_product(product),
                          q.normalize_strategy_family(strategy_family), q.normalize_model_limit(limit), min_win_rate)

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
        """createSimilarPortfolio: portfolio (max 10) from a same-product comparison group of a model, named like the page does."""
        def build():
            sim = q.build_similar_strategies(_date(body.date), body.model)
            groups = sim.get("groups") or {}
            if body.dimension not in groups:
                raise ValueError(f"unknown dimension {body.dimension!r}; use one of {sorted(groups)}")
            ref = sim["reference"]
            label = {"family": "Family", "window": "Window", "tp": "TP", "sl": "SL"}[body.dimension]
            win = "" if ref.get("window") is None else f" W{ref['window']}"
            base = f"{str(ref['product']).upper()} {label}{win} T{ref['tp']} S{ref['sl']}"[:32]
            existing = store.list(owner)["portfolios"]
            name = body.name or base
            if not body.name and name in existing:
                n = 2
                while f"{name[:28]} {n}" in existing:
                    n += 1
                name = f"{name[:28]} {n}"
            return store.put(owner, name, [g["model"] for g in groups[body.dimension]][:MAX_PORTFOLIO_MODELS])
        return await _run(build)

    @app.get("/api/coverage", response_model=None, responses=_ok(m.CoverageResponse), summary="What data exists (dates, products, snapshot times)",
             description="Call this first: the dashboard endpoints return empty results for dates outside `dates`, and curves need `snapshot_dates`.")
    async def coverage():
        def build():
            with q._connect() as conn, conn.cursor() as cur:
                cur.execute("SELECT DISTINCT created::date FROM combined_trades_closed ORDER BY 1")
                dates = [r[0].isoformat() for r in cur.fetchall()]
                cur.execute("SELECT DISTINCT snapshot_timestamp::date FROM tbl_dna_model_summary_snapshots_5min ORDER BY 1")
                snap_dates = [r[0].isoformat() for r in cur.fetchall()]
                cur.execute("SELECT to_char(MAX(snapshot_timestamp), 'YYYY-MM-DD HH24:MI:SS') FROM tbl_dna_model_summary_snapshots_5min")
                latest = cur.fetchone()[0]
                cur.execute("SELECT DISTINCT LOWER(TRIM(product)) FROM product_forex WHERE product IS NOT NULL ORDER BY 1")
                products = [r[0] for r in cur.fetchall()]
            return {"source": "PostgreSQL tradedb", "first_date": dates[0] if dates else None, "last_date": dates[-1] if dates else None,
                    "dates": dates, "snapshot_dates": snap_dates, "latest_snapshot": latest, "products": products,
                    "intelligence": app.state.intelligence_coverage() if hasattr(app.state, "intelligence_coverage") else None}
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
        "GET /api/model_trades_summary": "same params as model_trades -> trades/open/win_rate/closed_net/closed_alt_net chips",
        "GET /api/scenarios": "scenario catalogue + the day's dynamic ids (top5_*, top3_tp*_sl*)",
        "POST /api/scenario_candidates": "EngineRequest -> getScenarioCandidates/getEligibleModels (win-rate, product, family filters)",
        "POST /api/ribbon": "EngineRequest -> summed/per-model delta net/buy/sell baseline->head",
        "POST /api/replay_frame": "EngineRequest -> base/head points per model, max_frames (replay, baseline, scrubber)",
        "POST /api/overlay_signals": "EngineRequest(model) -> tri-split B/S/X signals, paired trades, flip result, daily-target hit",
        "POST /api/leader_rotation": "EngineRequest -> Total Net leader rotation signals/trades/target",
        "POST /api/multi_split_rotation": "EngineRequest -> Multi-Split buy/sell rotation signals/trades/target",
        "GET|PUT|DELETE /api/portfolios[/{name}]": "named portfolios (max 10 strategies), plus POST /{name}/models, DELETE /{name}/models/{model}",
        "POST /api/portfolio_merge": "{name, sources[]} -> de-duplicated merge",
        "POST /api/portfolio_from_similar": "{name?, date, model, dimension: family|window|tp|sl} -> portfolio from a comparison group",
        "GET /api/coverage": "available dates, snapshot dates, products, latest snapshot",
        "GET /api/point_in_time_scenario_hours": "date, scenario, filters -> the cohort re-selected at every completed clock-hour, {at_time, models:[{rank,model,strategy,trades,win_rate,net}]} - no curves",
        "GET /api/point_in_time_scenario": "date, at=HH:MM, scenario, return_type, filters -> the scenario cohort as it would have been selected as-of that time, with full-day curves",
    },
    "engine_request_fields": list(EngineRequest.model_fields),
    "ui_only": ["theme", "collapse/expand sections", "chart drawing/tooltips", "trades-modal column sorting", "scrubber speed"],
}
