# Task: Fix and Optimize Trade File Refresh Logic
# Date: 2026-05-13 13:20
# Version: V20260513_1320

## Task Type
Bug Fix / Optimization

## Destination Folder
TradeApps/breakout/fs

## Dependency
None

## Plan
1. Refactor `_update_open_trade_json_prices` in `TradeApps/breakout/fs/common.py` [V20260513_1320]:
    - Group products by their resolved day directory to minimize redundant disk scanning.
    - Use more specific glob pattern (`*_op.json`) to target only open trades and ignore closed/archived ones.
    - Add explicit `exists()` check before loading to prevent `FileNotFoundError` warnings during concurrent file moves (archiving).
2. Update `VERSION` in `TradeApps/breakout/fs/constants.py` to `V20260513_1320`.
3. Verify the changes by running a manual refresh cycle if possible, or checking code correctness.

## Evidence Inventory
- Objective: Eliminate "Failed to refresh open trade file" warnings.
- Delivery: Refactored logic in `common.py`.
- Coverage: Fixes the reported race conditions and improves performance.
- Auto-Acceptance: Warning logs should cease once deployed.

## Log
- 2026-05-13 13:20: Task started. Identified root cause in `_update_open_trade_json_prices`.
- 2026-05-13 13:25: Refactored `_update_open_trade_json_prices` to use grouped directory scanning and `*_op.json` glob pattern.
- 2026-05-13 13:27: Updated version to `V20260513_1320` in `constants.py`.
- 2026-05-13 13:30: Verified changes in `common.py`. Task completed.
