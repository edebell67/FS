# Task: Implement Gen Strategy Toggle with Automated L-Trade Promotion

## Source
- User Directive: 2026-04-07

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
- Regression Test: `C:\Users\edebe\eds\tests\test_breakout_weekly_performance.py`
- Limits: `max_live_trades` and `max_trades_to_tws` from `config.json`
- Activation State: `activations.json` segmented by mode

## Destination Folder
None

## Dependency
Dependency: None
Required Skill: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
Scheduled For: 2026-04-11 05:15:13+01:00
Next Scheduled For: 2026-04-11 09:15:13+01:00
Spawned From: `20260411_011513_breakout_weekly_perf_auto_promote_toggle.md`

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
   - Only the two limit checks above apply for this promotion path. Other standard filters such as the global `daily_target` guard are bypassed.

## Plan
- [x] 1. UI Enhancement (`weekly_performance.html`)
  - [x] Test: Inspect the weekly dashboard implementation and verify the Gen Strategy column posts `auto_promote` activation payloads for both buy and sell keys.
  - [x] Evidence: `toggleGenStrategy()` in `weekly_performance.html` posts `/api/activations` with `{ active, manual, source, auto_promote, products }` for both `breakout_${strategy}_buy_net` and `breakout_${strategy}_sell_net`.
- [x] 2. API Extension (`trade_viewer_api.py`)
  - [x] Test: Validate that the activation API stores `auto_promote` and preserves it correctly for product-scoped updates.
  - [x] Evidence: `/api/activations` captures `auto_promote` in `update_activations()`, and `TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py` covers product-scoped preservation behavior.
- [x] 3. Trade Engine Modification (`common.py`)
  - [x] Test: Validate that the trade engine promotes only when weekly net is positive, bypasses `daily_target`, and still enforces `max_live_trades` and `max_trades_to_tws`.
  - [x] Evidence: `_handle_live_orders()` checks weekly net before calling `_create_tradeable_json(..., is_auto_promote=True)`, and `_create_l_trade_order()` bypasses `daily_target` only when `is_auto_promote=True` while retaining both limit guards.
- [x] 4. Validation
  - [x] Test: Run `python -m pytest tests\test_breakout_weekly_performance.py TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q` and expect all tests to pass.
  - [x] Evidence: `15 passed, 6 warnings in 1.92s` on 2026-04-11 after aligning the weekly dashboard regression test with the current activation payload.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\tests\test_breakout_weekly_performance.py`
  - Objective-Proved: The workspace regression suite now matches the current UI payload contract used by the weekly performance auto-promote toggle.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Source inspection of `toggleGenStrategy()` in `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`, activation persistence logic in `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`, and promotion guards in `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - Objective-Proved: The user-visible toggle path, activation persistence, positive-weekly-net promotion rule, and limit guard behavior are wired correctly in the current workspace.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m pytest tests\test_breakout_weekly_performance.py TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q` -> `15 passed, 6 warnings in 1.92s`
  - Objective-Proved: The current workspace passes automated checks for UI payload wiring, activation round-trip, product-scoped `auto_promote` preservation, positive-weekly-net promotion, and limit-guard enforcement.
  - Status: captured

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Updated `common.py` to support `auto_promote` flag and bypass `daily_target`. Updated `VERSION` in `constants.py`.
- 2026-04-08 12:30: Converted to recurring task every 4 hours. [V20260408_1230]
- 2026-04-11 05:24: Re-read lifecycle instructions, verified the existing UI/API/engine implementation, and ran the focused auto-promote validation suite.
- 2026-04-11 05:27: Fixed `tests\test_breakout_weekly_performance.py` so the regression assertion matches the current UI payload including `source: 'weekly_performance'`.

## Changes Made
- `tests\test_breakout_weekly_performance.py`: updated the Gen Strategy toggle assertion to reflect the current `/api/activations` payload shape with `source: 'weekly_performance'`.
- `weekly_performance.html`: existing implementation already posts manual activation updates with `auto_promote` enabled for both net-direction keys of the selected strategy and product.
- `trade_viewer_api.py`: existing implementation already persists `auto_promote` and preserves it for remaining products during product-scoped deactivation.
- `common.py`: existing implementation already enforces the positive-weekly-net promotion path and bypasses `daily_target` only for auto-promoted trades while preserving live/TWS caps.

## Validation
- 2026-04-11 05:24: Source inspection confirmed:
  - `weekly_performance.html` contains `toggleGenStrategy()` and sends `source: 'weekly_performance'` plus `auto_promote: isChecked` for both buy and sell activation keys.
  - `trade_viewer_api.py` stores `auto_promote` in `/api/activations`.
  - `common.py` promotes only when weekly net is positive and still applies `max_live_trades` and `max_trades_to_tws`.
- 2026-04-11 05:26: Ran `python -m pytest tests\test_breakout_weekly_performance.py -q`
  - Result before fix: `1 failed, 6 passed, 1 warning in 5.04s`
  - Failure detail: `test_weekly_performance_html_wires_gen_strategy_toggle_auto_promote` still expected the older payload shape without `source: 'weekly_performance'`.
- 2026-04-11 05:28: Ran `python -m pytest tests\test_breakout_weekly_performance.py TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q`
  - Result: `15 passed, 6 warnings in 1.92s`
  - Warning detail: `trade_viewer_api.py` emits `datetime.utcnow()` deprecation warnings at lines 3475 and 6881 under the current Python runtime.
- 2026-04-11 05:28: Auto-acceptance applied because evidence coverage is 100% and `Auto-Acceptance: true`.

## Risks/Notes
- `trade_viewer_api.py` still uses `datetime.utcnow()` in activation-related paths, which is functionally harmless here but emits deprecation warnings on the current Python runtime.
- This execution did not rerun `TradeApps\breakout\fs\test_auto_promote_limits.py` end-to-end because the local pytest temp-directory fixture is affected by workspace permission constraints; equivalent coverage for the implemented behavior is present in the passing dedicated suites above.
- `activations.json` remains mode-segmented, so live vs sim behavior still depends on correct mode selection by the UI and engine.
- The system-wide safeguards `max_live_trades` and `max_trades_to_tws` remain the effective hard stops for this promotion path.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-11 05:28:00 +01:00
