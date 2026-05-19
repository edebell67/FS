## Task

- Centralize breakout `fs` path and URL definitions in `config.json`
- Allow users to choose their own generated-data location without editing code

## Task Type

- implementation

## Project

- breakout

## Destination Folder

- `workstream/200_inprogress/general`

## Dependency

- `TradeApps/breakout/fs/config.json`
- `TradeApps/breakout/fs/paths.py`

## Plan

1. Add a minimal config schema for generated-data root and core service URLs.
2. Update `paths.py` to resolve from `config.json` first, then fall back safely.
3. Update key active consumers that currently hardcode localhost URLs to use the config values.
4. Validate path and URL resolution under default and overridden settings.

## Evidence

- Task opened to move path/url ownership into `config.json`.
- Added config-backed central definitions in [config.json](<C:/Users/edebe/eds/TradeApps/breakout/fs/config.json>):
- `path_settings.generated_data_root`
- `service_urls.breakout_api_base`
- `service_urls.quote_api_base`
- Updated [paths.py](<C:/Users/edebe/eds/TradeApps/breakout/fs/paths.py>) to resolve:
- generated-data root from `config.json` first, then environment fallback
- breakout API base URLs from `config.json`
- quote API base URL from `config.json`
- Updated active consumers to use config-backed values:
- `market_update_generator.py`
- `run_twitter_canonical_workflow.py`
- `run_twitter_consolidated_leaderboard_workflow.py`
- `run_twitter_top5_multi_product_workflow.py`
- `run_twitter_consolidated_every4h.bat`
- `run_daily_top3_post.bat`
- Existing path centralization remains in place through `paths.py`, so users can now change generated-data location through `config.json` without editing code.
- Note: some secondary or legacy live files still carry hardcoded localhost URLs and would need a second URL-cleanup pass for full repo-wide centralization.

## Validation

- `python -m py_compile TradeApps/breakout/fs/paths.py TradeApps/breakout/fs/market_update_generator.py TradeApps/breakout/fs/run_twitter_canonical_workflow.py TradeApps/breakout/fs/run_twitter_consolidated_leaderboard_workflow.py TradeApps/breakout/fs/run_twitter_top5_multi_product_workflow.py`
- Python import check confirmed:
- `generated_data_root_cfg=C:\Users\edebe\eds`
- `BREAKOUT_API_BASE_URL=http://127.0.0.1:5000`
- `BREAKOUT_API_HEALTH_URL=http://127.0.0.1:5000/api/health`
- `BREAKOUT_X_API_POST_URL=http://127.0.0.1:5000/api/social/x_api_post`
- `BREAKOUT_X_API_THREAD_POST_URL=http://127.0.0.1:5000/api/social/x_api_thread_post`
- Consumer import checks confirmed the active workflow modules now resolve API URLs from the central config-backed layer.
- Targeted `rg` on the updated workflow files shows no remaining hardcoded `localhost:5000` or `127.0.0.1:5000` references except the fallback literal embedded in the `run_daily_top3_post.bat` config-reader command.

## Completion Status

- Complete
