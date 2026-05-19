# TASK A1: Define Publishable Signal Schema

**Workstream:** A — DATA LAYER
**Epic:** Autonomous Trading Signal Platform
**Status:** [x] Complete

## Source

- [Autonomous Trading Signal Platform](C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md)

## Task Summary

Define the minimal public-facing signal dataset, store it as `publishable_signal_schema.json`, and document how local trading-system fields map into the publishable contract.

## Context

- Local signal source structures currently expose internal fields such as `guid`, `created`, `product`, `signal`, `entry_price`, `target_profit`, `target_loss`, `model`, and `strategy_name`.
- Relevant references reviewed:
  - `db_scripts/create_combined_trades_open_snapshot_pg.sql`
  - `api_server_sql/main.py`
- Output artifact target: `json/publishable_signal_schema.json`

## Plan

- [x] 1. Inspect current local trading signal field names and define the public field mapping.
  - [x] Test: Review `db_scripts/create_combined_trades_open_snapshot_pg.sql` and `api_server_sql/main.py`; pass if each requested public field can be mapped to an existing or derivable internal field.
  - Evidence: Confirmed mappings from internal fields: `guid -> signal_id`, `created -> timestamp`, `product -> asset`, `signal -> direction`, `entry_price -> entry`, `target_profit -> tp`, `target_loss -> sl`, `strategy_name/model -> strategy`; `confidence` remains a required normalized public field pending upstream producer population.
- [x] 2. Create `json/publishable_signal_schema.json` with the required public fields, types, constraints, and a source-field mapping note.
  - [x] Test: File exists and contains all required fields (`signal_id`, `timestamp`, `asset`, `direction`, `entry`, `tp`, `sl`, `strategy`, `confidence`) with `additionalProperties: false`.
  - Evidence: Added `json/publishable_signal_schema.json` as a JSON Schema Draft 2020-12 document with required field list, per-field constraints, example payload, and `x-source-field-mapping`.
- [x] 3. Validate the schema artifact parses as JSON and update this task record with validation results.
  - [x] Test: `@'import json, pathlib; p = pathlib.Path("json/publishable_signal_schema.json"); data = json.loads(p.read_text()); required = {"signal_id","timestamp","asset","direction","entry","tp","sl","strategy","confidence"}; assert required == set(data["required"]); assert data["additionalProperties"] is False; print("schema_ok")'@ | python -`; pass if command prints `schema_ok`.
  - Evidence: Command executed successfully and printed `schema_ok`.

## Implementation Log

- 2026-03-09 16:51:48+00:00 Reviewed `skills/workstream-task-lifecycle/SKILL.md` and the assigned task file.
- 2026-03-09 16:52:00+00:00 Reviewed source epic and sibling task stubs to confirm intended artifact naming and scope.
- 2026-03-09 16:53:00+00:00 Inspected live source structures in `db_scripts/create_combined_trades_open_snapshot_pg.sql` and `api_server_sql/main.py` to ground the public schema in existing internal field names.
- 2026-03-09 16:54:00+00:00 Created `json/publishable_signal_schema.json` with required public fields, JSON Schema constraints, an example object, and explicit internal-to-public mapping metadata.
- 2026-03-09 16:55:00+00:00 Ran JSON parse validation against `json/publishable_signal_schema.json`; command passed and printed `schema_ok`.

## Changes Made

- Added `json/publishable_signal_schema.json`.
- Defined the publishable signal contract with required fields:
  - `signal_id`
  - `timestamp`
  - `asset`
  - `direction`
  - `entry`
  - `tp`
  - `sl`
  - `strategy`
  - `confidence`
- Documented source-field mapping:
  - `guid -> signal_id`
  - `created/last_update -> timestamp`
  - `product -> asset`
  - `signal -> direction`
  - `entry_price -> entry`
  - `target_profit -> tp`
  - `target_loss -> sl`
  - `strategy_name/model -> strategy`
- Explicitly constrained `direction` to `buy|sell` and `confidence` to `0..1`.

## Validation

- Executed:
  - `@'import json, pathlib; p = pathlib.Path("json/publishable_signal_schema.json"); data = json.loads(p.read_text()); required = {"signal_id","timestamp","asset","direction","entry","tp","sl","strategy","confidence"}; assert required == set(data["required"]); assert data["additionalProperties"] is False; print("schema_ok")'@ | python -`
- Result:
  - Pass. Output: `schema_ok`
- User verification not required because this task defines a data contract artifact rather than a user-facing interactive behavior.

## Risks/Notes

- Internal `target_profit` and `target_loss` fields may currently represent offsets or PnL-style values in some sources rather than absolute price levels; downstream sync/export code must normalize these before publishing if required by consumers.
- No upstream `confidence` producer was found in the reviewed trading signal sources. The field is included because it is explicitly required by the task and epic contract.

## Completion Status

Complete as of 2026-03-09 16:55:00+00:00. All checklist items, tests, and evidence are recorded.
