# Task: Live Market Data - Normalization Layer

## Status
TODO

## Source
- **Backlog**: `workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md`
- **Phase**: Phase 3 - Data Quality
- **Project**: Live Market Data Pipeline

## Description
Implement data normalization to convert provider-specific responses into unified schema.

## Objective
Transform heterogeneous provider data formats into a consistent `MarketTick` structure.

## Sub-tasks
- [ ] Create `src/middleware/normalizer.py` with:
  ```python
  class TickNormalizer:
      def normalize(self, raw_data: Dict, provider: str, symbol: str) -> MarketTick
      def map_symbol(self, provider_symbol: str, provider: str) -> str
      def map_asset_class(self, symbol: str) -> AssetClass
      def normalize_timestamp(self, ts: Any) -> datetime
  ```
- [ ] Implement provider-specific normalizers:
  - Each provider may have different field names
  - Handle: price/last/close variations
  - Handle: timestamp formats (epoch, ISO, custom)
- [ ] Create symbol mapping registry:
  - `BTC-USD` (Coinbase) -> `BTCUSD` (standard)
  - `GCZ24` (CME) -> `GC` (standard)
- [ ] Handle missing optional fields (bid, ask, volume)
- [ ] Add latency calculation (now - tick timestamp)
- [ ] Validate normalized output against schema

## Verification Test
1. Coinbase BTC response normalizes to `MarketTick`
2. CME Gold futures response normalizes correctly
3. Missing `bid` field results in `None`, not error
4. Epoch timestamp converts to UTC datetime
5. Symbol mapping works: `BTC-USD` -> `BTCUSD`
6. Latency is calculated correctly

## Completion Date
(To be filled)
