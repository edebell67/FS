# Task: Live Market Data - Provider Adapter Base Class

## Status
TODO

## Source
- **Backlog**: `workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md`
- **Phase**: Phase 2 - Provider Infrastructure
- **Project**: Live Market Data Pipeline

## Description
Create the abstract base class for all provider adapters using the plug-in pattern.

## Objective
Define a consistent interface that all data providers must implement, enabling easy addition of new providers.

## Sub-tasks
- [ ] Create `src/providers/base.py` with:
  ```python
  class BaseProvider(ABC):
      name: str
      supported_assets: List[AssetClass]

      @abstractmethod
      async def connect(self) -> bool

      @abstractmethod
      async def disconnect(self) -> None

      @abstractmethod
      async def fetch_tick(self, symbol: str) -> MarketTick

      @abstractmethod
      async def fetch_batch(self, symbols: List[str]) -> List[MarketTick]

      @abstractmethod
      async def health_check(self) -> ProviderStatus
  ```
- [ ] Add rate limit awareness methods:
  - `get_rate_limit()` -> returns limits
  - `get_remaining_calls()` -> returns remaining
- [ ] Add latency tracking
- [ ] Add error handling hooks
- [ ] Create `ProviderRegistry` for dynamic registration

## Verification Test
1. Create mock provider implementing `BaseProvider`
2. Verify all abstract methods must be implemented
3. Registry can register and retrieve providers
4. Provider reports correct `supported_assets`

## Completion Date
(To be filled)
