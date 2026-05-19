# Task: Live Market Data - Storage Layer

## Status
TODO

## Source
- **Backlog**: `workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md`
- **Phase**: Phase 5 - Storage & Integration
- **Project**: Live Market Data Pipeline

## Description
Implement flexible storage layer supporting database, message queue, and file outputs.

## Objective
Enable configurable data persistence suitable for both live trading and historical analysis.

## Sub-tasks
- [ ] Create `src/storage/base.py` with:
  ```python
  class BaseStorage(ABC):
      @abstractmethod
      async def write(self, tick: MarketTick) -> bool
      @abstractmethod
      async def write_batch(self, ticks: List[MarketTick]) -> int
      @abstractmethod
      async def close(self) -> None
  ```
- [ ] Create `src/storage/postgres.py`:
  - Implement asyncpg connection
  - Batch inserts for performance
  - Create table schema for ticks
  - Support connection pooling
- [ ] Create `src/storage/sqlserver.py`:
  - Implement aioodbc connection
  - Compatible with existing trading system DB
- [ ] Create `src/storage/redis.py`:
  - Implement aioredis stream
  - Pub/sub for real-time consumers
  - TTL for automatic cleanup
- [ ] Create `src/storage/jsonfile.py`:
  - Rotating JSON files by date
  - Suitable for replay/backtesting
- [ ] Create storage factory based on config
- [ ] Add buffering for batch writes

## Verification Test
1. Postgres writer inserts tick successfully
2. Batch insert of 100 ticks completes < 100ms
3. Redis publishes tick to channel
4. JSON file rotates at midnight
5. Storage factory creates correct writer from config
6. Connection pool handles concurrent writes

## Completion Date
(To be filled)
