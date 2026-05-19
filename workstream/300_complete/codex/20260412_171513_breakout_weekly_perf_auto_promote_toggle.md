# Task: Implement Gen Strategy Toggle with Automated L-Trade Promotion

## Source
- User Directive: 2026-04-07
- Spawned From: `20260412_131513_breakout_weekly_perf_auto_promote_toggle.md`

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
Enhance `TradeApps/breakout/fs/weekly_performance.html` so "Gen Strategy" rows act as toggle buttons. When enabled, new trades for that strategy and product auto-promote to `is_live_trade: true` and trigger L-Trade creation, provided the strategy has positive weekly net return and the system respects only `max_live_trades` and `max_trades_to_tws`.

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
Required Skill: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
Scheduled For: 2026-04-12 17:15:13+01:00
Next Scheduled For: 2026-04-12 21:15:13+01:00

## Scheduled For
2026-04-08 12:00:00

## Detailed Logic (when Toggle is TRUE)
1. Trigger: a new trade is created for the selected strategy and product.
2. Pre-check:
   - `count(is_live_trade:true) < max_live_trades`
   - `count(is_live_trade:true and order_sent_net:true) < max_trades_to_tws`
3. Condition: the selected strategy must have a positive current-week `net_return`.
4. Action:
   - Set trade attribute `is_live_trade` to `true`.
   - Kick off L-Trade creation and promotion to TWS.
   - Bypass normal standard filters such as the daily target guard for these toggled strategies.
   - Keep the two cap checks above fully enforced.

## Plan
- [x] 1. UI Enhancement (`weekly_performance.html`)
  - [x] Test: Inspect `weekly_performance.html` and confirm the Gen Strategy column renders toggle controls that call `/api/activations` with `sync_grid_live: true`, `auto_promote`, and product-scoped activation payloads.
  - Evidence: `rg -n "toggleGenStrategy|auto_promote: isChecked|sync_grid_live" TradeApps/breakout/fs/weekly_performance.html` returned matches at lines 776, 782, 784, and 785.
- [x] 2. API Extension (`trade_viewer_api.py`)
  - [x] Test: Run `python -m pytest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q` and confirm the API preserves product-scoped `auto_promote` state and syncs weekly-performance activations into `grid_live.json`.
  - Evidence: Pytest passed `2 passed in 5.60s`; API wiring also confirmed by `rg -n "sync_grid_live|auto_promote|products" TradeApps/breakout/fs/trade_viewer_api.py`.
- [x] 3. Trade Engine Modification (`common.py`)
  - [x] Test: Run `python -m pytest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q` and confirm auto-promote uses weekly net, bypasses daily target, and still respects `max_live_trades` and `max_trades_to_tws`.
  - Evidence: Pytest passed `7 passed in 4.72s`; engine hooks confirmed by `rg -n "_is_auto_promote_active|_get_weekly_summary_net|is_auto_promote|daily_target > 0 and not is_auto_promote|max_trades_to_tws reached|max_live_trades reached" TradeApps/breakout/fs/common.py`.
- [x] 4. Validation
  - [x] Test: Execute the focused API and engine validation suite and confirm the dashboard wiring, activation persistence, grid sync, weekly-net gating, and cap enforcement all behave as required.
  - Evidence: Focused validation passed with `9` tests total; static dashboard inspection confirms the toggle sends the required payload for weekly-performance auto-promotion.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: Existing workspace implementation in `TradeApps/breakout/fs/weekly_performance.html`, `TradeApps/breakout/fs/trade_viewer_api.py`, and `TradeApps/breakout/fs/common.py`
  - Objective-Proved: The required UI, API, and engine behavior is present in the workspace for this task.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m pytest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q` -> `7 passed in 4.72s`
  - Objective-Proved: Auto-promote uses weekly total net, bypasses daily target, and still enforces `max_live_trades` and `max_trades_to_tws`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m pytest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q` -> `2 passed in 5.60s`
  - Objective-Proved: Weekly-performance activations persist `auto_promote`, preserve remaining product scope on deactivation, and sync correctly to `grid_live.json`.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `rg -n "toggleGenStrategy|auto_promote: isChecked|sync_grid_live|toggleInput.onchange = \\(\\) => toggleGenStrategy" TradeApps/breakout/fs/weekly_performance.html`
  - Objective-Proved: The weekly performance UI renders toggles and wires them to the activation API with product-scoped auto-promote payloads.
  - Status: captured
- Evidence-Type: user_feedback
  - Artifact: pending_user_verification
  - Objective-Proved: Final confirmation that the dashboard toggle behaves correctly in the live UI.
  - Status: planned

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Updated `common.py` to support `auto_promote` flag handling and bypass the daily-target guard for auto-promoted trades. Updated `constants.py` version marker at that time.
- 2026-04-08 12:30: Converted to recurring task every 4 hours. `[V20260408_1230]`
- 2026-04-12 17:17: Read and followed `skills/workstream-task-lifecycle/SKILL.md`, reviewed the task’s referenced files, and verified the workspace already contains the required UI, API, and trade-engine implementation.
- 2026-04-12 17:17: Ran focused validation for the feature via the dedicated API and engine pytest suites; both passed.
- 2026-04-12 17:17: Updated lifecycle evidence, completed the final checklist item, and recorded pending user verification for the UI behavior.

## Changes Made
- `TradeApps/breakout/fs/weekly_performance.html`
  - Toggle UI posts weekly-performance activation updates with `sync_grid_live: true`, `auto_promote`, and product-scoped payloads.
  - Rendered strategy rows bind the live-trade toggle to `toggleGenStrategy(...)`.
- `TradeApps/breakout/fs/trade_viewer_api.py`
  - Activation merge logic preserves `auto_promote` across remaining active products.
  - Weekly-performance activation writes can sync directly into `grid_live.json`.
- `TradeApps/breakout/fs/common.py`
  - Auto-promote detection checks activation entries for `auto_promote`.
  - Live-order handling uses weekly total net as the promotion criterion.
  - L-Trade creation bypasses `daily_target` only for auto-promoted trades while still enforcing `max_live_trades` and `max_trades_to_tws`.
- `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260412_171513_breakout_weekly_perf_auto_promote_toggle.md`
  - Refreshed lifecycle status, evidence, validation results, and checklist completion for this execution.

## Validation
- `python -m pytest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q`
  - Result: `7 passed in 4.72s`
- `python -m pytest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q`
  - Result: `2 passed in 5.60s`
  - Note: pytest reported existing deprecation warnings in `trade_viewer_api.py` for `datetime.utcnow()` usage; this is outside the task scope.
- `rg -n "toggleGenStrategy|auto_promote: isChecked|sync_grid_live|toggleInput.onchange = \\(\\) => toggleGenStrategy" TradeApps/breakout/fs/weekly_performance.html`
  - Result: confirmed the dashboard toggle wiring at lines 776, 782, 784, 785, and 1363.
- `rg -n "sync_grid_live|auto_promote|products" TradeApps/breakout/fs/trade_viewer_api.py`
  - Result: confirmed activation merge and grid-sync handling at lines 3477, 3502, 3521, 3530, and 3546.
- `rg -n "_is_auto_promote_active|_get_weekly_summary_net|is_auto_promote|daily_target > 0 and not is_auto_promote|max_trades_to_tws reached|max_live_trades reached" TradeApps/breakout/fs/common.py`
  - Result: confirmed auto-promote gating and cap enforcement at lines 1244, 1391, 1410, 1886, 3250, 3280, 3316, and 3345.
- 2026-04-12 17:17: User verification requested for the live dashboard toggle behavior. Awaiting pass/fail confirmation from the user after manual UI exercise.

## Risks/Notes
- This execution did not introduce new code changes; it validated the existing workspace implementation and updated the lifecycle record.
- The final user-visible acceptance step is still pending. The dashboard should be exercised manually to confirm the toggle state, activation persistence, and live auto-promotion behavior in the target runtime.
- Existing deprecation warnings from `datetime.utcnow()` remain in `trade_viewer_api.py` but do not block this feature.

## Completion Status
- State: Awaiting user verification
- Timestamp: 2026-04-12 17:17:34+01:00
