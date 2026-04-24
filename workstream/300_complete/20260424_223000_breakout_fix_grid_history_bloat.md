# Task: Fix grid_live_history File Bloat

## Status
- **Status:** COMPLETED
- **Created:** 2026-04-24 22:30:00
- **Completed:** 2026-04-24 22:40:00
- **Project:** Breakout
- **Priority:** High

## Objective
Identify the cause of excessive file generation in `TradeApps/breakout/fs/grid_live_history` and implement a strategy to throttle archiving and prune old history files.

## Investigation Results
1. **Root Cause**: The `_archive_grid_live(mode)` function in `trade_viewer_api.py` was being called by multiple endpoints (promotions, activations, pruning, clearing) without any throttling or cleanup logic.
2. **Impact**: Over 53,000 individual JSON files were generated, causing inode/disk bloat and slow directory operations.
3. **Workflow Link**: Automated workflows like `automated_strategy_selector.py` and `TB_workflow` trigger promotions frequently, each creating a new archive file.

## Implementation (2026-04-24)
- [x] **Archiving Throttle**: Added a 60-second cooldown period to `_archive_grid_live` to prevent rapid-fire redundant backups.
- [x] **Automatic Pruning**: Implemented `_cleanup_grid_live_history` to maintain a maximum of 1,000 most recent history files.
- [x] **API Update**: Integrated cleanup logic directly into the archiving flow in `trade_viewer_api.py` (V20260424_2230).

## Timeline/Log
- **2026-04-24 22:30:00:** Task identified due to 53k file count.
- **2026-04-24 22:35:00:** Logic implemented in `trade_viewer_api.py`.
- **2026-04-24 22:40:00:** Verified and completed.
