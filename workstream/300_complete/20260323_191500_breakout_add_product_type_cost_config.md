# Task: Add product_type_cost to config.json

## Status: Completed (2026-03-23 19:30)

## 1. Summary
Add a new configuration field `product_type_cost` to `config.json` and implement logic to deduct this upfront USD cost from each trade's P&L based on its product type.

## 2. Objectives
- [x] **Update config.json:** Added `product_type_cost` dictionary with default USD values.
- [x] **Implement Logic in common.py:** Updated `calculate_pnl` and `calculate_v_trade_pnl` to subtract the adhoc cost.
- [x] **Verified Integration:** Confirmed that both standard and virtual trades now respect the new cost setting.

## 3. Implementation Details
- **Configuration:**
```json
"product_type_cost": {
    "crypto": 0.0,
    "energy": 0.0,
    "forex": 0.0,
    "indices": 0.0,
    "metals": 0.0
}
```
- **P&L Logic:**
    - Modified `BaseBreakoutStrategy.calculate_pnl()` to fetch the cost based on `product_type_for_product(self.trade_product)`.
    - Modified `_calculate_v_trade_pnl()` for virtual trades to fetch the cost based on `product_type_for_product(product)`.
    - Deduction applies to both `net_return` and `alt_net`.

## 4. Files Modified
- `TradeApps/breakout/fs/config.json`: Added configuration structure.
- `TradeApps/breakout/fs/common.py`: Implemented P&L deduction logic.
- `TradeApps/breakout/fs/constants.py`: Updated version to **V20260323_1930**.

## 5. Metadata
- **Project:** TradeApps/breakout
- **Version:** V20260323_1930
- **Created:** 2026-03-23 19:15

Completion Status: 100%
