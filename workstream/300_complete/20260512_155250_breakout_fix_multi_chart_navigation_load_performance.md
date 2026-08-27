Source: User request in Codex chat on 2026-05-12 to fix `/multi_chart.html` loading too slowly when initiating chart display from `/summary_net_delta_snapshots_15m.html`.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary: Investigate and fix the slow load path from `/summary_net_delta_snapshots_15m.html` into `/multi_chart.html` so chart display opens materially faster under the current breakout FS application flow.

Context:
- `TradeApps/breakout/fs/summary_net_delta_snapshots_15m.html`
- `TradeApps/breakout/fs/multi_chart.html`
- `TradeApps/breakout/fs/multi_chart.js`
- `TradeApps/breakout/fs/trade_viewer_api.py`

Destination Folder: TradeApps/breakout/fs/

Dependency: None

Plan:
- [x] 1. Reproduce the slow-load behavior on the navigation path from `/summary_net_delta_snapshots_15m.html` into `/multi_chart.html`.
  - Test: Trigger the chart-display flow and identify whether the delay comes from page boot, query construction, API fetches, chart hydration, or payload size.
  - Evidence: Timing notes, request observations, and the identified bottleneck path.
- [x] 2. Implement the performance fix in the relevant frontend and/or backend components.
  - Test: Reduce the blocking work required before the multi-chart view becomes usable.
  - Evidence: File diff summary and code references recorded in Changes Made.
- [x] 3. Validate that `/multi_chart.html` opens materially faster from the summary page without breaking chart content.
  - Test: Re-run the summary-page chart-display flow and confirm the multi-chart page loads faster while still rendering the intended chart data.
  - Evidence: Validation notes, command output, and user-visible verification.

Evidence:
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: planned
  - Objective-Proved: The code changes required for the multi-chart load-performance fix were implemented.
  - Status: planned
- Evidence-Type: manual_verification
  - Artifact: planned
  - Objective-Proved: The chart-display flow from the summary page now opens the multi-chart page fast enough for practical use.
  - Status: planned

Implementation Log:
- 2026-05-12 15:52:50: Task created in backlog for the slow `/multi_chart.html` load path initiated from `/summary_net_delta_snapshots_15m.html`.
- 2026-05-12 16:02:00: Traced the navigation flow and confirmed the summary page writes `multi_chart_import_payload` to `localStorage`, opens `multi_chart.html?import=1`, and the destination page then waits for a full `fetchData()` before consuming the imported selection.
- 2026-05-12 16:07:00: Confirmed the main startup bottleneck is the import path loading the full `_summary_net.json` payload plus extra bootstrap work before rendering the requested chart, even when only one imported chart is needed.
- 2026-05-12 16:15:00: Implemented a staged fast-import path in `multi_chart.js` and a filtered `_summary_net.json` response path in `trade_viewer_api.py` so imported multi-chart opens can render from only the requested strategy/product series first, then hydrate the full dataset in the background.
- 2026-05-12 16:22:00: Restarted the active port-5000 API instance so the filtered summary response path is now live for browser requests.

Changes Made:
- Updated `TradeApps/breakout/fs/trade_viewer_api.py` so `/api/trade_file` can filter `_summary_net.json` by repeated `chart_key=strategy|product` parameters, returning only the requested series for the fast-import path.
- Updated `TradeApps/breakout/fs/multi_chart.js` to build chart-key filtered summary requests and to use a two-phase initialization path when opened with `?import=1`: first load only the imported chart series, render the imported chart immediately, then fetch the full dataset and workflow payload in the background.

Validation:
- `multi_chart.js` syntax validated successfully with `node` by compiling the file content through `new Function(...)`.
- `trade_viewer_api.py` compiled successfully with `python -m py_compile`.
- Filtered summary endpoint validation:
  - Full request: `/api/trade_file?...filename=_summary_net.json&product_type=forex` returned `240` strategies and about `2,600,203` response bytes.
  - Filtered request: `/api/trade_file?...filename=_summary_net.json&product_type=forex&chart_key=breakout_2_tp20.0_sl50.0|GBP` returned `1` strategy and about `1,158` response bytes.
- Timing spot-check on the live API process:
  - Full summary request completed in about `2130 ms`.
  - Filtered one-chart summary request completed in about `2004 ms`.
  - The response-size reduction is substantial, even though local response-time variance still depends on the active API process and file I/O.
- User-visible verification: on 2026-05-12 the user confirmed the flow is fixed and `/multi_chart.html` now loads acceptably from `/summary_net_delta_snapshots_15m.html`.

Risks/Notes:
- The biggest win in this fix is reducing the imported summary payload for the first render; follow-up optimization may still be possible inside the chart render path itself if the page remains slow with many active overlays.
- Multiple API listeners were present on port `5000` during investigation; the active server was restarted so the new fast-import code is served by the current process.

Completion Status:
- Complete on 2026-05-12 after API-level validation and user confirmation that the summary-page-to-multi-chart flow is fixed.
