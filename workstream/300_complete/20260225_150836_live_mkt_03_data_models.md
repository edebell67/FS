# Task: Live Market Data - Core Data Models

## Status
TODO

## Source
- **Backlog**: `workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md`
- **Phase**: Phase 1 - Foundation
- **Project**: Live Market Data Pipeline

## Description
Define the normalized data schema and Pydantic models for all market data types.

## Objective
Create a unified data structure that all providers normalize to, ensuring consistent downstream processing.

## Sub-tasks
- [ ] Create `src/core/models.py` with:
  ```python
  class MarketTick(BaseModel):
      symbol: str
      asset_class: Literal["futures", "metals", "energy", "crypto", "stocks"]
      exchange: str
      timestamp: datetime  # UTC
      bid: Optional[float]
      ask: Optional[float]
      last: float
      volume: Optional[int]
      source: str  # provider name
      latency_ms: int
  ```
- [ ] Create `AssetClass` enum
- [ ] Create `ProviderStatus` model for health tracking
- [ ] Create `ValidationResult` model for rejected ticks
- [ ] Add serialization helpers (to_dict, to_json)
- [ ] Add factory method `from_provider_response()`

## Verification Test
1. Create `MarketTick` with valid data - should pass
2. Create `MarketTick` with negative price - should fail validation
3. Serialize to JSON and back - should be identical
4. `asset_class` with invalid value should raise error

## Completion Date
(To be filled)
