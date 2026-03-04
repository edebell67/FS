# Source
- User request on 2026-02-28: all DB-support files should be located in \DB.

# Task Summary
Create DB-only launcher and support scripts inside `TradeApps/breakout/DB`.

# Context
- Existing launcher was at repo root and referenced external OneDrive batch files.

# Implementation Log
- 2026-02-28 16:44:31: Task created.
- 2026-02-28 16:46: Added DB-local launcher in `TradeApps/breakout/DB`.
- 2026-02-28 16:46: Added DB-local restart helper batch in `TradeApps/breakout/DB`.

# Changes Made
- Added `TradeApps/breakout/DB/start_breakout_db_services.bat`
  - Starts DB API (`trade_viewer_api.py`)
  - Starts DB-local restart helper (`live_01_restart_DB_Trade_db.bat`)
  - Starts DB watchdog (`verify_algo_execution_and_restart_02.py`)
  - No dependency on OneDrive batch folder.
- Added `TradeApps/breakout/DB/live_01_restart_DB_Trade_db.bat`
  - Runs `python live_scheduler.py` from DB folder.

# Validation
- `Get-Content TradeApps/breakout/DB/start_breakout_db_services.bat`
- `Get-Content TradeApps/breakout/DB/live_01_restart_DB_Trade_db.bat`
- Result: Both scripts present and DB-local path references verified.

# Risks/Notes
- Existing root-level launcher remains in repo; use DB-local launcher path for DB-only workflow.

# Completion Status
- Complete (2026-02-28 16:47)
