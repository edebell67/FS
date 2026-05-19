# V2 and V3 Multi-Chart Splitting Alignment

## Scope
Applying the new `multi_chart.js` Single-Canvas Auto-Split feature (combining Buy and Sell onto one Net chart dynamically mapping to fa-columns vs fa-compress logic) to the alternative dashboard systems: `fs/multi_chart_v2.js` and `fs/multi_chart_v3.js`.

## Context
- Targets: 
  - `C:/Users/edebe/eds/TradeApps/breakout/fs/multi_chart_v2.js`
  - `C:/Users/edebe/eds/TradeApps/breakout/fs/multi_chart_v3.js`

## Plan
- [x] 1. Delete `ChartMode` and `groupSplitModes` dictionaries and helper functions from both V2 and V3.
  - Test: Code no longer uses `groupSplitModes` in `clearAllOverlays` or `updateCharts` filters.
  - Evidence: Deleted old boilerplate logic.
- [x] 2. Sync `getGroupSplitState` and `handleSplitComboAction` to match V1 in both files.
  - Test: Returns 'split' or 'combo' based purely on active overlays combinations, and successfully pushes/pops `buy_net`/`sell_net`.
  - Evidence: Implemented state fetching and logic using activeOverlays inplace mutation.
- [x] 3. Refactor `renderGroupCharts` to force `renderNetChart` in both files.
  - Test: Split view panels no longer attempt to render.
  - Evidence: Updated to single render call unconditionally.
- [x] 4. Delete `renderSplitCharts` function completely from both files.
  - Test: Function block removed entirely.
  - Evidence: Block effectively removed.
- [x] 5. Update `createGroupCard` innerHTML payload to remove `<div class="chart-container split-view">` and map dynamic split UI button logic in both files.
  - Test: split-toggle button is rendered conditionally without the secondary split canvas wrapper.
  - Evidence: Old HTML layout pruned and toolbar mutation implemented on `updateCharts()`.

## Implementation Log
- Initial creation.
- Applied V1 single-canvas and grid-safe split logics directly into `v2` and `v3` JS builds.
- Cleaned up grid DOM configurations.

## Validation 
Manual refresh and tests required by user.

## Risks/Notes
V2 and V3 had slightly different parameter names (e.g. `getMetricValueV2` vs `getMetricValue`). Logic port manually adjusted to avoid breaking compatibility.

## Completion Status
COMPLETE - User validated V2 and V3 split behavior matches V1.
