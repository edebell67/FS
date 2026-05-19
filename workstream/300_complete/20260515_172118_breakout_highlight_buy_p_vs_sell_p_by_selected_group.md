Source: User request in Codex chat on 2026-05-15
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
  workflow_stage: todo
  depends_on: []
  feeds_into: []
Task Summary: Modify `strategy_snapshots_15m.html` so the page compares `Buy P` and `Sell P` for the currently selected group and highlights in yellow whichever column has the larger average.
Context: `TradeApps/breakout/fs/strategy_snapshots_15m.html`, the `Buy P` / `Sell P` table columns, the selected-group filter behavior, and the snapshot row data sourced from `_strategy_snapshots_15m.json`
Destination Folder: `TradeApps/breakout/fs/`
Dependency: None
Plan:
- [ ] 1. Inspect how `Buy P`, `Sell P`, and the selected group filter are currently rendered.
  - [ ] Test: Review the table column definitions, render flow, and selected-group logic in `strategy_snapshots_15m.html`; pass if the exact render path for `buy_profit` and `sell_profit` is identified.
  - Evidence: Document the active column definitions and where filtered rows for the selected group are prepared.
- [ ] 2. Define the comparison rule for the selected group.
  - [ ] Test: Confirm the average should be computed from the currently filtered rows for the selected group and current view, rather than from all groups or all snapshots.
  - Evidence: The task notes specify the aggregation scope and tie-break behavior if the averages are equal.
- [ ] 3. Implement yellow highlighting for the winning column.
  - [ ] Test: Inspect the updated table render logic; pass if `Buy P` or `Sell P` receives a distinct yellow highlight when its average is larger for the selected group.
  - Evidence: Diff shows the comparison calculation and the conditional header/cell highlight treatment.
- [ ] 4. Validate that the highlight updates correctly when the selected group changes.
  - [ ] Test: Verify the highlight recalculates when the group filter or snapshot/view changes.
  - Evidence: Focused verification confirms the highlight tracks the selected group dynamically and does not bleed into unrelated columns.
Evidence:
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false
- Evidence-Type: pending
  - Artifact: `TradeApps/breakout/fs/strategy_snapshots_15m.html`
  - Objective-Proved: The larger-average `Buy P` or `Sell P` column is highlighted in yellow for the selected group.
  - Status: pending
Implementation Log:
- 2026-05-15 17:21:18 BST: Created backlog task to compare `Buy P` and `Sell P` and highlight the larger-average column in yellow for the selected group.
Changes Made:
- Created this lifecycle task file only. No application code changed.
Validation:
- Not run yet. This task is a todo entry awaiting implementation.
Risks/Notes:
- The task should define whether “average” means average across the currently visible filtered rows in the table or some broader per-group aggregate; default to the selected group’s currently filtered table rows unless clarified otherwise.
- Tie handling should be explicit so equal averages do not create ambiguous highlight behavior.
Completion Status: Todo.
