# Task: Fix L-Trade Contract Mapping for Non-Forex Products

## Source
- User Directive: 2026-04-07 (following discovery of hardcoded values in `common.py`)

## Task Summary
Modify `common.py` to stop using hardcoded Forex values (`secType: CASH`, `exchange: IDEALPRO`) for all L-Trade orders. The system must instead dynamically load contract details from `tws_order_templates.json` based on the product being traded (e.g., SIL should use `secType: FUT`, `exchange: COMEX`, and include `multiplier` and `lastTradeDateOrContractMonth`).

## Context
- **Script**: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- **Template Source**: `C:\Users\edebe\eds\TradeApps\breakout\fs\tws_order_templates.json`
- **Problem**: `_create_l_trade_order` currently ignores the product type and forces all orders into Forex format, causing failures for Futures/Metals in TWS.

## Plan
- [x] 1. **Load Templates**: Update `common.py` to load and cache `tws_order_templates.json`.
- [x] 2. **Implement Lookup Logic**:
  - [x] Create a helper function `_get_tws_contract_details(product)` that identifies the correct template.
  - [x] Handle the `product_type_by_product` mapping from `config.json` to resolve the category.
- [x] 3. **Update `_create_l_trade_order`**:
  - [x] Replace hardcoded `secType`, `exchange`, `currency` with template values.
  - [x] Add support for Futures-specific fields: `multiplier` and `lastTradeDateOrContractMonth`.
  - [x] Ensure `quantity` logic remains consistent with the product type requirements.
- [x] 4. **Validation**:
  - [x] Code implemented and version updated to `V20260407_1730`.
  - [ ] Generate a test order for a Forex product (e.g., GBP) and verify it still produces `CASH/IDEALPRO`.
  - [ ] Generate a test order for a Metal (e.g., SIL) and verify it produces `FUT/COMEX` with the correct expiry and multiplier.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-07 17:30:00
