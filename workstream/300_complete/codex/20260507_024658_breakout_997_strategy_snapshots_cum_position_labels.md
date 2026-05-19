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
Task Summary: Append each strategy's cumulative rank-position movement to the displayed strategy name in `strategy_snapshots_15m.html`, using the loaded snapshot sequence up to the currently selected snapshot.
Context: `TradeApps/breakout/fs/strategy_snapshots_15m.html`, `TradeApps/breakout/fs/json/*/_strategy_snapshots_15m.json`
Destination Folder: TradeApps/breakout/fs/
Dependency: None
Plan:
- [x] 1. Define and confirm the cumulative-position calculation against the existing snapshot ranking logic.
  - [x] Test: Review the current rank-delta helpers and a real snapshot JSON file; pass if cumulative movement can be derived deterministically from snapshot-to-snapshot rank changes.
  - Evidence: Reviewed the existing `profit_net` ranking helpers in `TradeApps/breakout/fs/strategy_snapshots_15m.html` and the live forex snapshot JSON for `2026-05-07`; confirmed cumulative movement can be derived as the sum of `previous_rank - current_rank` across snapshots, where rank improvement is positive.
- [x] 2. Implement strategy-label formatting so the strategy column renders `strategy_name (cum_position)` while preserving sorting, filters, and current rank highlighting.
  - [x] Test: Inspect the HTML diff after implementation; pass if the strategy label is decorated from computed data without changing underlying sort keys.
  - Evidence: `git -C C:\Users\edebe\eds\TradeApps diff -- breakout/fs/strategy_snapshots_15m.html` shows `formatSignedPosition`, cumulative-rank movement computation, and `_displayStrategy` label formatting applied only at render time.
- [x] 3. Validate the computed labels against a real JSON artifact and record expected sample outputs.
  - [x] Test: Run a local verification script over `_strategy_snapshots_15m.json`; pass if at least one strategy returns a signed cumulative value and the inline script remains syntactically valid.
  - Evidence: `node --check` passed on the extracted inline script, and a Python validation against `TradeApps/breakout/fs/json/live/forex/2026-05-07/_strategy_snapshots_15m.json` returned sample labels including `breakout_R_Rev_4_tp20.0_sl30.0 (+29)` and `breakout_R_3_tp5.0_sl20.0 (-46)`.
Evidence:
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `git -C C:\Users\edebe\eds\TradeApps diff -- breakout/fs/strategy_snapshots_15m.html`
  - Objective-Proved: The HTML page now computes and displays cumulative rank-position movement in the strategy label.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `node --check <extracted inline script>` and Python validation output against `TradeApps/breakout/fs/json/live/forex/2026-05-07/_strategy_snapshots_15m.json`
  - Objective-Proved: The cumulative values match real snapshot data and the file remains syntactically valid.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Pending user review in `TradeApps/breakout/fs/strategy_snapshots_15m.html`
  - Objective-Proved: The user can verify the displayed strategy labels include the expected signed cumulative position values.
  - Status: planned
Implementation Log:
- 2026-05-07 02:46:58 BST: Created lifecycle task from the user request.
- 2026-05-07 02:48:00 BST: Reviewed the existing row-decoration logic and confirmed the strategy label could be decorated at render time without changing source row data or sorting keys.
- 2026-05-07 02:49:00 BST: Implemented cumulative movement tracking as the sum of snapshot-to-snapshot rank changes using the existing `profit_net` ranking basis.
- 2026-05-07 02:49:30 BST: Updated the strategy cell rendering to append signed cumulative values like `(+29)` or `(-46)` and extended row tooltips with the same context.
- 2026-05-07 02:50:00 BST: Validated the inline script syntax and checked sample cumulative labels against the live forex snapshot series for 2026-05-07.
- 2026-05-07 02:50:00 BST: Restored the lifecycle file to `200_inprogress` after the environment left the primary copy in backlog.
Changes Made:
- Added `formatSignedPosition` to render cumulative values with explicit signs.
- Added `buildCumulativeRankMovementMap` to accumulate signed rank movement across loaded snapshots up to the selected snapshot.
- Extended row decoration to store `_cumPosition` and `_displayStrategy`.
- Updated strategy-cell rendering so the `strategy` column displays `strategy_name (cum_position)` while keeping sort and comparison logic based on raw row fields.
- Extended the row tooltip to include cumulative position context.
Validation:
- `git -C C:\Users\edebe\eds\TradeApps diff -- breakout/fs/strategy_snapshots_15m.html`
  - Result: Confirmed the label logic is confined to the target HTML page and applied at render time.
- Extracted the inline `<script>` block and ran `node --check` on the temporary JS file.
  - Result: Passed with exit code `0`.
- Ran a Python validation against `TradeApps/breakout/fs/json/live/forex/2026-05-07/_strategy_snapshots_15m.json`.
  - Result: Sample labels include `breakout_R_Rev_4_tp20.0_sl30.0 (+29)`, `breakout_R_Rev_4_tp20.0_sl50.0 (+29)`, and `breakout_R_3_tp5.0_sl20.0 (-46)`.
  - Result: The computed values follow the signed cumulative rank-movement rule `previous_rank - current_rank`.
- User verification requested: confirm that the strategy column in `TradeApps/breakout/fs/strategy_snapshots_15m.html` now shows labels like `breakout_Rev_2_tp20.0_sl20.0 (+N)` or `(-N)` using the cumulative position movement you expect.
Risks/Notes:
- Assumption used for implementation: `cum_position` is the cumulative signed movement in leaderboard rank across consecutive snapshots up to the selected snapshot, positive for rising in relative position and negative for falling.
- The displayed value is render-only; the underlying strategy field remains unchanged so sorting by strategy still uses the original raw name.
Completion Status: Awaiting user verification as of 2026-05-07 02:50:00 BST.
