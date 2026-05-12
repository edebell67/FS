## Task
- Perform a final alignment of state file paths in Python scripts to ensure absolute drive letters and hardcoded relative JSON paths are replaced with dynamic variables.
- This ensures all .json state files and trade transaction files correctly target the X: drive workspace.

## Task Type
- implementation

## Destination Folder
- TradeApps/breakout/fs

## Dependency
- TradeApps/breakout/fs/paths.py

## Plan
1. [x] Update 
arrative_generator.py:
   - Replaced BASE_DIR = Path(__file__).parent with BASE_DIR = BREAKOUT_DATA_FS_ROOT.
   - **HOTFIX**: Restored missing dd_narrative_routes and other API-related methods accidentally removed during refactoring.
2. [x] Update ackfill_trades.py:
   - Replaced ROOT_FS_DIR = BREAKOUT_FS_ROOT with ROOT_FS_DIR = BREAKOUT_DATA_FS_ROOT.
3. [x] Update common.py:
   - Replaced all remaining os.path.dirname(CONFIG_FILE_PATH) / 'json' hardcodes with BREAKOUT_JSON_ROOT.
   - Updated ACTIVATIONS_FILE, GRID_LIVE_FILE_PATH, GLOBAL_ACTIVE_TRADES_FILE, and lock files to use BREAKOUT_DATA_FS_ROOT.
   - Updated TWS_ORDER_TEMPLATES_PATH to use BREAKOUT_DATA_FS_ROOT.
4. [x] Replaced hardcoded .env path in ackfill_last_week_live_oneoff.py.
5. [x] Standardized check_pnl.py and check_pnl_v2.py.

## Evidence
- Objective: Total decoupling of state and trade data from local source directory.
- Delivery: All state-managing scripts verified as using centralized variables.
- Coverage: Narrative generation, backfilling, trade execution, and status checking.

## Status
- 2026-05-10 21:00: Task created.
- 2026-05-10 21:30: Final sweep and alignment completed.
- 2026-05-10 21:40: Fixed leftover os.path.dirname(CONFIG_FILE_PATH) hardcodes in common.py that were causing some bots to still write to C:.
- 2026-05-10 21:45: Verified all processes now writing to X:\eds\TradeApps\breakout\fs\json\live\forex\2026-05-11.
- 2026-05-11 02:20: **HOTFIX** applied to 
arrative_generator.py to restore API routes after reported ImportError.
- 2026-05-11 02:25: Verified API server back online and serving narratives from the X: drive.
- 2026-05-11 02:30: Task marked as complete.
