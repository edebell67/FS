# Task: Live Market Data - Central Orchestrator

## Status
TODO

## Source
- **Backlog**: `workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md`
- **Phase**: Phase 5 - Storage & Integration
- **Project**: Live Market Data Pipeline

## Description
Implement the central orchestrator that coordinates all components for continuous data ingestion.

## Objective
Create the main entry point that manages providers, polling, validation, and storage in a unified async workflow.

## Sub-tasks
- [ ] Create `src/core/orchestrator.py` with:
  ```python
  class MarketDataOrchestrator:
      def __init__(self, config: Config)
      async def start(self) -> None
      async def stop(self) -> None
      async def run_polling_loop(self) -> None
      async def process_tick(self, tick: MarketTick) -> None
  ```
- [ ] Implement polling scheduler:
  - Configurable interval per asset class
  - Staggered requests to avoid bursts
- [ ] Wire together components:
  - Provider registry
  - Failover manager
  - Rate limiter
  - Validator
  - Normalizer
  - Storage writer
- [ ] Implement graceful shutdown:
  - Catch SIGTERM/SIGINT
  - Drain pending writes
  - Close connections
- [ ] Support simulated mode (no real API calls)
- [ ] Create `main.py` entry point

## Verification Test
1. Orchestrator starts and polls configured symbols
2. Ticks flow through validation -> normalization -> storage
3. Failover triggers on provider error
4. Graceful shutdown completes within 5 seconds
5. Simulated mode works without API credentials
6. Logs show complete processing pipeline

## Completion Date
(To be filled)
