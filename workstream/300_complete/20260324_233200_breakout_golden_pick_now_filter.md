# Breakout Golden Pick Now Filter

Source: User request

Task Summary: Implement data-driven "Golden Filter" for `pick_now` strategy selection to maximize win-rate based on historical analysis.

Context:
- Project: TradeApps/breakout
- Files to Modify: 
  - `TradeApps/breakout/fs/config.json`
  - `TradeApps/breakout/fs/strategy_predictor.py`
  - `TradeApps/breakout/fs/Constants.py`

Priority: 1

## 1. Understanding of Requirements
Based on a recent comprehensive 6-day data analysis, the `pick_now` strategy selection logic needs to be constrained to avoid entering trades when the strategy edge has been exhausted or during historically toxic time windows. The new rules specify: 
1. Only pick when the strategy net is between 600 and 799.
2. Only pick if the strategy has executed fewer than 20 trades.
3. Exclude any strategies containing `"breakout_Rev_"` in their name due to low win rates.
4. Do not make any new picks during snapshots 85 through 99 (approx. 08:30 AM to 10:00 AM).

These configurable thresholds will be managed via `config.json` and evaluated within `strategy_predictor.py`.

## 2. Plan of Approach
1.  **Update Configuration**: Add new constraint keys to `config.json`.
2.  **Update Predictor Parameters**: Modify `load_pick_now_config` in `strategy_predictor.py` to extract the new variables with safe fallbacks.
3.  **Implement Golden Filter Logic**: Modify `evaluate_pick_now_logic` in `strategy_predictor.py` to assert the 4 new constraints against the incoming strategy metrics before allowing `pick_now` to equal `True`.
4.  **Version Bump**: Update version string in `Constants.py`.

## 3. List of Changes
- [x] **`TradeApps/breakout/fs/config.json`**:
    - Add `"min_net_at_pick": 600`
    - Add `"max_net_at_pick": 799`
    - Add `"max_trade_count": 19`
    - Add `"exclude_strategy_string": "breakout_Rev_"`
    - Add `"dead_zone_start_snapshot": 85`
    - Add `"dead_zone_end_snapshot": 99`
- [x] **`TradeApps/breakout/fs/strategy_predictor.py`**:
    - Modify `load_pick_now_config()` to load the 6 new parameters.
    - Modify `evaluate_pick_now_logic()` to evaluate `current_net`, `trade_count`, `strategy_name`, and `snapshot_number` against the new config bounds.
- [x] **`TradeApps/breakout/fs/Constants.py`**:
    - Update version number.
- [x] **Verification**:
    - Double check AND VERIFY that all changes have been implemented correctly.
