Source: User request in Codex chat on 2026-05-07
Task Type: standard
Task Attributes:
  recurring_task: false
  recurrence_type: scheduled
  recurrence_rule: None
  looping_task: false
  loop_until: manual_stop
  loop_interval: None
  splittable_task: false
  split_output_type: files
  split_outputs: []
  split_routing:
    process: ""
    mode: sequential
    target_board: ""
    target_stage: ""
  split_spawn_task: false
  spawn_template: ""
  split_failure_mode: independent
  workflow_task: false
  workflow_name: ""
  workflow_stage: in_progress
  depends_on: []
  feeds_into: []
Task Summary: Update `summary_net_delta_snapshots_15m.html` so the top-3 total appearance delta value panel is reactive to the currently selected snapshot time, meaning each total only sums appearances up to and including the selected snapshot rather than the whole available day.
Context: `TradeApps/breakout/fs/summary_net_delta_snapshots_15m.html`, `TradeApps/breakout/fs/json/*/_summary_net_delta_snapshots_15m.json`
Destination Folder: TradeApps/breakout/fs/
Dependency: None
Plan:
- [x] 1. Inspect the current top-3 aggregation logic and define the selected-snapshot cutoff rule precisely.
  - [x] Test: Review the current HTML aggregation function and a real delta snapshot artifact; pass if it is clear how to limit the aggregation to snapshots `<= selectedIndex`.
  - Evidence: Reviewed `TradeApps/breakout/fs/summary_net_delta_snapshots_15m.html` and the live forex delta snapshot artifact; confirmed the existing aggregate scanned the full `payload.snapshots` list and could be constrained safely to `payload.snapshots.slice(0, selectedIndex + 1)`.
- [x] 2. Implement reactive top-3 aggregation so totals are recalculated only up to the selected snapshot for the active 30m/60m window.
  - [x] Test: Inspect the page logic; pass if changing snapshot chips or prev/next changes the top-3 totals accordingly.
  - Evidence: Updated `buildAppearanceLeaders()` to aggregate only through the currently selected snapshot and added cutoff-time display in the aggregate cards so the user can see which snapshot boundary the totals reflect.
- [x] 3. Validate the reactive totals against a real artifact using at least two different selected snapshots.
  - [x] Test: Run a focused verification against `_summary_net_delta_snapshots_15m.json`; pass if the same strategy/product can show different cumulative totals at different selected snapshots as expected.
  - Evidence: Verified `live/forex/2026-05-07` at cutoff index `10` (`02:30`) and cutoff index `43` (`10:45`), with materially different top-3 totals for both `30m` and `60m` windows.
Evidence:
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `git -C C:\Users\edebe\eds\TradeApps diff -- breakout/fs/summary_net_delta_snapshots_15m.html`
  - Objective-Proved: The top-3 aggregation now respects the selected snapshot cutoff.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `node --check <extracted inline script>` and Python verification against `TradeApps/breakout/fs/json/live/forex/2026-05-07/_summary_net_delta_snapshots_15m.json`
  - Objective-Proved: The reactive totals were validated against real snapshot data at multiple cutoff times.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Pending user review in `TradeApps/breakout/fs/summary_net_delta_snapshots_15m.html`
  - Objective-Proved: The user can confirm that selecting an earlier snapshot changes the top-3 totals to reflect only history up to that point.
  - Status: planned
Implementation Log:
- 2026-05-07 13:05:53 BST: Created lifecycle task from the user request.
- 2026-05-07 13:06:20 BST: Updated the top-3 aggregation function so it only scans snapshots from the start through the currently selected snapshot index.
- 2026-05-07 13:06:45 BST: Added cutoff-time display to the aggregate cards to make the selected-snapshot boundary visible in the UI.
- 2026-05-07 13:07:18 BST: Validated the reactive totals at two different snapshot cutoffs against the live forex artifact.
Changes Made:
- Updated `TradeApps/breakout/fs/summary_net_delta_snapshots_15m.html`.
- Changed the aggregate panel to compute totals only up to and including the selected snapshot.
- Added a cutoff-time display on each aggregate card.
Validation:
- Extracted the inline `<script>` from `TradeApps/breakout/fs/summary_net_delta_snapshots_15m.html` and ran `node --check`.
  - Result: Passed with exit code `0`.
- Ran Python verification against `TradeApps/breakout/fs/json/live/forex/2026-05-07/_summary_net_delta_snapshots_15m.json`.
  - Result at cutoff index `10` / `02:30`:
    - `top10_30m`: `breakout_R_Rev_4_tp20.0_sl20.0 / GBPAUD_C` total `555.0`; `breakout_R_Rev_4_tp20.0_sl30.0 / GBPAUD_C` total `555.0`; `breakout_R_Rev_4_tp20.0_sl5.0 / GBPAUD_C` total `555.0`
    - `top10_60m`: `breakout_R_Rev_4_tp20.0_sl20.0 / GBPAUD_C` total `940.0`; `breakout_R_Rev_4_tp20.0_sl30.0 / GBPAUD_C` total `940.0`; `breakout_R_Rev_4_tp20.0_sl5.0 / GBPAUD_C` total `940.0`
  - Result at cutoff index `43` / `10:45`:
    - `top10_30m`: `breakout_R_Rev_4_tp20.0_sl5.0 / GBPAUD_C` total `1202.5`; `breakout_R_Rev_4_tp20.0_sl3.0 / GBPEUR_C` total `1195.0`; `breakout_R_Rev_4_tp20.0_sl30.0 / GBPAUD_C` total `1010.0`
    - `top10_60m`: `breakout_R_Rev_4_tp20.0_sl30.0 / GBPAUD_C` total `1757.5`; `breakout_R_Rev_4_tp20.0_sl5.0 / GBPAUD_C` total `1675.0`; `breakout_R_Rev_4_tp20.0_sl5.0 / NZDAUD_C` total `1625.0`
- User verification requested: open `TradeApps/breakout/fs/summary_net_delta_snapshots_15m.html`, select an early snapshot and then a late snapshot, and confirm that the top-3 panel changes to reflect only appearances up to the selected snapshot.
Risks/Notes:
- Assumption: “up to until the selected snapshot” means include all top-10 appearances from the first snapshot through the currently selected snapshot, inclusive.
- The reactive cutoff should apply separately for the selected `30m` or `60m` window using the existing active window selector.
Completion Status: Awaiting user verification as of 2026-05-07 13:07:18 BST.


# User Feedback
User Verified: PASS
