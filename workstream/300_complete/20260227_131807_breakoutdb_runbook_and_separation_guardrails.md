# Task: BreakoutDB runbook and separation guardrails (20260227_131807_breakoutdb_runbook_and_separation_guardrails)

## Status
COMPLETE

## Source
- backlog: `workstream/000_backlog/20260227_131612_BreakoutDB_fs_to_db_full_parity_migration.md`
- project: `breakoutdb`

## Task Summary
Document startup/testing runbook for DB variant and implement guardrails to prevent accidental dependencies on `fs/json`.

## Context
- target docs/config/scripts: `TradeApps/breakout/DB`

## Objective
Operationalize DB variant with clear instructions and enforceable separation checks.

## Sub-tasks
- [x] Create DB run/start/test instructions.
- [x] Add environment/config prerequisites for PostgreSQL.
- [x] Add automated grep/check to fail on `fs/json` references in DB.
- [x] Document maintenance expectations for keeping variants separate.

## Verification Test
1. Execute runbook from clean shell/session.
2. Run separation guardrail checks.
3. Confirm DB variant starts and tests pass using only PostgreSQL dependencies.

## Implementation Log
- `2026-02-27 13:18:07` Task created from BreakoutDB backlog decomposition.
- `2026-02-27 13:43:35` Added DB runbook (`README_DB.md`) with setup/start/backfill procedures.
- `2026-02-27 13:43:35` Added `.env.example` with DB configuration contract.
- `2026-02-27 13:43:35` Added `check_no_fs_refs.ps1` guardrail script and executed it successfully.
- `2026-02-27 15:22:25` Added `DB/.env` and validated runtime API calls against existing PostgreSQL.

## Changes Made
- Added: `TradeApps/breakout/DB/README_DB.md`
- Added: `TradeApps/breakout/DB/.env.example`
- Added: `TradeApps/breakout/DB/check_no_fs_refs.ps1`
- Added: `TradeApps/breakout/DB/.env`

## Validation
- `pwsh -File TradeApps/breakout/DB/check_no_fs_refs.ps1 -Root TradeApps/breakout/DB` passed.
- Runtime verification from credentialed environment:
  - DB connection test returned `('tradedb2', 'postgres')`
  - `GET /api/dates?mode=live` and `GET /api/trades?mode=live&date=2026-02-03` both passed.

## Risks/Notes
- Guardrail strictness must avoid false positives in comments/docs.

## Completion Status
- `COMPLETE` at `2026-02-27 15:22:25`
