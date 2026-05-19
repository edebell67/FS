Source: User request in Codex chat on 2026-05-07
Task Type: follow-up
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
  workflow_stage: backlog
  depends_on:
  - 20260507_160840_breakout_999_summary_net_lead_lag_correlation_analysis.md
  - 20260507_163621_breakout_998_summary_net_product_level_lead_lag_analysis.md
  - 20260507_170629_breakout_997_lead_lag_snapshot_html_screen.md
  feeds_into: []
Task Summary: Add lag-confidence and lag-stability scoring to the lead/lag analyzer and HTML screen so reported lag minutes are supported by repeated evidence rather than a single best-fit correlation peak.
Context: `summary_net_lead_lag_analysis.py`, `lead_lag_snapshots.html`, and user concern that a reported lag like `90m` may be coincidental
Destination Folder: TradeApps/breakout/fs/
Dependency: Corrected positive-lag lead/lag methodology already implemented
Plan:
- [ ] 1. Define lag confidence and stability metrics.
  - [ ] Test: Review the metric definitions; pass if they explicitly address best-lag separation, repeated confirming moves, and sensitivity to outliers.
  - Evidence: planned
- [ ] 2. Implement confidence/stability scoring in the analyzer and expose it in the screen.
  - [ ] Test: Run the analyzer and inspect the screen; pass if each reported pair can show best lag, nearby lag scores, and a confidence classification.
  - Evidence: planned
- [ ] 3. Validate the revised output on at least one suspicious-looking pair.
  - [ ] Test: Re-check a pair such as the current `90m` example; pass if the confidence layer helps distinguish stable lag from coincidence.
  - Evidence: planned
Evidence:
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false
- Evidence-Type: methodology
  - Artifact: planned
  - Objective-Proved: Lag-confidence logic is explicit and reviewable.
  - Status: planned
- Evidence-Type: diff
  - Artifact: planned
  - Objective-Proved: Analyzer and screen expose the new confidence/stability outputs.
  - Status: planned
- Evidence-Type: manual_verification
  - Artifact: planned
  - Objective-Proved: The user can inspect whether a reported lag appears robust or coincidental.
  - Status: planned
Implementation Log:
- 2026-05-07 17:30:24 BST: Created follow-up task for lag confidence and lag stability.
Changes Made:
- Created this backlog task only. No code changes yet.
Validation:
- Task creation only. No validation run.
Risks/Notes:
- A best-fit lag alone is not sufficient evidence of a true lead/lag relationship.
- The implementation should distinguish between “best lag found” and “high-confidence lag.”
Completion Status: Backlog created at 2026-05-07 17:30:24 BST.
