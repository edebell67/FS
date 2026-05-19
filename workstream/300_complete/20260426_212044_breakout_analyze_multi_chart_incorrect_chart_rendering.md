Source: User request in Codex session on 2026-04-26
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
Task Summary: Analyze why `TradeApps/breakout/fs/multi_chart.html` is rendering incorrect-looking charts even when the underlying series data is considered correct.
Context: Screenshot from `/multi_chart.html`, chart rendering path in `TradeApps/breakout/fs/multi_chart.js`, and active sim summary data in `TradeApps/breakout/fs/json/sim/forex/2026-04-26/_summary_net.json`.
Destination Folder: TradeApps/breakout/fs/
Dependency: None

Plan:
- [x] 1. Trace the chart rendering path from `_summary_net.json` into `multi_chart.js`.
  - [x] Test: Inspect the summary fetch, processed-series transformation, and chart dataset build path; pass when the data flow is identified.
- [x] 2. Inspect the underlying summary series for the strategies/products shown in the screenshot.
  - [x] Test: Read the relevant strategy/product series and identify whether the anomalous shape starts in the stored points or after chart transformation.
- [x] 3. Identify the chart-layer failure mode and document where the visual distortion begins.
  - [x] Test: Correlate source code behavior with the duplicated/sparse timestamps in the stored series; pass when the first concrete divergence point is identified.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: source_trace
  - Artifact: `TradeApps/breakout/fs/multi_chart.js`
  - Objective-Proved: `fetchData()` loads `_summary_net.json`, converts points to `processedSeries`, then `buildSteppedSeries(...)` passes all points directly into a Chart.js stepped time series without collapsing duplicate timestamps.
  - Status: captured
- Evidence-Type: data_inspection
  - Artifact: `TradeApps/breakout/fs/json/sim/forex/2026-04-26/_summary_net.json`
  - Objective-Proved: The visible strategy/product series contain multiple points with identical timestamps but different `net` values, which creates visual backtracks/vertical spikes on a stepped time chart.
  - Status: captured

## Implementation Log
- 2026-04-26 21:20:44+01:00 Created lifecycle task for diagnosing incorrect chart rendering in `multi_chart.html`.
- 2026-04-26 21:21:10+01:00 Traced the chart path in `multi_chart.js`: `_summary_net.json` -> `processedSeries` -> `buildSteppedSeries(...)` -> Chart.js `stepped: true`.
- 2026-04-26 21:22:20+01:00 Inspected `breakout_2_tp20.0_sl50.0` and `breakout_3_tp20.0_sl50.0` series in the active sim `_summary_net.json` and confirmed repeated timestamps with different values within the same strategy/product series.
- 2026-04-26 21:23:00+01:00 Identified the rendering failure mode: the chart uses a stepped time series with all duplicate timestamps preserved, so multiple same-time updates render as stacked vertical jumps/backtracks at one x-position, which matches the screenshot.

## Changes Made
- No code changes. Diagnostic task only.

## Validation
- Read `TradeApps/breakout/fs/multi_chart.js` around `fetchData()`, `buildSteppedSeries(...)`, and `updateCharts()`.
- Inspected `_summary_net.json` strategy/product series for duplicated timestamps.
- Confirmed duplicate examples:
  - `breakout_2_tp20.0_sl50.0 | GBPEUR_C`: `2026-04-26T00:09:17.718315` -> `[1460.0, 2380.0]`, `2026-04-26T02:30:12.168981` -> `[2180.0, 3100.0]`
  - `breakout_2_tp20.0_sl50.0 | EUR`: `2026-04-26T00:58:13.339732` -> `[80.0, -25.0]`, `2026-04-26T14:02:16.019794` -> `[-395.0, -500.0]`
  - `breakout_3_tp20.0_sl50.0 | GBPEUR_C`: `2026-04-26T02:17:02.686434` -> `[2000.0, 2920.0]`

## Risks/Notes
- This analysis indicates the screenshot issue begins in the presentation layer, not necessarily in the persisted summary values themselves.
- If the business rule is “keep all same-timestamp trade events,” then `multi_chart.js` needs to collapse or sequence equal-time points before sending them to Chart.js. If the business rule is “summary series should have one point per timestamp,” then the generator layer needs to aggregate same-time events earlier.

## Completion Status
- Complete.
