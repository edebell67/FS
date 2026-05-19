## Task
- Create a preventative architecture-level fix for recurring empty dashboard/table pages caused by page-specific startup races and inconsistent config/data-root initialization.
- Capture and implement the shared bootstrap/data-health approach discussed on 2026-05-13.

## Task Type
- new feature / fix-followup

## Destination Folder
- workstream/300_complete

## Dependency
- TradeApps/breakout/fs/trade_viewer_api.py
- TradeApps/breakout/fs/strategy_performance.html
- TradeApps/breakout/fs/live_trades.html
- TradeApps/breakout/fs/dashboard_bootstrap.js
- TradeApps/breakout/fs/paths.py
- X:\eds workspace availability

## Plan
1. [x] Inspect existing dashboard pages for repeated `/api/config` + data fetch startup patterns.
   - Test: Searched frontend files for `/api/config`, `loadStats()`, `product_type`, `runMode`.
   - Evidence: `strategy_performance.html` and `live_trades.html` both had config/data startup race patterns; broader dashboard pages also use duplicated page-local startup logic.
2. [x] Add shared `dashboard_bootstrap.js` helper.
   - Test: `node --check TradeApps/breakout/fs/dashboard_bootstrap.js`.
   - Evidence: helper exposes config-first context initialization, product type/mode/date resolution, and standard diagnostics.
3. [x] Add backend `/api/data_health` diagnostic endpoint.
   - Test: Windows HTTP request returned JSON diagnostics after API restart.
   - Evidence: `/api/data_health?mode=live&date=2026-05-12&product_type=forex` returned HTTP 200 JSON with X:\eds roots and summary/top20 existence.
4. [x] Migrate `strategy_performance.html` to use the helper as first consumer.
   - Test: served page loads; inline JS syntax passes.
   - Evidence: page source includes `dashboard_bootstrap.js`; startup uses `DashboardBootstrap.bootstrapDashboardPage()` before `loadStats()`.
5. [x] Migrate another obvious affected page.
   - Test: served `live_trades.html`; inline JS syntax passes.
   - Evidence: `live_trades.html` now uses the shared bootstrap before first `loadLiveTrades()` call.

## Evidence
- Objective: Prevent recurring all-pages empty data failures when config/data root/product type initialization is not ready.
- Delivery: Shared dashboard bootstrap helper + backend data health endpoint + initial migrations for `strategy_performance.html` and `live_trades.html`.
- Coverage: Core dashboard startup path, X:\eds path diagnostics, standard failure message foundation.
- Auto-Acceptance:
  - `/api/data_health` returns HTTP 200 JSON with root/path diagnostics.
  - Shared JS helper passes syntax check.
  - `strategy_performance.html` no longer owns a bespoke config-before-stats race fix; it uses the shared bootstrap contract.
  - `live_trades.html` no longer starts config and first data fetch in parallel.
  - Existing `/api/stats_summary` still returns populated data.

## Implementation Log
- 2026-05-13 11:43: Task created and moved to in-progress.
- 2026-05-13: Added `dashboard_bootstrap.js` with shared `DashboardBootstrap.bootstrapDashboardPage()` contract.
- 2026-05-13: Added `/api/data_health` to `trade_viewer_api.py` for root/data diagnostics.
- 2026-05-13: Migrated `strategy_performance.html` to shared bootstrap before `loadStats()`.
- 2026-05-13: Migrated `live_trades.html` to shared bootstrap before `loadLiveTrades()`.
- 2026-05-13: Restarted Windows-host Breakout API so `/api/data_health` route was active.

## Changes Made
- `TradeApps/breakout/fs/dashboard_bootstrap.js`
  - New shared helper for config-first dashboard startup.
  - Resolves config, product type, run mode, date, and standard error banner.
- `TradeApps/breakout/fs/trade_viewer_api.py`
  - Added `/api/data_health` route returning source/data/json roots, existence flags, and summary/top20 file checks.
- `TradeApps/breakout/fs/strategy_performance.html`
  - Includes `dashboard_bootstrap.js`.
  - Calls shared bootstrap before first `loadStats()`.
- `TradeApps/breakout/fs/live_trades.html`
  - Includes `dashboard_bootstrap.js`.
  - Calls shared bootstrap before first `loadLiveTrades()`.
- `TradeApps/breakout/fs/paths.py`
  - Previous related hardening remains in place to avoid WSL treating `X:\eds`/`x:\eds` as accidental local relative directories.

## Validation
- Syntax:
  - `/usr/bin/python3 -m py_compile TradeApps/breakout/fs/trade_viewer_api.py TradeApps/breakout/fs/paths.py` passed.
  - `node --check TradeApps/breakout/fs/dashboard_bootstrap.js` passed.
  - Extracted inline JS from `strategy_performance.html`; `node --check` passed.
  - Extracted inline JS from `live_trades.html`; `node --check` passed.
- Local Flask test client:
  - `/api/data_health?mode=live&date=2026-05-12&product_type=forex` returned HTTP 200.
  - `/dashboard_bootstrap.js` returned HTTP 200 text/javascript.
- Windows-host API after restart:
  - `/api/data_health?mode=live&date=2026-05-12&product_type=forex` returned HTTP 200 `application/json`.
  - Data health reported summary exists true, top20 exists true, summary size 5,316,222 bytes.
  - `/api/stats_summary?mode=live&date=2026-05-12&product_type=forex&limit=3&view=top&sort_key=total_net&sort_dir=desc&include_dist=false` returned HTTP 200.
  - `/strategy_performance.html` returned HTTP 200.
  - `/live_trades.html` returned HTTP 200.

## Risks/Notes
- This is an incremental preventative fix: shared helper + first two migrations. Other pages that own bespoke startup logic should be migrated when touched.
- Avoid changing trade logic, strategy selection, trade sizing, or buy/sell decision rules.
- If running under WSL, Windows mapped drive X: may not be visible as `/mnt/x`; Windows-host API should still use `X:\eds`.

## Completion Status
- Complete.
