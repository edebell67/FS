Source: User request in Codex chat on 2026-05-07
Task Type: fix
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
  - 20260507_173608_breakout_997_lead_lag_snapshot_persistence_detection.md
  feeds_into: []
Task Summary: Improve `lead_lag_snapshots.html` so the link between a ranked entity and its counterpart is obvious, including surfacing the strongest linked counterpart directly on the summary card and allowing table filtering by selected entity.
Context: `TradeApps/breakout/fs/lead_lag_snapshots.html`, user confusion about what a leader/lagger aggregate row actually links to
Destination Folder: TradeApps/breakout/fs/
Dependency: Existing lead/lag snapshot screen
Plan:
- [x] 1. Expose the strongest linked counterpart directly in the leader/lagger summary cards.
  - [x] Test: Review the card output; pass if a ranked row clearly shows who its strongest linked counterpart is, with lag and correlation.
  - Evidence: Added `Strongest link` to each summary card with counterpart name, correlation sign/value, and lag minutes.
- [x] 2. Add interaction so selecting a ranked entity filters the relationship tables to that entity.
  - [x] Test: Inspect the filtered view; pass if clicking a rank item makes the relevant links obvious in the tables.
  - Evidence: Added click-to-select cards, active state highlighting, and pair-table filtering by `selectedEntity`.
- [x] 3. Validate the updated page script.
  - [x] Test: Run a syntax validation on the inline script; pass if the page remains valid.
  - Evidence: `node --check` passed on the extracted inline script.
Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/lead_lag_snapshots.html`
  - Objective-Proved: The screen makes counterparts obvious from the UI.
  - Status: complete
- Evidence-Type: usability
  - Artifact: summary-card strongest-link line and click-to-filter behavior
  - Objective-Proved: A selected entity can be traced to its concrete links.
  - Status: complete
- Evidence-Type: test_output
  - Artifact: `node --check` validation of extracted inline script
  - Objective-Proved: The revised page script remains valid.
  - Status: complete
Implementation Log:
- 2026-05-07 20:55:34 BST: Created counterpart-visibility task for `lead_lag_snapshots.html`.
- 2026-05-07 21:00:00 BST: Added `top_link` extraction to the ranking aggregates so each ranked entity now carries its strongest explicit counterpart.
- 2026-05-07 21:02:00 BST: Added selectable summary cards and filtered table rendering based on the selected entity.
- 2026-05-07 21:03:00 BST: Validated the revised page script with `node --check`.
Changes Made:
- Updated `TradeApps/breakout/fs/lead_lag_snapshots.html` to show strongest counterpart detail on rank cards and to filter relationship tables by selected entity.
Validation:
- Pass: extracted the inline `<script>` block from `lead_lag_snapshots.html` and ran `node --check` with no syntax errors.
- Pending user verification: click a summary card and confirm the tables immediately narrow to links involving that entity.
Risks/Notes:
- The UI should expose counterpart detail without overwhelming the summary cards.
Completion Status: Awaiting user verification at 2026-05-07 21:03:00 BST.


# User Feedback
User Verified: PASS
