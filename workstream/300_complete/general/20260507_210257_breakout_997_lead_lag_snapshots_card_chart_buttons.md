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
Task Summary: Add chart buttons to the summary cards in `lead_lag_snapshots.html` so a visible linked strategy pair can be sent to `multi_chart` using the existing import handoff pattern.
Context: `TradeApps/breakout/fs/lead_lag_snapshots.html`, visible strongest-link counterpart data on the rank cards, and existing `multi_chart` import flow used elsewhere in breakout pages
Destination Folder: TradeApps/breakout/fs/
Dependency: Existing lead/lag snapshot screen
Plan:
- [x] 1. Add a chart action to each rank card.
  - [x] Test: Review the card UI; pass if a chart button is available where a concrete pair can be sent to `multi_chart`.
  - Evidence: Added `Chart Pair` actions to rank cards in `strategy + product` mode, plus an explicit note in plain strategy mode.
- [x] 2. Reuse the existing `multi_chart` import payload handoff for the visible linked pair.
  - [x] Test: Inspect the payload logic; pass if the selected card sends the intended pair without changing the established import contract.
  - Evidence: Added `getImportPayloadItems()`, `sendToMultiChart()`, and `openCardChartPair()` using the same localStorage + BroadcastChannel import flow used elsewhere in breakout pages.
- [x] 3. Validate the updated page script.
  - [x] Test: Run a syntax validation on the inline script; pass if the page remains valid.
  - Evidence: `node --check` passed on the extracted inline script.
Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/lead_lag_snapshots.html`
  - Objective-Proved: Summary cards include chart actions.
  - Status: complete
- Evidence-Type: integration
  - Artifact: card chart button import payload handoff in `lead_lag_snapshots.html`
  - Objective-Proved: The card action uses the existing multi-chart handoff.
  - Status: complete
- Evidence-Type: test_output
  - Artifact: `node --check` validation of extracted inline script
  - Objective-Proved: The revised page script remains valid.
  - Status: complete
Implementation Log:
- 2026-05-07 21:02:57 BST: Created task for lead/lag snapshot card chart buttons.
- 2026-05-07 21:07:00 BST: Added chart button styles and the shared multi-chart handoff helpers to `lead_lag_snapshots.html`.
- 2026-05-07 21:09:00 BST: Added `Chart Pair` actions to rank cards for `strategy + product` mode and explicit unavailable-state messaging for plain strategy mode.
- 2026-05-07 21:10:00 BST: Validated the revised page script with `node --check`.
Changes Made:
- Updated `TradeApps/breakout/fs/lead_lag_snapshots.html` to add per-card chart buttons and the underlying multi-chart import handoff.
Validation:
- Pass: extracted the inline `<script>` block from `lead_lag_snapshots.html` and ran `node --check` with no syntax errors.
- Pending user verification: in `strategy + product` mode, click `Chart Pair` on a rank card and confirm the expected linked pair opens in `multi_chart`.
Risks/Notes:
- `multi_chart` requires concrete `strategy + product` items, so plain strategy-grain cards cannot send an unambiguous pair without further design decisions.
Completion Status: Awaiting user verification at 2026-05-07 21:10:00 BST.


# User Feedback
User Verified: PASS
