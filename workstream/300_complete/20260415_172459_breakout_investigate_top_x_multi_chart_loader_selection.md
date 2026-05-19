# Investigate Top X Multi-Chart Loader Selection

Source: User request on 2026-04-15 to investigate why `AUTO_TB_0415_021144_286_GBPEUR_C_breakout_2_tp5_0_sl30_0` was selected by workflow in `fs/trade_bucket.html`.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false
- depends_on: []
- feeds_into: []

Task Summary: Investigate why the `Top X Multi-Chart Loader` workflow selected `AUTO_TB_0415_021144_286_GBPEUR_C_breakout_2_tp5_0_sl30_0` in the trade bucket UI/data path, and record the selection path, ranking/filter criteria, and any suspected defect or expected behavior.

Context:
- `fs/trade_bucket.html`
- Top X Multi-Chart Loader workflow code and data sources
- Trade bucket candidate metadata and selection/ranking outputs

Destination Folder: None

Dependency: None

Plan:
- [x] 1. Locate the trade bucket page and selection workflow implementation.
  - Test: [x] `rg -n "Top X|Multi-Chart|multi_chart|top_x|top-x|workflow" TradeApps\breakout\fs -S -g "!pytest-cache-files-*"` returned `TradeApps\breakout\fs\trade_viewer_api.py`, `workflow_automation.html`, `workflows.json`, and `trade_bucket.html` references.
  - Evidence: `trade_viewer_api.py:1855` defines `_run_top_x_multi_chart_workflow`; `workflows.json:114-148` defines the Top X workflow config.
- [x] 2. Trace the candidate's score, filters, sort keys, and workflow state.
  - Test: [x] Inspected `_run_top_x_multi_chart_workflow`, `workflows.json`, and the 2026-04-15 forex trade bucket artefacts to identify the selection path.
  - Evidence: The selected bucket is in `_trade_buckets.json:5` with `created_by_workflow` at line `51`. The workflow loops `sliced = filtered[:top_x]` at `trade_viewer_api.py:2067`, creates TBs when `add_to_tb and sliced` at `2168`, expands same-parameter family at `2213`, and writes `created_by_workflow: top_x_multi_chart_workflow` at `2326`.
- [x] 3. Validate the conclusion against local artefacts without changing production behavior.
  - Test: [x] Read-only PowerShell/rg commands confirmed bucket contents, sibling duplicate buckets, current workflow config, and same-parameter expansion behavior.
  - Evidence: `_trade_buckets.json` contains three buckets created at `2026-04-15T02:11:44`: `...breakout_2_tp5_0_sl30_0`, `...breakout_2_tp5_0_sl50_0`, and `...breakout_R_2_tp5_0_sl30_0`. The reported bucket contains both `breakout_R_2_tp5.0_sl30.0 | GBPEUR_C` and `breakout_2_tp5.0_sl30.0 | GBPEUR_C`.
- [x] 4. Document findings and close the lifecycle task.
  - Test: [x] Lifecycle file includes findings, validation commands/results, risks, and completion status before moving to `workstream/300_complete`.
  - Evidence: This file records the investigation result and validation summary.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `rg` and PowerShell output against `TradeApps\breakout\fs\trade_viewer_api.py`, `TradeApps\breakout\fs\workflows.json`, and `TradeApps\breakout\fs\json\live\forex\2026-04-15\_trade_buckets.json`
  - Objective-Proved: Selection path and candidate reason are verified from local files.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `workstream/300_complete/20260415_172459_breakout_investigate_top_x_multi_chart_loader_selection.md`
  - Objective-Proved: Investigation narrative is captured in the required lifecycle file.
  - Status: captured

Implementation Log:
- 2026-04-15 17:24: Created task file in `workstream/100_todo` per mandatory lifecycle process.
- 2026-04-15 17:25: Moved the same task file to `workstream/200_inprogress`.
- 2026-04-15 17:26: Located the active trade bucket page at `TradeApps\breakout\fs\trade_bucket.html` and the Top X implementation in `TradeApps\breakout\fs\trade_viewer_api.py`.
- 2026-04-15 17:29: Confirmed the reported bucket is persisted in `TradeApps\breakout\fs\json\live\forex\2026-04-15\_trade_buckets.json` and is marked `created_by_workflow: top_x_multi_chart_workflow`.
- 2026-04-15 17:32: Confirmed the relevant workflow config has `top_x: 5`, `add_to_tb: true`, `add_same_parameter_strategies_metrics: true`, `require_positive_total_net: true`, and `sort_by_most_trades: true`.
- 2026-04-15 17:34: Identified the likely defect: duplicate prevention tracks only the selected candidate key after bucket creation, not every expanded family member, allowing overlapping same-parameter buckets.

Changes Made:
- Created and maintained this lifecycle investigation file only.
- No production code or data files were modified.

Findings:
- The reported bucket was created by `Top X Multi-Chart Loader`, not by `trade_bucket.html` itself. `trade_bucket.html` displays the persisted bucket; the selection and creation logic lives in `_run_top_x_multi_chart_workflow()` in `TradeApps\breakout\fs\trade_viewer_api.py`.
- The workflow config in `TradeApps\breakout\fs\workflows.json` currently has `add_to_tb: true` and `add_same_parameter_strategies_metrics: true`, so the Top X workflow is allowed to create live trade buckets and expand a selected candidate into same-parameter family members.
- In `trade_viewer_api.py`, the Top X workflow filters positive candidates, optionally sorts by `trade_count` when `sort_by_most_trades` is true, slices `filtered[:top_x]`, and then iterates every candidate in `sliced` when `add_to_tb` is enabled.
- The reported bucket contains two strategies: `breakout_R_2_tp5.0_sl30.0 | GBPEUR_C` and `breakout_2_tp5.0_sl30.0 | GBPEUR_C`. This happened because same-parameter expansion groups by TP/SL/product, so the `breakout_2_tp5.0_sl30.0` candidate pulled in the `breakout_R_2_tp5.0_sl30.0` sibling.
- `_trade_buckets.json` shows three Top X-created buckets at essentially the same timestamp: the reported `breakout_2_tp5.0_sl30.0` bucket, a `breakout_2_tp5.0_sl50.0` bucket, and another `breakout_R_2_tp5.0_sl30.0` bucket. The first and third contain the same two strategy keys, which indicates duplicate family creation.
- Suspected defect: after creating a bucket, the code adds only `_norm_key(best_model, best_product)` to `existing_keys`. It does not add all keys in `processed_strategies`. Therefore, if both `breakout_2_tp5.0_sl30.0 | GBPEUR_C` and `breakout_R_2_tp5.0_sl30.0 | GBPEUR_C` are in the sliced Top X set, each can create a separate bucket even though same-parameter expansion gives both buckets the same family members.

Validation:
- `rg -n "sort_by_most_trades|sliced = filtered|if add_to_tb and sliced|bucket_name =|created_by_workflow|_family_for_same_param|require_pick_now" TradeApps\breakout\fs\trade_viewer_api.py`
  - Result: confirmed `require_pick_now` is optional (`1912`, `2055`), `sort_by_most_trades` controls ranking (`2061`), Top X slicing occurs at `2067`, TB creation starts at `2168`, family expansion is called at `2213`, bucket name generation at `2232`, and workflow attribution at `2326`.
- `rg -n "top_x_multi_chart_workflow|Top X Multi-Chart Loader|top_x|add_to_tb|add_same_parameter_strategies_metrics|sort_by_most_trades|require_positive_total_net" TradeApps\breakout\fs\workflows.json`
  - Result: confirmed workflow config at lines `114-148`, including `top_x: 5`, `add_to_tb: true`, `add_same_parameter_strategies_metrics: true`, `require_positive_total_net: true`, and `sort_by_most_trades: true`.
- PowerShell JSON read of `_trade_buckets.json`
  - Result: confirmed reported bucket name, `start_time: 2026-04-15T02:11:44.286294`, `created_by_workflow: top_x_multi_chart_workflow`, and two member keys: `breakout_R_2_tp5.0_sl30.0 | GBPEUR_C`; `breakout_2_tp5.0_sl30.0 | GBPEUR_C`.
- PowerShell summary of all buckets in `_trade_buckets.json`
  - Result: confirmed three workflow-created buckets at `02:11:44`, including duplicate same-parameter family membership for the reported bucket and `AUTO_TB_0415_021144_590_GBPEUR_C_breakout_R_2_tp5_0_sl30_0`.

Risks/Notes:
- The exact `_top20.json` state from 02:11 was not preserved in the current live file, so the precise rank at that moment cannot be reconstructed from a frozen Top20 snapshot. The persisted bucket metadata and workflow code are sufficient to establish the creation path and the duplicate-family behavior.
- No fix was applied. A likely fix would update duplicate tracking to add every final strategy key in `processed_strategies` to `existing_keys`, or deduplicate by same-parameter family signature before creating TBs.

Completion Status: Complete on 2026-04-15 17:36.
