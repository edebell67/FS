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
Task Summary: Build a new snapshot-style analysis over `_summary_net.json` that, at each 15-minute snapshot, identifies the top 10 most improved strategy/product net values over the trailing 30-minute and trailing 60-minute windows, and present the output in a screen similar to `strategy_snapshots_15m.html`.
Context: `TradeApps/breakout/fs/summary_net_generator.py`, `TradeApps/breakout/fs/analyze_top_strategies.py`, `TradeApps/breakout/fs/strategy_snapshots_15m.html`, `TradeApps/breakout/fs/json/*/_summary_net.json`
Destination Folder: TradeApps/breakout/fs/
Dependency: None
Plan:
- [x] 1. Inspect `_summary_net.json` series structure and existing 15-minute snapshot tooling to define the canonical rolling-delta calculation.
  - [x] Test: Review `analyze_top_strategies.py`, a real `_summary_net.json`, and `strategy_snapshots_15m.html`; pass if the 15-minute snapshot times, series keys, and 30m/60m delta formula are unambiguous.
  - Evidence: Reviewed `TradeApps/breakout/fs/analyze_top_strategies.py`, `TradeApps/breakout/fs/strategy_snapshots_15m.html`, and `TradeApps/breakout/fs/json/live/forex/2026-05-07/_summary_net.json`; confirmed timestamped per-strategy/product series use `t` and `net`, and rolling deltas can be computed from the latest point at or before each snapshot and baseline timestamp.
- [x] 2. Design the output artifact and/or page contract for two leaderboards per snapshot: top 10 by last-30m net delta and top 10 by last-60m net delta.
  - [x] Test: Document the intended JSON/output shape in this lifecycle file; pass if each snapshot clearly contains timestamped `top10_30m` and `top10_60m` rankings with strategy, product, baseline net, current net, and delta.
  - Evidence: Implemented and documented `_summary_net_delta_snapshots_15m.json` with `snapshots[].top10_30m`, `snapshots[].top10_60m`, `summary_30m`, `summary_60m`, and row fields `strategy_group`, `strategy`, `product`, `baseline_time`, `current_time`, `baseline_net`, `current_net`, and `delta_net`.
- [x] 3. Implement the generator/analysis pipeline that reads `_summary_net.json`, samples every 15 minutes, computes rolling deltas, and emits the snapshot artifact.
  - [x] Test: Run the generator on a real date/product sample; pass if it writes the new snapshot artifact with populated 30m and 60m top-10 lists.
  - Evidence: Ran `python TradeApps/breakout/fs/summary_net_delta_snapshots_15m_generator.py --mode live --product-type forex --date 2026-05-07`, which wrote `TradeApps/breakout/fs/json/live/forex/2026-05-07/_summary_net_delta_snapshots_15m.json`.
- [x] 4. Add or wire a screen similar to `strategy_snapshots_15m.html` so each 15-minute snapshot can be inspected visually with separate 30m and 60m improvement views.
  - [x] Test: Open or inspect the page/output contract; pass if a user can browse each snapshot in a `strategy_snapshots_15m.html`-style UI and see the top 10 most improved strategy/product rows for both windows.
  - Evidence: Added `TradeApps/breakout/fs/summary_net_delta_snapshots_15m.html` with matching control bar, snapshot strip, summary cards for 30m/60m, sortable table, and fetch path for `_summary_net_delta_snapshots_15m.json`; also added a sidebar entry for the new page.
- [x] 5. Validate the rolling-delta results against a real `_summary_net.json` sample and capture representative outputs.
  - [x] Test: Run a focused verification on at least one date/product; pass if sample snapshot entries prove the 30m and 60m delta calculations are correct.
  - Evidence: For `live/forex/2026-05-07`, the generated artifact reported `snapshot_count=44`; latest `10:45` snapshot top 30m row was `breakout_R_2_tp10.0_sl5.0 / GBPNZD_C` with `baseline_net=480`, `current_net=560`, `delta_net=80`, and top 60m row was `breakout_R_Rev_2_tp20.0_sl3.0 / EURNZD_C` with `baseline_net=-457.5`, `current_net=-307.5`, `delta_net=150`.
Evidence:
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `git -C C:\Users\edebe\eds\TradeApps diff -- breakout/fs/summary_net_delta_snapshots_15m_generator.py breakout/fs/summary_net_delta_snapshots_15m.html breakout/fs/sidebar.html`
  - Objective-Proved: The generator/viewer code and task outputs for rolling 30m/60m snapshot leaderboards were added.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python TradeApps/breakout/fs/summary_net_delta_snapshots_15m_generator.py --mode live --product-type forex --date 2026-05-07`, `node --check <extracted inline script>`, and spot-check output from `TradeApps/breakout/fs/json/live/forex/2026-05-07/_summary_net_delta_snapshots_15m.json`
  - Objective-Proved: The rolling-delta artifact is generated from real `_summary_net.json` data and produces valid top-10 snapshots.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Pending user review in `TradeApps/breakout/fs/summary_net_delta_snapshots_15m.html`
  - Objective-Proved: The user can inspect the snapshot output and confirm it matches the intended “most improved over last 30m / 60m” behavior.
  - Status: planned
Implementation Log:
- 2026-05-07 10:03:21 BST: Created lifecycle task from the user request.
- 2026-05-07 10:03:21 BST: Identified nearby implementation context including `analyze_top_strategies.py`, `strategy_snapshots_15m.html`, and multiple `_summary_net.json` consumers under `TradeApps/breakout/fs`.
- 2026-05-07 10:03:21 BST: Clarified that the deliverable must include a screen similar to `strategy_snapshots_15m.html`, not only a generated JSON artifact.
- 2026-05-07 10:44:00 BST: Implemented `summary_net_delta_snapshots_15m_generator.py` to sample 15-minute snapshots and compute trailing 30m/60m top-10 deltas from `_summary_net.json`.
- 2026-05-07 10:46:00 BST: Added `summary_net_delta_snapshots_15m.html` with a `strategy_snapshots_15m.html`-style layout for snapshot browsing and window switching.
- 2026-05-07 10:47:00 BST: Added a sidebar link for the new screen.
- 2026-05-07 10:49:39 BST: Generated and validated the live forex artifact for `2026-05-07` and confirmed sample top rows for both windows.
Changes Made:
- Added `TradeApps/breakout/fs/summary_net_delta_snapshots_15m_generator.py`.
- Added `TradeApps/breakout/fs/summary_net_delta_snapshots_15m.html`.
- Updated `TradeApps/breakout/fs/sidebar.html` to include a `Delta Snapshots` entry.
- Generated `TradeApps/breakout/fs/json/live/forex/2026-05-07/_summary_net_delta_snapshots_15m.json` for validation.
Validation:
- `python TradeApps/breakout/fs/summary_net_delta_snapshots_15m_generator.py --mode live --product-type forex --date 2026-05-07`
  - Result: Wrote `TradeApps/breakout/fs/json/live/forex/2026-05-07/_summary_net_delta_snapshots_15m.json`.
- Extracted the inline `<script>` from `TradeApps/breakout/fs/summary_net_delta_snapshots_15m.html` and ran `node --check`.
  - Result: Passed with exit code `0`.
- Inspected the generated artifact for `live/forex/2026-05-07`.
  - Result: `snapshot_count=44`, latest snapshot `2026-05-07T10:45:00`.
  - Result: Latest `top10_30m` leader: `breakout_R_2_tp10.0_sl5.0 / GBPNZD_C`, baseline `480`, current `560`, delta `80`.
  - Result: Latest `top10_60m` leader: `breakout_R_Rev_2_tp20.0_sl3.0 / EURNZD_C`, baseline `-457.5`, current `-307.5`, delta `150`.
- User verification requested: open `TradeApps/breakout/fs/summary_net_delta_snapshots_15m.html` and confirm the screen structure and the 30m/60m leaders match the intended “most improved in the last 30/60 minutes” behavior.
Risks/Notes:
- Assumption: “most improved strategy/product net” means ranking by `current_net - net_at_30_minutes_ago` and `current_net - net_at_60_minutes_ago` at each 15-minute snapshot.
- Assumption: rankings should be at the strategy+product grain, not strategy-only, because the request says “strategy/product net”.
- Implemented baseline lookup uses the latest source point at or before the target baseline timestamp, which is the safest option for irregular `_summary_net.json` timestamps.
- `sidebar.html` already had unrelated working-tree differences; only the new `Delta Snapshots` entry was intentionally added.
Completion Status: Awaiting user verification as of 2026-05-07 10:49:39 BST.


# User Feedback
User Verified: PASS
