## Task
- Standardize root path references in TradeApps/breakout/fs/trade_viewer_api.py to distinguish between **Source Code** and **Data Storage**.
- This ensures all dashboards (Delta Snapshots, Lead Lag, Real-Time Stats, etc.) can be redirected to the X: drive by changing a single variable in config.json.
- Grouping logic:
  - SOURCE_ROOT: Points to BREAKOUT_FS_ROOT (for .html, .js, .css).
  - DATA_ROOT: Points to BREAKOUT_DATA_FS_ROOT (for grid_live.json, ctivations.json, ealtime_stats_cache.json).
  - JSON_STATIC_ROOT: Points to BREAKOUT_JSON_ROOT (for daily trade JSON data).

## Task Type
- implementation

## Destination Folder
- TradeApps/breakout/fs

## Dependency
- TradeApps/breakout/fs/paths.py (Already provides the necessary variables)

## Plan
1. [x] Define SOURCE_ROOT, DATA_ROOT, and JSON_STATIC_ROOT at the top of 	rade_viewer_api.py.
2. [x] Replace all ROOT_PATH references used for **Data** with DATA_ROOT.
3. [x] Replace all ROOT_PATH references used for **Serving Static Files** with SOURCE_ROOT.
4. [x] Update config.json to set generated_data_root to X:\eds.
5. [x] Verify that all menu-accessible pages load correctly.
6. [x] Verify that Real-Time Stats and Delta Snapshots are reading from the intended root.

## Evidence
- Objective: Decouple source code from data storage for multi-drive migration.
- Delivery: 	rade_viewer_api.py updated and config.json flipped to X:.
- Coverage: All API endpoints and static file routes.

## Status
- 2026-05-10 17:15: Task created and moved to in-progress.
- 2026-05-10 17:30: Refactoring of 	rade_viewer_api.py completed.
- 2026-05-10 17:31: config.json updated to point generated_data_root to X:\eds.
- 2026-05-10 19:15: Verification complete. All dashboards correctly accessing X: drive data while UI remains on C:.
