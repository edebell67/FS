# TASK A2: Define Publishable Trade Result Schema

**Workstream:** A — DATA LAYER
**Epic:** Autonomous Trading Signal Platform
**Status:** [x] Complete

## Source

- [Autonomous Trading Signal Platform](C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md)

## Task Summary

Define the minimal public-facing closed trade result dataset, store it as `publishable_trade_schema.json`, and document how current local closed-trade fields map into the publishable contract.

## Context

- Local closed-trade sources currently expose internal fields such as `guid`, `created`, `last_update`, `entry_price`, `latest_price`, `net_return`, `trade_reason`, and `close_type`.
- Relevant references reviewed:
  - `db_scripts/create_combined_trades_closed_arc_pg.sql`
  - `api_server_sql/main.py`
  - `trades_rt3_sim/orders/breakout_343163e2_GBPEUR_C_breakout_2_tp20.0_sl20.0_BUY_20260308_191912_close_tradeable.json`
- Output artifact target: `json/publishable_trade_schema.json`

## Plan

- [x] 1. Inspect current local closed-trade field names and define the public field mapping.
  - [x] Test: Review `db_scripts/create_combined_trades_closed_arc_pg.sql`, `api_server_sql/main.py`, and one representative `_close_tradeable.json` file; pass if each requested public field can be mapped to an existing or derivable internal field or documented as an upstream gap.
  - Evidence: Confirmed mappings from internal fields: `guid -> trade_id`, `created -> open_time`, `last_update/int_profit_time/max_net_return_time/min_net_return_time -> close_time candidates`, `entry_price -> entry_price`, `latest_price -> exit_price`, `net_return -> profit_loss`; `signal_id` is required for the public contract but is not present in the reviewed closed-trade sources and must be populated by the future sync layer from the originating signal/trade linkage.
- [x] 2. Create `json/publishable_trade_schema.json` with the required public fields, types, constraints, and a source-field mapping note.
  - [x] Test: File exists and contains all required fields (`trade_id`, `signal_id`, `open_time`, `close_time`, `entry_price`, `exit_price`, `profit_loss`) with `additionalProperties: false`.
  - Evidence: Added `json/publishable_trade_schema.json` as a JSON Schema Draft 2020-12 document with required field list, per-field constraints, example payload, and `x-source-field-mapping`.
- [x] 3. Validate the schema artifact parses as JSON and update this task record with validation results.
  - [x] Test: `python -c "import json, pathlib; p = pathlib.Path(r'json/publishable_trade_schema.json'); data = json.loads(p.read_text()); required = {'trade_id','signal_id','open_time','close_time','entry_price','exit_price','profit_loss'}; assert required == set(data['required']); assert data['additionalProperties'] is False; print('schema_ok')"`; pass if command prints `schema_ok`.
  - Evidence: Command executed successfully and printed `schema_ok`.

## Implementation Log

- 2026-03-09 17:00:00+00:00 Reviewed `skills/workstream-task-lifecycle/SKILL.md`, the assigned task file, and the epic backlog entry for task A2.
- 2026-03-09 17:01:00+00:00 Reviewed the completed A1 signal-schema lifecycle file and existing `json/publishable_signal_schema.json` to match established schema and documentation patterns.
- 2026-03-09 17:03:00+00:00 Inspected local closed-trade source structures in `db_scripts/create_combined_trades_closed_arc_pg.sql`, `api_server_sql/main.py`, and a representative `_close_tradeable.json` file to ground the public schema in existing internal fields.
- 2026-03-09 17:05:00+00:00 Created `json/publishable_trade_schema.json` with required public fields, JSON Schema constraints, an example object, and explicit internal-to-public mapping metadata including the current `signal_id` source gap.
- 2026-03-09 17:06:00+00:00 Ran JSON parse validation against `json/publishable_trade_schema.json`; command passed and printed `schema_ok`.

## Changes Made

- Added `json/publishable_trade_schema.json`.
- Defined the publishable trade result contract with required fields:
  - `trade_id`
  - `signal_id`
  - `open_time`
  - `close_time`
  - `entry_price`
  - `exit_price`
  - `profit_loss`
- Documented source-field mapping:
  - `guid -> trade_id`
  - `guid/originating signal linkage -> signal_id`
  - `created -> open_time`
  - `last_update`, `int_profit_time`, `max_net_return_time`, `min_net_return_time` -> `close_time`
  - `entry_price -> entry_price`
  - `latest_price -> exit_price`
  - `net_return` or normalized PnL equivalent -> `profit_loss`

## Validation

- Executed:
  - `python -c "import json, pathlib; p = pathlib.Path(r'json/publishable_trade_schema.json'); data = json.loads(p.read_text()); required = {'trade_id','signal_id','open_time','close_time','entry_price','exit_price','profit_loss'}; assert required == set(data['required']); assert data['additionalProperties'] is False; print('schema_ok')"`
- Result:
  - Pass. Output: `schema_ok`
- User verification not required because this task defines a data contract artifact rather than a user-facing interactive behavior.

## Risks/Notes

- The reviewed local closed-trade sources do not expose a durable `signal_id`. Downstream sync logic must carry forward the originating signal identifier when publishing trade results, otherwise this field cannot be populated reliably.
- `close_time` is derivable from multiple internal timestamps depending on which producer finalized the trade. The sync/export layer should normalize this to a single authoritative close timestamp before publishing.
- `latest_price` is the closest reviewed internal source for exit price in archived closed trades, but downstream publication should confirm it is the final execution/close price rather than a trailing snapshot value.

## Completion Status

Complete as of 2026-03-09 17:06:00+00:00. All checklist items, tests, and evidence are recorded.
