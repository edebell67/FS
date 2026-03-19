# Top X Multi-Chart Loader — Metric Type Selector

**Source**: User request 2026-03-06
**Created**: 2026-03-06 18:45:00

## Task Summary

Add a metric type dropdown to the **Top X Multi-Chart Loader** workflow (#5) in the Workflow Automation UI. Currently the workflow only uses `total_net` when selecting and displaying strategies in the multi_chart. The new selector should allow the user to choose which metric drives both the ranking/selection and the chart display.

## Context

- **UI File**: `TradeApps/breakout/fs/workflow_automation.html`
  - `render()` function — top_x_multi_chart_workflow section (lines 362-388)
  - `saveWorkflow()` function — top_x config block (lines 481-493)
- **Backend File**: `TradeApps/breakout/fs/trade_viewer_api.py`
  - `_run_top_x_multi_chart_workflow()` (lines 1271-1577)
  - `_default_workflows_payload()` (lines 329-453 — default config for top_x)
- **Payload File**: `TradeApps/breakout/fs/workflow_multi_chart_payload.json`
  - Currently has `"preferred_metric": "net"` hardcoded (line 1424)

## Metric Options

| Option     | Config Value | Description                                        |
|------------|-------------|----------------------------------------------------|
| Total Net  | `net`       | Current default — sort/display by total net         |
| Buy Net    | `buy_net`   | Sort/display by buy-side net only                   |
| Sell Net   | `sell_net`  | Sort/display by sell-side net only                  |
| Buy + Sell | `buy_sell`  | Display both buy and sell as separate overlay lines  |

## Plan

- [x] 1. **UI: Add metric type dropdown to workflow card** (`workflow_automation.html` → `render()`)
  - Add a `<select>` with id `topx_metric_{w.id}` alongside existing controls
  - Options: Total Net (net), Buy Net (buy_net), Sell Net (sell_net), Buy + Sell (buy_sell)
  - Pre-select from `cfg.metric` (default: `net`)
  - Test: Refresh workflow_automation.html → dropdown appears in Top X card with correct selection
  - Evidence: Added select element at line 371-379 of workflow_automation.html

- [x] 2. **UI: Save metric in config payload** (`workflow_automation.html` → `saveWorkflow()`)
  - Read `topx_metric_{id}` value and include as `metric` in payload.config
  - Test: Change metric dropdown, click Save → verify metric persists in workflows.json
  - Evidence: Added metric capture at line 489 of workflow_automation.html

- [x] 3. **Backend: Add metric to default workflow config** (`trade_viewer_api.py` → `_default_workflows_payload()`)
  - Add `"metric": "net"` to the `top_x_multi_chart_workflow` config defaults
  - Test: Verify default config includes metric: net
  - Evidence: Added at line 444 of trade_viewer_api.py

- [x] 4. **Backend: Use selected metric for sorting** (`trade_viewer_api.py` → `_run_top_x_multi_chart_workflow()`)
  - Read `cfg.get("metric", "net")` 
  - When sorting `filtered` list, use the chosen metric field (`total_net`, `buy_net`, `sell_net`) from top20 entries instead of hardcoded `total_net`
  - For `buy_sell`, sort by `total_net` (default) but flag both metrics for display
  - Test: Set metric to buy_net, Run Now → verify payload sorts by buy_net
  - Evidence: Sort field mapping + sort at line 1379 of trade_viewer_api.py

- [x] 5. **Backend: Pass metric to multi-chart payload** (`trade_viewer_api.py` → `_run_top_x_multi_chart_workflow()`)
  - Set `preferred_metric` in the payload output to the selected metric value
  - For `buy_sell`, set `preferred_metric: "buy_sell"` so the multi_chart can render both lines
  - Test: Run workflow with sell_net → verify workflow_multi_chart_payload.json has `preferred_metric: "sell_net"`
  - Evidence: Line 1436 of trade_viewer_api.py

- [x] 6. **Backend: Use metric for same-parameter expansion** (`trade_viewer_api.py` → `_family_for_same_param()`)
  - When `add_same_parameter` is enabled, sort family members by the selected metric (buy_net/sell_net) instead of hardcoded `latest_net` (which is total_net)
  - Test: Enable same-parameter with buy_net metric → verify family sorted by buy_net
  - Evidence: series_net_field used at line 1332 of trade_viewer_api.py

- [x] 7. **Backend: Use metric for TB creation net values** (`trade_viewer_api.py` → TB section)
  - When creating auto TB, use the selected metric for `total_net` capture and bucket metric field
  - Currently `cfg.get("metric", "net")` is already passed to `new_bucket["metric"]` — verified this works with new metric values
  - Test: Create TB with sell_net metric → verify bucket metric field is sell_net
  - Evidence: Line 1560 already reads cfg metric, now correctly receives selected_metric values

- [ ] 8. **Verify end-to-end flow**
  - Set metric to buy_net → Run Now → check multi_chart payload + TB if enabled
  - Set metric to sell_net → Run Now → verify
  - Set metric to buy_sell → Run Now → verify dual-line output
  - Test: Full cycle for each metric option
  - Evidence: _awaiting user verification_

- [ ] 9. **Update version in Constants.py**
  - Test: Version number incremented
  - Evidence: _N/A - no Constants.py found in fs project_

## Implementation Log

- 2026-03-06 19:23: Moved task to 200_inprogress
- 2026-03-06 19:25: Verified _top20.json contains buy_net and sell_net fields
- 2026-03-06 19:26: Added Metric Type dropdown to workflow_automation.html render()
- 2026-03-06 19:26: Added metric capture to saveWorkflow() in workflow_automation.html
- 2026-03-06 19:27: Added "metric": "net" to default config in trade_viewer_api.py
- 2026-03-06 19:28: Added metric sort/series field mappings in _run_top_x_multi_chart_workflow()
- 2026-03-06 19:28: Changed sort from hardcoded total_net to selected metric field
- 2026-03-06 19:28: Changed payload preferred_metric from hardcoded "net" to selected_metric
- 2026-03-06 19:28: Added buy_sell dual-line handling (creates two overlay entries)
- 2026-03-06 19:28: Changed _family_for_same_param to use series_net_field

## Changes Made

### workflow_automation.html
- `render()`: Added Metric Type `<select>` dropdown with 4 options to top_x_multi_chart_workflow card
- `saveWorkflow()`: Captures `topx_metric_{id}` value and includes as `metric` in config payload

### trade_viewer_api.py
- `_default_workflows_payload()`: Added `"metric": "net"` to top_x_multi_chart_workflow default config
- `_run_top_x_multi_chart_workflow()`: 
  - Added `selected_metric` extraction from config
  - Added `_METRIC_SORT_FIELD` mapping (metric → _top20.json field)
  - Added `_METRIC_SERIES_FIELD` mapping (metric → _summary_net.json series field)
  - Sort uses `sort_field` instead of hardcoded `"total_net"`
  - Family expansion uses `series_net_field` instead of hardcoded `"net"`
  - Payload items include `metric` field for each overlay
  - buy_sell creates two entries per strategy (one buy_net, one sell_net)
  - `preferred_metric` in payload output set to `selected_metric`

## Validation

_Pending_

## Risks/Notes

- The `_top20.json` file must contain `buy_net` and `sell_net` fields for those metrics to work. Need to verify these fields exist.
- The `buy_sell` option requires the multi_chart to handle dual-line rendering when importing from the payload — this may already be supported via the overlay `metric` field.
- DO NOT modify unrelated workflow functionality.

## Completion Status

**Awaiting user verification** — All code changes implemented. Need user to verify UI dropdown appears and end-to-end flow works.


# User Feedback
User Verified: PASS
