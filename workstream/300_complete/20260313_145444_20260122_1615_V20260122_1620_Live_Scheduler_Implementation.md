# Plan: Live Trade Scheduler & Immediate Activation Implementation

**Date:** 2026-01-22 16:30
**New Version:** V20260122_1630

## 1. Understanding of Requirements
1.  **Schedule-Based Activation**: Create a helper to scan `activations_is_live.json` (Schedule) to determine if a trade should be "live".
    *   Match: `product`, `strategy`, `parm`, `start_time` (on/after), `end_time` (before, if exists).
    *   Criterion: `is_live == true` in the record.
2.  **Immediate Activation for Open Trades**: If a trade is already open but not live:
    *   Condition: `config.json` has `"bypass_criteria_check": "immediately"`.
    *   Condition: Current time matches an active "live" record in `activations_is_live.json`.
    *   Action:
        *   Set `in_trade_entry_time` = current time.
        *   Set `in_trade_entry_price` = current ask/bid.
        *   Set `is_live_trade` = `true`.
        *   Generate the tradeable JSON order for TWS immediately.
3.  **Syntax Fix**: Repair `activations_is_live.json` syntax errors.

## 2. Plan of Approach
1.  **Fix `fs/activations_is_live.json`**:
    *   Convert to valid JSON (double quotes, array for `live`, etc.).
2.  **Implement `fs/live_scheduler.py`**:
    *   `get_matching_live_schedule(product, strategy, parm, current_time, mode='live')`: Scans the config and returns the record if a match is found and `is_live` is true.
3.  **Modify `fs/common.py`**:
    *   Import `get_matching_live_schedule`.
    *   Update `BaseBreakoutStrategy.enter_trade`:
        *   Check schedule during entry. If live, mark for order generation.
    *   Update `BaseBreakoutStrategy.process_new_tick`:
        *   Add logic to check already open trades (`not is_live_trade`).
        *   If `bypass_criteria_check == "immediately"` and a schedule match occurs:
            *   Log `in_trade_entry_time` and `in_trade_entry_price`.
            *   Trigger `_create_tradeable_json` directly (bypassing normal guards if necessary).
    *   Update `_save_trade_json` to persist these new fields.
4.  **Update `fs/Constants.py`**: Increment version to `V20260122_1630`.

## 3. List of Changes
- [ ] **`fs/activations_is_live.json`**: Fix JSON syntax and structure.
- [ ] **`fs/live_scheduler.py`**: Create new helper module.
- [ ] **`fs/common.py`**: 
    *   Modify `enter_trade` to check schedule.
    *   Modify `process_new_tick` to handle "immediately" bypass for open trades.
    *   Update `_save_trade_json` for new metadata fields.
- [ ] **`fs/Constants.py`**: Update version to `V20260122_1630`.

## 4. Confirmation
Please confirm this plan before I proceed.
