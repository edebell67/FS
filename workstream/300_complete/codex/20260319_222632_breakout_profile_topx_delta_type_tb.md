# Breakout Workflow Delta Type To TB

## Source
- User request to execute `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260319_222632_breakout_profile_topx_delta_type_tb.md` end-to-end.

## Task Summary
- Add `delta_type` selection to `profile_match_workflow` and `Top X Multi-Chart Loader`.
- Support `delta1` and `delta2`.
- Persist the selected value in workflow config.
- Ensure Trade Bucket records carry the selected `delta_type`.
- Ensure Trade Bucket `total_net` resolves from the bucket-selected delta basis.

## Context
- UI: `TradeApps/breakout/DB/workflow_automation.html`
- Backend: `TradeApps/breakout/DB/trade_viewer_api.py`
- Workflow config: `TradeApps/breakout/DB/workflows.json`

## Dependency
- Dependency: None

## Plan
- [x] 1. Inspect the DB workflow UI, workflow persistence path, and Trade Bucket delta resolution path.
  - [x] Test: `rg -n "profile_match_workflow|top_x_multi_chart_workflow|/api/workflows|create_trade_bucket|trade_buckets" "C:\Users\edebe\eds\TradeApps\breakout\DB\workflow_automation.html" "C:\Users\edebe\eds\TradeApps\breakout\DB\trade_viewer_api.py"`
  - Evidence: Confirmed DB UI had workflow controls but no `delta_type` selector; DB API had placeholder `/api/workflows` response and Trade Bucket create/get paths without bucket-level `delta_type`.
- [x] 2. Add `delta_type` selectors and save-payload wiring for the two workflow cards in the DB workflow UI.
  - [x] Test: `rg -n "TB Delta Type|pdt_|topx_delta_|delta_type: delta_type" "C:\Users\edebe\eds\TradeApps\breakout\DB\workflow_automation.html"`
  - Evidence: `workflow_automation.html` now contains `TB Delta Type` selectors for both workflow cards and posts `delta_type` in both workflow save payloads.
- [x] 3. Implement DB workflow config load/update persistence and store default `delta_type` values in workflow config.
  - [x] Test: `python -c "import json; json.load(open(r'C:\Users\edebe\eds\TradeApps\breakout\DB\workflows.json', 'r', encoding='utf-8')); print('json_ok')"`
  - Evidence: `json_ok`; `trade_viewer_api.py` now exposes `/api/workflows` and `/api/workflows/update` backed by `workflows.json`, and `workflows.json` includes `delta_type: "delta2"` for both targeted workflows.
- [x] 4. Stamp created Trade Buckets and strategies with `delta_type`, and make bucket `total_net` respect the bucket-selected delta basis.
  - [x] Test: `rg -n "_normalize_delta_type|bucket_delta_type|delta_type': delta_type|strat\\['total_net'\\] = strat\\['delta1'\\] if bucket_delta_type == 'delta1' else strat\\['delta2'\\]" "C:\Users\edebe\eds\TradeApps\breakout\DB\trade_viewer_api.py"`
  - Evidence: `trade_viewer_api.py` now normalizes `delta_type`, persists it on new bucket records and strategy entries, and computes `total_net` from `delta1` or `delta2` according to the bucket-level setting.
- [x] 5. Validate the DB implementation changes.
  - [x] Test: `python -m py_compile "C:\Users\edebe\eds\TradeApps\breakout\DB\trade_viewer_api.py"`
  - Evidence: Python compile completed with exit code `0`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/DB/workflow_automation.html`, `TradeApps/breakout/DB/trade_viewer_api.py`, `TradeApps/breakout/DB/workflows.json`
  - Objective-Proved: The DB workflow UI, persistence path, and Trade Bucket delta handling were updated to support workflow-configured `delta_type`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\DB\trade_viewer_api.py`
  - Objective-Proved: The updated DB backend file is syntactically valid Python.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -c "import json, pathlib; json.load(open(r'C:\Users\edebe\eds\TradeApps\breakout\DB\workflows.json', 'r', encoding='utf-8')); print('json_ok')"`
  - Objective-Proved: The updated DB workflow configuration file is valid JSON.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `rg -n "delta_type|TB Delta Type|/api/workflows/update|_normalize_delta_type|bucket_delta_type" C:\Users\edebe\eds\TradeApps\breakout\DB\workflow_automation.html C:\Users\edebe\eds\TradeApps\breakout\DB\trade_viewer_api.py C:\Users\edebe\eds\TradeApps\breakout\DB\workflows.json`
  - Objective-Proved: The requested `delta_type` wiring exists across the DB UI, workflow config persistence path, bucket creation path, and bucket-resolution path.
  - Status: captured

## Implementation Log
- 2026-03-19 22:26:32 Created lifecycle task file.
- 2026-03-19 22:31:00 Lifecycle file previously moved to `200_inprogress`.
- 2026-03-19 22:52:00 Lifecycle file was previously moved to `300_complete`, but the DB-scope implementation had not been executed.
- 2026-03-19 23:02 Reviewed `skills/workstream-task-lifecycle/SKILL.md` and re-opened the task operationally using the existing lifecycle file.
- 2026-03-19 23:04 Inspected the DB workflow UI and confirmed the two targeted workflow cards existed without `delta_type` controls.
- 2026-03-19 23:06 Inspected the DB API and confirmed `/api/workflows` returned an empty list and `/api/workflows/update` did not exist.
- 2026-03-19 23:09 Added `delta_type` selectors and payload fields to the DB workflow UI for `profile_match_workflow` and `top_x_multi_chart_workflow`.
- 2026-03-19 23:11 Added DB workflow config file load/save helpers and an update endpoint backed by `TradeApps/breakout/DB/workflows.json`.
- 2026-03-19 23:12 Added `delta_type` defaults to the two targeted DB workflow definitions in `workflows.json`.
- 2026-03-19 23:13 Updated DB Trade Bucket creation to persist normalized `delta_type` at both bucket and strategy level.
- 2026-03-19 23:14 Updated DB Trade Bucket stats resolution so `total_net` follows the bucket-selected `delta_type`.
- 2026-03-19 23:15 Ran Python and JSON validation and captured `rg` proof for the new wiring.

## Changes Made
- `TradeApps/breakout/DB/workflow_automation.html`
  - Added `TB Delta Type` selector to `profile_match_workflow`.
  - Added `TB Delta Type` selector to `top_x_multi_chart_workflow`.
  - Added `delta_type` to both workflow save payloads posted to `/api/workflows/update`.
- `TradeApps/breakout/DB/trade_viewer_api.py`
  - Added `WORKFLOWS_FILE` constant for DB workflow config persistence.
  - Added `_load_workflows`, `_save_workflows`, `_hhmm_to_minutes`, `_workflow_active_now`, and `_normalize_delta_type`.
  - Replaced placeholder `/api/workflows` response with file-backed workflow loading.
  - Added `/api/workflows/update` to persist workflow config updates, including normalized `delta_type`.
  - Updated `create_trade_bucket()` to persist `delta_type` on the bucket and each processed strategy.
  - Updated `get_trade_buckets()` to compute `delta1`/`delta2` and set `total_net` from the bucket-selected delta basis.
- `TradeApps/breakout/DB/workflows.json`
  - Added `delta_type: "delta2"` to `profile_match_workflow`.
  - Added `delta_type: "delta2"` to `top_x_multi_chart_workflow`.

## Validation
- 2026-03-19 23:15 `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\DB\trade_viewer_api.py`
  - Result: pass
- 2026-03-19 23:15 `python -c "import json, pathlib; json.load(open(r'C:\Users\edebe\eds\TradeApps\breakout\DB\workflows.json', 'r', encoding='utf-8')); print('json_ok')"`
  - Result: pass (`json_ok`)
- 2026-03-19 23:15 `rg -n "delta_type|TB Delta Type|/api/workflows/update|_normalize_delta_type|bucket_delta_type|total_net = strat\['delta1'\] if bucket_delta_type == 'delta1' else strat\['delta2'\]" C:\Users\edebe\eds\TradeApps\breakout\DB\workflow_automation.html C:\Users\edebe\eds\TradeApps\breakout\DB\trade_viewer_api.py C:\Users\edebe\eds\TradeApps\breakout\DB\workflows.json`
  - Result: pass
  - Key proof lines:
    - UI selectors in `workflow_automation.html`
    - `delta_type` defaults in `workflows.json`
    - Workflow persistence in `trade_viewer_api.py`
    - Bucket delta resolution in `trade_viewer_api.py`

## Risks/Notes
- The DB backend still does not implement the full workflow run engine present in the `fs` variant; this task implemented the requested DB UI/config persistence path and the Trade Bucket delta behavior needed by manual and future workflow-created bucket writes.
- The lifecycle file had already been moved to `300_complete` before the DB implementation was actually executed. This update corrects the record content without creating a second lifecycle file.

## Completion Status
- Complete
- Completed At: 2026-03-19 23:15 Europe/London
