# Task: Implement Gen Strategy Toggle with Automated L-Trade Promotion

## Source
- User Directive: 2026-04-07
- Spawned From: `20260408_171513_breakout_weekly_perf_auto_promote_toggle.md`

## Task Type
standard

## Task Attributes
recurring_task: true
recurrence_type: scheduled
recurrence_rule: interval
recurrence_interval_hours: 4
looping_task: false
splittable_task: false
workflow_task: false

## Task Summary
Enhance `fs\weekly_performance.html` so the `Gen Strategy` column acts as a product-scoped toggle. When toggled on, matching strategies with positive weekly net return should auto-promote new trades to `is_live_trade: true` and generate L-Trade orders, while only enforcing `max_live_trades` and `max_trades_to_tws`.

## Context
- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Backend API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Trade Engine: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Tests: `C:\Users\edebe\eds\TradeApps\breakout\fs\test_auto_promote_limits.py`, `C:\Users\edebe\eds\tests\test_breakout_weekly_performance.py`
- Limits: `max_live_trades`, `max_trades_to_tws` from `config.json`
- Activation State: `activations.json` segmented by mode

## Destination Folder
None

## Dependency
Dependency: None

Scheduled For: 2026-04-08 21:15:13+01:00
Next Scheduled For: 2026-04-09 01:15:13+01:00

## Detailed Logic (when Toggle is TRUE)
1. Trigger: a new trade is created for the selected strategy/product.
2. Pre-check:
   - `count(is_live_trade:true) < max_live_trades`
   - `count(order_sent_net:true) < max_trades_to_tws`
3. Condition: the selected strategy must have positive current-week net return.
4. Action:
   - set trade `is_live_trade` to `true`
   - create the L-Trade order payload for TWS promotion
   - bypass the normal `daily_target` guard only for the explicit auto-promote path

## Plan
- [x] 1. UI Enhancement (`weekly_performance.html`)
  - [x] Test: Inspect and execute the weekly performance client logic; pass when the table renders sortable columns, the `Gen Strategy` column uses a toggle control, and toggle updates rehydrate activation state from the API response.
  - Evidence: Added `renderTable`, `setSort`, and `createHeaderCell`; manual validation script and HTML assertions passed.
- [x] 2. API Extension (`trade_viewer_api.py`)
  - [x] Test: Exercise `/api/activations` POST+GET round-trip; pass when `auto_promote` survives normalization and returns to the UI with product scoping intact.
  - Evidence: Added API round-trip coverage in `tests/test_breakout_weekly_performance.py`; manual validation passed.
- [x] 3. Trade Engine Modification (`common.py`)
  - [x] Test: Validate order creation guards; pass when explicit auto-promote bypasses `daily_target`, while normal/scheduled promotion paths still honor `daily_target` and both paths still enforce live/TWS limits.
  - Evidence: Fixed non-toggle call sites to stop passing `is_auto_promote=True`; regression coverage added in `TradeApps/breakout/fs/test_auto_promote_limits.py`.
- [x] 4. Validation
  - [x] Test: Run targeted automated checks for engine, API, and weekly performance UI contracts; pass when all assertions succeed or environment limitations are documented with an equivalent manual execution path.
  - Evidence: Manual Python validation executed all 11 target assertions successfully after `pytest` temp-cleanup permission failures were isolated to the environment.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/common.py`, `TradeApps/breakout/fs/trade_viewer_api.py`, `TradeApps/breakout/fs/weekly_performance.html`, `TradeApps/breakout/fs/test_auto_promote_limits.py`, `tests/test_breakout_weekly_performance.py`
  - Objective-Proved: UI, API, engine, and regression-test changes required by the task were implemented.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Manual Python validation output on 2026-04-08 confirming 11 PASS results across weekly UI/API and auto-promote engine assertions.
  - Objective-Proved: End-to-end task behavior is covered by executable assertions despite `pytest` temp cleanup limitations in this environment.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `weekly_performance.html` now contains sortable header/render logic plus product-scoped `Gen Strategy` toggle wiring that reloads merged activation state from `/api/activations`.
  - Objective-Proved: The user-visible weekly performance page contains the intended toggle behavior and rendering path.
  - Status: captured

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Updated `common.py` to support `auto_promote` flag and bypass `daily_target`. Updated version stamp in prior workstream context.
- 2026-04-08 12:30: Converted to recurring task every 4 hours. [V20260408_1230]
- 2026-04-08 21:05: Verified workspace state against task requirements; found missing weekly page render/sort logic and an engine regression where non-toggle promotion paths were incorrectly marked as auto-promote.
- 2026-04-08 21:12: Patched `common.py` so only the explicit auto-promote branch bypasses `daily_target`; normal and scheduled promotions now use standard guards again.
- 2026-04-08 21:15: Patched `trade_viewer_api.py` activation normalization/merge logic to preserve `auto_promote` through GET/POST round-trips.
- 2026-04-08 21:19: Restored weekly performance table rendering and sortable headers in `weekly_performance.html`; updated toggle refresh behavior to use merged activation state returned by the API.
- 2026-04-08 21:22: Added regression coverage for auto-promote limits, standard daily-target enforcement, API round-trip preservation, and weekly page toggle contract; executed manual validation path after `pytest` temp cleanup permission failures.

## Changes Made
- `TradeApps/breakout/fs/common.py`
  - Removed erroneous `is_auto_promote=True` from non-toggle/scheduled `_create_tradeable_json(...)` call sites.
  - Preserved explicit `is_auto_promote=True` only for the dedicated auto-promote activation branch.
- `TradeApps/breakout/fs/trade_viewer_api.py`
  - Extended `_coerce_entry` and `_merge_entries` so `auto_promote` survives normalization and merging.
- `TradeApps/breakout/fs/weekly_performance.html`
  - Restored missing `renderTable`, `setSort`, and `createHeaderCell` logic.
  - Added sortable weekly day/total/trade headers and row rendering for product, strategy, gen strategy toggle, chart button, and per-day totals.
  - Changed `toggleGenStrategy` success handling to replace the local activation cache with the server-returned merged activation map.
- `TradeApps/breakout/fs/test_auto_promote_limits.py`
  - Added regression test proving standard live orders still respect `daily_target`.
- `tests/test_breakout_weekly_performance.py`
  - Added coverage for Gen Strategy toggle auto-promote wiring.
  - Added activation API round-trip coverage for `auto_promote`.

## Validation
- Attempted command:
  - `pytest TradeApps/breakout/fs/test_auto_promote_limits.py tests/test_breakout_weekly_performance.py`
  - Result: blocked by environment temp-directory permission errors (`WinError 5` during pytest temp setup/cleanup), not by task assertions.
- Equivalent validation executed successfully:
  ```powershell
  @'
  from pathlib import Path
  from pytest import MonkeyPatch
  import TradeApps.breakout.fs.test_auto_promote_limits as auto_tests
  import tests.test_breakout_weekly_performance as weekly_tests
  ...
  '@ | python -
  ```
  - Pass condition: all targeted assertions complete without failure.
  - Result summary:
    - `PASS test_get_week_bounds_aligns_to_monday_sunday`
    - `PASS test_aggregate_for_product_type_outputs_full_monday_to_sunday_week`
    - `PASS test_weekly_performance_api_returns_aligned_week_payload`
    - `PASS test_weekly_performance_html_defines_sortable_columns`
    - `PASS test_weekly_performance_html_wires_gen_strategy_toggle_auto_promote`
    - `PASS test_aggregate_for_product_type_keeps_strategy_and_gen_strategy_separate`
    - `PASS test_auto_promote_bypasses_daily_target_but_still_writes_order`
    - `PASS test_auto_promote_still_respects_max_live_trades_limit`
    - `PASS test_auto_promote_still_respects_tws_limit`
    - `PASS test_standard_live_order_still_respects_daily_target`
    - `PASS test_activation_api_round_trip_preserves_auto_promote`

## Risks/Notes
- `pytest` itself remains impacted by environment-level temp directory cleanup permissions on this machine; the task assertions were validated through direct Python execution instead.
- Existing activation data may contain older entries without `auto_promote`; the updated API now preserves the flag when present and returns it consistently.
- The task objective is satisfied without a browser screenshot because the page contract is now covered by source-level and executable validation.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-08 21:22:25
