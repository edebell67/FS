# Add Workflow Strategy Group Filters

Source: User request to add strategy group selection to `/workflow_automation.html` for `profile_match_workflow` and `Top X Multi-Chart Loader`.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary:
Add strategy group filtering to `profile_match_workflow` and `top_x_multi_chart_workflow` so the workflow can load all strategies by default, or only selected strategy groups (`breakout`, `breakout_r`, `breakout_rev`, `breakout_r_rev`) into Multi Chart when one or more groups are selected.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\workflow_automation.html`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\workflows.json`

Destination Folder: `C:\Users\edebe\eds\TradeApps\breakout\fs`

Dependency: None

Plan:
- [x] 1. Inspect workflow UI save/load and backend Multi Chart payload generation.
  - [x] Test: Locate config handling for both target workflows and identify strategy fields used in emitted Multi Chart selections.
  - Evidence: `workflow_automation.html` renders/saves per-workflow config; `trade_viewer_api.py` builds Multi Chart payloads in `_run_profile_match_workflow_once` and `_run_top_x_multi_chart_workflow`.
- [x] 2. Add strategy group multi-select UI and persist selections to workflow config.
  - [x] Test: `Select-String` confirms strategy group option rendering and save handling for both workflows.
  - Evidence: `WORKFLOW_STRATEGY_GROUP_OPTIONS`, `renderStrategyGroupMultiSelect`, `getSelectedWorkflowStrategyGroups`, and saved `strategy_groups` config were found in `workflow_automation.html`.
- [x] 3. Enforce selected strategy groups in backend Multi Chart payload generation.
  - [x] Test: Backend helper accepts no selection as all groups, and filters exact groups without mixing `breakout_r` with `breakout_r_rev`.
  - Evidence: Helper validation returned PASS for all cases, including `breakout_R_Rev` excluded from `breakout_r` and included for `breakout_r_rev`; empty selection returned allowed.
- [x] 4. Validate syntax and API behavior.
  - [x] Test: `python -m py_compile trade_viewer_api.py` passes; workflow API accepts config update shape; helper-level validation confirms matching semantics.
  - Evidence: `python -m py_compile trade_viewer_api.py` passed; inline scripts in `workflow_automation.html` parsed successfully via Node; `/api/workflows` returned both target workflows after API restart.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `git -C C:\Users\edebe\eds\TradeApps\breakout\fs diff -- workflow_automation.html trade_viewer_api.py`
  - Objective-Proved: Shows UI and backend strategy group filter implementation.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m py_compile trade_viewer_api.py`; Node inline script parse check; helper test output for `breakout`, `breakout_r`, `breakout_rev`, `breakout_r_rev`; `/api/workflows` check.
  - Objective-Proved: Confirms syntax/API/filter validation passed.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `http://localhost:5000/workflow_automation.html`
  - Objective-Proved: User can select strategy groups for the two workflows.
  - Status: captured

Implementation Log:
- 2026-04-30 00:59:18 - Task created from user request.
- 2026-04-30 01:05:00 - Added strategy group multi-select UI for `profile_match_workflow` and `top_x_multi_chart_workflow`.
- 2026-04-30 01:08:00 - Added backend strategy group normalization and exact family matching.
- 2026-04-30 01:11:00 - Restarted local Trade Viewer API so backend filtering is active.

Changes Made:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\workflow_automation.html`
  - Added strategy group options: `breakout`, `breakout_r`, `breakout_rev`, `breakout_r_rev`.
  - Added multi-select controls for `profile_match_workflow` and `top_x_multi_chart_workflow`.
  - Saved selected groups as `config.strategy_groups`; empty selection remains `[]`.
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Added workflow strategy group option constants and exact group classifier.
  - Added `strategy_groups: []` defaults for workflow config.
  - Applied filtering to profile-match candidates and same-parameter expansions.
  - Applied filtering to Top X candidates and same-parameter expansions.
  - Included selected groups in generated Multi Chart payloads and Top X audit config.

Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` passed.
- `node -e "...new Function(script)..."` against `workflow_automation.html` returned `workflow_automation inline scripts parse OK`.
- Helper-level validation:
  - `breakout_2_tp3.0_sl3.0` with `['breakout']`: `True PASS`.
  - `breakout_R_2_tp3.0_sl3.0` with `['breakout_r']`: `True PASS`.
  - `breakout_R_Rev_2_tp3.0_sl3.0` with `['breakout_r']`: `False PASS`.
  - `breakout_R_Rev_2_tp3.0_sl3.0` with `['breakout_r_rev']`: `True PASS`.
  - `breakout_Rev_2_tp3.0_sl3.0` with `['breakout_rev']`: `True PASS`.
  - `breakout_R_2_tp3.0_sl3.0` with no selected groups: `True PASS`.
- `/api/workflows` returned `profile_match_workflow` and `top_x_multi_chart_workflow` after API restart.

Risks/Notes:
- No selected groups must preserve current behavior: all strategy groups remain eligible.
- Exact family matching is required so `breakout_r` does not include `breakout_r_rev`.
- Existing uncommitted changes in `workflow_automation.html` and `trade_viewer_api.py` predate this task; they were not reverted.

Completion Status:
Complete - 2026-04-30 01:11:00
