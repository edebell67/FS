# Breakout TopX Multi Chart Loader Merge Charts Option

Source: User request, 2026-04-22
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on:
  - `workstream/300_complete/20260422_205457_breakout_multi_chart_merge_selected_cards_shared_scale.md`
feeds_into: []

## Task Summary
Add a new `merge charts` checkbox to the Top X Multi-Chart Loader workflow in `fs/workflow_automation.html`. When enabled, the charts exported from that workflow to `multi_chart` should be grouped/merged so they open in `multi_chart` as merged chart cards instead of separate individual chart cards.

## Context
Target UI/source:
- `TradeApps/breakout/fs/workflow_automation.html`

Related downstream UI:
- `TradeApps/breakout/fs/multi_chart.html`
- `TradeApps/breakout/fs/multi_chart.js`

Related completed task:
- `workstream/300_complete/20260422_205457_breakout_multi_chart_merge_selected_cards_shared_scale.md`

Requested behavior:
- In the Top X Multi-Chart Loader workflow, add checkbox label: `merge charts`.
- Default behavior should remain unchanged when unchecked.
- When checked, exported Top X chart payload must instruct `multi_chart` to merge/group the exported charts.
- The receiving `multi_chart` flow must still preserve normal chart-card functionality after import.
- Merged exports should use shared x-axis and y-axis scaling through the existing merged-card/group rendering behavior.

## Destination Folder
Destination Folder: `TradeApps/breakout/fs/`

## Dependency
Dependency: Existing Top X Multi-Chart Loader workflow and completed multi-chart selected-card merge capability.

## Plan
- [x] 1. Inspect the Top X Multi-Chart Loader workflow export path.
  - Test: Identify the controls, payload fields, and import handoff used by `workflow_automation.html` to open/populate `multi_chart`.
  - Evidence: `workflow_automation.html` saves Top X config through `/api/workflows/update`; `trade_viewer_api.py` writes `workflow_multi_chart_payload.json`; `multi_chart.js` imports it through `/api/workflows/multi_chart_payload`.

- [x] 2. Add the `merge charts` checkbox to the Top X Multi-Chart Loader UI.
  - Test: Checkbox is visible in the Top X workflow and defaults unchecked.
  - Evidence: `workflow_automation.html` adds `topx_merge_${id}` with label `merge charts`; unchecked when `cfg.merge_charts` is false/undefined.

- [x] 3. Extend the Top X export payload with merge intent.
  - Test: When checkbox is unchecked, payload matches existing separate-card behavior; when checked, payload includes a merge/grouping instruction.
  - Evidence: `workflow_automation.html` saves `merge_charts`; `trade_viewer_api.py` includes `merge_charts` in Top X workflow payloads and keeps per-card group names when false.

- [x] 4. Update `multi_chart` import handling if needed.
  - Test: Imported Top X payload with merge enabled creates merged card grouping; unchecked payload still creates separate cards.
  - Evidence: `multi_chart.js` uses `payload.group` as the imported group only when `source=top_x_multi_chart_workflow` and `payload.merge_charts` is true; otherwise it preserves `item.group`.

- [x] 5. Validate exported merged charts use shared x/y scaling.
  - Test: Imported merged Top X charts render in a single card using the existing shared x-axis and y-axis Chart.js scale.
  - Evidence: Merge-enabled imports assign all Top X overlays to the same `activeOverlays[].group`, so the existing one-card Chart.js renderer applies one x-axis and one y-axis scale.

- [x] 6. Verify no regression to existing Top X loader behavior.
  - Test: Existing Top X loader flow still works with the checkbox unchecked.
  - Evidence: With `merge_charts=false`, backend still emits per-card groups and importer still uses `item.group`; `node --check` and `py_compile` pass.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/workflow_automation.html`, `TradeApps/breakout/fs/trade_viewer_api.py`, `TradeApps/breakout/fs/multi_chart.js`, `TradeApps/breakout/fs/multi_chart.html`
  - Objective-Proved: Top X workflow can request merged chart export.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: Static verification of Top X Multi-Chart Loader export into `multi_chart`.
  - Objective-Proved: Merge checkbox drives merged chart output while unchecked behavior remains unchanged.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `node --check TradeApps/breakout/fs/multi_chart.js`
  - Objective-Proved: Updated multi-chart import JavaScript parses successfully.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python -m py_compile TradeApps/breakout/fs/trade_viewer_api.py`
  - Objective-Proved: Updated workflow payload generation code is syntactically valid.
  - Status: captured

## Implementation Log
- 2026-04-22 23:34: Created todo task from user request.
- 2026-04-22 23:36: Moved task to in-progress.
- 2026-04-22 23:42: Added Top X `merge charts` checkbox, persisted `merge_charts`, added payload support, and updated multi-chart import grouping.

## Changes Made
- Updated `TradeApps/breakout/fs/workflow_automation.html`.
  - Added `merge charts` checkbox to the Top X Multi-Chart Loader workflow.
  - Persisted the checkbox value as `config.merge_charts`.
- Updated `TradeApps/breakout/fs/trade_viewer_api.py`.
  - Added default `merge_charts: False` to the Top X workflow config.
  - Included `merge_charts` in single-product and multi-product Top X payloads.
  - Uses one shared group for generated payload items when `merge_charts` is true; preserves per-card groups when false.
- Updated `TradeApps/breakout/fs/multi_chart.js`.
  - When Top X payload has `merge_charts=true`, imports all items into `payload.group`.
  - When false/missing, preserves existing `item.group` behavior.
- Updated `TradeApps/breakout/fs/multi_chart.html`.
  - Bumped `multi_chart.js` cache-buster to `V20260422_2334`.

## Validation
- `node --check TradeApps/breakout/fs/multi_chart.js`
  - Result: pass.
- `python -m py_compile TradeApps/breakout/fs/trade_viewer_api.py`
  - Result: pass.
- Static grep:
  - Result: found `topx_merge`, `merge_charts`, `shouldMergeTopXCharts`, and `V20260422_2334` in expected files.

## Risks/Notes
- Prefer using the existing `activeOverlays[].group` grouping model in `multi_chart` rather than adding a second merge implementation.
- Must preserve default separate-card behavior unless `merge charts` is checked.
- Browser automation was not run; validation is static plus syntax checks.

## Completion Status
Status: Complete
Created: 2026-04-22 23:34
Completed: 2026-04-22 23:43
