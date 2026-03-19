# Filter Trade Execution Console by Visibility Status

**Date**: 2025-11-28 20:36  
**Objective**: Filter the Trade Execution Console page to show only trade titles whose VIEW_STATUS is set to 'visible'

## 1. Understanding of Requirements

Currently, the Trade Execution Console displays ALL trade titles from `config_trade.json`, regardless of their `VIEW_STATUS` setting. The user wants to filter this list to show only titles marked as 'visible', excluding those marked as 'hidden'.

The visibility status is managed on the "Configure Real-Time (RT) Trade Titles" page and stored in the `VIEW_STATUS` field of each trade configuration.

## 2. Plan of Approach

### Changes Required:

1. **Modify `execution_manager.list_trade_statuses()`**:
   - Add an optional parameter `include_hidden` (default: `False`)
   - Filter the returned list based on the `VIEW_STATUS` field in the trade config
   - Only return trades with `VIEW_STATUS == 'visible'` when `include_hidden=False`

2. **Update `view_trade_execution_console()` in trade_monitor.py**:
   - Call `execution_manager.list_trade_statuses()` without parameters (defaults to showing only visible)
   - This ensures the Trade Execution Console only displays visible trade titles

## 3. List of Changes

### File: `execution_manager.py`
- [x] Modify `list_trade_statuses()` function:
  - Add `include_hidden: bool = False` parameter
  - Filter results based on `VIEW_STATUS` field from configs
  - Add comment explaining the filtering logic with timestamp

### File: `trade_monitor.py`
- [x] No changes needed (already calls `list_trade_statuses()` without parameters, which will default to visible-only)

## 4. Implementation Details

The filtering will happen in `execution_manager.list_trade_statuses()`:
- Load trade configs to access `VIEW_STATUS` for each title
- When building the statuses list, check each config's `VIEW_STATUS`
- Skip titles with `VIEW_STATUS == 'hidden'` unless `include_hidden=True`
- Maintain backward compatibility by defaulting to show only visible trades

## 5. Testing Plan

After implementation:
- [x] Test 1: Verify Trade Execution Console loads without errors
- [ ] Test 2: Verify hidden trades do not appear in Trade Execution Console
- [ ] Test 3: Verify visible trades appear in Trade Execution Console
- [ ] Test 4: Verify RT Config page still shows all trades (both visible and hidden)
- [ ] Test 5: Test toggling visibility status and confirm updates

## 6. Implementation Log

### Change 1: Modified `execution_manager.list_trade_statuses()`
- Added `include_hidden: bool = False` parameter
- Added filtering logic to exclude hidden trades by default
- Timestamp: 2025-11-28 20:38
