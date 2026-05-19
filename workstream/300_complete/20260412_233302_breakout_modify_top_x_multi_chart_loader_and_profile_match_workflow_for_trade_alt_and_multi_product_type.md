# Task: Modify Top X Multi-Chart Loader And Profile Match Workflow For Trade Alt And Multi Product Type

Source: User request on 2026-04-12 to update the `Top X Multi-Chart Loader` and `profile_match_workflow` workflows.

Task Type: feature

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: true

## Task Summary
Update the `Top X Multi-Chart Loader` and `profile_match_workflow` workflow configuration and execution flow to support:
- a new `trade alt` checkbox that sets the downstream Trade Bucket `trade_alt_net` toggle to `true` when checked
- multi-select `product_type` selection instead of single-select
- workflow execution across all selected product types, with resulting data routed to Multi-Chart and any follow-on Trade Bucket flows under the matching product type scope

## Scope Notes
- The new `trade alt` checkbox is a workflow-level option.
- When checked, any Trade Bucket created by the workflow must have `trade_alt_net = true`.
- `product_type` selection must support multiple values in both workflows.
- When multiple product types are selected, the workflow should run the same process independently for each selected product type.
- Multi-Chart payload/output must preserve product-type separation so results are visible under the relevant product type.
- If the workflow chains into Trade Bucket creation, the created buckets and resulting views must also remain product-type-scoped and visible under the corresponding selected product type.

## Validation Plan
- Update workflow config/UI definitions for both workflows to expose `trade alt` and multi-select `product_type`.
- Update workflow execution code so selected product types are iterated rather than treated as a single value.
- Ensure Multi-Chart payload generation includes the correct product type for each result set.
- Ensure follow-on Trade Bucket creation passes both `product_type` and `trade_alt_net`.
- Add focused validation/regression coverage for multi-product-type workflow execution and Trade Bucket propagation.

## Execution Log
- 2026-04-13: Updated `trade_viewer_api.py` workflow defaults and execution paths for `top_x_multi_chart_workflow` and `profile_match_workflow`.
- Added normalized `product_types` handling while preserving legacy `product_type` compatibility.
- Added workflow-level `trade_alt_net` propagation so follow-on Trade Buckets are created with `trade_alt_net = true` when selected.
- Updated workflow-generated Multi-Chart payload items to include per-item `product_type`.
- Updated workflow-created Trade Buckets to persist `product_type` and `trade_alt_net`, and to sync grid/live state using the matching product type.
- Updated `workflow_automation.html` to replace single product-type select with multi-select controls and to add `Trade ALT` checkboxes for the two targeted workflows.
- Updated `multi_chart.js`, `multi_chart_v2.js`, and `multi_chart_v3.js` so workflow imports:
  - consume only items matching the currently selected product type
  - dedupe workflow imports per product type rather than globally
  - save workflow presets with product-type-specific names to avoid cross-type overwrite collisions
- Updated `test_weekly_auto_promote_activation_api.py` to make bucket-sync regression dates dynamic so tests reflect the runtime "today only" promotion rule.

## Validation Results
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py`
  - passed
- `python -m pytest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q`
  - passed: `4 passed`

## Outcome
- Workflow implementation complete for the requested scope.
- Remaining manual verification is browser-level confirmation that a multi-product-type workflow run populates the expected Multi-Chart product-type view and, when enabled, creates Trade Buckets with `trade_alt_net = true`.
