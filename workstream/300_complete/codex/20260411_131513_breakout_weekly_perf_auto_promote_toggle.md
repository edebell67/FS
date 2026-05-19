# Task: Implement Gen Strategy Toggle with Automated L-Trade Promotion

## Source
- User Directive: 2026-04-07
- Spawned From: `20260411_091513_breakout_weekly_perf_auto_promote_toggle.md`

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
Enhance `TradeApps/breakout/fs/weekly_performance.html` so the Gen Strategy column uses toggle controls. When toggled on, the selected strategy/product should automatically promote newly created trades to `is_live_trade: true` and generate the L-Trade payload, provided the strategy's current-week net return is positive and the system still respects `max_live_trades` and `max_trades_to_tws`.

## Context
- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Backend API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Trade Engine: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Config limits: `max_live_trades`, `max_trades_to_tws`, `daily_target`
- Activation state: `C:\Users\edebe\eds\TradeApps\breakout\fs\activations.json`

## Destination Folder
None

## Dependency
Dependency: None
Required Skill: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
Scheduled For: 2026-04-11 13:15:13+01:00
Next Scheduled For: 2026-04-11 17:15:13+01:00

## Detailed Logic (when Toggle is TRUE)
1. Trigger on new trade creation for the selected strategy/product.
2. Pre-check:
   - `count(is_live_trade=true) < max_live_trades`
   - `count(order_sent_to_tws=true) < max_trades_to_tws`
3. Condition:
   - current-week net return for the selected strategy must be positive.
4. Action:
   - set `is_live_trade` to `true`
   - create the L-Trade order payload / promotion artefact
   - bypass the normal daily-target guard for this promotion path
   - do not bypass the two hard capacity limits above

## Plan
- [x] 1. UI Enhancement (`weekly_performance.html`)
  - [x] Test: Inspect the weekly performance page implementation and confirm the Gen Strategy column renders toggle controls wired to `/api/activations`.
  - Evidence: `toggleGenStrategy()` posts `auto_promote` payloads for buy/sell net keys and row rendering binds checkbox state to activation status.
- [x] 2. API Extension (`trade_viewer_api.py`)
  - [x] Test: Run `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q` and confirm activation persistence plus grid-live sync pass.
  - Evidence: `2 passed in 2.20s`; API preserves `auto_promote` on scoped deactivation and syncs weekly-performance activations into `grid_live.json`.
- [x] 3. Trade Engine Modification (`common.py`)
  - [x] Test: Run `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q` and confirm market-bias bypass plus limit enforcement logic pass.
  - Evidence: `6 passed in 1.56s`; engine bypasses market-bias and daily-target gating for auto-promote while still enforcing hard live/TWS limits.
- [x] 4. Validation
  - [x] Test: Run targeted technical validation for the full auto-promote path:
    - `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q`
    - `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q`
    - `python -m pytest TradeApps\breakout\fs\test_auto_promote_limits.py -q`
    - fallback manual equivalence run for `test_auto_promote_limits.py` using an inline Python harness inside `TradeApps\breakout\fs\codex_validation_manual_20260411`
  - Evidence: pytest suites for UI/API-backed activation and engine behavior passed; the standalone `test_auto_promote_limits.py` pytest run was blocked by temp-directory permissions, and the equivalent inline harness passed all six assertions against the same code paths.

## Evidence
Objective-Delivery-Coverage: 95%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/weekly_performance.html`
  - Objective-Proved: Weekly Performance UI contains Gen Strategy toggle controls that post `auto_promote` activation payloads through `/api/activations`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q`
  - Objective-Proved: Engine path bypasses standard market-bias gating for auto-promote and still enforces live-trade/TWS hard limits.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q`
  - Objective-Proved: Activation API persists `auto_promote` correctly and syncs weekly-performance toggles into `grid_live.json`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Inline Python validation run in `TradeApps/breakout/fs/codex_validation_manual_20260411`
  - Objective-Proved: Equivalent assertions for `test_auto_promote_limits.py` passed for daily-target bypass, live/TWS limit enforcement, and weekly-net positive/negative promotion behavior.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `TradeApps/breakout/fs/weekly_performance.html` opened against the local API/browser flow by user
  - Objective-Proved: Final visual/user-facing confirmation that the toggle behaves correctly in the live dashboard.
  - Status: planned

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Updated `common.py` to support `auto_promote` flag and bypass `daily_target`. Updated `VERSION` in `constants.py`.
- 2026-04-08 12:30: Converted to recurring task every 4 hours. [V20260408_1230]
- 2026-04-11 13:15: Re-read lifecycle instructions and inspected the current workspace implementation before making changes.
- 2026-04-11 13:23: Confirmed the feature implementation already exists in `weekly_performance.html`, `trade_viewer_api.py`, and `common.py`; no additional code changes were required in this execution.
- 2026-04-11 13:25: Ran targeted regression suites for `test_weekly_auto_promote_common.py` and `test_weekly_auto_promote_activation_api.py`; both passed.
- 2026-04-11 13:26: Attempted `test_auto_promote_limits.py` under pytest; run was blocked by temp-directory permission errors in the environment rather than feature assertions.
- 2026-04-11 13:27: Executed an inline Python validation harness covering the same auto-promote limit scenarios; all six assertions passed.
- 2026-04-11 13:28: Updated lifecycle checklist, evidence, and validation notes; task remains open pending user-facing verification of the dashboard toggle.

## Changes Made
- Existing implementation already present in workspace:
  - `TradeApps/breakout/fs/weekly_performance.html`
    - Gen Strategy rendered as row-level toggle controls.
    - Toggle POST payload includes `auto_promote` for both `buy_net` and `sell_net`.
  - `TradeApps/breakout/fs/trade_viewer_api.py`
    - `/api/activations` persists `auto_promote`.
    - weekly-performance activation updates can sync into `grid_live.json`.
  - `TradeApps/breakout/fs/common.py`
    - auto-promote path checks positive weekly net before promotion.
    - auto-promoted L-Trade creation bypasses `daily_target`.
    - auto-promoted L-Trade creation still enforces `max_live_trades` and `max_trades_to_tws`.
- This execution changed the lifecycle file only; no additional code edits were needed after verification.

## Validation
- `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q`
  - Result: PASS
  - Summary: `6 passed in 1.56s`
- `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q`
  - Result: PASS
  - Summary: `2 passed in 2.20s`
  - Note: emits existing `datetime.utcnow()` deprecation warnings in `trade_viewer_api.py`, unrelated to this task outcome.
- `python -m pytest TradeApps\breakout\fs\test_auto_promote_limits.py -q`
  - Result: ENVIRONMENT BLOCKED
  - Summary: pytest temp-path setup hit Windows permission errors under both default temp and explicit `--basetemp` attempts.
- Inline Python validation harness executed from `C:\Users\edebe\eds`
  - Result: PASS
  - Summary:
    - `auto_promote_bypasses_daily_target_but_still_writes_order=PASS`
    - `auto_promote_still_respects_max_live_trades_limit=PASS`
    - `auto_promote_still_respects_tws_limit=PASS`
    - `standard_live_order_still_respects_daily_target=PASS`
    - `handle_live_orders_auto_promotes_only_when_weekly_net_positive=PASS`
    - `handle_live_orders_blocks_auto_promote_when_weekly_net_not_positive=PASS`
- User verification requested:
  - Open `TradeApps/breakout/fs/weekly_performance.html` against the local API, toggle a positive-week strategy on, and confirm:
    - the toggle persists
    - activation/grid-live state updates correctly
    - a newly created qualifying trade is auto-promoted

## Risks/Notes
- Final browser-level verification is still pending; this task changes user-visible behavior, so the dashboard should be checked once in the live local flow.
- `test_auto_promote_limits.py` is valid logically, but current pytest temp-dir handling is unreliable in this environment due permission restrictions; the fallback manual harness covered those assertions.
- `trade_viewer_api.py` still contains `datetime.utcnow()` usage that produces deprecation warnings during tests; this did not block delivery of the requested behavior.

## Completion Status
- State: AWAITING_USER_VERIFICATION
- Timestamp: 2026-04-11 13:28:00+01:00
