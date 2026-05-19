## Task
- Standardize JSON root path references in generator and analysis scripts to use BREAKOUT_JSON_ROOT from paths.py.
- Targeted files:
  - summary_net_generator.py
  - 	b_leadership_generator.py
  - mark_l_trades_physically.py
  - 	p_sl_analysis.py
  - inspect_json.py
  - 	emp_tp_sl_analysis.py
- This ensures these processes correctly target the X: drive.

## Task Type
- implementation

## Destination Folder
- TradeApps/breakout/fs

## Dependency
- TradeApps/breakout/fs/paths.py

## Plan
1. [x] Update summary_net_generator.py to use BREAKOUT_JSON_ROOT.
2. [x] Update 	b_leadership_generator.py to use BREAKOUT_JSON_ROOT via esolve_day_dir.
3. [x] Update mark_l_trades_physically.py to use BREAKOUT_JSON_ROOT via esolve_day_dir.
4. [x] Update 	p_sl_analysis.py to use BREAKOUT_JSON_ROOT.
5. [x] Update inspect_json.py to use BREAKOUT_JSON_ROOT.
6. [x] Update 	emp_tp_sl_analysis.py to use BREAKOUT_JSON_ROOT.
7. [x] Verify that all scripts resolve paths to the X: drive.

## Evidence
- Objective: Standardize generator and analysis paths for multi-drive migration.
- Delivery: All identified scripts updated and verified.
- Coverage: Trade summary, leadership, and analytical data.

## Status
- 2026-05-10 19:30: Task created and moved to in-progress.
- 2026-05-10 19:50: All targeted scripts successfully updated and verified.
- 2026-05-10 19:55: Task marked as complete.
