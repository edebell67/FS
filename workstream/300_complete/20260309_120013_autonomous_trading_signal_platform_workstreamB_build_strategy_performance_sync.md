# TASK B4: Build Strategy Performance Sync

**Workstream:** B - SYNC ENGINE
**Epic:** Autonomous Trading Signal Platform
**Status:** [x] Complete

## Source

- [Autonomous Trading Signal Platform](C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md)
- Prior dependency: `C:\Users\edebe\eds\workstream\300_complete\20260309_120010_workstreamB_create_sync_configuration.md`
- Prior dependency: `C:\Users\edebe\eds\workstream\300_complete\20260309_120003_workstreamA_create_online_database_schema.md`
- Prior dependency: `C:\Users\edebe\eds\workstream\300_complete\20260309_120002_workstreamA_define_strategy_summary_schema.md`

## Task Summary

Implement the `sync_strategy_performance_service` for Workstream B so publishable strategy summary rows can be normalized from local performance aggregates and upserted into the online PostgreSQL `strategy_performance` table.

## Context

- Existing sync configuration lives in `sync_config.json` and `sync_engine/config.py`.
- The online database contract is defined in `online_db_schema.sql`, where `strategy_performance` requires an existing `strategy_id` foreign key and a unique `(strategy_id, performance_date)` row.
- The publishable source contract is defined in `json/strategy_schema.json`.
- The prior sync services in `sync_engine/signal_sync_service.py` and `sync_engine/trade_result_sync_service.py` establish the repository/service pattern to follow.

## Plan

- [x] 1. Normalize this task file and confirm the source-to-target strategy-performance contract from the existing schema/config artifacts.
  - [x] Test: Review `sync_engine/config.py`, `sync_config.json`, `json/strategy_schema.json`, and `online_db_schema.sql`; pass if the required source fields, target columns, and FK/date-key dependencies are documented in this file.
  - Evidence: Reviewed the four dependency artifacts and documented the required mapping in this file: publishable summary fields come from the strategy schema/config, online persistence additionally requires a strategy FK and `performance_date`, and rows are upserted on `(strategy_id, performance_date)`.
- [x] 2. Implement `sync_strategy_performance_service` with source-row normalization, performance-date handling, strategy upsert support, and PostgreSQL upsert behavior using publishable fields only.
  - [x] Test: `python -m pytest tests/test_strategy_performance_sync_service.py -q`; pass if the sync service unit tests cover transformation and sync behavior successfully.
  - Evidence: Command passed with `3 passed in 0.31s`, covering direct field mapping, fallback field handling, and service-level strategy plus performance upsert orchestration.
- [x] 3. Run focused technical validation for the service entry point and package exports, then record results.
  - [x] Test: `python -c "from sync_engine import StrategyPerformanceSyncService; from sync_engine.strategy_performance_sync_service import build_publishable_strategy_performance; print(StrategyPerformanceSyncService.__name__ + ':ok')"`; pass if command prints `StrategyPerformanceSyncService:ok`.
  - Evidence: Command passed and printed `StrategyPerformanceSyncService:ok`; an additional regression command `python -m pytest tests/test_signal_sync_service.py tests/test_trade_result_sync_service.py tests/test_strategy_performance_sync_service.py tests/test_sync_config.py -q` also passed with `10 passed in 0.30s`.

## Implementation Log

- 2026-03-09 17:26:54+00:00 Read `skills/workstream-task-lifecycle/SKILL.md`, the assigned B4 task stub, and the completed dependency task files for sync configuration, online schema, and strategy summary schema.
- 2026-03-09 17:26:54+00:00 Reviewed `sync_engine/config.py`, `sync_config.json`, `json/strategy_schema.json`, and `online_db_schema.sql`; confirmed the service must normalize publishable summary rows while resolving a required `strategy_id` FK and a daily `performance_date` key.
- 2026-03-09 17:26:54+00:00 Replaced the stub task content with the required lifecycle structure and ordered checklist before editing code.
- 2026-03-09 17:30:00+00:00 Added `sync_engine/strategy_performance_sync_service.py` with normalized strategy-performance dataclass, strategy resolution, performance-date fallback handling, and PostgreSQL upsert logic keyed on `(strategy_id, performance_date)`.
- 2026-03-09 17:31:00+00:00 Updated `sync_engine/__init__.py` exports and added `tests/test_strategy_performance_sync_service.py` for deterministic validation of mapping and sync orchestration.
- 2026-03-09 17:31:30+00:00 Ran the first focused pytest command, found a missing `timeframe` fallback in the new service, and corrected the implementation to default from the shared `StrategyRecord` logic.
- 2026-03-09 17:32:00+00:00 Re-ran `python -m pytest tests/test_strategy_performance_sync_service.py -q`; pytest passed with `3 passed in 0.31s`.
- 2026-03-09 17:32:10+00:00 Ran the import smoke check; it passed with `StrategyPerformanceSyncService:ok`.
- 2026-03-09 17:32:20+00:00 Ran the combined sync-engine regression subset `python -m pytest tests/test_signal_sync_service.py tests/test_trade_result_sync_service.py tests/test_strategy_performance_sync_service.py tests/test_sync_config.py -q`; it passed with `10 passed in 0.30s`.

## Changes Made

- Added `sync_engine/strategy_performance_sync_service.py`
  - Added `PublishableStrategyPerformanceRecord` for normalized strategy summary sync payloads.
  - Added `build_publishable_strategy_performance()` to map local summary fields such as `strategy_name`, `asset`, `timeframe`, `win_rate`, `profit_factor`, `drawdown`, and `trade_count` into the online `strategy_performance` shape.
  - Added fallback handling for `performance_date` using `performance_date`, `report_date`, `as_of`, `snapshot_date`, `date`, `timestamp`, `created`, or `last_update`.
  - Added optional support for persisting `total_profit_loss` and `avg_profit_loss` when present, while leaving them null/default otherwise.
  - Added `PostgresStrategyPerformanceSyncRepository` with strategy upsert and `strategy_performance` upsert SQL keyed on `(strategy_id, performance_date)`.
  - Added `StrategyPerformanceSyncService.sync()` to orchestrate row normalization, strategy resolution, and performance upserts.
- Updated `sync_engine/__init__.py`
  - Exported `StrategyPerformanceSyncService`, `PublishableStrategyPerformanceRecord`, and `build_publishable_strategy_performance()`.
- Added `tests/test_strategy_performance_sync_service.py`
  - Covered direct field mapping, fallback field handling, and service orchestration against a fake repository.

## Validation

- Executed:
  - Lifecycle step 1 artifact review as documented above.
  - `python -m pytest tests/test_strategy_performance_sync_service.py -q`
  - `python -c "from sync_engine import StrategyPerformanceSyncService; from sync_engine.strategy_performance_sync_service import build_publishable_strategy_performance; print(StrategyPerformanceSyncService.__name__ + ':ok')"`
  - `python -m pytest tests/test_signal_sync_service.py tests/test_trade_result_sync_service.py tests/test_strategy_performance_sync_service.py tests/test_sync_config.py -q`
- Result:
  - Pass. Required mapping, FK, and unique-key behavior documented in this file.
  - Pass. Focused pytest output: `3 passed in 0.31s`
  - Pass. Import smoke output: `StrategyPerformanceSyncService:ok`
  - Pass. Combined regression output: `10 passed in 0.30s`
- User verification not required because this task delivers backend sync service logic and automated test coverage rather than a user-facing interactive change.

## Risks/Notes

- The publishable strategy summary schema includes a public `strategy_id` string field, while the online table requires the internal `strategies.strategy_id` UUID foreign key; the sync service must therefore resolve or upsert the online strategy using a deterministic natural key rather than inserting the public identifier directly.
- The online `strategy_performance` table requires `performance_date`, `total_profit_loss`, and optionally `avg_profit_loss`, but the publishable schema only guarantees summary metrics; the service should derive a safe `performance_date` from source metadata and leave non-publishable optional metrics null/default unless provided.

## Completion Status

Complete as of 2026-03-09 17:32:30+00:00. All checklist items, tests, and evidence are recorded.
