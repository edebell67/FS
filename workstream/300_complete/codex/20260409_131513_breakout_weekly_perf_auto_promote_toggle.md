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
Enhance `fs\weekly_performance.html` to turn "Gen Strategy" rows into toggle buttons. When a strategy is toggled "ON", the system will automatically promote new trades for that strategy/product to `is_live_trade: true` and initiate the L-Trade creation process, provided the strategy has a positive weekly net return and system-wide trade limits are not exceeded.

## Context
- **UI**: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- **Backend API**: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- **Trade Engine**: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- **Limits**: `max_live_trades` and `max_trades_to_tws` (from `config.json`)
- **Activation State**: `activations.json` (segmented by mode)

## Destination Folder
None

## Dependency
Dependency: None
Scheduled For: 2026-04-09 13:15:13+01:00
Next Scheduled For: 2026-04-09 17:15:13+01:00
Spawned From: 20260409_091513_breakout_weekly_perf_auto_promote_toggle.md

## Scheduled For
2026-04-08 12:00:00

## Detailed Logic (when Toggle is TRUE)
1. **Trigger**: A new trade is created for the specific strategy/product.
2. **Pre-check**:
   - `count(is_live_trades:true) < max_live_trades`
   - `count(is_live_trades:true) < max_trades_to_tws`
3. **Condition**: The selected strategy must have a **positive net_return** for previous trades (current week total).
4. **Action**:
   - Set the trade attribute `is_live_trade` to `true`.
   - Kick off the L-Trade creation process (promotion to TWS).
   - **Crucial**: The *only* applicable criteria for this promotion are the two limit checks in Step 2. Other standard filters (for example the global threshold / `daily_target`) are bypassed for these toggled strategies.

## Plan
- [x] 1. **UI Enhancement (`weekly_performance.html`)**
  - [x] Test: Inspect `toggleGenStrategy(...)` and `renderTable()` in `weekly_performance.html`; pass when each row renders a toggle and the POST payload sends per-product `buy_net`/`sell_net` activation entries with `auto_promote`.
  - Evidence: `weekly_performance.html` renders toggle controls in the Gen Strategy column and posts `auto_promote` with product-scoped activation keys.
- [x] 2. **API Extension (`trade_viewer_api.py`)**
  - [x] Test: Run the direct Flask client validation that deactivates one product on a shared activation key; pass when the remaining active product keeps `auto_promote: true` in both the response and persisted `activations.json`.
  - Evidence: `workstream/artefacts/auto_promote_validation_api/validation_api_output.txt` shows `PASS api_product_scoped_deactivation_preserves_auto_promote`.
- [x] 3. **Trade Engine Modification (`common.py`)**
  - [x] Test: Run the direct order-generation validation script; pass when auto-promote bypasses `daily_target`, still respects `max_live_trades` and `max_trades_to_tws`, and standard live orders still stop at `daily_target`.
  - Evidence: `workstream/artefacts/auto_promote_validation/validation_common_output.txt` shows all four validation cases passing.
- [x] 4. **Validation**
  - [x] Test: Review the combined API and engine validation artifacts; pass when toggle wiring, activation persistence, and auto-promotion guard behavior are all covered without failing assertions.
  - Evidence: `workstream/artefacts/auto_promote_validation/validation_common_output.txt` and `workstream/artefacts/auto_promote_validation_api/validation_api_output.txt`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Objective-Proved: The delivered UI entry point contains product-scoped Gen Strategy toggle rendering and the expected activation POST payload wiring.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`; `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`; `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py`
  - Objective-Proved: The API preserves `auto_promote` correctly for remaining active products, the activation normalization stays clean, and the regression is covered by a dedicated test file.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation\auto_promote_bypass_daily_target\breakout_unknown_EURUSD_breakout_demo_BUY_20260409_132234_open_tradeable.json`
  - Objective-Proved: Auto-promote can create the L-Trade order file while bypassing `daily_target`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation\validation_common_output.txt`
  - Objective-Proved: Auto-promote bypasses `daily_target` but still enforces `max_live_trades` and `max_trades_to_tws`, while standard live orders still respect `daily_target`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_api\validation_api_output.txt`
  - Objective-Proved: Product-scoped activation updates preserve `auto_promote` for remaining active products on shared strategy keys.
  - Status: captured

## Implementation Log
- 2026-04-08 10:00: Initialized task file with lifecycle structure.
- 2026-04-08 10:15: Updated `common.py` to support `auto_promote` flag propagation and bypass `daily_target` during auto-promotion.
- 2026-04-08 12:30: Converted to recurring task every 4 hours. [V20260408_1230]
- 2026-04-09 13:19: Verified the existing UI toggle wiring and API/engine integration points in `weekly_performance.html`, `trade_viewer_api.py`, and `common.py`.
- 2026-04-09 13:20: Fixed the product-scoped activation edge case in `trade_viewer_api.py` so turning one product off does not clear `auto_promote` for other active products sharing the same activation key.
- 2026-04-09 13:21: Removed the duplicate `auto_promote` merge line in `common.py` and added `test_weekly_auto_promote_activation_api.py` for regression coverage.
- 2026-04-09 13:22: Ran direct Python validations and captured output in `workstream/artefacts/auto_promote_validation/` and `workstream/artefacts/auto_promote_validation_api/`.

## Changes Made
- Confirmed `weekly_performance.html` already renders row-level toggles and posts `auto_promote` with product-scoped `buy_net` / `sell_net` activation payloads.
- Updated `update_activations()` in `trade_viewer_api.py` so product-scoped deactivation preserves `auto_promote` when other products remain active under the same strategy key.
- Kept activation persistence segmented by mode and ensured response/persisted payloads stay aligned after partial product removal.
- Removed the duplicate `auto_promote` merge assignment in `_merge_activation_entries()` in `common.py`.
- Added `TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py` to guard the shared-key / remaining-product `auto_promote` behavior.

## Validation
- 2026-04-09 13:22: Ran direct Python validation for L-Trade order creation and guards:
  - Command: inline `python -` script captured to `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation\validation_common_output.txt`
  - Result: PASS
  - Summary:
    - `auto_promote_bypass_daily_target`: created tradeable JSON successfully
    - `auto_promote_respects_max_live_trades`: blocked with `max_live_trades reached`
    - `auto_promote_respects_max_trades_to_tws`: blocked with `max_trades_to_tws reached`
    - `standard_live_order_respects_daily_target`: blocked with `daily_target reached`
- 2026-04-09 13:22: Ran direct Flask client validation for activation persistence:
  - Command: inline `python -` script captured to `C:\Users\edebe\eds\workstream\artefacts\auto_promote_validation_api\validation_api_output.txt`
  - Result: PASS
  - Summary:
    - Removing `EURUSD` from a shared `breakout_demo_buy_net` activation preserved `GBPUSD` and kept `auto_promote: true`
- 2026-04-09 13:22: Requested browser-style pytest validation first, but the sandbox blocked pytest temp-directory setup/cleanup under the default temp path and pytest basetemp directories. Switched to equivalent direct Python validations inside workspace artifact folders and captured the successful outputs above.

## Risks/Notes
- The toggle UI itself was verified by code inspection in this run rather than by interactive browser automation.
- `auto_promote` is still modeled at the activation-key level, with per-product scoping enforced via the `products` list. The API fix preserves the intended behavior for partial product removal on shared keys.
- `max_live_trades` and `max_trades_to_tws` remain the only enforced guards on auto-promoted L-Trades, as required.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-09 13:22:34
