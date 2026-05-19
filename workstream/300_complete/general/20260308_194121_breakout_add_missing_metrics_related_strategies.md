# Workstream Task: Add Missing Metrics for Related Strategies

## Source
Created based on user request on 2026-03-08.
Reference plan: `C:\Users\edebe\eds\plans\20260308_1941_V20260308_1941_add_metrics_related_strategies.md`

## Task Summary
Modify the `addRelatedStrategies` function in the Breakout dashboard's Multi-Chart views so that when a user clicks the "Add all strategies with same parameters" button, the system accurately detects *all* currently plotted metrics (e.g., "buy", "sell", "net") for the source strategy on the chart card, and inherently duplicates those same metrics when it builds out the complete standard strategy suite.

## Context
- `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart.js`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart_v2.js`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart_v3.js`
- `C:\Users\edebe\eds\DataInsights\src\Constants.py`

## Plan
- [x] 1. Identify distinct metrics on the active chart group.
  - Test: Run grep lookup for metric collection logic in JS files.
  - Evidence: Reviewed existing JavaScript. Confirmed we need to extract from activeOverlays.
- [x] 2. Refactor `addRelatedStrategies` within `multi_chart.js` to iterate over all found metrics rather than just relying on the first found, utilizing tag `[V20260308_1941]`.
  - Test: Verify the logic uses `const inheritedMetrics = [...new Set(...)];` and a nested loop.
  - Evidence: Updated to `metricsToApply.forEach(...)`.
- [x] 3. Apply the same logic and tag update to `multi_chart_v2.js`.
  - Test: Check that `addRelatedStrategies` is updated correctly in V2.
  - Evidence: Updated to `metricsToApply.forEach(...)`.
- [x] 4. Apply the same logic and tag update to `multi_chart_v3.js`.
  - Test: Check that `addRelatedStrategies` is updated correctly in V3.
  - Evidence: Updated to `metricsToApply.forEach(...)`.
- [x] 5. Increment version number in `Constants.py` to `V20260308_1941`.
  - Test: Verify the `VERSION` constant is now `"V20260308_1941"`.
  - Evidence: Version constant successfully updated to `"V20260308_1941"`.

## Implementation Log
- **2026-03-08 19:41**: Generated formal workstream task and corresponding plan file per user instructions.
- **2026-03-08 20:41**: Made the required changes to `multi_chart.js`, `multi_chart_v2.js`, and `multi_chart_v3.js`. The logic now identifies all metrics bound to the current group/overlay reference (e.g. both 'buy' and 'sell') and guarantees that the added strategies inherit all of them via a nested `forEach` loop.
- **2026-03-08 20:41**: Bumped the application version in `Constants.py` to `V20260308_1941`.

## Changes Made
- Modified `addRelatedStrategies()` in `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart.js`
- Modified `addRelatedStrategies()` in `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart_v2.js`
- Modified `addRelatedStrategies()` in `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart_v3.js`
- Updated global configuration version key in `C:\Users\edebe\eds\DataInsights\src\Constants.py`

## Validation
- Pending User review of functionality in the internal dashboard when using the component. Please test the "Add Related" button on a group containing multiple metrics.

## Risks/Notes
- Assumes the underlying dataset mapping arrays contain comparable metric parameters for all target strategies on an equivalent subset basis.

## Completion Status
Awaiting user verification.


# User Feedback
User Verified: PASS
