## Task
- Expose path_settings (generated_data_root and json_data_root) in the Configuration UI of 	rade_viewer.html.
- This allows easy monitoring and potential updating of the data drive mappings directly from the browser.

## Task Type
- implementation

## Destination Folder
- TradeApps/breakout/fs

## Dependency
- TradeApps/breakout/fs/trade_viewer.html
- TradeApps/breakout/fs/config.json

## Plan
1. [x] Update enderConfigForm in 	rade_viewer.html:
   - Add a new section "📁 Path Settings".
   - Include fields for path_settings.generated_data_root and path_settings.json_data_root.
2. [x] Verify that the fields correctly load values from config.json.
3. [x] Verify that saving from the UI correctly updates the config.json file on disk.

## Evidence
- Objective: Make drive migration settings visible/editable in the dashboard.
- Delivery: Config UI updated with Path Settings.
- Coverage: Main system configuration dashboard.

## Status
- 2026-05-10 20:15: Task created and moved to in-progress.
- 2026-05-10 20:25: UI implementation completed. Verified that it correctly reads/writes nested path_settings from/to config.json.
- 2026-05-10 20:27: Task marked as complete.
