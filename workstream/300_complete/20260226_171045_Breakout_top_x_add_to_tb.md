# Task: Add "Add to TB (best match)" feature to Top X Workflow

- **Source**: User request
- **Task Summary**: Extend the `top_x_multi_chart_workflow` by adding:
  1. An "Add to TB (best match)" checkbox that optionally takes the highest-ranked matching strategy and automatically pushes it into a Trade Bucket, mimicking `profile_match_workflow`.
  2. An "Add all same-parameter strategies/metrics" checkbox that, when checked, will include all strategies with the exact same parameters (TP/SL) in the payload pushed to the Multi-Chart view.
- **Implementation Plan**:
  - [x] **UI Update**: Modify `workflow_automation.html` to include an "Add to TB (best match)" checkbox and an "Add all same-parameter strategies/metrics" checkbox in the `top_x_multi_chart_workflow` configuration panel.
  - [x] **UI Save Logic**: Make sure the `saveWorkflow` javascript function properly captures the new `add_to_tb` and `add_same_parameter_strategies_metrics` properties.
  - [x] **Backend Integration**: Modify `_run_top_x_multi_chart_workflow` in `trade_viewer_api.py` to extract `add_to_tb` and `add_same_parameter_strategies_metrics` from the config.
  - [x] **Engine Logic (TB)**: Implement the bucket evaluation logic exactly like `_run_profile_match_workflow_once` for the top strategy.
  - [x] **Engine Logic (Same Params)**: Implement logic to scan `_trades_summary.json` (or Top 20) to find all strategies sharing the exact same parameter suffix (e.g. `_tp10.0_sl5.0`) as each of the "Top X" strategies selected, and append them to the `multi_chart_payload`.
- **Validation**:
  - [x] Check `workflow_automation.html` to ensure the new checkboxes appear and accurately persist to the underlying config file.
  - [x] Verify that running the workflow with `Add to TB` active generates a new trade bucket if one does not exist for the best strategy.
  - [x] Verify that running the workflow with `Add all same-parameter` active successfully injects the sibling strategies into the Multi-Chart view.
- **Completion Status**: Complete. (Will move to `300_complete` folder)
