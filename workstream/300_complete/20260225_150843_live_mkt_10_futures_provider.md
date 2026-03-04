# Task: Live Market Data - Futures/Metals/Energy Provider Adapter

## Status
TODO

## Source
- **Backlog**: `workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md`
- **Phase**: Phase 4 - Provider Implementations
- **Project**: Live Market Data Pipeline

## Description
Implement provider adapters for futures (financials, metals, energy) from CME/COMEX/NYMEX.

## Objective
Enable live futures price feeds for T-Bills, Treasury Bonds, Gold, Silver, Crude Oil, Brent.

## Sub-tasks
- [ ] Research available free/low-cost futures data APIs:
  - Yahoo Finance (delayed)
  - Alpha Vantage (limited)
  - Quandl/Nasdaq Data Link
  - Tradier (requires account)
  - Interactive Brokers (if available)
- [ ] Create `src/providers/futures/yahoo.py`:
  - Implement `BaseProvider` interface
  - Delayed data (15-20 min) acceptable for some use cases
  - Support: GC (Gold), SI (Silver), CL (Crude)
- [ ] Create `src/providers/futures/alphavantage.py`:
  - Implement `BaseProvider` interface
  - 5 calls/min free tier
  - Support: Commodities, some futures
- [ ] Create `src/providers/futures/tradingview.py` (if API available):
  - Scraping fallback if no API
- [ ] Handle futures contract month codes (Z24, F25, etc.)
- [ ] Create symbol mapping: `GC=F` -> `GC`
- [ ] Add unit tests with mocked responses

## Verification Test
1. Provider fetches Gold (GC) futures price
2. Provider fetches Crude Oil (CL) price
3. Provider fetches Treasury futures (if available)
4. Contract month codes handled correctly
5. Response normalizes to `MarketTick`
6. Failover between providers works

## Completion Date
(To be filled)
