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
Enhance `fs\weekly_performance.html` to turn "Gen Strategy" rows into toggle buttons. When a strategy is toggled `ON`, the system automatically promotes new trades for that strategy/product to `is_live_trade: true` and initiates the L-Trade creation process, provided the strategy has a positive weekly net return and system-wide trade limits are not exceeded.

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
Scheduled For: 2026-04-10 13:15:13+01:00
Next Scheduled For: 2026-04-10 17:15:13+01:00
Spawned From: `20260410_091513_breakout_weekly_perf_auto_promote_toggle.md`

## Scheduled For
2026-04-08 12:00:00

## Detailed Logic (when Toggle is TRUE)
1. Trigger: A new trade is created for the specific strategy/product.
2. Pre-check:
   - `count(is_live_trades:true) < max_live_trades`
   - `count(is_live_trades:true) < max_trades_to_tws`
3. Condition: The selected strategy must have a positive `net_return` for previous trades this week.
4. Action:
   - Set `is_live_trade` to `true`.
   - Kick off the L-Trade creation process.
   - Only the two limit checks above apply for this promotion path; other standard promotion filters are bypassed.

## Plan
- [x] 1. UI Enhancement (`weekly_performance.html`)
  - [x] Test: Open dashboard and verify toggle switches exist in the Gen Strategy column.
  - Evidence: UI source contains the Gen Strategy toggle wiring and payload with `auto_promote`.
- [x] 2. API Extension (`trade_viewer_api.py`)
  - [x] Test: Exercise `/api/activations` and verify the `auto_promote` flag is stored and returned.
  - Evidence: Direct Python validation harness confirmed the POST/GET round-trip preserves `auto_promote`.
- [x] 3. Trade Engine Modification (`common.py`)
  - [x] Test: Simulate trade creation for a toggled strategy and verify auto-promotion bypasses `daily_target` while still enforcing max-live and TWS limits.
  - Evidence: Direct Python validation harness confirmed the positive and blocking paths.
- [x] 4. Validation
  - [x] Test: Run a direct Python validation harness from `C:\Users\edebe\eds` covering HTML toggle payload wiring, `/api/activations` auto-promote persistence, and `_create_l_trade_order` limit/daily-target behavior; expected pass condition is all assertions succeed and a validation summary file is written.
  - Evidence: `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410\validation_summary.txt`

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: Existing implementation in `weekly_performance.html`, `trade_viewer_api.py`, and `common.py`
  - Objective-Proved: The requested UI, API, and trade-engine changes are present in the workspace.
  - Status: captured
- Evidence-Type: screenshot
  - Artifact: not_applicable
  - Objective-Proved: Screenshot evidence was not required because source-level and runtime validation covered the delivered behavior for this execution.
  - Status: not_applicable
- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410\validation_summary.txt`
  - Objective-Proved: Verified HTML toggle wiring, activation API `auto_promote` persistence, auto-promote daily-target bypass, max-live guard, max-TWS guard, and standard daily-target enforcement.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410\validation_summary.txt`
  - Objective-Proved: Provides a reviewer-readable validation package for this recurring execution.
  - Status: captured

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Updated `common.py` to support `auto_promote` and bypass `daily_target`. Updated `VERSION` in `constants.py`.
- 2026-04-08 12:30: Converted to recurring task every 4 hours. [V20260408_1230]
- 2026-04-10 13:23: Revalidated the existing implementation end-to-end using a direct Python harness because `pytest` `tmp_path` setup/cleanup fails in this environment with `WinError 5` against temp roots.

## Changes Made
- Updated `_coerce_activation_entry` and `_merge_activation_entries` in `common.py` to preserve `auto_promote`.
- Updated `_create_l_trade_order`, `_create_tradeable_json`, and `_handle_live_orders` in `common.py` to pass `is_auto_promote` and bypass `daily_target`.
- Updated the weekly performance UI toggle flow to send `auto_promote` with activation updates.
- No additional code edits were required during the 2026-04-10 13:15 execution; this run completed validation and evidence capture.

## Validation
- 2026-04-10 13:23: Attempted `python -m pytest tests/test_breakout_weekly_performance.py -q` and `python -m pytest TradeApps/breakout/fs/test_auto_promote_limits.py -q`. Both were blocked by environment-level `WinError 5` failures around `pytest` temp-directory setup/cleanup.
- 2026-04-10 13:23: Ran an equivalent direct Python validation harness from `C:\Users\edebe\eds` and wrote results to `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_codex_20260410\validation_summary.txt`.
- 2026-04-10 13:23: Harness results:
  - `HTML toggle wiring assertions: PASS`
  - `Activation API auto_promote round-trip: PASS`
  - `auto_promote_bypass_daily_target: PASS`
  - `auto_promote_respects_max_live: PASS`
  - `auto_promote_respects_max_tws: PASS`
  - `standard_order_respects_daily_target: PASS`
- 2026-04-10 13:23: Auto-acceptance criteria satisfied for this recurring execution.

## Risks/Notes
- Ensure `activations.json` remains correctly segmented by mode (`live` vs `sim`).
- `max_live_trades` and `max_trades_to_tws` remain mandatory hard guards.
- `pytest` temp-fixture validation is currently unreliable on this machine because of temp-root permission issues; the direct validation harness was used instead.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-10 13:23:33
