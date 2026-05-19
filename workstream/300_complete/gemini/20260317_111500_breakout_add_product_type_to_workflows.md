# Task: Add product_type to Workflows

## Description
Integrate `product_type` filtering into workflow execution and UI to allow asset-class-specific automation (Forex/Indices).

## Status: COMPLETE

## Checklist
- [x] Update `trade_viewer_api.py` to include `product_type` in default workflow payloads.
- [x] Update `_run_profile_match_workflow_once` to filter by `product_type` across multiple day directories.
- [x] Update `_select_tb_workflow_candidate` (used by `TB_workflow`) to filter candidates by `product_type`.
- [x] Update `_run_tb_prune_all_negative_once` to respect `product_type` when loading buckets and summary data.
- [x] Update `workflow_automation.html` UI to include a `Product Type` selector for all workflows.
- [x] Update `workflow_automation.html` `saveWorkflow` logic to persist `product_type` in workflow configuration.
- [x] Update `constants.py` version to `V20260317_1110`.

## Validation
- Verified `trade_viewer_api.py` compiles without syntax errors.
- Verified `workflow_automation.html` UI shows the new dropdown and correctly passes it during Save/Run.
- Verified backend workflow runners correctly extract `product_type` and use `_iter_day_dirs_for`.

## Completion
- **Time**: 2026-03-17 11:15
- **Version**: V20260317_1110
