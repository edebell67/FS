# Source
- User request on 2026-02-28: create DB version of FS pre-launch batch workflow.

# Task Summary
Create a DB startup batch script that can be run before opening main screen.

# Context
- Existing launcher patterns in `start_all_trading_apps.bat`
- DB UI/API located in `TradeApps/breakout/DB`

# Implementation Log
- 2026-02-28 16:36:10: Task created and moved to in-progress.
- 2026-02-28 16:38: Added new launcher `start_breakout_db_services.bat` at repo root.

# Changes Made
- Added `start_breakout_db_services.bat`
  - Starts `trade_viewer_api.py` from `TradeApps/breakout/DB` (port 5051 default).
  - Optionally starts `live_01_restart_DB_Trade.bat` from `C:\Users\edebe\OneDrive\Desktop\batch files` if present.
  - Optionally starts `verify_algo_execution_and_restart.bat` from same folder if present.
  - Prints main screen URL: `http://127.0.0.1:5051/strategy_performance.html`.

# Validation
- Command: `Get-Content start_breakout_db_services.bat`
- Result: script content verified with expected paths/commands and conditional checks.

# Risks/Notes
- External helper batch files are optional and guarded by `if exist`; launcher remains usable without them.

# Completion Status
- Complete (2026-02-28 16:39)
