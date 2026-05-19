Source: User request on 2026-05-06 to change pip-delta measurement in `C:\Users\edebe\eds\epics\ep_018_multi_product_trade_manager\trade_manager_pair_entry_maintain_buy_sell.py` to use mid-price delta, specifically `current_mid_price - open_mid_price`, to reduce bid/ask noise.
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
  depends_on: []
  feeds_into: []
Task Summary: Modify the script so pip-delta measurement is based on execution mid price rather than current executable exit side, by storing an `execution_mid_price` basis for each trade leg and using current mid minus execution mid as the market-move basis. This change should reduce noise in the displayed `pips=` field and in any reduction logic that depends on adverse pip distance.
Context: The current `open_pips()` function measures BUY legs from current `bid` versus `entry_price` and SELL legs from `entry_price` versus current `ask`, which makes pip delta noisy because spread movement changes the result. The corrected requirement is to use current mid versus `execution_mid_price` instead. Relevant areas are `Trade`, `create_trade()`, `add_size()`, `open_pips()`, `manage_trade()`, `print_status()`, and decision-log output.
Destination Folder: None
Dependency: None

## Plan
- [x] 1. Identify the current pip-delta basis and the code paths that need an execution-mid reference.
  - [x] Test: Manual review confirms where pip delta is calculated, where entry basis is set, and where position adds must update the basis.
  - Evidence: Confirmed the relevant paths are `Trade`, `create_trade()`, `add_size()`, `open_pips()`, and `manage_trade()`.
- [x] 2. Implement execution-mid tracking and switch pip-delta calculations to current-mid versus execution-mid.
  - [x] Test: Code review confirms each trade stores an `execution_mid_price` basis, adds update that basis correctly, and pip delta now uses mid price instead of bid/ask exit-price noise.
  - Evidence: Added `Trade.execution_mid_price`, `current_mid_price()`, mid-based initialization in `create_trade()`, weighted updates in `add_size()`, and mid-based `open_pips()` / signal-aware adverse reduction logic in `manage_trade()`.
- [x] 3. Validate BUY and SELL pip deltas using controlled quotes to confirm the new measurement is stable and directionally correct.
  - [x] Test: Targeted validation proves BUY and SELL legs compute pip delta from mid-price movement and that the adverse reduction logic now keys off the same mid-based pip delta.
  - Evidence: Function-level validation confirmed:
    - BUY leg with `execution_mid_price=1.1001` and current mid `1.0998` reports `-3.0` pips and triggers one `10k` reduction
    - SELL leg with `execution_mid_price=1.1001` and current mid `1.1004` reports `-3.0` pips and triggers one `10k` reduction

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: C:\Users\edebe\eds\epics\ep_018_multi_product_trade_manager\trade_manager_pair_entry_maintain_buy_sell.py
  - Objective-Proved: Confirms the script now stores `execution_mid_price`, computes pip delta from current mid versus execution mid, and uses the same basis for adverse-reduction checks.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -c "import importlib.util; ..."` validation executed on 2026-05-06 against `open_pips()` and `manage_trade()`
  - Objective-Proved: Confirms BUY and SELL legs both measure pip delta from current mid versus execution mid and both trigger adverse reduction at the 3-pip boundary.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: C:\Users\edebe\eds\workstream\300_complete\20260506_144144_ep_018_998_use_mid_price_delta_for_pip_measurement.md
  - Objective-Proved: Confirms the lifecycle task for the mid-price pip-delta change was created and activated.
  - Status: captured

## Implementation Log
- 2026-05-06 14:41:44 BST: User requested changing pip delta to use mid-price delta rather than bid/ask exit-price noise.
- 2026-05-06 14:41:44 BST: Created this lifecycle task directly in `workstream\200_inprogress` for the active implementation.
- 2026-05-06 14:41:44 BST: User corrected the basis from `open_mid_price` to `execution_mid_price`.
- 2026-05-06 14:41:44 BST: Updated the script to store `execution_mid_price`, compute pip delta from current mid versus execution mid, and keep adverse reduction logic signal-aware.
- 2026-05-06 14:41:44 BST: Added a floating-point boundary guard so a nominal 3.0-pip move triggers reliably.
- 2026-05-06 14:41:44 BST: Corrected the SELL adverse trigger so directional `open_pips()` is not double-adjusted.
- 2026-05-06 14:41:44 BST: Ran function-level validation for BUY and SELL mid-price pip measurement and reduction triggering.

## Changes Made
- Created a dedicated lifecycle task for the mid-price pip-delta change.
- Updated the target script so each trade now stores `execution_mid_price`.
- Changed pip-delta measurement to use current mid versus execution mid instead of bid/ask exit-price noise.
- Added `current_mid_price()` and `pip_step_count()` helpers.
- Updated `add_size()` so the execution-mid basis is maintained as a weighted average when size is added.

## Validation
- Verified the current `open_pips()` implementation uses `bid` for BUY and `ask` for SELL against `entry_price`, which introduces spread noise.
- Verified the new implementation reports directional pip delta from current mid versus `execution_mid_price`.
- Executed controlled validation with these outcomes:
  - BUY: current mid `1.0998` vs execution mid `1.1001` produced `-3.0` pips and one `REDUCE_SIZE` action to `20000`
  - SELL: current mid `1.1004` vs execution mid `1.1001` produced `-3.0` pips and one `REDUCE_SIZE` action to `20000`
- Verified the 3-pip boundary now triggers reliably despite floating-point representation noise.

## Risks/Notes
- PnL should remain based on actual executable prices; only pip-delta measurement should move to mid-price basis unless explicitly requested otherwise.
- SELL legs still need directional sign handling so adverse movement remains negative and favorable movement remains positive from the trade’s perspective.
- Because the reduction rule already depends on `open_pips()`, this change will alter both displayed pip values and reduction-trigger timing.

## Completion Status
- State: Complete
- Timestamp: 2026-05-06 14:41:44 BST
