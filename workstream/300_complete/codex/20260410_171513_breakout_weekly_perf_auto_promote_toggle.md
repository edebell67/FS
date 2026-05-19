# Task: Implement Gen Strategy Toggle with Automated L-Trade Promotion

## Source
- User Directive: 2026-04-07
- Spawned From: `20260410_131513_breakout_weekly_perf_auto_promote_toggle.md`

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
Enhance `TradeApps\breakout\fs\weekly_performance.html` so the weekly performance table exposes per-strategy toggle controls that store `auto_promote` activation state. When enabled, new trades for the selected strategy and product must auto-promote to `is_live_trade: true` and create the L-Trade order only when weekly net return is positive and the system-wide `max_live_trades` and `max_trades_to_tws` caps still allow promotion. Daily-target blocking must be bypassed for this path.

## Context
- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Backend API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Trade Engine: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Regression Tests: `C:\Users\edebe\eds\TradeApps\breakout\fs\test_auto_promote_limits.py`, `C:\Users\edebe\eds\tests\test_breakout_weekly_performance.py`
- Limits: `max_live_trades` and `max_trades_to_tws` from `config.json`
- Activation State: `activations.json` segmented by mode

## Destination Folder
None

## Dependency
Dependency: None
Required Skill: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
Scheduled For: 2026-04-10 17:15:13+01:00
Next Scheduled For: 2026-04-10 21:15:13+01:00

## Detailed Logic (when Toggle is TRUE)
1. Trigger: A new trade is created for the specific strategy and product.
2. Pre-check:
   - `count(is_live_trades:true) < max_live_trades`
   - `count(order_sent_net:true on OPEN trades) < max_trades_to_tws`
3. Condition: The selected strategy must have a positive current-week net return.
4. Action:
   - Set `is_live_trade` to `true`
   - Create the L-Trade promotion order
   - Bypass the normal daily-target guard for this auto-promote path

## Plan
- [x] 1. UI enhancement in `weekly_performance.html`
  - [x] Test: Inspect the weekly dashboard source and verify the table toggle wiring posts activation payloads with `auto_promote: isChecked` for buy and sell net keys.
  - [x] Evidence: `weekly_html_toggle_wiring: PASS` recorded in `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410_run\manual_validation_summary.txt`.
- [x] 2. API extension in `trade_viewer_api.py`
  - [x] Test: Execute the activation API round-trip validation and confirm `auto_promote` persists in `activations.json` for the selected mode and product.
  - [x] Evidence: `activation_api_roundtrip: PASS` recorded in `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410_run\manual_validation_summary.txt`.
- [x] 3. Trade engine modification in `common.py`
  - [x] Test: Execute engine validations covering positive-weekly-net promotion, daily-target bypass, and enforcement of `max_live_trades` and `max_trades_to_tws`.
  - [x] Evidence: `test_auto_promote_bypasses_daily_target_but_still_writes_order: PASS`, `test_auto_promote_still_respects_max_live_trades_limit: PASS`, `test_auto_promote_still_respects_tws_limit: PASS`, `test_handle_live_orders_auto_promotes_only_when_weekly_net_positive: PASS`, and `test_handle_live_orders_blocks_auto_promote_when_weekly_net_not_positive: PASS` recorded in `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410_run\manual_validation_summary.txt`.
- [x] 4. Validation
  - [x] Test: `@' ... '@ | python - *> C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410_run\manual_validation_output.txt`
  - [x] Evidence: Full validation summary captured at `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410_run\manual_validation_summary.txt` with 13/13 checks passing.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Objective-Proved: The weekly performance UI exposes toggle controls that wire the activation payload for strategy auto-promotion.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\test_auto_promote_limits.py`
  - Objective-Proved: Regression coverage now proves the positive-weekly-net gate and blocked non-positive path in addition to the existing limit and daily-target checks.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410_run\manual_validation_summary.txt`
  - Objective-Proved: End-to-end task validation passed for weekly aggregation, UI wiring, activation persistence, daily-target bypass, and live/TWS cap enforcement.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410_run\manual_validation_output.txt`
  - Objective-Proved: Validation logs show the runtime auto-promote branch creating orders on positive weekly net and rejecting promotion when the weekly net is non-positive or limits are exceeded.
  - Status: captured

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Updated `common.py` to support the `auto_promote` flag and bypass the daily-target guard for auto-promoted trades. Updated `constants.py`.
- 2026-04-08 12:30: Converted the task to a recurring four-hour validation work item.
- 2026-04-10 17:10: Reviewed the required lifecycle skill and inspected the current UI, API, and trade-engine implementation.
- 2026-04-10 17:17: Added focused regression tests in `test_auto_promote_limits.py` for the positive-weekly-net auto-promote path and the blocked non-positive-weekly-net path.
- 2026-04-10 17:24: Ran a clean manual validation harness covering weekly aggregation, dashboard wiring, activation persistence, daily-target bypass, and cap enforcement; captured outputs under `workstream\artefacts\auto_promote_validation_codex_20260410_run`.

## Changes Made
- Existing production implementation already present and validated in:
  - `weekly_performance.html` for toggle wiring
  - `trade_viewer_api.py` for activation persistence of `auto_promote`
  - `common.py` for weekly-net gating, `is_live_trade` promotion, and limit-guard enforcement
- Added regression tests in `TradeApps\breakout\fs\test_auto_promote_limits.py` to cover:
  - auto-promotion only when weekly net is positive
  - rejection when weekly net is zero or negative
  - previously implemented daily-target bypass and cap checks

## Validation
- Manual validation harness executed on 2026-04-10 via inline Python command and wrote:
  - `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410_run\manual_validation_output.txt`
  - `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410_run\manual_validation_summary.txt`
- Validation result summary:
  - `weekly_bounds: PASS`
  - `weekly_aggregate_full_week: PASS`
  - `weekly_api_aligned_payload: PASS`
  - `weekly_html_sortable_columns: PASS`
  - `weekly_html_toggle_wiring: PASS`
  - `weekly_strategy_gen_strategy_split: PASS`
  - `activation_api_roundtrip: PASS`
  - `test_auto_promote_bypasses_daily_target_but_still_writes_order: PASS`
  - `test_auto_promote_still_respects_max_live_trades_limit: PASS`
  - `test_auto_promote_still_respects_tws_limit: PASS`
  - `test_standard_live_order_still_respects_daily_target: PASS`
  - `test_handle_live_orders_auto_promotes_only_when_weekly_net_positive: PASS`
  - `test_handle_live_orders_blocks_auto_promote_when_weekly_net_not_positive: PASS`
- Pytest was also attempted, but Windows denied access to the pytest base temp directory during teardown. The inline manual harness was used as the reliable validation path and all checks passed.

## Risks/Notes
- The recurring task remains sensitive to Windows ACL issues around pytest temp-folder cleanup; direct validation via the captured harness is currently more reliable on this workspace.
- Promotion still depends on weekly aggregation artifacts being available for the current trading week.
- Mode-scoped activation data in `activations.json` must remain consistent across live and sim runs.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-10 17:25:07
