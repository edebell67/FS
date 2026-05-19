# Task: Implement Gen Strategy Toggle with Automated L-Trade Promotion

## Source
- User Directive: 2026-04-07
- Spawned From: `20260410_171513_breakout_weekly_perf_auto_promote_toggle.md`

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
Enhance `TradeApps/breakout/fs/weekly_performance.html` so the `Gen Strategy` column acts as a toggle for product-scoped strategy auto-promotion. When enabled, new qualifying trades for that strategy/product should be promoted to `is_live_trade: true` and sent into the L-Trade creation path when weekly net return is positive, while still enforcing `max_live_trades` and `max_trades_to_tws`.

## Context
- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Backend API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Trade Engine: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Validation: `C:\Users\edebe\eds\tests\test_breakout_weekly_performance.py`
- Validation: `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py`
- Validation: `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py`

## Destination Folder
None

## Dependency
Dependency: None
Required Skill: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
Scheduled For: 2026-04-10 21:15:13+01:00
Next Scheduled For: 2026-04-11 01:15:13+01:00

## Detailed Logic (when Toggle is TRUE)
1. Trigger: a new trade is created for the specific strategy/product.
2. Pre-check:
   - `count(is_live_trades:true) < max_live_trades`
   - `count(is_live_trades:true) < max_trades_to_tws`
3. Condition: the selected strategy has positive current-week `net_return`.
4. Action:
   - Set `is_live_trade` to `true`.
   - Initiate the L-Trade creation process.
   - Bypass the standard daily-target/global-threshold path for these toggled strategies, while still enforcing the two trade-cap guards above.

## Plan
- [x] 1. UI Enhancement (`weekly_performance.html`)
  - [x] Test: `pytest tests/test_breakout_weekly_performance.py -k test_weekly_performance_html_wires_gen_strategy_toggle_auto_promote`
  - Evidence: `workstream/artefacts/auto_promote_validation_codex_20260410_run/pytest_auto_promote_validation.log` shows the HTML toggle wiring assertion passing.
- [x] 2. API Extension (`trade_viewer_api.py`)
  - [x] Test: `pytest tests/test_breakout_weekly_performance.py -k test_activation_api_round_trip_preserves_auto_promote && pytest TradeApps/breakout/fs/tests/test_weekly_auto_promote_activation_api.py`
  - Evidence: `workstream/artefacts/auto_promote_validation_codex_20260410_run/pytest_auto_promote_validation.log` shows both activation API persistence tests passing.
- [x] 3. Trade Engine Modification (`common.py`)
  - [x] Test: `pytest TradeApps/breakout/fs/tests/test_weekly_auto_promote_common.py`
  - Evidence: `workstream/artefacts/auto_promote_validation_codex_20260410_run/pytest_auto_promote_validation.log` shows market-bias bypass, daily-target bypass, and cap-enforcement tests passing.
- [x] 4. Validation
  - [x] Test: `pytest tests/test_breakout_weekly_performance.py TradeApps/breakout/fs/tests/test_weekly_auto_promote_activation_api.py TradeApps/breakout/fs/tests/test_weekly_auto_promote_common.py`
  - Evidence: `14 passed, 2 warnings in 10.32s` recorded in `workstream/artefacts/auto_promote_validation_codex_20260410_run/pytest_auto_promote_validation.log`.

## Evidence
Objective-Delivery-Coverage: 95%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\tests\test_breakout_weekly_performance.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py`
  - Objective-Proved: Regression coverage now explicitly protects the Gen Strategy toggle wiring, activation persistence, daily-target bypass for auto-promote, and trade-cap enforcement.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410_run\pytest_auto_promote_validation.log`
  - Objective-Proved: The targeted validation slice for UI wiring, API persistence, and common auto-promote guard behavior passed end-to-end.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Objective-Proved: Reviewer entry point for confirming the visible `Gen Strategy` toggle state and live behavior in the dashboard.
  - Status: planned
- Evidence-Type: user_feedback
  - Artifact: pending user verification request/response for the live dashboard toggle and promotion flow
  - Objective-Proved: Final user-visible confirmation that the shipped behavior matches the requested workflow in the running app.
  - Status: planned

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Existing implementation updated `common.py` to support `auto_promote` flag and daily-target bypass. `constants.py` version bumped in prior execution.
- 2026-04-08 12:30: Converted to recurring task every 4 hours. [V20260408_1230]
- 2026-04-10 21:16: Read `skills/workstream-task-lifecycle/SKILL.md` and this task file before taking action, per repository instructions.
- 2026-04-10 21:18: Audited `weekly_performance.html`, `trade_viewer_api.py`, and `common.py`; confirmed product code already implemented the requested toggle, API persistence, and auto-promotion path.
- 2026-04-10 21:20: Ran targeted pytest validation; initial run exposed sandbox temp-directory permission errors unrelated to feature logic.
- 2026-04-10 21:23: Updated regression tests to use repo-local temp directories instead of pytest/tmpfile defaults and added direct guard coverage for daily-target bypass plus `max_live_trades` / `max_trades_to_tws` enforcement.
- 2026-04-10 21:25: Re-ran the targeted validation slice successfully and captured the output log under `workstream/artefacts/auto_promote_validation_codex_20260410_run/`.

## Changes Made
- No product-code changes were required in `TradeApps/breakout/fs/weekly_performance.html`, `TradeApps/breakout/fs/trade_viewer_api.py`, or `TradeApps/breakout/fs/common.py`; the requested functionality was already present in the workspace.
- Updated `tests/test_breakout_weekly_performance.py` to validate the activation API round-trip using a repo-local temp directory.
- Updated `TradeApps/breakout/fs/tests/test_weekly_auto_promote_activation_api.py` to validate product-scoped deactivation with preserved `auto_promote` state using repo-local temp directories.
- Expanded `TradeApps/breakout/fs/tests/test_weekly_auto_promote_common.py` to cover:
  - market-bias bypass when auto-promote is active,
  - daily-target bypass for auto-promoted trades,
  - daily-target blocking for standard trades,
  - `max_live_trades` enforcement for auto-promoted trades,
  - `max_trades_to_tws` enforcement for auto-promoted trades.

## Validation
- 2026-04-10 21:19: `pytest tests/test_breakout_weekly_performance.py TradeApps/breakout/fs/tests/test_weekly_auto_promote_activation_api.py TradeApps/breakout/fs/tests/test_weekly_auto_promote_common.py`
  - Result: blocked by sandbox temp-root permissions under `C:\Users\edebe\AppData\Local\Temp\pytest-of-edebe`.
- 2026-04-10 21:24: `pytest tests/test_breakout_weekly_performance.py TradeApps/breakout/fs/tests/test_weekly_auto_promote_activation_api.py TradeApps/breakout/fs/tests/test_weekly_auto_promote_common.py`
  - Result: `14 passed, 2 warnings in 10.32s`
  - Warning Summary: `trade_viewer_api.py:3367` emits a deprecation warning for `datetime.utcnow()`.
- 2026-04-10 21:26: User verification will be requested in the completion response for:
  - Gen Strategy toggle rendering in the weekly dashboard.
  - Auto-promotion behavior for a positive-weekly-net strategy.
  - Guard behavior when `max_live_trades` or `max_trades_to_tws` is already saturated.

## Risks/Notes
- Manual browser verification is still pending for the visible dashboard toggle and live promotion flow.
- The validation slice surfaced a non-blocking deprecation warning in `trade_viewer_api.py` (`datetime.utcnow()`); it does not block this task but should be cleaned up separately.
- This execution validated and hardened the existing implementation rather than introducing new product logic.

## Completion Status
- State: AWAITING_USER_VERIFICATION
- Timestamp: 2026-04-10 21:26:11 +01:00
