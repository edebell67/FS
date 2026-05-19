# Task: Live Market Data - Crypto Provider Adapter

## Status
TODO

## Source
- **Backlog**: `workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md`
- **Phase**: Phase 4 - Provider Implementations
- **Project**: Live Market Data Pipeline

## Description
Implement provider adapters for cryptocurrency spot prices (BTC, ETH, major altcoins).

## Objective
Enable live crypto price feeds from multiple exchanges with redundancy.

## Sub-tasks
- [ ] Create `src/providers/crypto/coinbase.py`:
  - Implement `BaseProvider` interface
  - Use Coinbase Pro API (free tier)
  - Support: BTC, ETH, major pairs
  - Handle rate limits (10 req/sec)
- [ ] Create `src/providers/crypto/binance.py`:
  - Implement `BaseProvider` interface
  - Use Binance public API
  - Support: BTC, ETH, altcoins
  - Handle rate limits (1200 req/min)
- [ ] Create `src/providers/crypto/kraken.py` (backup):
  - Implement `BaseProvider` interface
  - Use Kraken public API
- [ ] Add WebSocket support (stretch):
  - Real-time price streams
  - Auto-reconnect on disconnect
- [ ] Create symbol mapping for each provider
- [ ] Add unit tests with mocked responses

## Verification Test
1. Coinbase provider fetches BTC/USD tick
2. Binance provider fetches ETH/USDT tick
3. Response normalizes to `MarketTick` correctly
4. Rate limiter prevents over-calling
5. Provider failover works: Coinbase -> Binance -> Kraken
6. Health check returns accurate status

## Completion Date
(To be filled)
