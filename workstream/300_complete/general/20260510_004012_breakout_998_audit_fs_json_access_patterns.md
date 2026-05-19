## Task

- Audit access to `TradeApps/breakout/fs/json/live/forex/2026-05-08`
- Identify which consumers read:
- directly from disk
- via API
- or both

## Task Type

- analysis

## Project

- breakout

## Destination Folder

- `workstream/200_inprogress/general`

## Dependency

- JSON data root: `C:\Users\edebe\eds\TradeApps\breakout\fs\json`
- API server: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`

## Plan

1. Identify the main live readers of the `fs/json/live/...` tree.
2. Separate direct filesystem readers from API-backed readers.
3. Note any hybrid flows where the browser hits API but the API itself reads disk.
4. Record the answer in concrete file-level terms.

## Evidence

- Task created to answer whether the target folder is accessed from disk, via API, or both.
- The target folder is accessed in all three practical ways:
- direct filesystem reads by Python/scripts
- API-backed reads through `trade_viewer_api.py`
- browser direct-path fetches of `json/...` files without using an `/api/...` endpoint

### Direct filesystem readers

- These consumers open files under the `fs/json/live/...` tree directly from disk:
- `automated_strategy_selector.py`
- `automated_strategy_picker.py`
- `grid_live_monitor.py`
- `grid_live_monitor_corrupt.py`
- `common.py`
- `analyze_buy_patterns.py`
- `analyze_top_strategies.py`
- `bidirectional_analysis.py`
- `day_profile_analyzer.py`
- `multi_date_analysis.py`
- `weighted_race.py`
- `tools/social_posting_package/generate_posting_package.py`
- `tools/data_story_engine/loader.py`

### API-backed readers

- Browser/UI clients call Flask endpoints in `trade_viewer_api.py`, and that API then reads the JSON files from disk using `_resolve_day_dir(...)` and `_iter_day_dirs_for(...)`.
- Key API endpoints include:
- `/api/dates`
- `/api/trades`
- `/api/trade_file`
- `/api/top20`
- `/api/stats_summary`
- `/api/weekly_performance`
- `/api/weekly_summary_net_30min`
- `/api/market_update`
- `/api/top10_history`
- `/api/trade_buckets`
- `/api/realtime_stats`

### Browser direct-path readers

- Some screens fetch the JSON file path directly rather than going through an API endpoint.
- Examples:
- `lead_lag_snapshots.html` fetches `json/${mode}/${type}/${date}/_summary_net.json`
- `frequency_explorer.html` constructs direct JSON file paths and fallback paths such as `_summary_net.json`

### Practical interpretation

- For `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-05-08`:
- Python automation reads it directly from disk.
- Several UI pages reach it indirectly through the Flask API.
- Some UI pages also request the JSON file path directly from the web server.
- So the correct classification is `both`, with a further split between:
- `via API`
- `direct file-path fetch from browser`

## Validation

- `rg -n "_summary_net|_top20|_trades_summary|api/trades|api/dates|api/stats|api/weekly|api/realtime" TradeApps/breakout/fs`
- `rg -n "@app.route\\(|_resolve_day_dir|_iter_day_dirs_for|BASE_PATH =" TradeApps/breakout/fs/trade_viewer_api.py`
- Static audit only

## Completion Status

- Complete
