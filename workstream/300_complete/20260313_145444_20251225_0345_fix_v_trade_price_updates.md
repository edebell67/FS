# Plan: Live Updates for Virtual Trade Prices and PnL

## 1. Requirement
The user wants `current_price` to be kept up to date in the JSON files for virtual trades (V-Trades). Currently, V-Trade files are created but not updated with the latest price as the market moves, unless they are closed or modified for other reasons.

## 2. Approach
I will modify `common.py` to:
1.  Implement a helper function `_calculate_v_trade_pnl` to calculate Gross PnL (pips), Net Return (USD), and Alt Net (USD) for V-Trades, using the standard logic (pip value, commission, spread).
2.  Update `_finalize_v_trade_record` to use this helper, ensuring closed V-Trades have accurate PnL data instead of default zeros.
3.  Modify `_manage_virtual_trades` to iterate through all *OPEN* V-Trades in every cycle. For each open trade:
    -   Fetch the latest price for its product.
    -   Update `current_price` in the JSON data.
    -   Recalculate PnL metrics using `_calculate_v_trade_pnl`.
    -   Save the updated JSON file to disk.

## 3. Checklist
- [x] Create `_calculate_v_trade_pnl` helper in `common.py`.
- [x] Refactor `_finalize_v_trade_record` in `common.py` to calculate PnL.
- [x] Update `_manage_virtual_trades` in `common.py` to perform live price/PnL updates for Open V-Trades.
- [x] Update `VERSION` in `constants.py`.

## 4. Verification
- [x] Verify `common.py` syntax.
- Verify that logic handles missing prices gracefully (skips update).
