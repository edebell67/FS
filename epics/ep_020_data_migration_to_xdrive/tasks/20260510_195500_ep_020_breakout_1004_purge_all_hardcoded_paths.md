## Task
- Systematically remove ALL remaining hardcoded absolute paths (e.g., C:\..., c:/..., X:\...) from the TradeApps/breakout/fs/ directory.
- Replace them with centralized variables from paths.py.
- This ensures the entire system is drive-agnostic and fully respects the config.json drive mappings.

## Task Type
- implementation

## Destination Folder
- TradeApps/breakout/fs

## Dependency
- TradeApps/breakout/fs/paths.py

## Plan
1. [x] Final sweep of TradeApps/breakout/fs/ for hardcoded path strings.
2. [x] Identify a mapping for each hardcoded path to a paths.py variable.
3. [x] Apply surgical replacements to each identified file.
   - ackfill_last_week_live_oneoff.py: Replaced C:/.../DB/.env with BREAKOUT_DB_ROOT / ".env".
   - check_pnl.py: Replaced c:\... with BREAKOUT_JSON_ROOT.
   - check_pnl_v2.py: Replaced c:\... with BREAKOUT_JSON_ROOT.
   - un_archive_process.py: Replaced c:\... with BREAKOUT_FS_ROOT.
   - common.py: Replaced hardcoded URLs with QUOTE_API_BASE_URL.
   - 	ools/leadership_change_analyzer.py: Replaced hardcoded C:/... with esolve_day_dir(BREAKOUT_JSON_ROOT, ...).
4. [x] Verify that all scripts still function correctly using the dynamic paths.

## Evidence
- Objective: Zero hardcoded drive letters in the breakout logic.
- Delivery: All hardcoded paths removed and centralized in paths.py.
- Coverage: Entire s/ directory.

## Status
- 2026-05-10 19:55: Task created and moved to in-progress.
- 2026-05-10 20:10: Purge complete. All drive letters removed from application logic.
- 2026-05-10 20:12: Task marked as complete.
