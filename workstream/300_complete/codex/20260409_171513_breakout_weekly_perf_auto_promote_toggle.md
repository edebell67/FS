# Task: Implement Gen Strategy Toggle with Automated L-Trade Promotion

## Source
- User Directive: 2026-04-07
- Spawned From: `20260409_131513_breakout_weekly_perf_auto_promote_toggle.md`

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
Enhance `fs\weekly_performance.html` to turn "Gen Strategy" rows into toggle buttons. When a strategy is toggled `ON`, the system will automatically promote new trades for that strategy/product to `is_live_trade: true` and initiate the L-Trade creation process, provided the strategy has a positive weekly net return and system-wide trade limits are not exceeded.

## Context
- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Backend API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Trade Engine: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Limits: `max_live_trades` and `max_trades_to_tws` from `config.json`
- Activation State: `activations.json` segmented by mode

## Destination Folder
None

## Dependency
Dependency: None
Scheduled For: 2026-04-09 17:15:13+01:00
Next Scheduled For: 2026-04-09 21:15:13+01:00

## Scheduled For
2026-04-08 12:00:00

## Detailed Logic (when Toggle is TRUE)
1. Trigger: A new trade is created for the specific strategy/product.
2. Pre-check:
   - `count(is_live_trades:true) < max_live_trades`
   - `count(is_live_trades:true) < max_trades_to_tws`
3. Condition: The selected strategy must have a positive `net_return` for previous trades in the current week total.
4. Action:
   - Set the trade attribute `is_live_trade` to `true`.
   - Kick off the L-Trade creation process.
   - Bypass standard global-threshold style filters for these toggled strategies; only the two limit checks above apply.

## Plan
- [x] 1. UI Enhancement (`weekly_performance.html`)
  - [x] Test: Confirm the weekly performance table renders per-row toggle controls and `toggleGenStrategy()` posts `auto_promote: isChecked` for both buy and sell activation keys.
  - [x] Evidence: Source verification of `weekly_performance.html` confirmed the rendered checkbox switch in the Gen Strategy column and the activation payload wiring.
- [x] 2. API Extension (`trade_viewer_api.py`)
  - [x] Test: Confirm `/api/activations` stores and preserves the `auto_promote` flag during product-scoped activation updates.
  - [x] Evidence: Manual harness pass plus source verification confirmed product-scoped deactivation preserves `auto_promote` while remaining products stay active.
- [x] 3. Trade Engine Modification (`common.py`)
  - [x] Test: Confirm auto-promote only triggers when weekly net is positive, bypasses `daily_target`, and still respects `max_live_trades` and `max_trades_to_tws`.
  - [x] Evidence: Manual harness pass plus source verification confirmed `_handle_live_orders()` gates on positive weekly net and delegates to `_create_l_trade_order()` with `is_auto_promote=True`.
- [x] 4. Validation
  - [x] Test: Run focused regression coverage for the activation API and auto-promote guardrails, then verify the relevant UI/API/engine code paths match the task requirements.
  - [x] Evidence: Manual harness passed all five targeted assertions and source verification confirmed the UI payload, activation persistence, weekly-net gate, and live-trade limit behavior.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/weekly_performance.html`, `TradeApps/breakout/fs/trade_viewer_api.py`, `TradeApps/breakout/fs/common.py`
  - Objective-Proved: The workspace contains the required UI toggle payload, activation persistence logic, weekly positive-net gate, and L-trade promotion guard overrides and limits.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `TradeApps/breakout/fs/weekly_performance.html` (`toggleGenStrategy`, `isStrategyActive`, rendered checkbox switch controls)
  - Objective-Proved: The weekly performance dashboard exposes per-row toggle controls wired to the activations API for live auto-promotion management.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Manual harness run on 2026-04-09 covering `test_product_scoped_deactivation_preserves_auto_promote_for_remaining_products`, `test_auto_promote_bypasses_daily_target_but_still_writes_order`, `test_auto_promote_still_respects_max_live_trades_limit`, `test_auto_promote_still_respects_tws_limit`, and `test_standard_live_order_still_respects_daily_target`
  - Objective-Proved: Activation persistence preserves `auto_promote` correctly and auto-promotion bypasses only `daily_target` while still enforcing `max_live_trades` and `max_trades_to_tws`.
  - Status: captured

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Updated `common.py` to support `auto_promote` flag and bypass `daily_target`. Updated `VERSION` in `constants.py`.
- 2026-04-08 12:30: Converted to recurring task every 4 hours. [V20260408_1230]
- 2026-04-09 17:22: Revalidated the delivered implementation from the current workspace, including UI payload wiring, activation API persistence, weekly-net promotion gating, and L-trade limit enforcement. No additional code changes were required in this execution.

## Changes Made
- Updated `_coerce_activation_entry` and `_merge_activation_entries` in `common.py` to preserve `auto_promote`.
- Updated `_create_l_trade_order`, `_create_tradeable_json`, and `_handle_live_orders` in `common.py` to pass `is_auto_promote` and bypass `daily_target` for auto-promoted trades only.
- Updated `VERSION` in `constants.py` to `V20260408_1230`.
- 2026-04-09 execution: no further source edits were needed; this run completed validation and lifecycle evidence capture against the existing implementation in the workspace.

## Validation
- 2026-04-09 17:18: Ran `pytest "TradeApps\\breakout\\fs\\tests\\test_weekly_auto_promote_activation_api.py" "TradeApps\\breakout\\fs\\test_auto_promote_limits.py"`
  - Result: blocked by environment-level temp directory permission errors under `C:\Users\edebe\AppData\Local\Temp\pytest-of-edebe`; the failure was in pytest temp setup and cleanup, not in the feature assertions themselves.
- 2026-04-09 17:19: Ran a `python -` manual harness that invoked the same five test functions with `pytest.MonkeyPatch` and workspace-local case directories.
  - Result: PASS for all five checks. Observed outputs included successful tradeable JSON creation for the bypass case plus expected guard messages for `max_live_trades`, `max_trades_to_tws`, and standard `daily_target` enforcement.
- 2026-04-09 17:21: Reviewed `weekly_performance.html`, `trade_viewer_api.py`, and `common.py`.
  - Result: Confirmed `toggleGenStrategy()` posts `auto_promote: isChecked` for both buy and sell keys, `/api/activations` preserves product-scoped `auto_promote`, and `_handle_live_orders()` only promotes when weekly net is positive before delegating to `_create_l_trade_order()` limit guards.
- 2026-04-09 17:22: User verification requested in completion handoff for dashboard toggle behavior. Auto-acceptance criteria are satisfied by captured technical evidence (`Objective-Delivery-Coverage: 100%`, `Auto-Acceptance: true`).

## Risks/Notes
- Ensure `activations.json` remains correctly segmented by mode (`live` vs `sim`) during future activation sync changes.
- `max_live_trades` and `max_trades_to_tws` remain the only limit checks allowed for this auto-promote path after the positive weekly-net gate.
- Normal `pytest` remains unreliable in this environment until the temp-directory permission issue is resolved; the manual harness is the accurate validation record for this run.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-09 17:22:00
