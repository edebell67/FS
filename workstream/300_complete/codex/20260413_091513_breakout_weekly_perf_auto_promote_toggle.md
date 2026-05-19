# Task: Implement Gen Strategy Toggle with Automated L-Trade Promotion

## Source
- User Directive: 2026-04-07
- Spawned From: `20260413_051513_breakout_weekly_perf_auto_promote_toggle.md`

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
Enhance `TradeApps/breakout/fs/weekly_performance.html` so Gen Strategy rows act as toggle controls. When toggled on, the selected strategy/product should auto-promote new trades to `is_live_trade: true` and create the L-Trade order when weekly net return is positive and the system limits (`max_live_trades`, `max_trades_to_tws`) still permit promotion.

## Context
- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Backend API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Trade Engine: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Tests: `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py`
- Tests: `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py`
- Limits: `max_live_trades`, `max_trades_to_tws` from `config.json`
- Activation State: `activations.json` segmented by mode

## Destination Folder
None

## Dependency
Dependency: None

Required Skill: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
Scheduled For: 2026-04-13 09:15:13+01:00
Next Scheduled For: 2026-04-13 13:15:13+01:00

## Detailed Logic (when Toggle is TRUE)
1. Trigger: A new trade is created for the specific strategy/product.
2. Pre-check:
   - `count(is_live_trade:true) < max_live_trades`
   - `count(order_sent_net:true on OPEN trades) < max_trades_to_tws`
3. Condition: The selected strategy must have positive current-week total `net_return`.
4. Action:
   - Set `is_live_trade` to `true`.
   - Kick off L-Trade creation / TWS promotion.
   - Bypass the normal daily-target/global-threshold gate for this path only.
   - Continue enforcing the two hard limits in step 2.

## Plan
- [x] 1. UI enhancement in `weekly_performance.html`.
  - [x] Test: Inspect `toggleGenStrategy`, `createStrategyRow`, and `updateStrategyRow` to confirm the Gen Strategy column renders a checkbox toggle and posts `auto_promote` plus `sync_grid_live`.
  - [x] Evidence: `weekly_performance.html` contains the toggle UI and `toggleGenStrategy()` posts both buy/sell activation payloads with `auto_promote: isChecked`, `source: 'weekly_performance'`, and `sync_grid_live: true`.
- [x] 2. API extension in `trade_viewer_api.py`.
  - [x] Test: Run `pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q` and confirm activation persistence plus weekly-performance grid sync pass.
  - [x] Evidence: `4 passed` and the API code preserves `auto_promote`, product-scoped activation state, and syncs weekly toggles into `grid_live.json`.
- [x] 3. Trade engine modification in `common.py`.
  - [x] Test: Run `pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q` and confirm auto-promote bypasses market-bias/daily-target checks while still respecting hard live/TWS caps.
  - [x] Evidence: `7 passed` and `_handle_live_orders()` plus `_create_l_trade_order()` route auto-promote through weekly net gating with limit enforcement intact.
- [x] 4. Validation.
  - [x] Test: Run both focused pytest modules end-to-end and confirm all 11 feature tests pass.
  - [x] Evidence: `11 passed` total across the two dedicated modules; only deprecation warnings remain for `datetime.utcnow()` in `trade_viewer_api.py`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: manual_verification
  - Artifact: `TradeApps/breakout/fs/weekly_performance.html` (`toggleGenStrategy`, `createStrategyRow`, `updateStrategyRow`)
  - Objective-Proved: The weekly performance UI exposes Gen Strategy as a live toggle control and sends the correct weekly-performance activation payload for the selected strategy/product.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/common.py`, `TradeApps/breakout/fs/trade_viewer_api.py`, `TradeApps/breakout/fs/weekly_performance.html`, `TradeApps/breakout/fs/tests/test_weekly_auto_promote_common.py`, `TradeApps/breakout/fs/tests/test_weekly_auto_promote_activation_api.py`
  - Objective-Proved: The workspace contains the implementation and dedicated regression tests for UI toggle state, activation persistence, grid sync, weekly-net auto-promotion, and hard-cap enforcement.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q` -> `7 passed in 6.74s`
  - Objective-Proved: Auto-promote logic in `common.py` works as intended, including bypassing market bias/daily target while still enforcing `max_live_trades` and `max_trades_to_tws`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q` -> `4 passed, 5 warnings in 8.77s`
  - Objective-Proved: The activation API persists `auto_promote`, preserves product-scoped activations, and syncs weekly-performance toggles to `grid_live`.
  - Status: captured
- Evidence-Type: diff
  - Artifact: No additional code changes were required in this execution; validated the existing implementation already present in the workspace.
  - Objective-Proved: This run served as completion verification and lifecycle reconciliation rather than introducing a new patch on top of the existing implementation.
  - Status: captured

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Updated `common.py` to support `auto_promote` flag and bypass `daily_target`. Updated version marker in constants.
- 2026-04-08 12:30: Converted to recurring task every 4 hours. `[V20260408_1230]`
- 2026-04-13 09:05: Reviewed existing workspace implementation and confirmed the required UI/API/engine paths were already present.
- 2026-04-13 09:17: Ran focused validation suites for weekly auto-promote API and trade-engine behavior; both passed.
- 2026-04-13 09:17: Reconciled this lifecycle file with actual evidence and marked the task complete under auto-acceptance rules.

## Changes Made
- Existing workspace implementation already includes:
- `weekly_performance.html`
  - Renders Gen Strategy as a switch control.
  - Sends buy/sell activation updates with `auto_promote: isChecked`.
  - Sends `source: 'weekly_performance'` and `sync_grid_live: true`.
- `trade_viewer_api.py`
  - Persists `auto_promote` in activation entries.
  - Preserves `auto_promote` during product-scoped deactivation when other products remain active.
  - Syncs weekly-performance activation changes into `grid_live.json`.
- `common.py`
  - Preserves `auto_promote` through activation normalization/merge.
  - Detects active auto-promote state for matching strategy/product.
  - Uses current-week total net for promotion eligibility.
  - Bypasses daily-target blocking for auto-promoted L-Trades.
  - Still enforces `max_live_trades` and `max_trades_to_tws`.
- Test coverage already present:
  - `test_weekly_auto_promote_common.py`
  - `test_weekly_auto_promote_activation_api.py`

## Validation
- 2026-04-13 09:17: Ran `pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q`
  - Result: `7 passed in 6.74s`
- 2026-04-13 09:17: Ran `pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q`
  - Result: `4 passed, 5 warnings in 8.77s`
  - Warning detail: `trade_viewer_api.py` still uses `datetime.utcnow()` in activation code paths; this is a deprecation warning only and did not block feature validation.
- 2026-04-13 09:17: Combined feature validation result
  - Result: `11 passed`

## Risks/Notes
- The feature is validated by focused automated tests, not a browser screenshot or live TWS integration run in this execution.
- `trade_viewer_api.py` emits deprecation warnings for `datetime.utcnow()`; behavior is currently correct, but the call sites should eventually move to timezone-aware UTC timestamps.
- The repository worktree contains extensive unrelated changes; this execution intentionally avoided touching them.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-13 09:17:48+01:00
