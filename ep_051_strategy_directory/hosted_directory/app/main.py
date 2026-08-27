"""Container-ready directory API and screen host.

Version history:
- 2.1.1 (2026-08-27): Serves the shared Tech Principle screen-theme stylesheet.
- 2.1.0 (2026-08-27): Adds profitable-strategy count and percentage to the selected-period directory summary.
- 2.0.0 (2026-08-25): Defines headline strategies as models executed within the selected period.
- 1.9.0 (2026-08-25): Reports exact constructed product_forex models as a reference total.
- 1.8.0 (2026-08-25): Keeps the full product_forex strategy population in directory summaries.
- 1.8.2 (2026-08-25): Falls back to fresh grant-free period evidence when the local snapshot has no matching day.
- 1.8.1 (2026-08-25): Adds full-filter directory summary totals so the listing can show persistent evidence coverage independently of pagination.
- 1.8.0 (2026-08-24): Caches period directory aggregates and avoids repeated snapshot validation.
- 1.7.0 (2026-08-24): Integrates discovery retrieval, private user objects and fail-closed regime APIs.
- 1.6.0 (2026-08-24): Adds validated natural-language-to-query-plan interpretation endpoint.
- 1.5.0 (2026-08-24): Adds explainable scoring and multi-strategy comparative intelligence APIs.
- 1.4.0 (2026-08-24): Adds the versioned server-side Strategy Intelligence Profile API.
- 1.2.0 (2026-08-24): Adds period-aware strategy equity-curve endpoint.
- 1.1.0 (2026-08-24): Adds inclusive date-range filtering and period metadata to directory responses.
- 1.0.0 (2026-08-23): Local SQL and hosted snapshot modes, ingestion and screens.
"""
from __future__ import annotations
import base64,hashlib,hmac, json,re,secrets, time as clock
from threading import Lock,Thread
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from fastapi import Depends, FastAPI, Header, HTTPException, Path as ApiPath, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse,Response

from .config import Settings, get_settings
from .contracts import Snapshot, Strategy
from .repository import MemoryRepository, PostgresRepository, local_closed_trades, local_equity_curve, local_equity_curves, local_period_strategies, local_products, local_strategies
from .intelligence.profile import UNITS, build_profile, build_summary_profile
from .intelligence.comparative import cohort_percentiles, correlation, related_strategies, score_profile, similarity
from .intelligence.discovery import NaturalLanguageRequest,StrategyQuery, exclusion_trace, facet_counts, interpret_with_trace, retrieve
from .intelligence.user import PostgresUserIntelligenceStore, UserIntelligenceStore, preference_trace
from .intelligence.regime import classify, recommend, strategy_regime_profile
from .intelligence.market import MarketFeatureStore, PostgresMarketFeatureStore, freshness_limit,join_regimes_without_lookahead,validate_market_cache
from .intelligence.contracts import (CollectionRequest, ConsentRequest, PreferenceRequest,
    MarketFeatureIngestRequest, RecommendationRequest, RegimeFeaturesRequest, SavedSearchRequest, SearchRequest)
from .intelligence.assurance import OperationsMonitor,ReleaseManager
from .intelligence.cache import validate_local_cache,validate_local_cache_freshness

WEB = Path(__file__).resolve().parents[1] / "web"


def html_signature():
    # Cheap staleness check (name+mtime+size only, no file reads) so the CSP
    # cache below can detect an edited web/*.html without hashing on every request.
    return tuple(sorted((p.name,p.stat().st_mtime_ns,p.stat().st_size) for p in WEB.glob("*.html")))


def content_security_policy():
    hashes=[]
    for path in WEB.glob("*.html"):
        for script in re.findall(r"<script>(.*?)</script>",path.read_text(encoding="utf-8"),re.DOTALL):
            digest=base64.b64encode(hashlib.sha256(script.encode()).digest()).decode();hashes.append(f"'sha256-{digest}'")
    return "default-src 'self'; script-src 'self' "+" ".join(sorted(set(hashes)))+"; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'"


def create_app(repository=None, settings: Settings | None = None) -> FastAPI:
    cfg = settings or get_settings()
    repo = repository or (PostgresRepository(cfg.database_url) if cfg.data_backend == "postgres" and cfg.database_url else None)
    app = FastAPI(title="DNA Strategy Directory API", version="1.0.0", docs_url=None, redoc_url=None)
    user_store=PostgresUserIntelligenceStore(cfg.database_url, verify_boundary=bool(cfg.intelligence_user_token), maintenance_database_url=cfg.maintenance_database_url) if cfg.data_backend=="postgres" and cfg.database_url else UserIntelligenceStore()
    market_store=PostgresMarketFeatureStore(cfg.database_url) if cfg.data_backend=="postgres" and cfg.database_url else MarketFeatureStore()
    if cfg.data_backend=="sqlserver":
        market_cache=Path(cfg.local_market_feature_cache_path);market_cache=market_cache if market_cache.is_absolute() else Path(__file__).resolve().parents[1]/market_cache
        try:
            payload=validate_market_cache(json.loads(market_cache.read_text(encoding="utf-8")))
            candidate_store=MarketFeatureStore()
            for feature in payload["features"]:candidate_store.ingest(feature["market"],feature["as_of"],feature["features"],feature["source_version"])
            market_store=candidate_store
        except (OSError,ValueError,KeyError,TypeError):pass
    app.state.repository = repo; app.state.settings = cfg; app.state.user_intelligence = user_store;app.state.market_features=market_store
    app.state.operations=OperationsMonitor();app.state.releases=ReleaseManager()
    app.state.csp_cache={"signature":None,"value":None};app.state.csp_cache_lock=Lock()
    app.state.profile_cache={"at":0.0,"profiles":None,"curves":None};app.state.profile_cache_lock=Lock()
    app.state.strategy_cache=None;app.state.strategy_cache_lock=Lock()
    app.state.local_snapshot_cache=None
    app.state.local_snapshot_cache_mtime=None
    app.state.period_strategy_cache={}
    app.state.period_strategy_cache_lock=Lock()
    app.state.period_refreshing=set()
    app.state.directory_summary_cache={"mtime":None,"payload":None}
    app.add_middleware(CORSMiddleware, allow_origins=cfg.cors_origins, allow_credentials=False,
                       allow_methods=["GET","POST","PUT","DELETE"], allow_headers=["Authorization","Content-Type","Idempotency-Key","X-User-ID"])

    def current_csp():
        # Recomputed whenever any web/*.html file's name/mtime/size changes, so an
        # edited inline <script> gets its new hash on the very next request instead
        # of requiring a process restart. The signature check is stat()-only and
        # cheap; the sha256 rehash only runs when it actually changed.
        signature=html_signature();cache=app.state.csp_cache
        if cache["signature"]!=signature:
            with app.state.csp_cache_lock:
                if cache["signature"]!=signature:
                    cache["value"]=content_security_policy();cache["signature"]=signature
        return cache["value"]

    @app.middleware("http")
    async def headers(request: Request, call_next):
        if request.url.path=="/internal/snapshots":
            raw=request.headers.get("content-length")
            if raw is None:raise HTTPException(411,"Content-Length is required")
            try:size=int(raw)
            except ValueError:raise HTTPException(400,"Invalid Content-Length")
            if size<0 or size>cfg.max_snapshot_bytes:raise HTTPException(413,"Snapshot body limit exceeded")
        request.state.request_id = request.headers.get("X-Request-ID", secrets.token_hex(8))[:64];started=clock.perf_counter()
        try:response = await call_next(request)
        except Exception:
            app.state.operations.observe((clock.perf_counter()-started)*1000,False);raise
        app.state.operations.observe((clock.perf_counter()-started)*1000,response.status_code<500);response.headers["X-Request-ID"] = request.state.request_id
        response.headers["X-Content-Type-Options"] = "nosniff"; response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"]=current_csp();response.headers["Permissions-Policy"]="camera=(), microphone=(), geolocation=()"
        return response

    def local_snapshot():
        if cfg.data_backend!="sqlserver":return None
        cache_path=Path(cfg.local_intelligence_cache_path);cache_path=cache_path if cache_path.is_absolute() else Path(__file__).resolve().parents[1]/cache_path
        try:
            mtime=cache_path.stat().st_mtime_ns
            if app.state.local_snapshot_cache is not None and app.state.local_snapshot_cache_mtime==mtime:
                return validate_local_cache_freshness(app.state.local_snapshot_cache,cfg.local_intelligence_cache_max_age_seconds)
            payload=json.loads(cache_path.read_text(encoding="utf-8"));validate_local_cache(payload,cfg.local_intelligence_cache_max_age_seconds);app.state.local_snapshot_cache=payload;app.state.local_snapshot_cache_mtime=mtime;return payload
        except (OSError,ValueError,KeyError,TypeError):return None

    def cached_summary(profile,points=None):
        metrics=profile["metrics"];evidence=profile["evidence"];identity=profile["identity"];classification=profile["classification"]
        if points is None:
            total=int(evidence["trade_count"]);net=metrics["total_return"]["value"] or 0;rate=metrics["win_rate"]["value"]
            wins=round(total*rate) if rate is not None else 0;losses=total-wins
        else:
            returns=[float(point["net_return"]) for point in points];total=len(returns);net=sum(returns);wins=sum(value>0 for value in returns);losses=sum(value<0 for value in returns);rate=wins/total if total else 0.0
            gains=sum(value for value in returns if value>0);loss_value=abs(sum(value for value in returns if value<0));profit_factor=gains/loss_value if loss_value else None
        instruments=classification.get("instruments") or []
        return Strategy(strategy_id=identity["strategy_id"],descriptive_name=identity.get("name"),market=classification.get("asset_class") or "FX",product_name=", ".join(instruments) or None,status="active",total_trades=total,wins=wins,losses=losses,breakevens=total-wins-losses,total_net_return=net,win_rate=rate,profit_factor=metrics["profit_factor"]["value"] if points is None else profit_factor,max_drawdown_money=metrics["max_drawdown"]["value"] if points is None else min((point["drawdown"] for point in points),default=None),quality_state="VALID" if total>=30 else "COLLECTING",evidence_start=evidence.get("start") if points is None else (points[0]["closed_at"] if points else None),evidence_end=evidence.get("end") if points is None else (points[-1]["closed_at"] if points else None))

    def refresh_period_in_background(cache_key,start,end,canonical_strategy):
        try:
            refreshed=[Strategy.model_validate(x) for x in local_period_strategies(
                cfg,start.replace(tzinfo=None),end.replace(tzinfo=None),canonical_strategy
            )]
            with app.state.period_strategy_cache_lock:
                app.state.period_strategy_cache[cache_key]=refreshed
        finally:
            with app.state.period_strategy_cache_lock:
                app.state.period_refreshing.discard(cache_key)

    def period_cache_key(date_from, date_to, canonical_strategy):
        """Refresh a live/current period at least once per minute."""
        today = datetime.now(timezone.utc).date()
        live_bucket = (
            datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
            if date_to is not None and date_to >= today else None
        )
        return (app.state.local_snapshot_cache_mtime,date_from,date_to,canonical_strategy,live_bucket)

    def current_directory_cache(request_date: date):
        cache_path=Path(__file__).resolve().parents[1]/"runtime"/"directory_summary_cache.json"
        try:
            mtime=cache_path.stat().st_mtime_ns
            if app.state.directory_summary_cache["mtime"] != mtime:
                payload=json.loads(cache_path.read_text(encoding="utf-8"))
                if payload.get("date_from") != request_date.isoformat():
                    raise ValueError("current-day directory cache is stale")
                app.state.directory_summary_cache={"mtime":mtime,"payload":payload}
            return app.state.directory_summary_cache["payload"]
        except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError):
            raise HTTPException(503,"Current-day directory cache is warming; retry shortly")

    def items(date_from: date | None = None, date_to: date | None = None, canonical_strategy: str | None = None, signal: str | None = None):
        if date_from and date_to and date_from > date_to:
            raise HTTPException(422, "date_from must be on or before date_to")
        start = datetime.combine(date_from, time.min,timezone.utc) if date_from else None
        end = datetime.combine(date_to + timedelta(days=1), time.min,timezone.utc) if date_to else None
        if cfg.data_backend == "sqlserver":
            # Current-day list and detail summaries share the same atomic cache
            # as the ledger and curve. This check must precede the exact-ID
            # fallback or strategy pages still issue a slow raw-table query.
            if date_from == datetime.now(timezone.utc).date() and date_to == date_from:
                payload=current_directory_cache(date_from)
                rows=payload["datasets"][signal or "BOTH"]
                if canonical_strategy:
                    rows=[row for row in rows if row["strategy_id"] == canonical_strategy]
                return [Strategy.model_validate(row) for row in rows]
            # Historical detail periods retain the bounded SQL fallback until
            # historical cache partitions are published.
            if canonical_strategy and start is not None and end is not None:
                return [Strategy.model_validate(x) for x in local_strategies(
                    cfg,start.replace(tzinfo=None),end.replace(tzinfo=None),canonical_strategy,signal
                )]
            # The grant-free entry-date cohort query completes within the UI
            # latency target and must be authoritative. Returning it directly
            # prevents a completed current-day result from being replaced by a
            # stale snapshot/cache entry while trading continues.
            if start is not None and end is not None:
                return [Strategy.model_validate(x) for x in local_period_strategies(
                    cfg,start.replace(tzinfo=None),end.replace(tzinfo=None),canonical_strategy,signal
                )]
            if signal is not None:
                return [Strategy.model_validate(x) for x in local_strategies(
                    cfg,canonical_strategy=canonical_strategy,signal=signal
                )]
            cached=local_snapshot()
            if cached is not None:
                profiles=cached["profiles"]
                if canonical_strategy:profiles=[profile for profile in profiles if profile["identity"]["strategy_id"]==canonical_strategy]
                if start is None and end is None:return [cached_summary(profile) for profile in profiles]
                cache_key=period_cache_key(date_from,date_to,canonical_strategy)
                period_cached=app.state.period_strategy_cache.get(cache_key)
                if period_cached is not None:return period_cached
                with app.state.period_strategy_cache_lock:
                    period_cached=app.state.period_strategy_cache.get(cache_key)
                    if period_cached is not None:return period_cached
                    output=[]
                    for profile in profiles:
                        strategy_id=profile["identity"]["strategy_id"];points=points_from_snapshot(cached,strategy_id,start,end)
                        if points:output.append(cached_summary(profile,points))
                    if not output and start is not None and end is not None:
                        # Display the complete strategy population immediately;
                        # live period evidence is refreshed outside the request.
                        output=[cached_summary(profile,[]) for profile in profiles]
                    if start is not None and end is not None:
                        # Snapshot evidence may contain only a partial current period.
                        # Always reconcile a requested period with the live source once,
                        # then atomically replace the provisional cached result.
                        app.state.period_refreshing.add(cache_key)
                        Thread(target=refresh_period_in_background,args=(cache_key,start,end,canonical_strategy),daemon=True).start()
                    app.state.period_strategy_cache[cache_key]=output
                    return output
            if not cfg.allow_synchronous_local_fallback:raise HTTPException(503,"Local intelligence snapshot is missing or stale; run the operator warm-up")
            if start is None and end is None:
                if app.state.strategy_cache is None:
                    with app.state.strategy_cache_lock:
                        if app.state.strategy_cache is None:
                            candidates=[Strategy.model_validate(x) for x in local_strategies(cfg)];candidates.sort(key=lambda item:(-item.total_trades,item.strategy_id));app.state.strategy_cache=candidates
                return [item for item in app.state.strategy_cache if canonical_strategy is None or item.strategy_id==canonical_strategy]
            return [Strategy.model_validate(x) for x in local_strategies(cfg,start.replace(tzinfo=None) if start else None,end.replace(tzinfo=None) if end else None,canonical_strategy)]
        if date_from or date_to:
            raise HTTPException(501, "Hosted period aggregates have not been published yet")
        if app.state.repository is None: raise HTTPException(503, "Directory repository is not configured")
        return app.state.repository.current_items()

    def trusted_user(authorization:str|None=Header(None),x_user_id:str|None=Header(None,alias="X-User-ID")):
        """Trust user identity only behind the configured shared edge boundary."""
        expected=cfg.intelligence_user_token or ""; supplied=(authorization or "").removeprefix("Bearer ")
        if not expected: raise HTTPException(503,"Private intelligence identity is not configured")
        if not hmac.compare_digest(supplied,expected): raise HTTPException(401,"Unauthorized")
        if not x_user_id or len(x_user_id)>128: raise HTTPException(401,"A trusted user identity is required")
        return x_user_id

    def trusted_publisher(authorization:str|None=Header(None)):
        expected=cfg.sync_token or "";supplied=(authorization or "").removeprefix("Bearer ")
        if not expected or not hmac.compare_digest(supplied,expected):raise HTTPException(401,"Unauthorized")

    def all_profiles():
        now=clock.monotonic();cached=app.state.profile_cache
        if cached["profiles"] is not None:return cached["profiles"]
        with app.state.profile_cache_lock:
            cached=app.state.profile_cache;now=clock.monotonic()
            if cached["profiles"] is not None:return cached["profiles"]
            if cfg.data_backend=="sqlserver":
                summaries=items();expected_ids={summary.strategy_id for summary in summaries};payload=local_snapshot()
                if payload is not None and {profile["identity"]["strategy_id"] for profile in payload["profiles"]}!=expected_ids:payload=None
                if payload is not None:
                    profiles=payload["profiles"];curves=payload["curves"]
                else:
                    profiles=[];curves={}
                    for summary_model in summaries:
                        profile=build_summary_profile(summary_model.model_dump(mode="json")).model_dump(mode="json");profile["score"]=score_profile(profile);profiles.append(profile)
            else:
                if app.state.repository is None:raise HTTPException(503,"Intelligence repository is not configured")
                profiles=app.state.repository.current_profiles();curves=app.state.repository.current_equity_curves()
                for profile in profiles:profile.setdefault("score",score_profile(profile))
            app.state.profile_cache={"at":clock.monotonic(),"profiles":profiles,"curves":curves};return profiles

    def points_from_snapshot(snapshot,strategy_id,start=None,end=None):
        if snapshot is None:return None
        points=[]
        for point in snapshot["curves"].get(strategy_id,[]):
            observed=datetime.fromisoformat(str(point["closed_at"]).replace("Z","+00:00"));observed=observed if observed.tzinfo else observed.replace(tzinfo=timezone.utc)
            if (start is None or observed>=start) and (end is None or observed<end):points.append(point)
        equity=peak=0.0;rebased=[]
        for index,point in enumerate(points,1):
            equity+=float(point["net_return"]);peak=max(peak,equity);rebased.append({**point,"trade_number":index,"equity":equity,"drawdown":equity-peak})
        return rebased

    def cached_points(strategy_id,start=None,end=None):
        snapshot=local_snapshot() if cfg.data_backend=="sqlserver" else None
        return points_from_snapshot(snapshot,strategy_id,start,end)

    def resolved_profile(strategy_id,start=None,end=None):
        if cfg.data_backend=="sqlserver":
            snapshot=local_snapshot();points=cached_points(strategy_id,start,end)
            if snapshot is not None:
                source=next((profile for profile in snapshot["profiles"] if profile["identity"]["strategy_id"]==strategy_id),None)
                if source is None:return None
                if start is None and end is None:return source
                if not points:return None
                return build_profile(cached_summary(source,points).model_dump(mode="json"),points).model_dump(mode="json")
            if not cfg.allow_synchronous_local_fallback:raise HTTPException(503,"Local intelligence snapshot is missing or stale; run the operator warm-up")
            summaries=local_strategies(cfg,start,end,strategy_id)
            if not summaries:return None
            return build_profile(summaries[0],local_equity_curve(cfg,strategy_id,start,end)).model_dump(mode="json")
        return next((profile for profile in all_profiles() if profile["identity"]["strategy_id"]==strategy_id),None)

    @app.get("/healthz")
    def health(): return {"status":"ok"}

    @app.get("/favicon.ico",include_in_schema=False)
    def favicon():return Response(status_code=204)

    @app.get("/readyz")
    def ready():
        try: items()
        except Exception: raise HTTPException(503,"Directory data is unavailable")
        return {"status":"ready"}

    @app.get("/api/dna/strategies")
    def strategies(page:int=Query(1,ge=1),page_size:int=Query(50,ge=1,le=100),search:str|None=Query(None,max_length=32,pattern=r"^[A-Za-z0-9_]*$"),
                   product:str|None=Query(None,max_length=32,pattern=r"^[A-Za-z0-9_]*$"),
                   minimum_trades:int=Query(0,ge=0),sort:str=Query("strategy_id",pattern=r"^(strategy_id|total_trades|total_net_return|win_rate|profit_factor|max_drawdown_money)$"),
                   direction:str=Query("asc",pattern=r"^(asc|desc)$"),
                   signal:str|None=Query(None,pattern=r"^(BUY|SELL)$"),
                   date_from:date|None=Query(None),date_to:date|None=Query(None)):
        exact_strategy = search.upper() if search and search.upper().startswith("DNA_") else None
        requested_product=product.upper() if product else None
        rows=[x for x in items(date_from,date_to,exact_strategy,signal)
              if x.total_trades>=minimum_trades
              and (not search or search.upper() in x.strategy_id.upper())
              and (not requested_product or requested_product in {part.strip().upper() for part in (x.product_name or "").split(",")})]
        rows.sort(key=lambda x:(getattr(x,sort) is None,getattr(x,sort)),reverse=direction=="desc")
        total=len(rows)
        # These headline values describe the exact evidence rows already loaded
        # for this request. Deriving them here keeps the public list independent
        # of SQL Server latency and guarantees a cache-only display path.
        headline_total=sum(row.total_trades>0 for row in rows)
        profitable_strategies=sum(
            row.total_trades>0 and float(row.total_net_return or 0)>0
            for row in rows
        )
        summary={
            "strategies":headline_total,
            "closed_trades":sum(row.total_trades for row in rows),
            "total_net_return":sum(float(row.total_net_return or 0) for row in rows),
            "profitable_strategies":profitable_strategies,
            "profitable_percentage":round(profitable_strategies/headline_total*100,2) if headline_total else 0.0,
            "evidence_ready":sum(row.quality_state=="VALID" for row in rows),
            "collecting":sum(row.quality_state=="COLLECTING" for row in rows),
        }
        if cfg.data_backend=="sqlserver" and not search and minimum_trades==0:
            summary.update(executed_trades=summary["closed_trades"],constructed_strategies=total)
        refresh_pending=False
        if cfg.data_backend=="sqlserver" and (date_from or date_to):
            refresh_key=period_cache_key(date_from,date_to,exact_strategy)
            with app.state.period_strategy_cache_lock:refresh_pending=refresh_key in app.state.period_refreshing
        rows=rows[(page-1)*page_size:page*page_size]
        snap=app.state.repository.current_snapshot() if cfg.data_backend=="postgres" and app.state.repository else None
        return {"data":{"items":[x.model_dump(mode="json") for x in rows],"page":page,"page_size":page_size,"total":total,"summary":summary,"refresh_pending":refresh_pending},
                "as_of":(snap.generated_at if snap else datetime.now(timezone.utc)).isoformat(),
                "basis":"net return; costs and commission already included","methodology_version":snap.methodology_version if snap else "1.0.0",
                "quality_state":"VALID","period":{"date_from":date_from.isoformat() if date_from else None,
                "date_to":date_to.isoformat() if date_to else None}}

    @app.get("/api/dna/products")
    def products():
        if cfg.data_backend == "sqlserver":
            values=local_products(cfg)
        else:
            values=sorted({part.strip().upper() for item in app.state.repository.current_items()
                           for part in (item.product_name or "").split(",") if part.strip()})
        return {"items":values,"total":len(values)}

    @app.get("/api/dna/strategies/{strategy_id}/equity-curve")
    def equity_curve(strategy_id:str=ApiPath(pattern=r"^DNA_[A-Za-z0-9]+$"),
                     date_from:date|None=Query(None),date_to:date|None=Query(None)):
        if date_from and date_to and date_from > date_to:
            raise HTTPException(422, "date_from must be on or before date_to")
        start = datetime.combine(date_from, time.min,timezone.utc) if date_from else None
        end = datetime.combine(date_to + timedelta(days=1), time.min,timezone.utc) if date_to else None
        if cfg.data_backend=="sqlserver" and date_from==datetime.now(timezone.utc).date() and date_to==date_from:
            trades=current_directory_cache(date_from).get("trades_by_strategy",{}).get(strategy_id,[])
            ordered=sorted(trades,key=lambda row:(row.get("exit_time") or "",row.get("entry_time") or "",row.get("guid") or ""))
            equity=peak=0.0;points=[]
            for number,row in enumerate(ordered,1):
                equity+=float(row["net_return"]);peak=max(peak,equity)
                points.append({"trade_number":number,"opened_at":row["entry_time"],"closed_at":row["exit_time"],
                               "net_return":row["net_return"],"equity":equity,"drawdown":equity-peak})
            return {"strategy_id":strategy_id,"points":points,"total_points":len(points),
                    "period":{"date_from":date_from.isoformat(),"date_to":date_to.isoformat()},
                    "basis":"cached cumulative net return; costs and commission already included"}
        # Individual SQL Server evidence must be internally consistent with the
        # live trade ledger. Snapshot curves can be non-empty but incomplete
        # when additional trades close, so never use them on this detail route.
        points = local_equity_curve(cfg,strategy_id,start,end) if cfg.data_backend=="sqlserver" else app.state.repository.current_equity_curve(strategy_id,start,end)
        if points is None:
            if not cfg.allow_synchronous_local_fallback:raise HTTPException(503,"Local intelligence snapshot is missing or stale; run the operator warm-up")
            points=local_equity_curve(cfg,strategy_id,start,end)
        return {"strategy_id":strategy_id,"points":points,"total_points":len(points),
                "period":{"date_from":date_from.isoformat() if date_from else None,
                          "date_to":date_to.isoformat() if date_to else None},
                "basis":"cumulative net return; costs and commission already included"}

    @app.get("/api/dna/strategies/{strategy_id}/trades")
    def closed_trades(strategy_id:str=ApiPath(pattern=r"^DNA_[A-Za-z0-9]+$"),
                      date_from:date|None=Query(None),date_to:date|None=Query(None),
                      limit:int=Query(1000,ge=1,le=5000)):
        if date_from and date_to and date_from > date_to:
            raise HTTPException(422, "date_from must be on or before date_to")
        start = datetime.combine(date_from, time.min,timezone.utc) if date_from else None
        end = datetime.combine(date_to + timedelta(days=1), time.min,timezone.utc) if date_to else None
        if cfg.data_backend != "sqlserver":
            raise HTTPException(501,"The raw trade ledger is not available from this data backend")
        if date_from==datetime.now(timezone.utc).date() and date_to==date_from:
            trades=current_directory_cache(date_from).get("trades_by_strategy",{}).get(strategy_id,[])[:limit]
        else:
            trades=local_closed_trades(cfg,strategy_id,start,end,limit)
        return {"strategy_id":strategy_id,"items":trades,"total":len(trades),"limit":limit,
                "period":{"date_from":date_from.isoformat() if date_from else None,
                          "date_to":date_to.isoformat() if date_to else None},
                "basis":"closed trades; net return includes costs and commission"}

    @app.get("/api/intelligence/strategies/{strategy_id}")
    def intelligence_profile(strategy_id:str=ApiPath(pattern=r"^DNA_[A-Za-z0-9]+$"),
                             date_from:date|None=Query(None),date_to:date|None=Query(None),fields:str|None=Query(None,max_length=120,pattern=r"^[a-z_,]*$")):
        if date_from and date_to and date_from > date_to: raise HTTPException(422,"date_from must be on or before date_to")
        start=datetime.combine(date_from,time.min,timezone.utc) if date_from else None
        end=datetime.combine(date_to+timedelta(days=1),time.min,timezone.utc) if date_to else None
        payload=resolved_profile(strategy_id,start,end)
        if payload is None: raise HTTPException(404,"Strategy evidence was not found")
        if fields:
            selected=[field for field in fields.split(",") if field];allowed={"schema_version","generated_at","identity","classification","metrics","evidence","robustness","links","methodology"}
            if any(field not in allowed for field in selected):raise HTTPException(422,"Unsupported profile field selection")
            payload={field:payload[field] for field in selected}
        return payload

    @app.get("/api/intelligence/metric-registry")
    def metric_registry():
        return {"methodology_version":"1.0.0","metrics":[{"name":name,"unit":unit,"computed_by":"intelligence-layer"} for name,unit in UNITS.items()]}

    @app.get("/api/intelligence/strategies/{strategy_id}/score")
    def intelligence_score(strategy_id:str=ApiPath(pattern=r"^DNA_[A-Za-z0-9]+$")):
        profile=resolved_profile(strategy_id)
        if profile is None: raise HTTPException(404,"Strategy evidence was not found")
        return {"strategy_id":strategy_id,"score":profile.get("score") or score_profile(profile)}

    def comparative_records():
        records=[]
        for profile in all_profiles():
            classification=profile["classification"];metrics=profile["metrics"];records.append({"strategy_id":profile["identity"]["strategy_id"],"quality_score":profile["score"]["quality_score"],"win_rate":metrics["win_rate"]["value"],"profit_factor":metrics["profit_factor"]["value"],"max_drawdown":metrics["max_drawdown"]["value"],"asset_class":classification["asset_class"],"family":classification.get("strategy_family"),"instrument":(classification.get("instruments") or [None])[0],"track_record":int(profile["evidence"]["years"] or 0)})
        return records

    @app.get("/api/intelligence/cohorts")
    def intelligence_cohorts(metric:str=Query("quality_score",pattern=r"^(quality_score|win_rate|profit_factor|max_drawdown)$")):
        records=comparative_records();return {"metric":metric,"minimum_cohort_size":5,"items":cohort_percentiles(records,metric),"methodology_version":"1.1.0"}

    @app.get("/api/intelligence/strategies/{strategy_id}/related")
    def intelligence_related(strategy_id:str=ApiPath(pattern=r"^DNA_[A-Za-z0-9]+$"),limit:int=Query(5,ge=1,le=20)):
        records=comparative_records();target=next((item for item in records if item["strategy_id"]==strategy_id),None)
        if target is None:raise HTTPException(404,"Strategy intelligence was not found")
        return {"strategy_id":strategy_id,"items":related_strategies(target,records,limit),"methodology_version":"1.1.0"}

    @app.get("/api/intelligence/compare")
    def intelligence_compare(strategy_ids:str=Query(min_length=1,max_length=160),format:str=Query("json",pattern=r"^(json|csv)$")):
        ids=[x.strip().upper() for x in strategy_ids.split(",") if x.strip()]
        if len(ids)<2 or len(ids)>5 or any(not x.startswith("DNA_") for x in ids): raise HTTPException(422,"Provide 2 to 5 canonical strategy IDs")
        profiles={}; points={}
        for strategy_id in ids:
            profile=resolved_profile(strategy_id)
            if profile is None: raise HTTPException(404,f"{strategy_id} was not found")
            if cfg.data_backend=="sqlserver":
                points[strategy_id]=cached_points(strategy_id)
                if points[strategy_id] is None:
                    if not cfg.allow_synchronous_local_fallback:raise HTTPException(503,"Local intelligence snapshot is missing or stale; run the operator warm-up")
                    points[strategy_id]=local_equity_curve(cfg,strategy_id)
            profile=dict(profile);profile.setdefault("score",score_profile(profile)); profiles[strategy_id]=profile
        relationships=[]
        def daily_returns(rows):
            buckets={}
            for point in rows:
                day=str(point["closed_at"])[:10];buckets[day]=buckets.get(day,0)+float(point["net_return"])
            return [{"timestamp":day,"return":value} for day,value in sorted(buckets.items())]
        daily={strategy_id:daily_returns(points[strategy_id]) for strategy_id in ids} if cfg.data_backend=="sqlserver" else app.state.repository.current_daily_returns(ids,2000)
        for index,left in enumerate(ids):
            for right in ids[index+1:]:
                lreturns=daily[left];rreturns=daily[right]
                lf={"quality_score":profiles[left]["score"]["quality_score"],"win_rate":profiles[left]["metrics"]["win_rate"]["value"],"profit_factor":profiles[left]["metrics"]["profit_factor"]["value"],"max_drawdown":profiles[left]["metrics"]["max_drawdown"]["value"]}
                rf={"quality_score":profiles[right]["score"]["quality_score"],"win_rate":profiles[right]["metrics"]["win_rate"]["value"],"profit_factor":profiles[right]["metrics"]["profit_factor"]["value"],"max_drawdown":profiles[right]["metrics"]["max_drawdown"]["value"]}
                relationships.append({"left":left,"right":right,"correlation":correlation(lreturns,rreturns),"similarity":similarity(lf,rf)})
        starts=[p["evidence"]["start"] for p in profiles.values() if p["evidence"]["start"]]
        ends=[p["evidence"]["end"] for p in profiles.values() if p["evidence"]["end"]]
        warnings=[]
        if starts and ends and (min(starts)!=max(starts) or min(ends)!=max(ends)):
            warnings.append("Evidence windows differ; period-sensitive metrics are not directly comparable.")
        payload={"profiles":profiles,"relationships":relationships,"warnings":warnings,"methodology_version":"1.0.0"}
        if format=="csv":
            columns=("strategy_id","quality_score","annualized_return","win_rate","sharpe","max_drawdown","evidence_start","evidence_end");lines=[",".join(columns)]
            for strategy_id,profile in profiles.items():
                values=(strategy_id,profile["score"]["quality_score"],profile["metrics"]["annualized_return"]["value"],profile["metrics"]["win_rate"]["value"],profile["metrics"]["sharpe"]["value"],profile["metrics"]["max_drawdown"]["value"],profile["evidence"]["start"],profile["evidence"]["end"]);lines.append(",".join("" if value is None else str(value) for value in values))
            return Response("\n".join(lines),media_type="text/csv",headers={"Content-Disposition":"attachment; filename=dna-strategy-comparison.csv"})
        return payload

    @app.post("/api/intelligence/query/interpret")
    def interpret_intelligence_query(request:NaturalLanguageRequest):
        result=interpret_with_trace(request.query);plan=result.pop("plan")
        return {"query":request.query,"plan":plan.model_dump(mode="json"),**result,"schema_version":"1.0.0",
                "notice":"The plan is validated and must be applied before ranking."}

    @app.post("/api/intelligence/query/search")
    def search_intelligence(request:SearchRequest):
        profiles=all_profiles();all_results=retrieve(profiles,request.plan);results=all_results[:cfg.intelligence_max_query_results];all_exclusions=exclusion_trace(profiles,request.plan)
        return {"plan":request.plan.model_dump(mode="json"),"items":results,"total":len(all_results),"facets":facet_counts([item["profile"] for item in all_results]),"exclusions":all_exclusions[:cfg.intelligence_max_query_results],"excluded_total":len(all_exclusions),
                "constraint_order":"filter-before-rank","schema_version":"1.0.0"}

    @app.get("/api/intelligence/user")
    def user_export(user_id:str=Depends(trusted_user)):
        payload=app.state.user_intelligence.export(user_id)
        try:versions={profile["identity"]["strategy_id"]:profile.get("generated_at") for profile in all_profiles()}
        except HTTPException:versions={}
        payload["watchlist_details"]=[{"strategy_id":strategy_id,"saved_evidence_version":payload.get("watch_versions",{}).get(strategy_id),"current_evidence_version":versions.get(strategy_id),"stale":bool(payload.get("watch_versions",{}).get(strategy_id) and payload.get("watch_versions",{}).get(strategy_id)!=versions.get(strategy_id))} for strategy_id in payload["watchlist"]]
        for collection in payload["collections"].values():collection["stale_strategy_ids"]=[strategy_id for strategy_id,version in collection.get("evidence_versions",{}).items() if version and version!=versions.get(strategy_id)]
        return payload

    @app.delete("/api/intelligence/user",status_code=204)
    def user_delete(user_id:str=Depends(trusted_user)):
        app.state.user_intelligence.delete(user_id)

    @app.put("/api/intelligence/user/consent")
    def user_consent(request:ConsentRequest,user_id:str=Depends(trusted_user)):
        app.state.user_intelligence.set_consent(user_id,request.history);return {"history":request.history}

    @app.put("/api/intelligence/user/watchlist/{strategy_id}")
    def watch_strategy(strategy_id:str=ApiPath(pattern=r"^DNA_[A-Za-z0-9]+$"),user_id:str=Depends(trusted_user)):
        profile=resolved_profile(strategy_id) if cfg.data_backend!="memory" or app.state.repository is not None else None
        if profile is None and cfg.data_backend!="memory":raise HTTPException(404,"Strategy evidence was not found")
        version=profile.get("generated_at") if profile else None;app.state.user_intelligence.watch(user_id,strategy_id,version);return {"strategy_id":strategy_id,"watched":True,"evidence_version":version}

    @app.delete("/api/intelligence/user/watchlist/{strategy_id}")
    def unwatch_strategy(strategy_id:str=ApiPath(pattern=r"^DNA_[A-Za-z0-9]+$"),user_id:str=Depends(trusted_user)):
        app.state.user_intelligence.unwatch(user_id,strategy_id);return {"strategy_id":strategy_id,"watched":False}

    @app.post("/api/intelligence/user/searches",status_code=201)
    def save_user_search(request:SavedSearchRequest,user_id:str=Depends(trusted_user)):
        item_id=app.state.user_intelligence.save_search(user_id,request.name,request.plan.model_dump(mode="json"));return {"id":item_id}

    @app.post("/api/intelligence/user/searches/{item_id}/replay")
    def replay_user_search(item_id:str=ApiPath(pattern=r"^[0-9a-fA-F-]{36}$"),user_id:str=Depends(trusted_user)):
        exported=app.state.user_intelligence.export(user_id);item=exported["searches"].get(item_id)
        if item is None:raise HTTPException(404,"Saved search was not found")
        plan=StrategyQuery.model_validate(item["plan"]);results=retrieve(all_profiles(),plan);ids=[result["profile"]["identity"]["strategy_id"] for result in results]
        replay=app.state.user_intelligence.replay_search(user_id,item_id,ids);previous=set(replay["previous_result_ids"])
        return {"id":item_id,"plan":plan.model_dump(mode="json"),"result_ids":ids,"added":sorted(set(ids)-previous),"removed":sorted(previous-set(ids)),"evidence_replayed_at":datetime.now(timezone.utc).isoformat()}

    @app.post("/api/intelligence/user/collections",status_code=201)
    def create_user_collection(request:CollectionRequest,user_id:str=Depends(trusted_user)):
        item_id=app.state.user_intelligence.create_collection(user_id,request.name,request.strategy_ids,request.notes,request.evidence_versions);return {"id":item_id}

    @app.put("/api/intelligence/user/preferences")
    def set_user_preferences(request:PreferenceRequest,user_id:str=Depends(trusted_user)):
        app.state.user_intelligence.set_preferences(user_id,request.preferences)
        return preference_trace(request.preferences,app.state.user_intelligence.export(user_id)["history"])

    @app.delete("/api/intelligence/user/preferences")
    def reset_user_preferences(user_id:str=Depends(trusted_user)):
        app.state.user_intelligence.reset_preferences(user_id);return {"reset":True}

    @app.post("/api/intelligence/regimes/classify")
    def classify_regime(request:RegimeFeaturesRequest):
        now=datetime.now(timezone.utc);at=request.as_of or now
        if at.tzinfo is None or at.utcoffset() is None:raise HTTPException(422,"as_of must include a timezone")
        at=at.astimezone(timezone.utc)
        if at>now+timedelta(minutes=5):raise HTTPException(422,"as_of cannot be in the future")
        row=app.state.market_features.as_of(request.market,at)
        if row is None:return {"market":request.market,"as_of":at,"state":"UNKNOWN","confidence":0,"reason":"NO_CANONICAL_FEATURES"}
        age=(at-row["as_of"]).total_seconds();limit=freshness_limit(at,cfg.intelligence_market_feature_max_age_seconds,cfg.intelligence_market_feature_weekend_max_age_seconds);fresh=age<=limit
        if request.as_of is None and not fresh:return {"market":request.market,"as_of":at,"feature_as_of":row["as_of"],"state":"UNKNOWN","confidence":0,"reason":"STALE","source_version":row["source_version"]}
        return {"market":request.market,"as_of":at,"feature_as_of":row["as_of"],"source_version":row["source_version"],"feature_sha256":row["sha256"],"fresh":fresh,**classify(row["features"])}

    @app.post("/api/intelligence/recommendations")
    def intelligence_recommendations(request:RecommendationRequest):
        now=datetime.now(timezone.utc);at=request.as_of or now
        if at.tzinfo is None or at.utcoffset() is None:raise HTTPException(422,"as_of must include a timezone")
        at=at.astimezone(timezone.utc)
        if at>now+timedelta(minutes=5):raise HTTPException(422,"as_of cannot be in the future")
        row=app.state.market_features.as_of(request.market,at)
        if row is None:return {"items":[],"total":0,"state":"UNKNOWN","reason":"NO_CANONICAL_FEATURES","methodology_version":"1.0.0","decision_support_only":True}
        age=(at-row["as_of"]).total_seconds()
        limit=freshness_limit(at,cfg.intelligence_market_feature_max_age_seconds,cfg.intelligence_market_feature_weekend_max_age_seconds)
        if age<0 or age>limit:return {"items":[],"total":0,"state":"UNKNOWN","reason":"STALE","feature_age_seconds":age,"feature_as_of":row["as_of"],"methodology_version":"1.0.0","decision_support_only":True}
        current=classify(row["features"]);profiles={item["identity"]["strategy_id"]:item for item in all_profiles()}
        curves=app.state.profile_cache.get("curves") or {};labels=[]
        for feature_row in app.state.market_features.history(request.market,through=at):labels.append({"as_of":feature_row["as_of"],"state":classify(feature_row["features"])["state"]})
        candidates=[]
        for strategy_id in request.strategy_ids:
            profile=profiles.get(strategy_id)
            if profile is None:continue
            joined=join_regimes_without_lookahead([{"timestamp":point["closed_at"],"return":point["net_return"]} for point in curves.get(strategy_id,[])],labels)
            regimes=strategy_regime_profile(joined,minimum=cfg.intelligence_min_regime_samples)
            candidates.append({"strategy_id":strategy_id,"quality_score":profile["score"]["quality_score"],"max_drawdown":profile["metrics"]["max_drawdown"]["value"],"regimes":regimes})
        result=recommend(current,candidates,request.risk_limit)
        return {"items":result,"total":len(result),"market":request.market,"regime":current,"feature_as_of":row["as_of"],"feature_age_seconds":age,"mode":"historical" if request.as_of else "current","source_version":row["source_version"],"feature_sha256":row["sha256"],"methodology_version":"1.0.0","decision_support_only":True}

    @app.post("/internal/intelligence/market-features",status_code=202)
    def ingest_market_features(request:MarketFeatureIngestRequest,_:None=Depends(trusted_publisher)):
        try:
            digest=app.state.market_features.ingest(request.market,request.as_of,request.features,request.source_version);result=classify(request.features)
            app.state.market_features.record_label(request.market,request.as_of,result,request.as_of,result["version"])
        except ValueError as exc:raise HTTPException(422,str(exc))
        return {"accepted":True,"market":request.market,"as_of":request.as_of,"sha256":digest,"regime":result}

    @app.post("/internal/snapshots",status_code=202)
    async def ingest(snapshot:Snapshot, _:None=Depends(trusted_publisher), idempotency_key:str|None=Header(None)):
        if idempotency_key != snapshot.snapshot_id: raise HTTPException(400,"Idempotency key mismatch")
        if snapshot.item_count > cfg.max_snapshot_items: raise HTTPException(413,"Snapshot item limit exceeded")
        now=datetime.now(timezone.utc)
        if snapshot.generated_at>now+timedelta(minutes=5) or snapshot.source_watermark>now+timedelta(minutes=5):raise HTTPException(422,"Snapshot timestamp is in the future")
        if now-snapshot.source_watermark>timedelta(hours=cfg.snapshot_max_age_hours):raise HTTPException(422,"Snapshot source watermark is stale")
        try: snapshot.verified(); app.state.repository.promote(snapshot);app.state.profile_cache={"at":0.0,"profiles":None,"curves":None}
        except ValueError as exc: raise HTTPException(422,str(exc))
        return {"accepted":True,"snapshot_id":snapshot.snapshot_id,"items":snapshot.item_count}

    @app.post("/internal/intelligence/refresh",status_code=202)
    def refresh_intelligence_profiles(_:None=Depends(trusted_publisher)):
        app.state.profile_cache={"at":0.0,"profiles":None,"curves":None}
        app.state.strategy_cache=None
        cache_path=Path(cfg.local_intelligence_cache_path);cache_path=cache_path if cache_path.is_absolute() else Path(__file__).resolve().parents[1]/cache_path
        if cfg.data_backend=="sqlserver" and cache_path.exists():cache_path.unlink()
        return {"accepted":True,"reason":"operator-authorized evidence refresh"}

    @app.post("/internal/intelligence/privacy/purge",status_code=202)
    def purge_private_history(_:None=Depends(trusted_publisher)):
        try:return {"state":"completed","deleted":app.state.user_intelligence.purge_expired()}
        except RuntimeError as exc:raise HTTPException(503,str(exc))

    @app.get("/api/intelligence/warmup-status")
    def warmup_status():
        cache_path=Path(cfg.local_intelligence_cache_path);cache_path=cache_path if cache_path.is_absolute() else Path(__file__).resolve().parents[1]/cache_path
        return {"ready":app.state.profile_cache.get("profiles") is not None or (cfg.data_backend=="sqlserver" and cache_path.exists()),"catalog_ready":app.state.strategy_cache is not None,"mode":cfg.data_backend}

    @app.get("/internal/intelligence/operations")
    def intelligence_operations(_:None=Depends(trusted_publisher)):
        report=app.state.operations.report();snap=app.state.repository.current_snapshot() if app.state.repository else None
        if snap:app.state.operations.data_state("directory_snapshot",max(0,(datetime.now(timezone.utc)-snap.generated_at).total_seconds()),cfg.snapshot_max_age_hours*3600)
        return app.state.operations.report()

    @app.post("/internal/intelligence/releases/{version}/stage")
    def stage_release(version:str=ApiPath(pattern=r"^[A-Za-z0-9._-]{1,80}$"),evidence:dict|None=None,mode:str=Query("shadow",pattern=r"^(shadow|canary)$"),_:None=Depends(trusted_publisher)):
        return app.state.releases.stage(version,evidence or {},mode)

    @app.post("/internal/intelligence/releases/{version}/promote")
    def promote_release(version:str=ApiPath(pattern=r"^[A-Za-z0-9._-]{1,80}$"),_:None=Depends(trusted_publisher)):
        try:return app.state.releases.promote(version)
        except ValueError as exc:raise HTTPException(409,str(exc))

    @app.post("/internal/intelligence/releases/rollback")
    def rollback_release(_:None=Depends(trusted_publisher)):
        try:return app.state.releases.rollback()
        except ValueError as exc:raise HTTPException(409,str(exc))

    @app.get("/internal/intelligence/releases")
    def release_status(_:None=Depends(trusted_publisher)):return app.state.releases.status()

    no_store={"Cache-Control":"no-store, no-cache, must-revalidate, max-age=0","Pragma":"no-cache","Expires":"0"}

    @app.get("/")
    def directory(): return FileResponse(WEB/"index.html",headers=no_store)
    @app.get("/{screen}.html")
    def screen(screen:str):
        if screen not in {"strategy","compare","builder","intelligence","account","regimes","search"}: raise HTTPException(404)
        return FileResponse(WEB/f"{screen}.html",headers=no_store)
    @app.get("/assets/{name}")
    def asset(name:str):
        if name not in {"styles.css","tech-principle-theme.css","api-client.js","period-filter.js","equity-chart.js","button-feedback.js","theme-toggle.js"}: raise HTTPException(404)
        return FileResponse(WEB/name,headers=no_store)
    return app


app=create_app()
