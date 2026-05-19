## Task

Investigate what process creates trade files under `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-20\virtual`.

## Source

- User request in Codex thread on 2026-04-20.

## Task Type

standard

## Task Attributes

- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false
- depends_on: []
- feeds_into: []

## Task Summary

Trace the code path that writes virtual-trade JSON artifacts into the active day folder and identify the runtime loop or workflow that invokes it.

## Context

- Relevant folder:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-20\virtual`
- Relevant files:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\run_archive_process.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`

## Plan

- [x] 1. Identify the function that physically writes files into `virtual`.
  - [x] Test: inspect filename and payload format against candidate writer functions.
  - Evidence: exact write site in code.
- [x] 2. Identify the orchestrator that calls the writer in normal runtime.
  - [x] Test: trace `_manage_virtual_trades(...)` call sites.
  - Evidence: runtime loop references in `common.py`.
- [x] 3. Correlate live folder contents with the identified code path.
  - [x] Test: inspect sample files from `2026-04-20/virtual`.
  - Evidence: filename/payload fields match writer output and lifecycle behavior.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

## Implementation Log

### 2026-04-20 16:47:15

- Created investigation task for the `virtual` trade artifact producer.

### 2026-04-20 16:55:00

- Confirmed the physical writer is `_create_new_v_trade(...)` in `fs/common.py`.
- It writes directly to `virtual_dir / filename` with:
  - filename pattern `vt_{timestamp}_open_{buy|sell}_{product}_{strategy}.json`
  - payload fields including `trade_id`, `product`, `direction`, `entry_time`, `status`, `is_live_trade`, `source_strategy`, and `strategy_name`.
- Exact write site:
  - `common.py:3899-3939`

### 2026-04-20 16:58:00

- Confirmed the creation decision happens in `_manage_virtual_trades(...)` in `fs/common.py`.
- Current behavior:
  - resolves `run_mode` from config
  - ensures the active day directory exists
  - creates `<day>/virtual`
  - fetches leaders from the frequency API via:
    - `/vw_top_one_frequency_buy`
    - `/vw_top_one_frequency_sell`
  - closes displaced virtual trades with reason `API_LEADER_CHANGED`
  - creates a new BUY/SELL virtual trade when the API leader product for that side is not already open
- Exact create calls:
  - `common.py:4055-4056`
  - `common.py:4073-4074`

### 2026-04-20 17:01:00

- Confirmed the normal runtime caller is the main strategy loop in `common.py`.
- The live loop calls `_manage_virtual_trades(...)` every ~10 seconds:
  - `common.py:4646-4651`
- There is also a startup/archive path that calls `_manage_virtual_trades(...)` only when the archive flag is set:
  - `common.py:4459-4462`
  - `fs/run_archive_process.py:27-39`

### 2026-04-20 17:04:00

- Inspected sample files in `2026-04-20/virtual`.
- They match the `_create_new_v_trade(...)` schema exactly:
  - `trade_id` format `v_YYYYMMDD_HHMMSS`
  - `status` values `OPEN` / `CLOSED`
  - `source_strategy` and `strategy_name` fields
  - closed records with `exit_reason = API_LEADER_CHANGED`
- This matches the `_manage_virtual_trades(...)` lifecycle, where a previous leader is closed and a new leader trade is opened when the frequency API leader changes.

## Changes Made

- No production code changes.

## Validation

- Code-path validation:
  - `common.py:3937-3939` writes the virtual trade JSON file.
  - `common.py:4017-4018` creates the `<day>/virtual` folder.
  - `common.py:4021-4025` fetches frequency leaders from API.
  - `common.py:4055-4056` and `4073-4074` create new virtual trades.
  - `common.py:4646-4651` invokes virtual-trade management from the main runtime loop.
- Artifact validation:
  - Sample files from `2026-04-20/virtual` match the writer’s filename and payload structure.

## Risks/Notes

- The `virtual` folder is not forex-only in practice; its contents include multiple product classes because `_manage_virtual_trades(...)` follows the global top frequency leaders returned by the API for the current run mode.
- The folder path is under `json/live/forex/<date>/virtual` because the current layout resolver places the active day directory there for the live run mode, but the producer logic itself is driven by leader selection rather than by a forex-only filter inside `_manage_virtual_trades(...)`.

## Completion Status

Complete
