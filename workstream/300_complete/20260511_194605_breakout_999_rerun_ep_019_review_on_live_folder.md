Source: User request in Codex chat on 2026-05-11 to rerun the `ep_019` review on the configured live folder.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary: Rerun the `ep_019` result review against the configured live daily-folder location, confirm the actual data used, and update findings based on the live dataset.

Context:
- `TradeApps/breakout/fs/config.json`
- `TradeApps/breakout/fs/paths.py`
- `TradeApps/breakout/fs/json_layout.py`
- `epics/ep_019_breakout_monetization/*.py`

Destination Folder: None

Dependency: `workstream/300_complete/20260511_193509_breakout_999_review_ep_019_results.md`

Plan:
- [x] 1. Verify the configured live folder is accessible from the current environment.
  - [x] Test: Resolve and inspect the live root declared by breakout configuration.
  - [x] Evidence: Escalated shell access confirmed `X:\eds\TradeApps\breakout\fs\json\live` exists and contains `forex` and dated live folders.
- [x] 2. If accessible, rerun the relevant analysis scripts or equivalent logic against that live dataset.
  - [x] Test: Capture updated runtime outputs using the live folder.
  - [x] Evidence: Live-folder reruns completed for preselection logic and `v6.12`-equivalent multi-move logic using `X:\eds\TradeApps\breakout\fs\json\live\forex`.
- [x] 3. If inaccessible, identify the blocker and record any accessible mirror/fallback path.
  - [x] Test: Search for an accessible equivalent of the configured live dataset.
  - [x] Evidence: Initial sandbox could not see `X:`; escalated environment could. No fallback mirror was needed after escalation.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: Escalated command outputs against `X:\eds\TradeApps\breakout\fs\json\live\forex`
  - Objective-Proved: Live-folder accessibility and rerun results were validated.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: This lifecycle file and final rerun summary
  - Objective-Proved: Final rerun status reflects the actual available live data path.
  - Status: captured

Implementation Log:
- 2026-05-11 19:46:05: Rerun task created for live-folder-based `ep_019` review.
- 2026-05-11 19:47: Initial sandbox checks could not see the mapped `X:` drive; escalated shell access was required.
- 2026-05-11 19:48: Confirmed live data root exists at `X:\eds\TradeApps\breakout\fs\json\live` with `forex` and `social_posting_package` directories.
- 2026-05-11 19:50: Enumerated 38 dated day folders under `X:\eds\TradeApps\breakout\fs\json\live\forex` containing `_summary_net.json`.
- 2026-05-11 19:52: Reran preselection logic directly on live `forex`; best result was only `55.6% (15/27)` for `balanced_50` at 6 AM.
- 2026-05-11 19:54: Reran `v6.12`-equivalent multi-move logic directly on live `forex`; result was `0.0% (0/35)` with total PnL `-$2145.00`.

Changes Made:
- None yet.

Validation:
- Escalated live-root inspection
  - Result: `X:\eds\TradeApps\breakout\fs\json\live` exists; sandbox visibility differed from full user session visibility.
- Live `forex` day-folder enumeration
  - Result: 38 dated folders found, spanning `2026-03-16` through `2026-05-11` plus a few earlier dates.
- Live preselection rerun on `X:\eds\TradeApps\breakout\fs\json\live\forex`
  - Result: `loaded_days 38`
  - Best min-5-sample result: `balanced_50 h=6 acc=55.6% hits=15/27 improv=22.2%`
  - Next best: `balanced_50 h=5 acc=51.9% hits=14/27`
- Live `v6.12`-equivalent multi-move rerun on `X:\eds\TradeApps\breakout\fs\json\live\forex`
  - Result: `found_paths 38`, `valid_results 35`
  - Accuracy: `0.0% hits=0/35`
  - Total PnL: `-2145.00`

Risks/Notes:
- The configured `X:` drive may not be mounted in the current execution environment.
- The original `ep_019` scripts still hardcode legacy C-paths, so this rerun used equivalent inline logic against the actual live X-drive data rather than the unmodified script files.
- Three live day files produced no valid simulation result in the `v6.12` logic path, so the denominator was 35 from 38 discovered files.
- Live-data results are materially worse than the earlier DB-backed rerun, which means prior conclusions were sensitive to data source selection.

Completion Status:
- Complete on 2026-05-11 19:55 after rerunning the review logic on the actual live folder.
