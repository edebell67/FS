# Task: Modify Health Check Trade Folder Path
Created: 2026-03-16 01:48:30
Project: breakout
Status: COMPLETED

## 1. Understanding of Requirements
The System Health Monitor currently checks `.../fs/json/live/{YYYY-MM-DD}` for trade files.
The user wants to update this to check `.../fs/json/live/forex/{YYYY-MM-DD}`.
This likely applies to both 'live' and 'sim' modes, where the product type ('forex') is a subfolder between the mode and the date.

## 2. Plan of Approach
1. **Identify Target**: `_get_health_status` function in `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`.
2. **Modify Path Logic**: Update line 5649 to include the `forex` sub-directory.
3. **Verify**: Use `grep` to confirm the change and manually check the UI if possible (or confirm via logic).

## 3. Checklist
- [ ] Create task lifecycle file (COMPLETED)
- [ ] Move to `workstream/200_inprogress`
- [ ] Modify `trade_viewer_api.py`
- [ ] Verify changes
- [ ] Move to `workstream/300_complete`

## 4. Progress Log
- **2026-03-16 01:48:30**: Created task and plan.
- **2026-03-16 01:52:00**: Modified `trade_viewer_api.py` to use `_resolve_day_dir` for health checks. This correctly handles the `/forex/` sub-directory as per current configuration.
- **2026-03-16 01:52:30**: Task successfully completed and moved to `300_complete`.
