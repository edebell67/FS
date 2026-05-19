Source: User request in Codex chat on 2026-05-07
Task Type: feature
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
  workflow_stage: inprogress
  depends_on:
  - 20260507_170629_breakout_997_lead_lag_snapshot_html_screen.md
  feeds_into: []
Task Summary: Add a selected-snapshot net filter to `lead_lag_snapshots.html` so entities with negative current net are excluded by default before candidate-universe and lead/lag calculations run.
Context: `TradeApps/breakout/fs/lead_lag_snapshots.html`, selected snapshot cutoff, candidate-universe selection, and lead/lag relationship detection
Destination Folder: TradeApps/breakout/fs/
Dependency: Existing lead/lag snapshot screen
Plan:
- [x] 1. Add a control to toggle selected-snapshot net filtering.
  - [x] Test: Review the controls; pass if the page exposes a `Snapshot Net` filter with a default that excludes negative net.
  - Evidence: Added a `Snapshot Net` select to `lead_lag_snapshots.html` with `exclude negative net` as the default option.
- [x] 2. Apply the filter before candidate-universe selection and relationship analysis.
  - [x] Test: Inspect the analysis path; pass if negative-current-net entities are omitted from the candidate set when the default filter is active.
  - Evidence: Added `currentNet` tracking in `entityActivity()` and filtered `selectAnalysisUniverse()` on the selected snapshot’s current net before pair generation.
- [x] 3. Validate the updated page script.
  - [x] Test: Run a syntax validation on the inline script; pass if the page remains valid after the filter is added.
  - Evidence: `node --check` passed on the extracted inline script.
Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
 - Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/lead_lag_snapshots.html`
  - Objective-Proved: The page exposes a selected-snapshot net filter and defaults to excluding negative net.
  - Status: complete
 - Evidence-Type: logic_path
  - Artifact: `entityActivity()` and `selectAnalysisUniverse()` in `lead_lag_snapshots.html`
  - Objective-Proved: Negative-current-net entities are excluded before candidate-universe selection and lead/lag pair analysis.
  - Status: complete
 - Evidence-Type: test_output
  - Artifact: `node --check` validation of the extracted inline script
  - Objective-Proved: The revised page script remains valid after the filter addition.
  - Status: complete
Implementation Log:
- 2026-05-07 22:29:35 BST: Created task for the lead/lag snapshot negative-net filter request.
- 2026-05-07 22:36:00 BST: Added the `Snapshot Net` control to `lead_lag_snapshots.html` with `exclude negative net` as the default.
- 2026-05-07 22:38:00 BST: Wired selected-snapshot `currentNet` into `entityActivity()` and filtered `selectAnalysisUniverse()` so negative-net entities do not enter analysis when the default filter is active.
- 2026-05-07 22:40:00 BST: Validated the updated inline script with `node --check`.
Changes Made:
- Updated `TradeApps/breakout/fs/lead_lag_snapshots.html` to add a selected-snapshot net filter, feed that state into the metadata display, and recompute immediately when the filter changes.
Validation:
- Pass: extracted the inline `<script>` block from `lead_lag_snapshots.html` and ran `node --check` with no syntax errors.
- Pending user verification: confirm that with `Snapshot Net = exclude negative net`, negative-current-net entities disappear from the candidate universe and resulting lead/lag relationships, and that switching to `include all` restores them.
Risks/Notes:
- The filter must use the selected snapshot’s current net, not the end-of-day net, or the screen will hide the wrong entities.
Completion Status: Awaiting user verification at 2026-05-07 22:40:00 BST.


# User Feedback
User Verified: PASS
