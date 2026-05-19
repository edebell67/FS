Source: User request on 2026-05-06 to change the size-increase criteria in `C:\Users\edebe\eds\epics\ep_018_multi_product_trade_manager\trade_manager_pair_entry_maintain_buy_sell.py` to 3 pips.
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
  depends_on: []
  feeds_into: []
Task Summary: Modify the trade manager so position size increases are triggered by a 3-pip favorable move instead of the current favorable-tick rule, while preserving the existing constraints that the leg must be profitable and must remain below `max_size`.
Context: Current add-size logic in `manage_trade()` adds when `direction == "FAVOURABLE"`, `t.open_pnl > 0`, and `t.size < cfg["max_size"]`. The script already uses directional mid-based pip delta and 3-pip adverse bands for size reduction. This change should make size increases use a similar favorable pip-band threshold, avoiding noisy add decisions from single-tick movement. Relevant areas include `manage_trade()`, `add_size()`, `open_pips()`, and any per-trade state needed to avoid repeated adds inside the same favorable band.
Destination Folder: None
Dependency: None

## Plan
- [x] 1. Trace the current add-size flow and define how the 3-pip favorable trigger should integrate with the existing mid-based pip logic.
  - [x] Test: Manual review confirms the current add-size path, favorable pip basis, and max-size gating that must be preserved.
  - Evidence: Confirmed the relevant paths are `manage_trade()`, `add_size()`, `open_pips()`, and `cfg["max_size"]`, with favorable pip measurement already using the directional mid-based `open_pips()` calculation.
- [x] 2. Implement a 3-pip favorable-band increase trigger that avoids repeated adds in the same band.
  - [x] Test: Code review confirms adds are no longer based on a single favorable tick, but on newly crossed 3-pip favorable bands while `open_pnl > 0` and `size < max_size`.
  - Evidence: Added `Trade.favourable_add_steps_applied` and changed `manage_trade()` to compute favorable pip bands and add only when a new 3-pip favorable band is crossed.
- [x] 3. Validate BUY and SELL behavior at, below, and above the 3-pip favorable threshold.
  - [x] Test: Targeted validation proves no add below threshold, one add at/above threshold, no duplicate add in the same favorable band, and max-size protection remains in effect.
  - Evidence: Function-level validation confirmed:
    - `buy_2_9`: no add below threshold, size stayed `30000`
    - `buy_3_0`: add triggered at `3.0` favorable pips, size moved `30000 -> 40000`
    - `buy_same_band`: repeated call in same favorable band caused no duplicate add
    - `sell_3_0`: add triggered at `3.0` favorable pips, size moved `30000 -> 40000`
    - `max_block`: no add when already at `max_size=50000`

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: C:\Users\edebe\eds\epics\ep_018_multi_product_trade_manager\trade_manager_pair_entry_maintain_buy_sell.py
  - Objective-Proved: Confirms the target script now uses favorable 3-pip bands rather than a single favorable tick for add-size decisions.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -c "import importlib.util; ..."` function-level validation executed on 2026-05-06 against `manage_trade()`
  - Objective-Proved: Confirms the new favorable-band add behavior for BUY and SELL legs, duplicate-band suppression, and max-size blocking.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: C:\Users\edebe\eds\workstream\300_complete\20260506_145309_ep_018_998_change_size_increase_criteria_to_3_pips.md
  - Objective-Proved: Confirms the lifecycle task for the add-size criteria change was created and activated.
  - Status: captured

## Implementation Log
- 2026-05-06 14:53:09 BST: User requested changing the size-increase criteria to 3 pips.
- 2026-05-06 14:53:09 BST: Created this lifecycle task directly in `workstream\200_inprogress` for the active implementation.
- 2026-05-06 14:53:09 BST: Replaced the favorable-tick add rule with a 3-pip favorable-band rule while preserving the existing `open_pnl > 0` and `max_size` gates.
- 2026-05-06 14:53:09 BST: Ran function-level validation for BUY and SELL add-size behavior at sub-threshold, threshold, repeated-band, and max-size cases.

## Changes Made
- Created a dedicated lifecycle task for the 3-pip size-increase criteria change.
- Updated the target script so add-size decisions now use favorable 3-pip bands instead of single favorable ticks.
- Added per-trade favorable-band state to avoid duplicate adds within the same favorable band.

## Validation
- Verified the current add-size rule is driven by favorable tick direction plus `open_pnl > 0`, not by a pip-distance threshold.
- Verified the updated code now keys add-size on directional favorable pip bands derived from the mid-based `open_pips()` calculation.
- Executed controlled validation with these outcomes:
  - BUY at `2.9` favorable pips returned `HOLD_SIZE`, size remained `30000`
  - BUY at `3.0` favorable pips returned `ADD_SIZE`, size moved to `40000`
  - repeated BUY call in the same band returned `HOLD_SIZE`, size remained `40000`
  - SELL at `3.0` favorable pips returned `ADD_SIZE`, size moved to `40000`
  - max-size case returned `HOLD_SIZE`, size remained `50000`

## Risks/Notes
- The favorable trigger should use the existing directional mid-based pip delta rather than reverting to bid/ask side noise.
- Repeated adds in the same favorable price band should be prevented, just as repeated reductions are prevented in the same adverse band.
- This change alters pyramiding cadence and could materially increase position size persistence in trending conditions.

## Completion Status
- State: Complete
- Timestamp: 2026-05-06 14:53:09 BST
