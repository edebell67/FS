# TASK A3: Define Strategy Summary Schema

**Workstream:** A - DATA LAYER
**Epic:** Autonomous Trading Signal Platform
**Status:** [x] Complete

## Source

- [Autonomous Trading Signal Platform](C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md)

## Task Summary

Define the strategy performance summary contract, store it as `json/strategy_schema.json`, and document how current local strategy/performance fields map into the publishable schema used by downstream sync and API work.

## Context

- Existing related schema artifacts already live under `json/`:
  - `json/publishable_signal_schema.json`
  - `json/publishable_trade_schema.json`
- Reviewed local source structures expose overlapping performance fields through:
  - `db_scripts/dbo.vw_113_Combined_trades_all.View.sql`
  - `db_scripts/dbo.vw_106_ModelPerformance_actual.View.sql`
  - `db_scripts/dbo.tbl_ModelPerformanceLog.Table.sql`
  - `workstream/clawd_originated/artefacts/miniapp_feed_extractor.py`
  - `workstream/clawd_originated/artefacts/projects/miniapp_feed_2026-03-06.json`
- Output artifact target: `json/strategy_schema.json`

## Plan

- [x] 1. Inspect current local strategy summary and performance field names and define the publishable field mapping.
  - [x] Test: Review the listed SQL/views and representative strategy feed artifact; pass if each requested field (`strategy_id`, `strategy_name`, `asset`, `timeframe`, `win_rate`, `profit_factor`, `drawdown`, `trade_count`) is mapped to an existing field, derivable aggregation, or documented upstream gap.
  - Evidence: Confirmed mappings and derivations from reviewed sources: `model/product/strategy_id -> strategy_id`, `product_forex.strategy_name/strategy_name -> strategy_name`, `product/pair -> asset`, `profitable_percent|win_rate|wr -> win_rate`, `total_trade_count|trade_count -> trade_count`, `drawdown|dd -> drawdown`; `timeframe` and `profit_factor` are required target fields but are not present as first-class values in the reviewed local sources and must be derived or populated by the sync layer.
- [x] 2. Create `json/strategy_schema.json` with the required fields, types, constraints, and a source-field mapping note.
  - [x] Test: File exists and contains all required fields (`strategy_id`, `strategy_name`, `asset`, `timeframe`, `win_rate`, `profit_factor`, `drawdown`, `trade_count`) with `additionalProperties: false`.
  - Evidence: Added `json/strategy_schema.json` as a JSON Schema Draft 2020-12 document with required field list, per-field constraints, example payload, and `x-source-field-mapping` metadata documenting both grounded fields and current upstream gaps.
- [x] 3. Validate the schema artifact parses as JSON and update this task record with validation results.
  - [x] Test: `python -c "import json, pathlib; p = pathlib.Path(r'json/strategy_schema.json'); data = json.loads(p.read_text()); required = {'strategy_id','strategy_name','asset','timeframe','win_rate','profit_factor','drawdown','trade_count'}; assert required == set(data['required']); assert data['additionalProperties'] is False; print('schema_ok')"`; pass if command prints `schema_ok`.
  - Evidence: Command executed successfully and printed `schema_ok`.

## Implementation Log

- 2026-03-09 17:09:00+00:00 Reviewed `skills/workstream-task-lifecycle/SKILL.md` and the assigned task file.
- 2026-03-09 17:10:00+00:00 Reviewed the epic backlog entry, sibling completed schema tasks, and existing JSON schema artifacts to match the established pattern.
- 2026-03-09 17:12:00+00:00 Inspected current strategy/performance source structures in SQL views, the model performance log table, and the representative miniapp feed artifact to ground the publishable contract in existing local fields.
- 2026-03-09 17:14:00+00:00 Created `json/strategy_schema.json` with the required strategy summary fields, constraints, example payload, and explicit source mapping metadata.
- 2026-03-09 17:15:00+00:00 Ran JSON parse validation against `json/strategy_schema.json`; command passed and printed `schema_ok`.

## Changes Made

- Added `json/strategy_schema.json`.
- Defined the publishable strategy summary contract with required fields:
  - `strategy_id`
  - `strategy_name`
  - `asset`
  - `timeframe`
  - `win_rate`
  - `profit_factor`
  - `drawdown`
  - `trade_count`
- Documented source-field mapping:
  - `model`, `product`, or an existing `strategy_id` token -> `strategy_id`
  - `product_forex.strategy_name` or source `strategy_name` -> `strategy_name`
  - `product` or `pair` -> `asset`
  - sync-defined reporting window label -> `timeframe`
  - `profitable_percent`, `win_rate`, or `wr` -> `win_rate`
  - sync-layer gross profit and gross loss aggregation -> `profit_factor`
  - `drawdown` or `dd` -> `drawdown`
  - `total_trade_count` or `trade_count` -> `trade_count`
- Applied numeric constraints:
  - `win_rate` limited to `0..100`
  - `profit_factor` minimum `0`
  - `drawdown` minimum `0`
  - `trade_count` integer minimum `0`

## Validation

- Executed:
  - `python -c "import json, pathlib; p = pathlib.Path(r'json/strategy_schema.json'); data = json.loads(p.read_text()); required = {'strategy_id','strategy_name','asset','timeframe','win_rate','profit_factor','drawdown','trade_count'}; assert required == set(data['required']); assert data['additionalProperties'] is False; print('schema_ok')"`
- Result:
  - Pass. Output: `schema_ok`
- User verification not required because this task defines a data contract artifact rather than a user-facing interactive behavior.

## Risks/Notes

- Current reviewed strategy feed examples emit `strategy_id`, `strategy_name`, and partial metrics, but do not yet expose all requested fields in final publishable form.
- `timeframe`, `profit_factor`, and maximum drawdown are not present as first-class fields in the reviewed source artifacts and will need to be derived or populated by the future sync layer.
- The representative miniapp feed currently uses `pair` rather than `asset` and may emit `null` metrics. Downstream sync/export work should normalize those values to this stricter contract before publication.

## Completion Status

Complete as of 2026-03-09 17:15:00+00:00. All checklist items, tests, and evidence are recorded.
