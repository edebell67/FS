# Market Prices - DB-Free API Delivery

## Project
marketPrices

## Task ID
20260226_114634_marketPrices_db_free_api_delivery

## Summary
Create a standalone market price API service that delivers crypto, futures, and forex prices without database dependency. Enables migration from current DB-reliant system to a resilient in-memory architecture.

## Problem Statement
Current market price delivery relies on SQL Server database which crashes frequently, causing price feed outages. Need a separate process that:
- Fetches live prices from upstream providers (Binance, Yahoo, existing forex feed)
- Caches in-memory (no DB writes required for delivery)
- Exposes same API contract as current `vw_000_*_quotes` endpoints
- Runs independently - can be migrated to without disrupting existing system

## Requirements

### Functional
1. **Price Sources**
   - Crypto: Binance API (BTC, ETH, SOL, XRP, AVAX, ADA, DOGE)
   - Futures: Yahoo Finance (ES, NQ, GC, SI, CL, BZ, NG)
   - Forex: Consume from existing `http://127.0.0.1:8001/api/vw_000_fx_quotes?db=tradedb` OR direct feed

2. **API Endpoints** (same contract as current)
   ```
   GET /api/vw_000_crypto_quotes  -> returns latest crypto quotes
   GET /api/vw_000_futures_quotes -> returns latest futures quotes
   GET /api/vw_000_fx_quotes      -> returns latest forex quotes (passthrough or cached)
   GET /api/health                -> health check
   ```

3. **Response Format** (match existing)
   ```json
   {
     "data": [
       {"id": 1, "timestamp": "ISO8601", "code": "btc", "type": "C", "bid": 68000.00, "ask": 68010.00},
       ...
     ]
   }
   ```

4. **Polling Intervals**
   - Crypto: 5 seconds
   - Futures: 30 seconds (Yahoo rate limit safe)
   - Forex: passthrough or 5 seconds

### Non-Functional
- **No database dependency** - pure in-memory cache
- **Fast startup** - ready within 10 seconds
- **Graceful degradation** - if one source fails, others continue
- **Configurable port** - default 8002 (parallel to existing 8001)
- **Logging** - structured JSON logs

## Technical Design

### Architecture
```
┌─────────────────────────────────────────────────────────┐
│                  Market Price API (port 8002)           │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Crypto      │  │ Futures     │  │ Forex       │     │
│  │ Fetcher     │  │ Fetcher     │  │ Fetcher     │     │
│  │ (Binance)   │  │ (Yahoo)     │  │ (Passthru)  │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│         ▼                ▼                ▼             │
│  ┌─────────────────────────────────────────────────┐   │
│  │              In-Memory Price Cache              │   │
│  │  { "btc": {...}, "eth": {...}, "es": {...} }    │   │
│  └─────────────────────────────────────────────────┘   │
│                          │                              │
│                          ▼                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │              FastAPI REST Endpoints             │   │
│  │  /api/vw_000_crypto_quotes                      │   │
│  │  /api/vw_000_futures_quotes                     │   │
│  │  /api/vw_000_fx_quotes                          │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Components
1. **price_cache.py** - Thread-safe in-memory cache with TTL
2. **fetchers/** - Background threads for each data source
3. **api.py** - FastAPI app exposing endpoints
4. **main.py** - Entry point, starts fetchers + API

### Migration Path
1. Deploy on port 8002 alongside existing system
2. Test endpoints return same format
3. Update consumers to use 8002
4. Decommission DB-based feeders

## Acceptance Criteria
- [ ] API returns crypto quotes within 10s of startup
- [ ] API returns futures quotes within 35s of startup
- [ ] Response format matches existing `vw_000_*` endpoints exactly
- [ ] No database connection required
- [ ] Survives source outages gracefully (returns stale data with warning)
- [ ] Health endpoint reports status of each fetcher
- [ ] Configurable via environment variables or config file

## Dependencies
- Python 3.11+
- FastAPI
- uvicorn
- aiohttp (for async fetching)
- No pyodbc/database drivers required

## Estimated Effort
Small-Medium (4-6 hours implementation)

## Priority
High - addresses production stability issue

## Notes
- Can reuse fetcher logic from `live_market_data/feeders/`
- Consider WebSocket streaming as future enhancement
- Optional: persist cache to JSON file for faster restarts
