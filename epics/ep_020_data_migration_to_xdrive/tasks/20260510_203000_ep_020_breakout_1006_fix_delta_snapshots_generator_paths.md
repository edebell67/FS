## Task
- Update generator and analysis scripts to use BREAKOUT_JSON_ROOT from paths.py.
- Targeted files:
  - summary_net_delta_snapshots_15m_generator.py
  - summary_net_lead_lag_analysis.py
- This ensures these background processes and analytical tools correctly target the X: drive.

## Task Type
- implementation

## Destination Folder
- TradeApps/breakout/fs

## Dependency
- TradeApps/breakout/fs/paths.py

## Plan
1. [x] Update summary_net_delta_snapshots_15m_generator.py to use BREAKOUT_JSON_ROOT.
2. [x] Update summary_net_lead_lag_analysis.py to use BREAKOUT_JSON_ROOT and remove redundant 'json/' path fragments.
3. [x] Verify that scripts resolve paths to the X: drive.

## Evidence
- Objective: Standardize remaining background script paths for multi-drive migration.
- Delivery: Generator and analysis scripts updated.
- Coverage: Historical delta snapshots and lead-lag analysis.

## Status
- 2026-05-10 20:30: Task created and moved to in-progress.
- 2026-05-10 20:45: Implementation completed and verified.
- 2026-05-10 20:50: Task marked as complete.
