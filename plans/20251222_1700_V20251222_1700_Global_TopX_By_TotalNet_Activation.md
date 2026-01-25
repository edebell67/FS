# 20251222_1700_V20251222_1700_Global_TopX_By_TotalNet_Activation

## 1. Understanding of Requirements

The user wants to streamline the strategy activation process. The new criteria will focus solely on the **largest `total_net`** (P&L) to determine the top strategies for activation. Instead of always taking the top 3, the number of strategies to activate (`X`) will be configurable.

Specifically:
*   **Selection Metric**: Rank strategies by `total_net` (P&L) in descending order.
*   **Limit**: Activate the top `X` strategies based on this ranking.
*   **Configurability**: `X` should be a configurable parameter in `config.json`.
*   **Independent Ranking**: The ranking and selection of top `X` applies independently to the buy side (based on `buy_net`) and the sell side (based on `sell_net`).
*   **Removal of Previous Filters**: The `min_avg_net_threshold` and `min_trade_count` filters are no longer required.

## 2. Plan of Approach

1.  **Modify `config.json`**:
    *   Remove `min_avg_net_threshold`.
    *   Remove `min_trade_count`.
    *   Add a new configurable parameter: `"top_n_strategies": 1` (defaulting to 1 as per the initial request for "top 1").
2.  **Modify `TradeApps/breakout/common.py`**:
    *   Update `_load_config` to reflect the changes in `config.json`.
    *   In `_perform_auto_activation_check`:
        *   Retrieve `top_n_strategies` from config.
        *   Remove the `min_avg_net_threshold` and `min_trade_count` filters from candidate selection.
        *   Modify the sorting key for `net_candidates_raw` and `alt_candidates_raw` to solely rank by `pnl` (`total_net`) in descending order.
        *   Adjust the slicing of candidates to use `top_n_strategies` instead of a hardcoded `3`.
3.  **Modify `TradeApps/breakout/trade_viewer.html`**:
    *   Remove fields for `min_avg_net_threshold` and `min_trade_count` from the configuration modal.
    *   Add a new field for `top_n_strategies` to the configuration modal.
4.  **Modify `TradeApps/breakout/constants.py`**:
    *   Update `VERSION` to `V20251222_1700`.

## 3. List of Changes

### `TradeApps/breakout/config.json`
- [ ] Remove `"min_avg_net_threshold": 20.0`.
- [ ] Remove `"min_trade_count": 3`.
- [ ] Add `"top_n_strategies": 1`.

### `TradeApps/breakout/common.py`
- [ ] Update `_load_config` to remove defaults for `min_avg_net_threshold` and `min_trade_count`, and add default for `top_n_strategies`.
- [ ] In `_perform_auto_activation_check`:
    - [ ] Retrieve `top_n_strategies` from `config`.
    - [ ] Remove conditions checking `min_avg_net_threshold` and `min_trade_count_filter` during candidate selection.
    - [ ] Change sorting key for `net_candidates_raw` and `alt_candidates_raw` to `key=lambda x: x['pnl']`, `reverse=True`.
    - [ ] Change slicing for `newly_activated_net` and `newly_activated_alt` to use `top_n_strategies`.
    - [ ] Adjust `slots_to_fill` calculation to use `top_n_strategies`.

### `TradeApps/breakout/trade_viewer.html`
- [ ] Remove `min_avg_net_threshold` and `min_trade_count` fields from `renderConfigForm`.
- [ ] Add `top_n_strategies` field to `renderConfigForm`.

### `TradeApps/breakout/constants.py`
- [ ] Update `VERSION` to `V20251222_1700`.

## 4. Verification Plan
- [ ] Restart strategy scripts.
- [ ] Observe `activations.json` to ensure only the top `X` strategies (based on `total_net`) are activated globally.
- [ ] Change `top_n_strategies` in `config.json` (or UI) and verify the change in activated strategies.

I will start by modifying `config.json`.