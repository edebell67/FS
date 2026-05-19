Source: User request to review the Breakout multi-chart screen after cards appeared blank while drilldown still showed underlying trades.
Task Summary: Review the likely cause of intermittent blank chart cards in TradeApps/breakout/fs multi-chart, capture evidence, and document suggested fixes for future recurrence. No code changes requested.
Context: TradeApps/breakout/fs/multi_chart.js; TradeApps/breakout/fs/multi_chart.html; TradeApps/breakout/fs/json/live/*/_summary_net.json; TradeApps/breakout/fs/grid_live.json
Plan:
- [x] 1. Inspect the multi-chart data fetch, card creation, and chart render pipeline.
  - [x] Test: Capture the functions responsible for creating cards/canvases and rendering Chart.js datasets.
  - [x] Evidence: Confirmed fetchData(), updateCharts(), renderChartOnCanvas(), and showTradeDrilldown() as the relevant pipeline in multi_chart.js.
- [x] 2. Identify the most likely blank-card failure mode from the live data and render logic.
  - [x] Test: Compare chart-series lookup path against drilldown trade lookup path and inspect a representative _summary_net.json payload.
  - [x] Evidence: Representative _summary_net.json contained `"strategies": {}` while chart cards still depend on activeOverlays from /api/grid_live and drilldown loads trades from /api/trades.
- [x] 3. Record suggested fixes and archive the review for future reference.
  - [x] Test: Lifecycle file includes findings, evidence, suggested fixes, and validation commands/results.
  - [x] Evidence: Review notes completed below; no code changes made.
Implementation Log:
- 2026-03-12 02:35:01 Created investigation task for multi-chart blank-card diagnosis.
- 2026-03-12 02:49:00 Reviewed the chart render path and confirmed cards are built from activeOverlays while plotted series come from processedSeries loaded from _summary_net.json.
- 2026-03-12 02:52:00 Reviewed drilldown logic and confirmed it fetches trades independently from /api/trades, which explains why drilldown can still work while cards are blank.
- 2026-03-12 02:55:00 Inspected a representative live _summary_net.json payload and found an empty strategies object, consistent with blank cards caused by transient missing chart series rather than a permanent canvas/CSS failure.
Changes Made:
- No product code changes.
- Lifecycle review updated and prepared for archive as a completed reference item.
Validation:
- [x] `Select-String` review of multi_chart.js confirmed:
  - fetchData() loads `/api/trade_file?..._summary_net.json` and `/api/grid_live`
  - updateCharts() renders cards from `activeOverlays` but datasets from `processedSeries[lookupKey]`
  - showTradeDrilldown() loads `/api/trades` independently of chart series rendering
- [x] `Get-Content` review of `TradeApps/breakout/fs/json/live/2026-01-24/_summary_net.json` showed:
  - `{"last_update":"2026-01-24T17:15:04.556983","strategies":{}}`
  - This is sufficient to produce blank cards if overlays exist but no plotted series are present.
- [x] User confirmed the screen later started working again, which is consistent with a transient datasource/state issue.
Risks/Notes:
- Most likely root cause: transient empty/stale `_summary_net.json` data or temporary mismatch between overlay keys and available processed series. Cards are still created because `/api/grid_live` can populate activeOverlays even when chart-series data is missing.
- Why drilldown still worked: drilldown does not depend on `_summary_net.json`; it separately fetches `/api/trades` and matches by model/product/time, so it can show trades even when plotted series are unavailable.
- Suggested future fix 1: add a guard in updateCharts/renderGroupCharts so cards with zero matched series show a clear "No chart data available" state instead of a blank canvas.
- Suggested future fix 2: log and surface a warning when `activeOverlays` exists but `processedSeries` is empty or a group resolves to zero datasets.
- Suggested future fix 3: normalize overlay keys in one shared helper instead of ad hoc `replace(' | ', '|')` so temporary formatting differences cannot suppress chart rendering.
- Suggested future fix 4: optionally trigger one automatic retry when `_summary_net.json` returns an empty `strategies` object but `/api/grid_live` still reports active groups.
Completion Status: Complete review archived on 2026-03-12 02:56:00
