# Plan: Trade Bucket L-Trade Generation Logic - 2026-01-19

This plan outlines the implementation of a new L-Trade generation mode called `trade_bucket`. This mode activates L-Trade generation based on a strategy's performance within a collection (bucket) rather than static activations.

## 1. Requirements Recap
- **Mode**: `l_trade_generation_mode` = "trade_bucket"
- **Criteria**: 
    - Strategy must be in a **live** bucket in `_trade_bucket.json`.
    - Must have the **highest positive total_net** in that bucket.
    - Must lead the next best strategy by $\ge$ `minimum_difference` (default 5.0).
    - Data Source: `_summary_totals.json` (latest totals).
- **Behavior**:
    - **Existing Trades**: If a strategy becomes leader, promote any open normal trade to L-Trade immediately.
    - **New Trades**: The next trade triggered by a leader is marked as an L-Trade.
- **Exclusion**: 
    - Virtual trades **CANNOT** generate L-trades in `trade_bucket` mode.
    - Manual promotions from Trade Viewer UI are blocked in `trade_bucket` mode.
    - L-trades only originate from **normal** trades (breakout strategies) via bucket leadership.

## 2. Plan of Approach

### 2.1 Backend Logic (common.py)
1. **Helper Method**: `_is_trade_bucket_leader(strategy_name, product)`
   - Load `_trade_bucket.json` for the current trading day.
   - Load `_summary_totals.json`.
   - Calculate leadership status.
2. **Handle Live Orders**:
   - Update `_handle_live_orders` to allow `trade_bucket` mode.
   - Inject the leader check into the order generation path.
3. **Immediate Promotion**:
   - Update `_maybe_force_immediate_live` to trigger if in `trade_bucket` mode and leadership is confirmed.

### 2.2 Constants
- Update version to `V20260119_1303`.

## 3. Check List
- [x] **Constants.py**: Update version number.
- [x] **common.py**: Implement `_is_trade_bucket_leader` helper.
- [x] **common.py**: Update `_maybe_force_immediate_live` to support `trade_bucket` mode.
- [x] **common.py**: Update `_handle_live_orders` to support `trade_bucket` mode.
- [x] **Audit**: Verify correct comments and datetime stamps.

## 4. Verification
- [x] Set mode to `trade_bucket`.
- [x] Verify leader promotion for existing trades.
- [x] Verify leader marking for new trades.
- [x] Verify absolute max_live_trades limit.
- [x] Verify virtual trades and manual API promotions are blocked from OPENING in `trade_bucket` mode.
- [x] Confirmed version V20260119_1303.
