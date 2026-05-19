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
Enhance `TradeApps\breakout\fs\weekly_performance.html` so Gen Strategy rows act as toggle buttons. When toggled on, new trades for that strategy and product should auto-promote to `is_live_trade: true` and trigger L-Trade creation when the strategy has positive weekly net return and the system remains within `max_live_trades` and `max_trades_to_tws`. Auto-promoted trades must bypass the normal daily-target gate.

## Context
- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Backend API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Trade Engine: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Limits: `max_live_trades` and `max_trades_to_tws` from `TradeApps\breakout\fs\config.json`
- Activation State: `TradeApps\breakout\fs\activations.json` segmented by mode

## Destination Folder
None

## Dependency
Dependency: None
Required Skill: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
Scheduled For: 2026-04-12 21:15:13+01:00
Next Scheduled For: 2026-04-13 01:15:13+01:00
Spawned From: `20260412_171513_breakout_weekly_perf_auto_promote_toggle.md`

## Scheduled For
2026-04-08 12:00:00

## Detailed Logic (when Toggle is TRUE)
1. Trigger: A new trade is created for the specific strategy and product.
2. Pre-check:
   - `count(is_live_trade:true) < max_live_trades`
   - `count(order_sent_net:true on OPEN trades) < max_trades_to_tws`
3. Condition: The selected strategy must have positive weekly total net return.
4. Action:
   - Set the trade attribute `is_live_trade` to `true`.
   - Kick off the L-Trade creation process.
   - Only the two trade-limit checks above should gate promotion; the daily-target block is bypassed for auto-promoted trades.

## Plan
- [x] 1. UI Enhancement (`weekly_performance.html`)
  - [x] Test: `rg -n "toggleGenStrategy|auto_promote|/api/activations" TradeApps\breakout\fs\weekly_performance.html` returns the toggle handler, persisted state wiring, and activation POST payload.
  - Evidence: `weekly_performance.html` contains `toggleGenStrategy(...)`, renders the Gen Strategy switch, and posts `auto_promote: isChecked` for buy/sell activation keys.
- [x] 2. API Extension (`trade_viewer_api.py`)
  - [x] Test: `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q` passes.
  - Evidence: API tests confirm product-scoped activation updates preserve `auto_promote` and weekly-performance toggles sync to `grid_live.json`.
- [x] 3. Trade Engine Modification (`common.py`)
  - [x] Test: `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q` passes.
  - Evidence: Engine tests confirm auto-promote bypasses market-bias and daily-target gates while still enforcing `max_live_trades` and `max_trades_to_tws`.
- [x] 4. Validation
  - [x] Test: Run both targeted pytest suites and review the wired code paths in the UI, API, and engine files.
  - Evidence: `7 passed in 7.75s` for `test_weekly_auto_promote_common.py`; `2 passed, 5 warnings in 9.00s` for `test_weekly_auto_promote_activation_api.py`.

## Evidence
Objective-Delivery-Coverage: 95%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `TradeApps\breakout\fs\weekly_performance.html`, `TradeApps\breakout\fs\trade_viewer_api.py`, `TradeApps\breakout\fs\common.py`
  - Objective-Proved: The workspace contains the implemented UI toggle flow, activation persistence/sync logic, and auto-promotion engine guards required by the task.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q` -> `7 passed in 7.75s`
  - Objective-Proved: Auto-promotion uses weekly total net, bypasses blocked bias and daily-target checks, and still respects trade-count/TWS limits.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q` -> `2 passed, 5 warnings in 9.00s`
  - Objective-Proved: Activation API persists `auto_promote` correctly and synchronizes weekly-performance toggles into `grid_live.json`.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `TradeApps\breakout\fs\weekly_performance.html` via the local trade viewer plus `/api/activations` round-trip in the running app
  - Objective-Proved: Final user-facing confirmation that the toggle appears and behaves correctly in the live dashboard.
  - Status: planned

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Updated `common.py` to preserve `auto_promote`, pass `is_auto_promote` through L-Trade creation, and bypass the daily-target gate for auto-promoted trades.
- 2026-04-08 12:30: Converted task into a recurring 4-hour execution slot. [V20260408_1230]
- 2026-04-12 21:17: Verified the existing implementation across `weekly_performance.html`, `trade_viewer_api.py`, and `common.py`; executed targeted API and engine pytest suites; refreshed this lifecycle file with concrete evidence and awaiting-user-verification status.

## Changes Made
- `TradeApps\breakout\fs\weekly_performance.html`
  - Gen Strategy column renders a live toggle.
  - `toggleGenStrategy(...)` posts buy/sell activation entries with `auto_promote` and `sync_grid_live`.
  - Auto-select logic reuses the same toggle path for automated leader switching.
- `TradeApps\breakout\fs\trade_viewer_api.py`
  - `/api/activations` GET/POST normalizes and persists `auto_promote`.
  - Weekly-performance activation writes can synchronize into `grid_live.json`.
  - Existing-open-trade promotion helpers remain available for activation-driven promotion.
- `TradeApps\breakout\fs\common.py`
  - Activation normalization preserves `auto_promote`.
  - `_is_auto_promote_active(...)` checks active toggles from `activations.json`.
  - `_handle_live_orders(...)` can promote trades when weekly total net is positive even if market bias would otherwise block standard promotion.
  - `_create_l_trade_order(...)` bypasses `daily_target` only for auto-promoted trades, while still enforcing `max_live_trades` and `max_trades_to_tws`.

## Validation
- 2026-04-12: `rg -n "toggleGenStrategy|auto_promote|/api/activations" TradeApps\breakout\fs\weekly_performance.html`
  - Result: confirmed UI toggle rendering, activation POST wiring, and persisted auto-select reuse.
- 2026-04-12: `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q`
  - Result: passed, `7 passed in 7.75s`.
- 2026-04-12: `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q`
  - Result: passed, `2 passed, 5 warnings in 9.00s`.
  - Warning note: pytest surfaced existing `datetime.utcnow()` deprecation warnings from `trade_viewer_api.py`; no functional failure.
- 2026-04-12: User verification required before lifecycle completion.
  - Requested verification scope: confirm the Gen Strategy toggle is visible in `weekly_performance.html`, persists activation state, and causes the intended auto-promotion behavior in the running dashboard.

## Risks/Notes
- User-facing verification is still pending; task should remain out of `300_complete` until pass/fail is captured.
- Existing deprecation warnings in `trade_viewer_api.py` use `datetime.utcnow()`; they do not block this feature but should be cleaned up separately.
- `activations.json` must remain correctly segmented by mode so live/sim toggles do not bleed across environments.

## Completion Status
- State: Awaiting user verification
- Timestamp: 2026-04-12 21:17:32+01:00
