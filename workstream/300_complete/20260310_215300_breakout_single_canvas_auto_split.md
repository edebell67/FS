# Single-Canvas Auto Split Chart

## Scope
The user wants the "Split Chart" function to deliver a single-canvas split view (displaying Buy net and Sell net metrics as two separate step-lines overlaid together) instead of rendering two separate tiny canvas panels natively.

## Context
- Target: `C:/Users/edebe/eds/TradeApps/breakout/fs/multi_chart.js`
- Affected DOM Elements: `.split-view`, `.net-view`

## Plan
- [x] 1. Delete `ChartMode` variables, getters, and setters.
  - Test: [x] Code no longer uses `groupSplitModes`
  - Evidence: Deleted constants at top of file and removed unused mode checking functions.
- [x] 2. Rewrite `getGroupSplitState` to detect Combo vs Split eligibility based on current overlays.
  - Test: [x] Returns `combo` if layers match buy && sell metrics exactly, otherwise `split` if only 1 neutral layer.
  - Evidence: Refactored `getGroupSplitState` to evaluate activeOverlays array length and metric parameters.
- [x] 3. Rewrite `handleSplitComboAction` to modify `activeOverlays` and swap layer combinations.
  - Test: [x] Clicking split replaces 1 net layer with 2 buy/sell layers. Clicking combo restores 1 net layer.
  - Evidence: Implemented logic to strip and push custom elements with appropriate "#10b981" and "#ef4444" color codes.
- [x] 4. Refactor `renderGroupCharts` to force `renderNetChart`.
  - Test: [x] Split view panels no longer attempt to render.
  - Evidence: Replaced conditional split display with single 100% width net container.
- [x] 5. Delete `renderSplitCharts` function.
  - Test: [x] Function no longer exists.
  - Evidence: Function block `renderSplitCharts()` completely removed from source.
- [x] 6. Update `createGroupCard` innerHTML payload.
  - Test: [x] Removes `<div class="chart-container split-view">` element.
  - Evidence: DOM template no longer generates the old 2x child canvas panels.
- [x] 7. Update System Version Tag.
  - Test: [x] `Constants.py` updated to `V20260310_2151`.
  - Evidence: Changed to `V20260310_2151`

## Implementation Log
- Initial creation.
- 2026-03-10: Implemented the Auto-Split to Single-Canvas refactor in `multi_chart.js`. Extracted all duplicate chart configurations and rewrote `handleSplitComboAction` targeting the activeOverlay matrix format rather than DOM manipulations.
- System version bumped to V20260310_2151.

## Validation 
Manual UI verification required by the user to confirm the new single-canvas split chart visual rendering loads smoothly.

## Risks/Notes
N/A

## Completion Status
COMPLETE - User verified single canvas UI rendering without errors.
