# Task: Live Market Data - Stocks Provider Adapter

## Status
TODO

## Source
- **Backlog**: `workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md`
- **Phase**: Phase 4 - Provider Implementations
- **Project**: Live Market Data Pipeline

## Description
Implement provider adapters for large-cap US stocks and global equities.

## Objective
Enable live equity price feeds for high-volume institutional-grade stocks.

## Sub-tasks
- [ ] Create `src/providers/stocks/finnhub.py`:
  - Implement `BaseProvider` interface
  - Free tier: 60 calls/min
  - Support: US stocks, some global
  - Real-time for US market hours
- [ ] Create `src/providers/stocks/polygon.py`:
  - Implement `BaseProvider` interface
  - Free tier available
  - Support: US equities
- [ ] Create `src/providers/stocks/alphavantage.py`:
  - Reuse/extend from futures provider
  - Support: Global stocks
- [ ] Create `src/providers/stocks/yahoo.py`:
  - Delayed data fallback
  - Wide coverage
- [ ] Define target stock list:
  - AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA
  - SPY, QQQ (ETFs)
- [ ] Handle pre-market/after-hours pricing
- [ ] Add unit tests with mocked responses

## Verification Test
1. Finnhub fetches AAPL real-time price
2. Polygon fetches MSFT price
3. Yahoo fallback works when others fail
4. Response normalizes to `MarketTick`
5. Pre-market/after-hours data handled
6. Rate limits respected across providers

## Completion Date
(To be filled)
