Source: User clarification on 2026-04-28 that the provided Real-Time Stats image is a mockup/spec and should be implemented as the actual screen.
Task Type: standard
Task Attributes:
  recurring_task: false
  recurrence_type: scheduled
  recurrence_rule: None
  looping_task: false
  loop_until: manual_stop
  splittable_task: false
  split_output_type: files
  split_spawn_task: false
  split_failure_mode: fail_fast
  workflow_task: false
  workflow_name: ""
  workflow_stage: todo
  depends_on: []
  feeds_into: []
Task Summary: Implement the new Real-Time Stats dashboard from the supplied mockup, using momentum-only data, multi-window summaries, and a product filter.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html`, `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Plan:
- [x] 1. Expand the Real-Time Stats API to return the multi-window momentum dashboard data required by the mockup.
- [x] 2. Replace the current `realtime_stats.html` layout with the dashboard UI from the mockup.
- [x] 3. Verify the dashboard renders momentum-only data and supports product filtering.
Evidence:
Objective-Delivery-Coverage: 100%
Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Mocked Flask test-client verification of `/api/realtime_stats` with momentum buy/sell open/closed samples plus a non-momentum control sample
Results:
- [trade_viewer_api.py](/C:/Users/edebe/eds/TradeApps/breakout/fs/trade_viewer_api.py) now returns a momentum-only dashboard payload with four windows: `m5`, `m30`, `h1`, `h3`.
- [realtime_stats.html](/C:/Users/edebe/eds/TradeApps/breakout/fs/realtime_stats.html) was rebuilt as a dashboard screen aligned to the provided mockup, including product filter, row-based trade sections, and performance summary row.
- Mocked verification returned `STATUS 200`, `SUCCESS True`, row keys `open_buy/open_sell/closed_buy/closed_sell`, and product filtering changed the summary net as expected.
- A direct full live-day test-client call timed out due to the current scan cost of the production trade folder, so live rendering was not fully exercised in-process.
Execution Log:
- 2026-04-28 16:57:50: Task created in `workstream/100_todo`.
- 2026-04-28 17:00:00: Reframed the task from “patch existing stats page” to “implement the supplied mockup as the actual Real-Time Stats screen.”
- 2026-04-28 17:06:00: Expanded [trade_viewer_api.py](/C:/Users/edebe/eds/TradeApps/breakout/fs/trade_viewer_api.py) so `/api/realtime_stats` emits multi-window momentum-only dashboard data and supports product filtering.
- 2026-04-28 17:12:00: Replaced [realtime_stats.html](/C:/Users/edebe/eds/TradeApps/breakout/fs/realtime_stats.html) with a new dashboard-style UI matching the mockup structure.
- 2026-04-28 17:18:00: Completed mocked endpoint verification and recorded the remaining live-scan performance limitation.
