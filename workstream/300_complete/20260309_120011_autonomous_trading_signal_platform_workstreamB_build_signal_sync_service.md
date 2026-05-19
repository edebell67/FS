# TASK B2: Build Signal Sync Service

**Workstream:** B - SYNC ENGINE
**Epic:** Autonomous Trading Signal Platform
**Status:** [x] Complete

## Source

- [Autonomous Trading Signal Platform](C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md)
- Prior dependency: `C:\Users\edebe\eds\workstream\300_complete\20260309_120010_workstreamB_create_sync_configuration.md`
- Prior dependency: `C:\Users\edebe\eds\workstream\300_complete\20260309_120003_workstreamA_create_online_database_schema.md`

## Task Summary

Implement the `sync_signals_service` for Workstream B so publishable signal rows can be transformed from local source records into the online PostgreSQL `signals` table, including the required strategy resolution needed by the online schema.

## Context

- Existing sync configuration lives in `sync_config.json` and `sync_engine/config.py`.
- The online database contract is defined in `online_db_schema.sql`, where `signals.strategy_id` is required and references `strategies(strategy_id)`.
- The publishable source contract for signals is defined in `json/publishable_signal_schema.json`.
- No existing signal sync service implementation exists yet under `sync_engine/`.

## Plan

- [x] 1. Normalize this task file and confirm the service contract from the existing schema/config artifacts.
  - [x] Test: Review `sync_engine/config.py`, `sync_config.json`, `json/publishable_signal_schema.json`, and `online_db_schema.sql`; pass if the required source fields, target columns, and strategy dependency are documented in this file.
  - Evidence: Reviewed the four dependency artifacts and documented the required mapping in this file: publishable source fields come from the signal schema/config, `signals.strategy_id` depends on an existing or newly upserted `strategies` row, and only publishable fields are included in the sync payload.
- [x] 2. Implement `sync_signals_service` with mapping, strategy upsert support, and signal upsert behavior using publishable fields only.
  - [x] Test: `python -m pytest tests/test_signal_sync_service.py -q`; pass if the sync service unit tests cover transformation and sync behavior successfully.
  - Evidence: Command passed with `3 passed in 0.27s`, covering local-row transformation, default strategy/timeframe resolution, and repository call ordering for strategy + signal upserts.
- [x] 3. Run focused technical validation for the service entry point and package exports, then record results.
  - [x] Test: `python -c "from sync_engine import SignalSyncService; from sync_engine.signal_sync_service import build_publishable_signal, build_strategy_record; print(SignalSyncService.__name__ + ':ok')"`; pass if command prints `SignalSyncService:ok`.
  - Evidence: Command passed and printed `SignalSyncService:ok`, confirming the package export and service import path are valid.

## Implementation Log

- 2026-03-09 17:33:00+00:00 Read `skills/workstream-task-lifecycle/SKILL.md`, the assigned B2 task stub, and existing Workstream A/B dependency files.
- 2026-03-09 17:35:00+00:00 Reviewed `sync_engine/config.py`, `sync_config.json`, `json/publishable_signal_schema.json`, and `online_db_schema.sql`; confirmed the service must map publishable signal rows and resolve a required `strategy_id` for the online `signals` table.
- 2026-03-09 17:39:00+00:00 Replaced the stub task content with the required lifecycle structure and ordered checklist before editing code.
- 2026-03-09 17:42:00+00:00 Added `sync_engine/signal_sync_service.py` with source-row normalization, strategy record derivation, PostgreSQL repository methods, and a `SignalSyncService.sync()` orchestration entry point.
- 2026-03-09 17:43:00+00:00 Updated `sync_engine/__init__.py` exports and added `tests/test_signal_sync_service.py` for deterministic unit validation of signal mapping and sync call flow.
- 2026-03-09 17:44:00+00:00 Ran `python -m pytest tests/test_signal_sync_service.py -q`; pytest passed with `3 passed in 0.27s`.
- 2026-03-09 17:45:00+00:00 Ran the package import smoke check; it passed with `SignalSyncService:ok`.

## Changes Made

- Added `sync_engine/signal_sync_service.py`
  - Added `StrategyRecord` and `PublishableSignalRecord` dataclasses for normalized sync payloads.
  - Added `build_strategy_record()` to derive the required online strategy identity from publishable/local fields.
  - Added `build_publishable_signal()` to map local fields such as `guid`, `created`, `product`, `signal`, `entry_price`, `target_profit`, and `target_loss` into the online signal shape.
  - Added confidence normalization logic that converts schema-style `0..1` confidence values into the online DB's `0..100` representation and preserves already-percent values.
  - Added `PostgresSignalSyncRepository` with strategy upsert and signal upsert SQL for the online PostgreSQL schema.
  - Added `SignalSyncService.sync()` to orchestrate row transformation, strategy resolution, and signal upsert execution.
- Updated `sync_engine/__init__.py`
  - Exported `SignalSyncService`, `StrategyRecord`, `PublishableSignalRecord`, `build_strategy_record()`, and `build_publishable_signal()`.
- Added `tests/test_signal_sync_service.py`
  - Covered source-shape mapping, default timeframe resolution, confidence normalization, and sync orchestration against a fake repository.

## Validation

- Executed:
  - `python -m pytest tests/test_signal_sync_service.py -q`
  - `python -c "from sync_engine import SignalSyncService; from sync_engine.signal_sync_service import build_publishable_signal, build_strategy_record; print(SignalSyncService.__name__ + ':ok')"`
- Result:
  - Pass. `pytest` output: `3 passed in 0.27s`
  - Pass. Import smoke output: `SignalSyncService:ok`
- User verification not required because this task delivers backend sync service logic and test coverage rather than a user-facing interactive change.

## Risks/Notes

- The publishable signal schema exposes `strategy` but not `strategy_id`, while the online `signals` table requires `strategy_id`; the service therefore needs a deterministic strategy-key derivation or caller-provided strategy identity to keep inserts valid.
- The implemented service resolves this by upserting `strategies` on the schema's natural key `(strategy_name, asset, timeframe)` and then using the returned UUID for `signals.strategy_id`.
- The online schema stores `confidence` as a `0..100` numeric value while the publishable schema example uses `0..1`; this implementation treats `<= 1` as normalized input and scales it to percent before persistence.

## Completion Status

Complete as of 2026-03-09 17:45:00+00:00. All checklist items, tests, and evidence are recorded.
