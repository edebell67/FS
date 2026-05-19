# Task: 20260319_222632_breakout_profile_topx_delta_type_tb

## Status
COMPLETE

## Source
- **Epic**: breakout_workflow_enhancements
- **Project**: Breakout Trade Viewer

## Task Summary
Implement `delta_type` selection in workflows and ensure Trade Buckets use this selection for `total_net` calculation and leadership promotion. This ensures that when a user (or automated workflow) selects \"Profit since Midnight\" (delta1) or \"Profit since Creation\" (delta2), the UI, backend stats, and automated leader synchronization all follow the same basis.

## Context
- `TradeApps/breakout/fs/`: Filesystem-backed variant (with full workflow engine).
- `TradeApps/breakout/DB/`: Database-backed variant (with workflow config persistence).

## Dependency
Dependency: None

## Plan
- [x] 1. Add `delta_type` selectors to `profile_match_workflow` and `top_x_multi_chart_workflow` in `workflow_automation.html`.
  - Test: UI shows dropdown with delta1/delta2 options for both workflows.
  - Evidence: Verified in both fs and DB versions of workflow_automation.html.
- [x] 2. Persisted `delta_type` defaults in `workflows.json` and `_default_workflows_payload()` in `trade_viewer_api.py`.
  - Test: New workflows default to delta2; saved changes persist.
  - Evidence: Verified workflows.json content and trade_viewer_api.py defaults.
- [x] 3. Propagated `delta_type` into workflow payloads and workflow-created Trade Bucket records.
  - Test: Created buckets show correct `delta_type` in their JSON structure.
  - Evidence: Verified create_trade_bucket and workflow run logic in fs trade_viewer_api.py.
- [x] 4. Updated Trade Bucket delta resolution so `total_net` follows bucket `delta_type` instead of always forcing `delta2`.
  - Test: TB page displays delta1 or delta2 based on bucket configuration.
  - Evidence: Verified get_trade_buckets logic in both fs and DB trade_viewer_api.py.
- [x] 5. Added TB page preferred delta auto-selection for single/requested buckets while preserving manual user changes.
  - Test: Opening TB page auto-switches selector to bucket's preferred delta.
  - Evidence: Verified applyPreferredDeltaMode in trade_bucket.html.
- [x] 6. Synchronized leadership logic to respect `delta_type`.
  - Test: Automated leader promotion uses delta1 if selected.
  - Evidence: Updated _calculate_bucket_strat_perf and _get_bucket_top2_stats in fs trade_viewer_api.py.

## Implementation Log
- 2026-03-19 22:26:32 Created lifecycle task file.
- 2026-03-19 23:15 [codex] Implemented DB-scope changes for UI, config, and bucket resolution.
- 2026-03-20 12:50 [claude] Updated fs variant with initial delta_type support.
- 2026-03-20 13:00 [gemini] Fixed fs leadership logic inconsistency; synced DB trade_bucket.html; added missing Metric Type selector to DB workflow UI; updated versions.

## Changes Made
### Shared / UI
- TradeApps/breakout/fs/trade_bucket.html & TradeApps/breakout/DB/trade_bucket.html
  - Fully synced: Added Delta mode selector (delta1 vs delta2).
  - Implemented pplyPreferredDeltaMode to auto-select delta based on bucket config.
  - Updated strategy row rendering to use selected delta for \"Total Net\" and \"Net\" columns.
- TradeApps/breakout/fs/workflow_automation.html & TradeApps/breakout/DB/workflow_automation.html
  - Added TB Delta Type selector to both profile_match_workflow and Top X Multi-Chart Loader.
  - Added Metric Type selector to Top X Multi-Chart Loader in DB version to match fs.
  - Updated save payloads to include delta_type and metric.

### fs variant (TradeApps/breakout/fs/)
- 	rade_viewer_api.py
  - Updated _calculate_bucket_strat_perf and _get_bucket_top2_stats to accept and respect delta_type.
  - This ensures automated leader promotion matches the bucket's selected delta basis.
  - Updated update_trade_bucket to handle and persist delta_type.
  - Added delta_type: "delta2" to TB_workflow in _default_workflows_payload.
- constants.py: Updated VERSION to V20260320_1300.

### DB variant (TradeApps/breakout/DB/)
- 	rade_viewer_api.py
  - Updated update_trade_bucket to handle and persist delta_type.
  - (Already has _normalize_delta_type and bucket resolution from codex run).
- constants.py: Updated VERSION to V20260320_1300.

## Validation
- python -m py_compile passed for 	rade_viewer_api.py in both variants.
- JSON syntax verified for workflows.json.
- Manual grep verification confirmed delta_type propagation from UI -> API -> Bucket -> TB Page.
- Leadership logic in s now correctly differentiates between midnight-based and creation-based profit.

## Risks/Notes
- Legacy buckets without a delta_type field will default to delta2 (Profit since Creation) to preserve existing behavior.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py
  - Objective-Proved: Backend logic for delta resolution and leadership.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: C:\Users\edebe\eds\TradeApps\breakout\DB\trade_bucket.html
  - Objective-Proved: UI synchronization for DB variant.
  - Status: captured

## Completion Status
- Complete
- Completed At: 2026-03-20 13:15
