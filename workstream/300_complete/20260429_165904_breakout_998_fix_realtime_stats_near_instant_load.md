# Fix Realtime Stats Near-Instant Load

Source: User request to further optimize `/realtime_stats.html` because dashboard data loading is extremely slow and must be near instant before completion approval.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary:
Identify and fix the remaining slow data-loading path for `/realtime_stats.html` so the dashboard renders from precomputed/cache data with near-instant response times. Validate load performance before requesting completion approval.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats_cache.json`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats_snapshots.json`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats_snapshot_index.json`

Destination Folder: `C:\Users\edebe\eds\TradeApps\breakout\fs`

Dependency: `C:\Users\edebe\eds\workstream\300_complete\20260429_114519_breakout_fix_realtime_stats_performance.md`

Plan:
- [x] 1. Measure current realtime stats data-path latency and identify the slow file/API path.
  - [x] Test: Run timed requests against `/api/realtime_stats` for latest and any historical/snapshot paths; inspect cache file sizes.
  - Evidence: Baseline live HTTP via `localhost` returned ~2,024-24,480 ms; `realtime_stats_snapshots.json` was ~85.49 MB; direct in-process payload assembly was ~0.3-31.7 ms, proving the slow path was request/runtime/data-path overhead rather than dashboard computation.
- [x] 2. Implement cache/data-path changes that avoid heavyweight reads or rebuilds during page load.
  - [x] Test: Code diff shows the page-load endpoint reads only lightweight precomputed data for latest dashboard state.
  - Evidence: Snapshot storage changed from rewriting the 85 MB monolithic snapshot file on every refresh to per-snapshot JSON files plus lightweight index; latest page fetch in `realtime_stats.html` now routes local API calls through `127.0.0.1` when loaded from `localhost`.
- [x] 3. Validate near-instant API response and frontend compatibility.
  - [x] Test: Timed API calls after restart should consistently return quickly from cache; `python -m py_compile trade_viewer_api.py` must pass.
  - Evidence: `python -m py_compile trade_viewer_api.py` passed. Timed `127.0.0.1` API calls: `all` avg 8.6 ms, `momentum_r` avg 10.1 ms, `momentum` avg 46.5 ms with one 319.5 ms warm sample and remaining samples 6-9 ms. CORS check from `Origin: http://localhost:5000` returned HTTP 200 with `Access-Control-Allow-Origin: http://localhost:5000`.
- [x] 4. Request user approval before marking the task complete.
  - [x] Test: User is asked to verify `/realtime_stats.html` load speed and approve or reject completion.
  - Evidence: Approval request included in final response; task remains in progress pending user verification.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: test_output
  - Artifact: Baseline: `localhost` API samples ~2.0s steady, up to 24.5s during refresh; after fix via local API route: `all` avg 8.6 ms, `momentum_r` avg 10.1 ms, `momentum` avg 46.5 ms.
  - Objective-Proved: Captures before/after response timings for realtime stats data loading.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `git -C C:\Users\edebe\eds\TradeApps\breakout\fs diff -- realtime_stats.html trade_viewer_api.py`
  - Objective-Proved: Shows the implementation changes that remove slow load behavior.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: User confirmation on 2026-04-29: "`998_fix_realtime_stats_near_instant_load` fixed!"
  - Objective-Proved: User confirms dashboard data loads near instantly.
  - Status: captured

Implementation Log:
- 2026-04-29 16:59:04 - Task created from user request.
- 2026-04-29 17:04:51 - Implemented per-snapshot JSON storage and lightweight snapshot index usage to avoid repeatedly reading/writing the 85 MB monolithic snapshot file.
- 2026-04-29 17:15:00 - Confirmed remaining fixed delay was specific to `localhost`; `127.0.0.1` API calls were sub-300 ms while `localhost` was ~2,058 ms.
- 2026-04-29 17:18:00 - Updated `realtime_stats.html` to use `127.0.0.1` for local API data fetches when the page is loaded from `localhost`.
- 2026-04-29 20:18:00 - User approved fix as complete.

Changes Made:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Added `REALTIME_STATS_SNAPSHOT_DIR`.
  - Made `_atomic_write_json` create parent folders.
  - Added per-snapshot file helpers.
  - Changed realtime stats snapshot recording to write one current snapshot file and a lightweight index, instead of loading and rewriting the full monolithic snapshot store every refresh.
  - Kept backward compatibility for old monolithic historical snapshot reads.
- `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html`
  - Added `API_ORIGIN` so data fetches use `127.0.0.1` when the page is opened at `localhost`, avoiding the observed Windows localhost delay.

Validation:
- Baseline timing before fix:
  - `momentum`: 24,480.2 ms, 9,859.4 ms, 19,987.1 ms, 9,414.3 ms, 10,814.4 ms during refresh contention.
  - Warm steady-state before final local-origin fix: ~2,024-2,357 ms via `localhost`.
- Cache/file inspection:
  - `realtime_stats_snapshots.json`: ~85.49 MB.
  - `realtime_stats_cache.json`: ~1.10 MB.
  - Direct in-process latest payload build: `momentum` 31.7 ms initially, then `momentum_r` 0.3 ms, `all` 0.8 ms.
- Technical validation:
  - `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` passed.
  - Per-snapshot record test wrote `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats_snapshots\2026-04-29T17_00_00.json` and later `2026-04-29T17_10_00.json`, each about 1.1 MB.
  - `Origin: http://localhost:5000` request to `http://127.0.0.1:5000/api/realtime_stats?strategy_group=momentum_r&product=` returned HTTP 200 and CORS allowed origin.
- After-fix timing through data URL used by the updated page:
  - `all`: min 7.7 ms, avg 8.6 ms, max 10.0 ms.
  - `momentum_r`: min 6.7 ms, avg 10.1 ms, max 26.9 ms.
  - `momentum`: min 6.0 ms, avg 46.5 ms, max 319.5 ms; excluding the first warm sample, remaining calls were 6.0-8.7 ms.

Risks/Notes:
- Completion requires user approval because the user explicitly requested validation before completion approval.
- Browser page load at `http://localhost:5000/realtime_stats.html` may still incur Windows localhost resolution delay for the initial HTML request, but dashboard data loading now bypasses that delay by using `127.0.0.1` for API fetches.
- Historical snapshot reads for old pre-existing monolithic snapshots still fall back to the large file if no per-snapshot file exists. New snapshots use the optimized per-file format.

Completion Status:
Complete - 2026-04-29 20:18:00
