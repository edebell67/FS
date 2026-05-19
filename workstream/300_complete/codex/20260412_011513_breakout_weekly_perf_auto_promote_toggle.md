# Task: Implement Gen Strategy Toggle with Automated L-Trade Promotion

## Source
- User Directive: 2026-04-07
- Spawned From: `20260411_211513_breakout_weekly_perf_auto_promote_toggle.md`

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
Enhance `TradeApps/breakout/fs/weekly_performance.html` so "Gen Strategy" rows act as toggle buttons. When toggled on, new trades for that strategy and product should be auto-promoted to `is_live_trade: true` and pushed into the L-Trade creation flow if weekly net return is positive and only the live-trade and TWS trade-count limits allow it.

## Context
- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Backend API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Trade engine: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Limits: `max_live_trades` and `max_trades_to_tws` from `config.json`
- Activation state: `activations.json` segmented by mode

## Destination Folder
None

## Dependency
Dependency: None
Required Skill: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
Scheduled For: 2026-04-12 01:15:13+01:00
Next Scheduled For: 2026-04-12 05:15:13+01:00

## Detailed Logic (when Toggle is TRUE)
1. Trigger: A new trade is created for the specific strategy and product.
2. Pre-check:
   - `count(is_live_trade:true) < max_live_trades`
   - `count(is_live_trade:true) < max_trades_to_tws`
3. Condition: The selected strategy must have a positive current-week total `net_return`.
4. Action:
   - Set the trade attribute `is_live_trade` to `true`.
   - Kick off the L-Trade creation process.
   - Bypass other standard promotion filters such as the global `daily_target`; only the two limit checks above still apply.

## Plan
- [x] 1. UI Enhancement (`weekly_performance.html`)
  - [x] Test: Open the dashboard code path and verify Gen Strategy renders as toggle switches that post `auto_promote` for both buy and sell activation keys.
  - Evidence: Verified in `tests/test_breakout_weekly_performance.py::test_weekly_performance_html_wires_gen_strategy_toggle_auto_promote`.
- [x] 2. API Extension (`trade_viewer_api.py`)
  - [x] Test: Exercise `/api/activations` round-trip and verify `auto_promote` persists with product-scoped activation metadata and weekly-performance grid sync.
  - Evidence: Verified in `tests/test_breakout_weekly_performance.py::test_activation_api_round_trip_preserves_auto_promote` and `TradeApps/breakout/fs/tests/test_weekly_auto_promote_activation_api.py`.
- [x] 3. Trade Engine Modification (`common.py`)
  - [x] Test: Verify auto-promotion uses positive weekly net, bypasses `daily_target`, and still respects `max_live_trades` and `max_trades_to_tws`.
  - Evidence: Verified in `TradeApps/breakout/fs/tests/test_weekly_auto_promote_common.py` and `TradeApps/breakout/fs/test_auto_promote_limits.py`.
- [x] 4. Validation
  - [x] Test: Run focused end-to-end validation across UI wiring, activation persistence, grid sync, and trade-promotion limit enforcement.
  - Evidence: `workstream/artefacts/auto_promote_validation_codex_20260412/validation_summary.txt`

## Evidence
Objective-Delivery-Coverage: 95%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/weekly_performance.html`, `TradeApps/breakout/fs/trade_viewer_api.py`, `TradeApps/breakout/fs/common.py`, `TradeApps/breakout/fs/constants.py`
  - Objective-Proved: Required UI, API, and engine logic is present in the workspace.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `workstream/artefacts/auto_promote_validation_codex_20260412/validation_summary.txt`
  - Objective-Proved: Targeted validation passed for toggle wiring, activation persistence, weekly-performance sync, and auto-promotion guard behavior.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `workstream/artefacts/auto_promote_validation_codex_20260412/manual_tmp/test_auto_promote_bypasses_daily_target_but_still_writes_order/breakout_unknown_EURUSD_breakout_demo_BUY_20260412_011837_open_tradeable.json`
  - Objective-Proved: Auto-promoted trade flow still writes the expected L-Trade order payload when daily target is already met.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `TradeApps/breakout/fs/weekly_performance.html`
  - Objective-Proved: The weekly dashboard code path exposes the Gen Strategy toggle and posts `auto_promote` through the activation API contract.
  - Status: captured
- Evidence-Type: user_feedback
  - Artifact: pending_user_verification
  - Objective-Proved: Final dashboard behavior has been confirmed by the user in the live UI.
  - Status: planned

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Updated `common.py` to support `auto_promote` propagation and L-Trade creation bypass of `daily_target` for auto-promoted trades. Updated `constants.py` version marker.
- 2026-04-08 12:30: Converted task to recurring execution every 4 hours. `[V20260408_1230]`
- 2026-04-12 01:18: Re-read lifecycle instructions and audited the active implementation across `weekly_performance.html`, `trade_viewer_api.py`, and `common.py`.
- 2026-04-12 01:19: Confirmed the required feature code was already present; no additional workspace code edits were required in this execution.
- 2026-04-12 01:23: Ran focused validation for the weekly performance UI wiring, activation API persistence, weekly grid sync, and common auto-promotion behavior. Captured summary under `workstream/artefacts/auto_promote_validation_codex_20260412/validation_summary.txt`.
- 2026-04-12 01:18:37: Directly executed the legacy limit tests that rely on `tmp_path` after isolating the pytest cleanup issue; all four assertions passed and produced an order artifact for the bypass case.

## Changes Made
- Existing implementation retained:
  - `_coerce_activation_entry` and `_merge_activation_entries` in `common.py` preserve `auto_promote`.
  - `_handle_live_orders`, `_create_tradeable_json`, and `_create_l_trade_order` in `common.py` propagate `is_auto_promote`, require positive weekly net, bypass `daily_target`, and still enforce `max_live_trades` and `max_trades_to_tws`.
  - `weekly_performance.html` posts `auto_promote` from the Gen Strategy toggle for both buy and sell activation keys.
  - `/api/activations` in `trade_viewer_api.py` persists `auto_promote` metadata and syncs weekly-performance toggles into `grid_live.json`.
- This execution added validation artefacts only:
  - `workstream/artefacts/auto_promote_validation_codex_20260412/validation_summary.txt`
  - `workstream/artefacts/auto_promote_validation_codex_20260412/manual_tmp/test_auto_promote_bypasses_daily_target_but_still_writes_order/breakout_unknown_EURUSD_breakout_demo_BUY_20260412_011837_open_tradeable.json`

## Validation
- 2026-04-12 01:20 UTC+01 command:
  - `python -m pytest tests\test_breakout_weekly_performance.py TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py --basetemp=C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260412\basetemp_core`
  - Result: `16 passed, 6 warnings in 7.73s`
- 2026-04-12 01:18 UTC+01 command:
  - Inline Python runner invoked the legacy cases in `TradeApps\breakout\fs\test_auto_promote_limits.py`
  - Result: 4 direct-execution cases passed
  - Passed cases:
    - `test_auto_promote_bypasses_daily_target_but_still_writes_order`
    - `test_auto_promote_still_respects_max_live_trades_limit`
    - `test_auto_promote_still_respects_tws_limit`
    - `test_standard_live_order_still_respects_daily_target`
- Environment note:
  - Direct standalone `pytest` execution of `TradeApps\breakout\fs\test_auto_promote_limits.py` is affected by a pytest tmpdir cleanup permission error in this workspace after the assertions run. The underlying assertions still pass when executed directly, and the validation summary records that limitation.
- User verification request:
  - Pending. The accompanying response requests pass/fail confirmation for the live weekly dashboard toggle behavior.

## Risks/Notes
- User-visible verification is still required in the live dashboard before promoting this task to complete.
- The standalone pytest cleanup permission issue should be investigated separately if that legacy test file needs to remain part of a broader automated suite.
- `activations.json` must continue to remain mode-segmented so live and sim toggles do not bleed across environments.

## Completion Status
- State: AWAITING_USER_VERIFICATION
- Timestamp: 2026-04-12 01:23:00+01:00
