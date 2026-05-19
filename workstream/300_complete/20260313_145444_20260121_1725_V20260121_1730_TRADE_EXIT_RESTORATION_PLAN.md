# Plan: Trade Exit & Database Recovery (V20260121_1730)

This plan addresses the critical failure where trades in PostgreSQL are not closing because their target levels are NULL.

## 1. Understanding of Requirements
- New trades in PostgreSQL are missing `target_profit` and `target_loss` column values.
- Existing open trades in PostgreSQL need their targets backfilled to allow the `pnl_update_service` to close them.
- A trailing stop-loss mechanism (similar to `sp_9004`) is needed in PostgreSQL for dynamic profit protection.

## 2. Plan of Approach

### Workstream 5.1: Repair Python Entry Logic
1.  Modify `common.py` -> `BaseBreakoutStrategy.enter_trade`.
2.  Calculate `tp_usd = self.tp_pips * PIP_VALUE` and `sl_usd = -self.sl_pips * PIP_VALUE`.
3.  Update the SQL `INSERT` into `trades` and `active_trades` to include columns: `target_profit`, `target_loss`, `tp_pips`, `sl_pips`.

### Workstream 5.2: Retroactive Fix
1.  Execute a one-time SQL script to update NULL targets on active trades.
2.  The script will parse the `strategy_key` (e.g., `2_0.00015_20.0_10.0`) to extract TP and SL values.

### Workstream 5.3: Trailing Stop-Loss in PG
1.  Create `update_trailing_stop_loss()` function in `pgsql_pnl_management.sql`.
2.  Modify `process_open_trades()` to call this new function every cycle.

## 3. List of Changes

### `TradeApps/breakout/common.py`
- [ ] Update `enter_trade` method to calculate USD targets.
- [ ] Update `INSERT INTO trades` SQL to include target/pip columns.
- [ ] Update `INSERT INTO active_trades` SQL to include target/pip columns.

### `TradeApps/breakout/db_scripts/pgsql_pnl_management.sql`
- [ ] Implement `update_trailing_stop_loss()` function.
- [ ] Add `update_trailing_stop_loss()` call to `process_open_trades()`.

### `TradeApps/breakout/constants.py`
- [ ] Update version to `V20260121_1730`.

### Database Recovery (SQL)
- [ ] Run recovery script to patch NULL targets.

## 4. Confirmation Required
- Does `$10.0 per pip` (PIP_VALUE) apply to all products currently being traded in PG?
- Should `target_loss` be stored as a negative number in the database (matching the `net_return` scale)? (Based on `sp_003` logic, it compares `net_return < target_loss`, so yes, the SL should be negative).
