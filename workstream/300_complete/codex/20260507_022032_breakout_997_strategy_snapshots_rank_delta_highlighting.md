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
Task Summary: Add comparative highlighting to `strategy_snapshots_15m.html` so rows turn green when profit net rises and relative rank improves versus the immediately previous snapshot, and turn red when relative rank drops versus peers.
Context: `TradeApps/breakout/fs/strategy_snapshots_15m.html`, `TradeApps/breakout/fs/json/*/_strategy_snapshots_15m.json`
Destination Folder: TradeApps/breakout/fs/
Dependency: None
Plan:
- [x] 1. Inspect the current snapshot page and JSON structure to determine the correct comparison keys and ranking basis for strategy and product views.
  - [x] Test: Review the HTML render logic and a real `_strategy_snapshots_15m.json` file; pass if the prior-snapshot comparison key and rank metric are unambiguous.
  - Evidence: Reviewed `TradeApps/breakout/fs/strategy_snapshots_15m.html`, `TradeApps/breakout/fs/strategy_snapshot_15m_generator.py`, and `TradeApps/breakout/fs/json/live/forex/2026-05-07/_strategy_snapshots_15m.json`; confirmed `profit_net` is the requested metric and previous-snapshot comparison can use strategy keys for strategy view and strategy+product keys for product view.
- [x] 2. Implement previous-snapshot rank/profit comparison and row highlighting in the page without breaking sorting, filtering, or paging.
  - [x] Test: Update the page logic and inspect the diff; pass if rows get deterministic green/red state from previous-snapshot comparison while existing controls remain intact.
  - Evidence: `git -C C:\Users\edebe\eds\TradeApps diff -- breakout/fs/strategy_snapshots_15m.html` shows helper functions for view-row selection, profit-net ranking, previous-snapshot lookup, and `rank-up` / `rank-down` row styling wired into the existing paged table render.
- [x] 3. Validate the comparison logic against a real JSON artifact and record outcomes in this lifecycle file.
  - [x] Test: Run a local verification script/inspection against `_strategy_snapshots_15m.json`; pass if at least one row demonstrates the intended state logic and no syntax issues are introduced in the edited file.
  - Evidence: `node --check` passed on the extracted inline script, and a Python validation against `TradeApps/breakout/fs/json/live/forex/2026-05-07/_strategy_snapshots_15m.json` found `green_candidates=56` and `red_candidates=82`, including `breakout_R_3_tp5.0_sl20.0` moving from prev rank 43 to current rank 40 with profit net `+1165` to `+1195`.
Evidence:
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `git -C C:\Users\edebe\eds\TradeApps diff -- breakout/fs/strategy_snapshots_15m.html`
  - Objective-Proved: The HTML page logic was updated to compute previous-snapshot comparison and styling.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `node --check <extracted inline script>` and Python validation output against `TradeApps/breakout/fs/json/live/forex/2026-05-07/_strategy_snapshots_15m.json`
  - Objective-Proved: The comparison logic matches real snapshot data and the file remains syntactically valid.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Pending user review in `TradeApps/breakout/fs/strategy_snapshots_15m.html`
  - Objective-Proved: The user can verify that the page highlights rows according to profit-net and relative-position changes.
  - Status: planned
Implementation Log:
- 2026-05-07 02:20:32 BST: Created lifecycle task from the user request.
- 2026-05-07 02:22:00 BST: Located the page at `TradeApps/breakout/fs/strategy_snapshots_15m.html` and confirmed it loads a time-series JSON artifact from `json/<mode>/<product>/<date>/_strategy_snapshots_15m.json`.
- 2026-05-07 02:23:00 BST: Implemented helper functions to build stable row keys, rank current and previous snapshots by `profit_net`, and attach row highlight metadata before sort/paging.
- 2026-05-07 02:24:00 BST: Added green and red row highlight styles and row tooltips showing previous profit net and rank context.
- 2026-05-07 02:24:38 BST: Validated the script syntax and checked the rule against live forex snapshot data for 2026-05-07.
- 2026-05-07 02:24:38 BST: Restored the lifecycle file to `200_inprogress` after an automated `.result.md` artifact left the primary task file state inconsistent.
Changes Made:
- Updated `TradeApps/breakout/fs/strategy_snapshots_15m.html` to add `rank-up` and `rank-down` row styles.
- Added `rowKey`, `rankRowsByProfitNet`, `getViewRows`, and `decorateRowsWithRankDelta` helpers.
- Changed table preparation so highlight state is computed from the immediately previous snapshot within the same view and active group filter before existing sort and paging are applied.
- Added row `title` metadata to expose previous profit-net and rank values on hover.
Validation:
- `git -C C:\Users\edebe\eds\TradeApps diff -- breakout/fs/strategy_snapshots_15m.html`
  - Result: Confirmed the page diff contains the comparison helpers and row highlight wiring only in the target HTML file.
- Extracted the inline `<script>` block and ran `node --check` on the temporary JS file.
  - Result: Passed with exit code `0`.
- Ran a Python validation against `TradeApps/breakout/fs/json/live/forex/2026-05-07/_strategy_snapshots_15m.json`.
  - Result: `green_candidates=56`, `red_candidates=82`.
  - Result: Sample green candidate `breakout_R_3_tp5.0_sl20.0` moved from rank `43` to `40` while `profit_net` increased from `+1165` to `+1195`.
  - Result: Sample red candidate `breakout_R_4_tp5.0_sl20.0` moved from rank `51` to `53`.
- User verification requested: confirm that rows which improved `profit_net` and moved up the `profit_net` leaderboard render green, and rows whose relative rank dropped render red when viewing `TradeApps/breakout/fs/strategy_snapshots_15m.html`.
Risks/Notes:
- The visual treatment is row-level highlighting rather than single-cell highlighting, which keeps the rank-change signal visible regardless of current sort column.
- The rank change is measured against the immediately previous snapshot in the loaded JSON series.
Completion Status: Awaiting user verification as of 2026-05-07 02:24:38 BST.
