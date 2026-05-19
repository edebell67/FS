# Task: Fix Pip Multiplier Lookup in breakout strategy

## 1. Understanding of Requirements
Currently, `BTC` (and potentially other crypto/indices) trades are using a default pip multiplier of `10000` (Forex default) instead of the product-specific multiplier specified in `config.json`. This causes P&L (net_return) and exit triggers (TP/SL) to be calculated incorrectly (10,000x larger for BTC).

The goal is to ensure `_get_pip_multiplier` in `common.py` correctly retrieves the multiplier from `config.json` using the hierarchical lookup (product-level first, then product-type, then fallback).

## 2. Plan of Approach
1.  **Verify Configuration Load**: Confirm `_load_config()` correctly parses `pip_multiplier_by_product` and `pip_multiplier_by_product_type` from `config.json`.
2.  **Debug `_get_pip_multiplier`**: Add temporary logging to `_get_pip_multiplier` in `fs/common.py` to see why it hits the fallback.
3.  **Fix Lookup Logic**: Correct the logic in `_get_pip_multiplier` to ensure it successfully retrieves values from the config.
4.  **Validate**: Run a test script to verify that `BTC` now resolves to a multiplier of `1` and `USDJPY` resolves to `100`.

## 3. List of Changes
- [ ] **`fs/common.py`**:
    - [ ] Add debug logging to `_get_pip_multiplier`.
    - [ ] Fix hierarchical lookup logic in `_get_pip_multiplier`.
    - [ ] Ensure `_load_config()` or `_load_layout_runtime_config()` correctly provides the required dictionaries.
- [ ] **Verification**:
    - [ ] Create a small test script to assert `_get_pip_multiplier('BTC') == 1`.
    - [ ] Assert `_get_pip_multiplier('GBP') == 10000`.

## 4. Status
- Date: 2026-03-17
- Version: V20260317_1600
- Status: TODO
