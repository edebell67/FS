"""
FastAPI server for market prices.
DB-free - serves from in-memory cache only.

Endpoints match existing vw_000_* contract for drop-in replacement.
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from inspect import signature
from typing import Any

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.routing import Router

try:
    from .price_cache import cache
    from .fetchers import CryptoFetcher, FuturesFetcher, FileForexFetcher, FileForexSimFetcher, IndexFetcher
except ImportError:
    from price_cache import cache
    from fetchers import CryptoFetcher, FuturesFetcher, FileForexFetcher, FileForexSimFetcher, IndexFetcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def local_timestamp() -> str:
    """Return an ISO timestamp in the host machine's local timezone."""
    return datetime.now().astimezone().isoformat()

# Initialize fetchers
crypto_fetcher = CryptoFetcher(cache)
futures_fetcher = FuturesFetcher(cache)
forex_fetcher = FileForexFetcher(cache)
forex_sim_fetcher = FileForexSimFetcher(cache)
index_fetcher = IndexFetcher(cache)

# [V20260413_1445] Symbols to exclude from futures and include in index endpoint
INDEX_SYMBOLS = {'es', 'mes', 'nq', 'mnq', 'rty', 'm2k'}

# Starlette 1.0 removed the deprecated on_startup/on_shutdown kwargs, but
# FastAPI 0.110 still passes them through even when they are None.
def _patch_starlette_router_init_for_fastapi() -> None:
    params = signature(Router.__init__).parameters
    if "on_startup" in params:
        return

    original_init = Router.__init__

    def compatible_init(
        self,
        routes=None,
        redirect_slashes: bool = True,
        default=None,
        on_startup=None,
        on_shutdown=None,
        lifespan=None,
        *,
        middleware=None,
    ) -> None:
        if on_startup or on_shutdown:
            raise RuntimeError(
                "Installed Starlette does not support legacy startup/shutdown "
                "handlers. Use lifespan handlers instead."
            )
        original_init(
            self,
            routes=routes,
            redirect_slashes=redirect_slashes,
            default=default,
            lifespan=lifespan,
            middleware=middleware,
        )

    Router.__init__ = compatible_init


_patch_starlette_router_init_for_fastapi()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Start and stop all fetchers with the app lifecycle."""
    logger.info("Starting market price fetchers...")
    crypto_fetcher.start()
    futures_fetcher.start()
    forex_fetcher.start()
    forex_sim_fetcher.start()
    index_fetcher.start()
    logger.info("All fetchers started")

    try:
        yield
    finally:
        logger.info("Stopping fetchers...")
        crypto_fetcher.stop()
        futures_fetcher.stop()
        forex_fetcher.stop()
        forex_sim_fetcher.stop()
        index_fetcher.stop()
        logger.info("All fetchers stopped")


# FastAPI app
app = FastAPI(
    title="Market Prices API",
    description="DB-free market price delivery - crypto, futures, forex",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# API Endpoints - Match existing vw_000_* contract
# ============================================================================

@app.get("/api/vw_000_crypto_quotes")
async def get_crypto_quotes(db: str = Query(None, description="Ignored - no DB needed")):
    """
    Get latest crypto quotes.
    Compatible with existing API contract.
    """
    quotes = cache.get_crypto()
    return {"data": quotes}


@app.get("/api/vw_000_futures_quotes")
async def get_futures_quotes(db: str = Query(None, description="Ignored - no DB needed")):
    """
    Get latest futures quotes (excluding indices).
    Compatible with existing API contract.
    """
    quotes = cache.get_futures()
    # Filter out index symbols
    filtered = [q for q in quotes if q.get('code', '').lower() not in INDEX_SYMBOLS]
    return {"data": filtered}


@app.get("/api/vw_000_index_quotes")
async def get_index_quotes(db: str = Query(None, description="Ignored - no DB needed")):
    """
    Get latest index quotes.
    [V20260413_1445] New endpoint for ES, MES, NQ, MNQ, RTY, M2K.
    """
    quotes = cache.get_indices()
    return {"data": quotes}


@app.get("/api/vw_000_fx_quotes")
async def get_forex_quotes(db: str = Query(None, description="Ignored - no DB needed")):
    """
    Get latest forex quotes.
    Compatible with existing API contract.
    """
    quotes = cache.get_forex()
    return {"data": quotes}


@app.get("/api/vw_000_fx_quotes_sim")
async def get_forex_quotes_sim(db: str = Query(None, description="Ignored - no DB needed")):
    """
    Get latest simulation forex quotes.
    [V20260424_2330] New endpoint for Z:\algo_forex\prices\forex_price_sim.json
    """
    quotes = cache.get_forex_sim()
    return {"data": quotes}


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/api/health")
async def health_check():
    """System health check."""
    stats = cache.get_stats()

    return {
        "status": "healthy",
        "timestamp": local_timestamp(),
        "cache": stats,
        "fetchers": {
            "crypto": crypto_fetcher.get_status(),
            "futures": futures_fetcher.get_status(),
            "forex": forex_fetcher.get_status(),
            "index": index_fetcher.get_status()
        }
    }


@app.get("/api/status")
async def get_status():
    """Detailed status of all fetchers."""
    return {
        "crypto": crypto_fetcher.get_status(),
        "futures": futures_fetcher.get_status(),
        "forex": forex_fetcher.get_status(),
        "index": index_fetcher.get_status(),
        "cache": cache.get_stats()
    }


@app.get("/api/quotes/all")
async def get_all_quotes():
    """Get all quotes (not part of original contract, convenience endpoint)."""
    return {
        "data": {
            "crypto": cache.get_crypto(),
            "futures": cache.get_futures(),
            "forex": cache.get_forex(),
            "indices": cache.get_indices()
        },
        "timestamp": local_timestamp()
    }


# ============================================================================
# Root
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "service": "Market Prices API",
        "version": "1.0.0",
        "endpoints": [
            "/api/vw_000_crypto_quotes",
            "/api/vw_000_futures_quotes",
            "/api/vw_000_index_quotes",
            "/api/vw_000_fx_quotes",
            "/api/health",
            "/api/status",
            "/api/quotes/all"
        ],
        "note": "DB-free - no database parameter required"
    }
