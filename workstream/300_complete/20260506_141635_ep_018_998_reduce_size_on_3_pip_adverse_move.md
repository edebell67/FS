Source: User request on 2026-05-06 to modify `C:\Users\edebe\eds\epics\ep_018_multi_product_trade_manager\trade_manager_pair_entry_maintain_buy_sell.py` so size is reduced when price moves 3 pips against a trade, reducing by `10k` per qualifying event, while maintaining a minimum open size of `1k` unless the stop-loss condition is broken.
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
  depends_on: []
  feeds_into: []
Task Summary: Change the adverse-move position-management rule in `trade_manager_pair_entry_maintain_buy_sell.py` so a trade only reduces size after a 3-pip move against the open leg, trims by `10,000` units per qualifying reduction, preserves a minimum residual size of `1,000`, and only allows the final `1,000` remainder to be removed when the stop-loss threshold is actually breached.
Context: Current code reduces size whenever the latest tick direction is `AGAINST` and `t.size > cfg["min_size"]`, with reduction quantity controlled by `cfg["size_step"]`. The new requirement replaces that tick-by-tick adverse reduction trigger with a distance-based adverse-move threshold of 3 pips and explicitly fixes the reduction slice to `10k` while preserving the existing stop-loss-driven final close behavior at min size. Relevant functions include `manage_trade()`, `reduce_size()`, `open_pips()`, `pip_size()`, and stop-loss handling in `close_trade()` / `active_pnl()` logic.
Destination Folder: None
Dependency: None

## Plan
- [x] 1. Trace the current reduction and stop-loss flow and define the exact code changes needed for the new adverse-move rule.
  - [x] Test: Manual review confirms the current reduction path, stop-loss path, pip-distance helpers, and size controls that must be updated.
  - Evidence: Confirmed the relevant paths are `manage_trade()`, `reduce_size()`, `open_pips()`, `pip_size()`, `active_pnl()`, and the `cfg["min_size"]` / `cfg["size_step"]` controls in the target script.
- [x] 2. Implement the new reduction rule so size only reduces after a 3-pip adverse move, by `10k` per reduction, while keeping a floor of `1k` until stop loss is breached.
  - [x] Test: Code review confirms the reduction trigger is based on adverse price distance rather than any single against-tick, the trim quantity is `10,000`, and the final `1,000` remains open unless stop loss closes it.
  - Evidence: Added `adverse_reduce_pips(cfg)`, `adverse_reduce_size(cfg)`, `Trade.adverse_reduce_steps_applied`, changed `reduce_size(..., "REDUCE")` to use a fixed `10,000` chunk, and changed `manage_trade()` to reduce only when a new 3-pip adverse band is crossed.
- [x] 3. Validate the new behavior with a focused runtime or function-level check covering adverse moves, reduction amount, min-size hold, and stop-loss close.
  - [x] Test: Targeted validation proves a position does not reduce before 3 adverse pips, reduces by `10k` once the threshold is met, does not go below `1k` via reduction, and only fully closes when the stop-loss condition is met at min size.
  - Evidence: Python validation output confirmed:
    - `case1`: no reduction at `2.9` adverse pips, size stayed `30000`
    - `case2`: reduction at `3.1` adverse pips, size moved `30000 -> 20000`
    - `case3`: no duplicate reduction in the same adverse band, size stayed `20000`
    - `case4`: reduction respects the `1000` floor, size moved `11000 -> 1000`
    - `case5`: stop loss closes the remaining `1000`, leaving `0` active trades

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: C:\Users\edebe\eds\epics\ep_018_multi_product_trade_manager\trade_manager_pair_entry_maintain_buy_sell.py
  - Objective-Proved: Confirms the target script now uses a 3-pip adverse threshold, a fixed `10,000` reduction chunk for adverse trims, and a protected `1,000` minimum size before stop-loss close.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -c "import importlib.util; ..."` function-level validation executed on 2026-05-06 against `manage_trade()`
  - Objective-Proved: Confirms the new rule sequence: no trim before 3 adverse pips, `10k` trim after threshold, no repeated trim inside the same band, `1k` floor, and stop-loss close at min size.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: C:\Users\edebe\eds\workstream\300_complete\20260506_141635_ep_018_998_reduce_size_on_3_pip_adverse_move.md
  - Objective-Proved: Confirms the lifecycle task for the requested behavior change was created.
  - Status: captured

## Implementation Log
- 2026-05-06 14:16:35 BST: User requested a new task to modify the trade manager so it reduces size after a 3-pip adverse move, by `-10k`, while keeping a `1k` minimum size except when stop loss is broken.
- 2026-05-06 14:16:35 BST: Created this lifecycle task in `workstream\100_todo` with the requested reduction threshold, reduction amount, and min-size rule captured explicitly.
- 2026-05-06 14:16:35 BST: Moved the task into `workstream\200_inprogress` when implementation began.
- 2026-05-06 14:16:35 BST: Replaced the prior tick-against reduction rule with a 3-pip adverse-band rule and fixed the reduction chunk for adverse trims to `10,000` units while preserving the `1,000` minimum-size stop-loss close behavior.
- 2026-05-06 14:16:35 BST: Ran a focused function-level validation against `manage_trade()` covering pre-threshold hold, threshold reduction, duplicate-band suppression, min-size floor protection, and stop-loss closure.

## Changes Made
- Created a dedicated lifecycle task for the 3-pip adverse-move size-reduction rule change.
- Captured the intended behavior precisely enough for later implementation and validation.
- Updated `trade_manager_pair_entry_maintain_buy_sell.py` so adverse reductions are now driven by pip distance rather than any single adverse tick.
- Added explicit helper functions for the adverse reduction threshold and chunk size.
- Added per-trade state to prevent repeated reductions inside the same 3-pip adverse band.

## Validation
- Verified the task filename uses the timestamped lowercase naming convention and includes `_998_` for a behavioral fix/change task.
- Verified the task description explicitly records:
  - 3-pip adverse-move trigger
  - `10k` reduction size
  - `1k` minimum retained size
  - final close only when stop loss is breached
- Verified the code now applies adverse reduction only after `open_pips <= -3.0`, using 3-pip bands and a fixed `10,000` reduction chunk for the `REDUCE` path.
- Executed function-level validation with these results:
  - `case1`: `2.9` adverse pips returned `HOLD_SIZE`, size remained `30000`
  - `case2`: `3.1` adverse pips returned `REDUCE_SIZE`, size moved to `20000`
  - `case3`: repeated call in the same adverse band returned `HOLD_SIZE`, size remained `20000`
  - `case4`: `11000` size reduced to the protected floor of `1000`, not below it
  - `case5`: at `1000` size with stop-loss breach, `STOP_LOSS` closed the remaining trade

## Risks/Notes
- The requirement needs careful interpretation for BUY versus SELL legs so the adverse 3-pip move is measured from the correct side of the market.
- The existing code currently uses tick-direction logic rather than an absolute adverse-move threshold, so implementation will likely require tracking the correct reference price for each reduction decision.
- The implementation uses configurable defaults `adverse_reduce_pips=3` and `adverse_reduce_size=10000` so the requested behavior is the default while remaining explicit in code.
- The implementation applies one `10k` reduction for each newly crossed 3-pip adverse band and does not re-fire repeatedly in the same band.
- The current implementation measures adverse movement from the trade's current effective entry basis via `open_pips()`, which is recalculated after adds.

## Completion Status
- State: Complete
- Timestamp: 2026-05-06 14:16:35 BST
