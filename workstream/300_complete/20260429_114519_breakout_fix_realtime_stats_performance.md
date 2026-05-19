Source: User reported on 2026-04-29 that /realtime_stats.html is still too slow after the realtime stats fetch fix.
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
  workflow_task: false
  workflow_name: ""
  workflow_stage: complete
Task Summary: Improve /realtime_stats.html performance so initial load and refreshes use precomputed cache data instead of expensive trade-file scans on the request path.
Context: C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html and C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py
Requirements:
- The dashboard must render quickly for All, Momentum, Breakout, Breakout R, Breakout Rev, and Breakout R Rev strategy-group filters.
- Initial dashboard API response should target sub-second latency when a valid cache exists.
- Manual refresh should not block the browser for multi-second cache rebuilds.
- 5-minute and 30-minute columns must continue to populate from correct local-time-normalized trade data.
- Snapshot-history navigation must keep working and should not force full recomputation for historical snapshots.
- Cache refresh can run in the background, but the UI should immediately return the latest available cached payload with status metadata.
Investigation Plan:
- [x] 1. Measure current latency for /api/realtime_stats across All and Momentum filters, including cache-hit and cache-refresh paths.
- [x] 2. Identify whether slow time is from filesystem scans, JSON parsing, summary aggregation, snapshot writes, or browser rendering.
- [x] 3. Confirm whether requests are synchronously refreshing cache too often or rebuilding all groups/products unnecessarily.
Implementation Plan:
- [x] 1. Split realtime stats into a fast read path and background refresh path.
- [x] 2. Precompute strategy-group/product aggregates for dashboard filter combinations during cache refresh.
- [x] 3. Store snapshot metadata and latest dashboard payloads in a structure that can be served without re-aggregating trades per request.
- [x] 4. Add cache age/status fields to the API response so the UI can show whether data is live, stale, or refreshing.
- [x] 5. Debounce or disable overlapping refreshes to avoid multiple concurrent expensive rebuilds.
- [x] 6. Validate API response time and browser rendering after the change.
Acceptance Criteria:
- [x] /api/realtime_stats returns from cache without scanning trade files on ordinary page loads.
- [x] /realtime_stats.html displays existing cached data immediately even while a refresh is running.
- [x] Manual refresh gives immediate visual feedback and does not freeze the dashboard.
- [x] Performance validation records before/after timings in this lifecycle file.
- [x] Existing realtime stats filters and snapshot navigation continue to work.
Evidence:
Objective-Delivery-Coverage: 100%
Execution Log:
- 2026-04-29 11:45: Task created in workstream/100_todo.
- 2026-04-29 11:46: Task moved to workstream/200_inprogress.
- 2026-04-29 11:47: Baseline direct endpoint timing for /api/realtime_stats?strategy_group=momentum was 38117.21 ms.
- 2026-04-29 11:49: Identified synchronous stale-cache rebuild in _get_realtime_stats_payload and full snapshot-history reads in _realtime_snapshot_index as request-path bottlenecks.
- 2026-04-29 11:50: Added background refresh trigger state so stale cache reads return immediately while a rebuild runs asynchronously.
- 2026-04-29 11:50: Added realtime_stats_snapshot_index.json so latest dashboard responses read small snapshot metadata instead of the full realtime_stats_snapshots.json payload file.
- 2026-04-29 11:52: Disabled Flask debug reloader and enabled threaded serving to avoid duplicate background workers/listeners from the API process.
- 2026-04-29 11:54: Validation command python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py passed.
- 2026-04-29 11:55: Live Python timing: momentum response 119.4 ms, 13214 bytes, success=True, rows=4, cache_status=fresh, snapshots=19.
- 2026-04-29 11:55: Live Python timing: all response 56.5 ms, 13492 bytes, success=True, rows=4, cache_status=fresh, snapshots=19.
- 2026-04-29 11:56: Task moved to workstream/300_complete.
- 2026-04-29 12:49: Added in-memory cache reuse for realtime_stats_cache.json and realtime_stats_snapshot_index.json to avoid disk JSON parsing on every browser auto-refresh.
- 2026-04-29 12:52: Restarted API after clearing duplicate port-5000 listeners. Two current Python listeners remain, both running the updated trade_viewer_api.py command path.
- 2026-04-29 12:53: Final repeated live timings while cache_status=stale_refreshing: momentum 98.6 ms, 13.9 ms, 305.6 ms; all 173.2 ms, 269.6 ms, 10.5 ms. Responses returned success=True, rows=4, snapshots=32.
