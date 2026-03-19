# Plan to Fix Incorrect Price in Virtual Trades

## 1. Issue Description
The user identified that the price for EUR in a virtual trade file (`vt_breakout_R_Rev_4_tp10.0_sl6.0_buy_net_EUR_20251225_002147.json`) was `0.646592`, which is incorrect for EUR (should be ~1.05+).
Analysis revealed that `_manage_virtual_trades` in `common.py` receives a single `current_price` argument (along with `latest_bid`, `latest_ask`). This price corresponds to the *last processed product* in the `run_multiwindow` loop (likely NZD or AUD, given the 0.64 value), not necessarily the product for which the virtual trade is being created.

## 2. Plan of Approach
I will refactor `run_multiwindow` to maintain a dictionary of the latest prices for *all* products. I will then pass this dictionary to `_manage_virtual_trades`.
Inside `_manage_virtual_trades`, I will use the specific product's price from this dictionary when creating or updating virtual trades, instead of using a global scalar.

## 3. List of Changes
*   **`c:\Users\edebe\eds\TradeApps\breakout\common.py`**:
    *   [x] In `run_multiwindow`:
        *   Initialize a `latest_prices` dictionary (e.g., `{product: {'price': X, 'bid': Y, 'ask': Z}}`) instead of scalar variables.
        *   Update this dictionary inside the product loop.
        *   Pass `latest_prices` dictionary to `_manage_virtual_trades` instead of scalar `current_price`, `bid`, `ask`.
    *   [x] In `_manage_virtual_trades`:
        *   Change signature to accept `latest_prices: Dict[str, Dict[str, float]]`.
        *   When calling `_finalize_v_trade_record` or `_create_new_v_trade`, look up the specific price for the target `product` from `latest_prices`.
            *   Fallback to 0.0 or handle missing price gracefully if product not in dict.
    *   [x] Verify the fix by ensuring parameter alignment.
