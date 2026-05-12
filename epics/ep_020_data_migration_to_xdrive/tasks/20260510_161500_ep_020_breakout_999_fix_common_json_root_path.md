## Task
- Modify TradeApps/breakout/fs/common.py to use BREAKOUT_JSON_ROOT from paths.py instead of a hardcoded local 'json' directory.
- This ensures all virtual trade data is written to the drive specified in config.json (currently X:\eds).

## Task Type
- implementation

## Destination Folder
- TradeApps/breakout/fs

## Dependency
- TradeApps/breakout/fs/paths.py (Provides central path resolution)
- TradeApps/breakout/fs/config.json (Source of json_data_root)

## Plan
1. [x] Update imports in common.py to include BREAKOUT_JSON_ROOT from paths.py.
   - Test: Python compile check.
   - Evidence: Successful compilation and manual code review.
2. [x] Redefine _json_root_dir() in common.py to return BREAKOUT_JSON_ROOT.
   - Test: Log the output of _json_root_dir() during a test run.
   - Evidence: Path resolves to \\Ebell-hp\d\EDS\TradeApps\breakout\fs\json (X: drive).

## Evidence
- Objective: Align common.py with global JSON path settings.
- Delivery: common.py updated and verified.
- Coverage: Core JSON path resolution function.

## Status
- 2026-05-10 16:15: Task created and moved to in-progress.
- 2026-05-10 16:25: Implementation completed and verified with 	est_path_fix.py.
- 2026-05-10 16:28: Fixed minor SyntaxWarning in docstring.
- 2026-05-10 16:30: Task marked as complete.
