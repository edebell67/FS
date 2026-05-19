# Task: Implement Upfront Product Type Costs & UI Configuration

## Status: Completed (2026-03-24 16:50)

## 1. Summary
Implement a system to apply adhoc upfront USD costs to every trade based on its product category. This ensures that trading performance (Net P&L) reflects real-world costs immediately upon trade entry.

## 2. Objectives
- [x] **Configuration Schema:** Add `product_type_cost` to `config.json` with per-category USD values.
- [x] **Upfront Logic:** Modify the P&L calculation engine to deduct these costs at the exact moment a trade is opened.
- [x] **JSON Transparency:** Record the deducted `adhoc_cost_usd` inside each trade JSON file for auditing.
- [x] **UI Management:** Add a dedicated "Product Type Costs" section to the Dashboard Config UI.

## 3. Implementation Details

### Backend Logic (`common.py`)
- **Config Storage:** Updated `BaseBreakoutStrategy` to persistently store the system configuration.
- **P&L Deduction:** Modified `calculate_pnl` and `_calculate_v_trade_pnl` to resolve the `product_type` and subtract the configured cost from `net_return` and `alt_net`.
- **Early Calculation:** Forced a P&L update during `_save_trade_json` so trades start with a negative balance (fixed costs) even before the first price tick arrives.

### UI Integration (`trade_viewer.html`)
- **New Section:** Added "💰 Product Type Costs" to the configuration modal.
- **Dynamic Inputs:** Created numeric fields for Forex, Crypto, Metals, Indices, and Energy.
- **Persistence:** Wired the fields to the nested `product_type_cost` object in `config.json` via the standard `saveConfig` workflow.

## 4. Files Modified
- `TradeApps/breakout/fs/config.json`: Added configuration structure.
- `TradeApps/breakout/fs/common.py`: Implemented upfront deduction and JSON recording.
- `TradeApps/breakout/fs/trade_viewer.html`: Added configuration UI section.
- `TradeApps/breakout/fs/constants.py`: Updated version to **V20260324_1645**.

## 5. Usage
1. Open **Trade Viewer** -> **Config**.
2. Set a cost (e.g., `Forex Cost: 2.0`).
3. Save Config.
4. Any new Forex trade will now open with `net_return: -12.0` (assuming $10 base commission + $2 adhoc cost).

## 6. Evidence
- **Audit:** Trade JSON files now contain `"adhoc_cost_usd": X.X`.
- **UI:** New "Product Type Costs" section confirmed visible and functional in the config modal.

Completion Status: 100%
