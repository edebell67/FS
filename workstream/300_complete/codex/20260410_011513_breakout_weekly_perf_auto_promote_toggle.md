# Task: Implement Gen Strategy Toggle with Automated L-Trade Promotion

## Source
- User Directive: 2026-04-07
- Spawned From: `20260409_211513_breakout_weekly_perf_auto_promote_toggle.md`

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
Enhance `fs/weekly_performance.html` so Gen Strategy rows act as toggle controls. When toggled on, the system should auto-promote new trades for that strategy/product to `is_live_trade: true` and trigger L-Trade creation when the strategy has a positive current-week net return and the live-trade/TWS caps are still available.

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
Scheduled For: 2026-04-10 01:15:13+01:00
Next Scheduled For: 2026-04-10 05:15:13+01:00

## Detailed Logic (when Toggle is TRUE)
1. Trigger: a new trade is created for the selected strategy/product.
2. Pre-check:
   - `count(is_live_trade:true) < max_live_trades`
   - `count(is_live_trade:true) < max_trades_to_tws`
3. Condition: the selected strategy must have positive current-week `net_return`.
4. Action:
   - Set `is_live_trade` to `true`.
   - Trigger L-Trade creation / TWS promotion.
   - Bypass standard promotion filters beyond the required weekly-profit check and the two cap checks above.

## Plan
- [x] 1. UI Enhancement (`weekly_performance.html`)
  - [x] Test: Verify the dashboard wiring still renders a Gen Strategy toggle that posts to `/api/activations` with `auto_promote`.
  - [x] Evidence: Static validation passed against `weekly_performance.html` (`toggleGenStrategy(...)`, `/api/activations`, and `auto_promote: isChecked` present).
- [x] 2. API Extension (`trade_viewer_api.py`)
  - [x] Test: Verify product-scoped deactivation preserves `auto_promote` while other products remain active for the same key.
  - [x] Evidence: Inline Flask client validation passed and persisted `workstream/artefacts/auto_promote_validation_api_manual/activations_validation.json` with `products == ["GBPUSD"]` and `auto_promote == true`.
- [x] 3. Trade Engine Modification (`common.py`)
  - [x] Test: Verify explicit auto-promote toggles bypass the market-bias gate while standard live-order promotion still respects that gate.
  - [x] Evidence: New regression tests in `TradeApps/breakout/fs/tests/test_weekly_auto_promote_common.py` passed.
- [x] 4. Validation
  - [x] Test: Run focused technical validation covering UI wiring, activation persistence, and auto-promote engine behavior.
  - [x] Evidence: `python -m unittest discover ...` passed; inline activation API validation passed; inline HTML wiring validation passed.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`; `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py`
  - Objective-Proved: Auto-promote now bypasses the residual market-bias gate for explicit toggle-driven promotion, and regression coverage was added for the engine path.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Objective-Proved: The weekly performance view still exposes Gen Strategy toggle wiring to `/api/activations` with `auto_promote`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m unittest discover -s C:\Users\edebe\eds\TradeApps\breakout\fs\tests -p test_weekly_auto_promote_common.py -v` -> `Ran 2 tests in 0.004s` / `OK`
  - Objective-Proved: Engine behavior matches the required bias-bypass path for auto-promote while preserving standard bias blocking for non-auto-promote flows.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Inline Flask client validation -> `API auto_promote preservation validation: PASS` with artifact `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_api_manual\activations_validation.json`
  - Objective-Proved: Activation updates preserve `auto_promote` on product-scoped deactivation when the strategy remains active for another product.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Inline HTML validation -> `Weekly performance toggle wiring validation: PASS`
  - Objective-Proved: The UI still contains the expected toggle wiring for the activation API and `auto_promote` flag submission.
  - Status: captured

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Updated `common.py` to support `auto_promote` flag persistence and bypass `daily_target`. Updated `VERSION` in `constants.py`.
- 2026-04-08 12:30: Converted to recurring task every 4 hours. `[V20260408_1230]`
- 2026-04-10 01:18: Reviewed `weekly_performance.html`, `trade_viewer_api.py`, and `common.py` against the task requirements and identified one remaining gap: explicit auto-promote still hit the market-bias gate before L-Trade creation.
- 2026-04-10 01:19: Patched `_handle_live_orders` in `common.py` so active auto-promote paths bypass the market-bias gate while normal promotion paths still respect it.
- 2026-04-10 01:20: Added `test_weekly_auto_promote_common.py` to lock in the auto-promote bias-bypass path and the unchanged standard market-bias block path.
- 2026-04-10 01:23: Ran focused validations for engine behavior, activation persistence, and UI toggle wiring; all checks passed.

## Changes Made
- Updated `BaseBreakoutStrategy._handle_live_orders` in `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py` to evaluate `auto_promote_active` before applying the market-bias block, so explicit auto-promote uses only the required weekly-profit and cap checks.
- Added `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py` with regression coverage for:
  - auto-promote NET orders bypassing the market-bias gate
  - standard live-order promotion continuing to respect the market-bias gate
- Confirmed no additional code changes were required in `weekly_performance.html` or `trade_viewer_api.py` for this execution because the toggle wiring and `auto_promote` persistence path were already implemented and validated successfully.

## Validation
- `python -m unittest discover -s C:\Users\edebe\eds\TradeApps\breakout\fs\tests -p test_weekly_auto_promote_common.py -v`
  - Result: PASS
  - Summary: `Ran 2 tests in 0.004s` / `OK`
- Inline Flask client activation validation against `trade_viewer_api.app.test_client()`
  - Result: PASS
  - Summary: `API auto_promote preservation validation: PASS`
  - Artifact: `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_api_manual\activations_validation.json`
- Inline HTML wiring validation for `weekly_performance.html`
  - Result: PASS
  - Summary: `Weekly performance toggle wiring validation: PASS`

## Risks/Notes
- This run aligned the implementation with the task’s explicit rule that toggle-driven auto-promotion should not be blocked by the market-bias gate.
- Validation for the dashboard UI in this run was static rather than browser-driven; the implementation wiring was verified directly in source and through the API contract.
- `max_live_trades` and `max_trades_to_tws` remain enforced inside `_create_l_trade_order`.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-10 01:23:40
