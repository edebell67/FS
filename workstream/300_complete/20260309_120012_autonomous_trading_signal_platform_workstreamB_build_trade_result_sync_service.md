# TASK B3: Build Trade Result Sync Service

**Workstream:** B - SYNC ENGINE
**Epic:** Autonomous Trading Signal Platform
**Status:** [x] Complete

## Source

- [Autonomous Trading Signal Platform](C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md)
- Prior dependency: `C:\Users\edebe\eds\workstream\300_complete\20260309_120010_workstreamB_create_sync_configuration.md`
- Prior dependency: `C:\Users\edebe\eds\workstream\300_complete\20260309_120003_workstreamA_create_online_database_schema.md`
- Prior dependency: `C:\Users\edebe\eds\workstream\300_complete\20260309_120001_workstreamA_define_publishable_trade_result_schema.md`

## Task Summary

Implement the `sync_trade_results_service` for Workstream B so closed local trades can be normalized into the publishable trade-result contract and upserted into the online PostgreSQL `trade_results` table.

## Context

- Existing sync configuration lives in `sync_config.json` and `sync_engine/config.py`.
- The online database contract is defined in `online_db_schema.sql`, where `trade_results` requires both `signal_id` and `strategy_id` foreign keys.
- The publishable trade-result contract is defined in `json/publishable_trade_schema.json`.
- The prior signal sync service in `sync_engine/signal_sync_service.py` establishes the repository/service pattern to follow.

## Plan

- [x] 1. Normalize this task file and confirm the source-to-target trade-result contract from the existing schema/config artifacts.
  - [x] Test: Review `sync_engine/config.py`, `sync_config.json`, `json/publishable_trade_schema.json`, and `online_db_schema.sql`; pass if the required source fields, target columns, and FK dependencies are documented in this file.
  - Evidence: Reviewed the four dependency artifacts and documented the required mapping in this file: publishable trade-result fields come from the trade schema/config, while online persistence additionally requires `signal_id` and `strategy_id` foreign keys and a closed-trade status.
- [x] 2. Implement `sync_trade_results_service` with source-row normalization, close-time fallback handling, and PostgreSQL upsert behavior using publishable fields only.
  - [x] Test: `python -m pytest tests/test_trade_result_sync_service.py -q`; pass if the sync service unit tests cover transformation and sync behavior successfully.
  - Evidence: Command passed with `3 passed in 0.14s`, covering closed-trade field mapping, close-time fallback selection, and service-level upsert orchestration across multiple rows.
- [x] 3. Run focused technical validation for the service entry point and package exports, then record results.
  - [x] Test: `python -c "from sync_engine import TradeResultSyncService; from sync_engine.trade_result_sync_service import build_publishable_trade_result; print(TradeResultSyncService.__name__ + ':ok')"`; pass if command prints `TradeResultSyncService:ok`.
  - Evidence: Command passed and printed `TradeResultSyncService:ok`; an additional regression command `python -m pytest tests/test_signal_sync_service.py tests/test_sync_config.py tests/test_trade_result_sync_service.py -q` also passed with `7 passed in 0.18s`.

## Implementation Log

- 2026-03-09 18:00:00+00:00 Read `skills/workstream-task-lifecycle/SKILL.md`, the assigned B3 task stub, and the completed dependency task files for sync configuration, online schema, and publishable trade-result schema.
- 2026-03-09 18:03:00+00:00 Reviewed `sync_engine/config.py`, `sync_config.json`, `json/publishable_trade_schema.json`, and `online_db_schema.sql`; confirmed the service must normalize closed-trade rows into the publishable contract while preserving the required online `signal_id` and `strategy_id` references.
- 2026-03-09 18:05:00+00:00 Replaced the stub task content with the required lifecycle structure and ordered checklist before editing code.
- 2026-03-09 18:09:00+00:00 Added `sync_engine/trade_result_sync_service.py` with normalized trade-result dataclass, close-time fallback mapping, PostgreSQL repository upsert logic, and `TradeResultSyncService.sync()` orchestration.
- 2026-03-09 18:10:00+00:00 Updated `sync_engine/__init__.py` exports and added `tests/test_trade_result_sync_service.py` for deterministic validation of mapping and sync behavior.
- 2026-03-09 18:11:00+00:00 Ran `python -m pytest tests/test_trade_result_sync_service.py -q`; pytest passed with `3 passed in 0.14s`.
- 2026-03-09 18:11:30+00:00 Ran the import smoke check; it passed with `TradeResultSyncService:ok`.
- 2026-03-09 18:12:00+00:00 Ran the combined sync-engine regression subset `python -m pytest tests/test_signal_sync_service.py tests/test_sync_config.py tests/test_trade_result_sync_service.py -q`; it passed with `7 passed in 0.18s`.

## Changes Made

- Added `sync_engine/trade_result_sync_service.py`
  - Added `PublishableTradeResultRecord` for the normalized online trade-result payload.
  - Added `build_publishable_trade_result()` to map local fields such as `guid`, `created`, `last_update`, `entry_price`, `latest_price`, and `net_return` into the online `trade_results` shape.
  - Added close-time fallback handling using `close_time`, `last_update`, `int_profit_time`, `max_net_return_time`, and `min_net_return_time`.
  - Added `PostgresTradeResultSyncRepository` with PostgreSQL upsert SQL keyed on `trade_result_id` and a forced closed status for synced rows.
  - Added `TradeResultSyncService.sync()` to orchestrate row normalization and repository upserts.
- Updated `sync_engine/__init__.py`
  - Exported `TradeResultSyncService`, `PublishableTradeResultRecord`, and `build_publishable_trade_result()`.
- Added `tests/test_trade_result_sync_service.py`
  - Covered direct field mapping, close-time fallback behavior, and multi-row sync orchestration against a fake repository.

## Validation

- Executed:
  - `python -m pytest tests/test_trade_result_sync_service.py -q`
  - `python -c "from sync_engine import TradeResultSyncService; from sync_engine.trade_result_sync_service import build_publishable_trade_result; print(TradeResultSyncService.__name__ + ':ok')"`
  - `python -m pytest tests/test_signal_sync_service.py tests/test_sync_config.py tests/test_trade_result_sync_service.py -q`
- Result:
  - Pass. `pytest` output: `3 passed in 0.14s`
  - Pass. Import smoke output: `TradeResultSyncService:ok`
  - Pass. Combined regression output: `7 passed in 0.18s`
- User verification not required because this task delivers backend sync service logic and automated test coverage rather than a user-facing interactive change.

## Risks/Notes

- The publishable schema requires `signal_id`, but some local closed-trade sources may not carry a durable signal identifier directly; the sync service must require that linkage from the caller rather than inventing it.
- The online `trade_results` schema includes additional operational columns such as `status` and `profit_loss_pct` that are outside the publishable schema; the sync service should populate only the minimum required persistence fields and let optional fields remain null unless provided.

## Completion Status

Complete as of 2026-03-09 18:12:00+00:00. All checklist items, tests, and evidence are recorded.
