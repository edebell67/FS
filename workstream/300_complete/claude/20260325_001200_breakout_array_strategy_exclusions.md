# Breakout Array Strategy Exclusions

Source: User request

Task Summary: Expand the `pick_now` strategy exclusion logic to accept multiple dynamically configured strings, allowing the system to naturally block toxic parameter combinations like `tp10.0_sl5.0`.

Context:
- Project: TradeApps/breakout
- Files to Modify: 
  - `TradeApps/breakout/fs/config.json`
  - `TradeApps/breakout/fs/strategy_predictor.py`
  - `TradeApps/breakout/fs/Constants.py`

Priority: 1

## 1. Understanding of Requirements
Recent backfilled data performance grouping revealed that certain parameter geometries (like `tp10.0_sl5.0`) result in consistent overarching losses. The existing Golden Filter uses a hard-coded single-string exclusion (`"exclude_strategy_string"`). To support multiple specific negative variants effortlessly, the configuration property must be refactored into an array (`"exclude_strategy_strings"`) capable of dropping any sequence fed into it.

## 2. Plan of Approach
1. **Update Configuration Structure**: Replace `exclude_strategy_string` with `exclude_strategy_strings` array in `config.json` containing `breakout_Rev_` and `tp10.0_sl5.0`.
2. **Update Predictor Default Parameter**: Adjust `DEFAULT_PICK_NOW_CONFIG` inside `strategy_predictor.py` to match the new dynamic list format.
3. **Iterative Evaluation**: Refactor `evaluate_pick_now_logic()` to loop through the user-defined array for every strategy, immediately returning `pick_now=False` if any substring hits a match.
4. **Version Bump**: Update version string in `Constants.py`.

## 3. List of Changes
- [ ] **`TradeApps/breakout/fs/config.json`**:
    - Remove `"exclude_strategy_string": "breakout_Rev_"`.
    - Add `"exclude_strategy_strings": ["breakout_Rev_", "tp10.0_sl5.0"]`.
- [ ] **`TradeApps/breakout/fs/strategy_predictor.py`**:
    - Update defaults constant structure.
    - Alter parameter extraction `config.get()`.
    - Change `is_not_toxic` logic to iteratively compare `exclude_strings` array against `strategy_name`.
- [ ] **`TradeApps/breakout/fs/Constants.py`**:
    - Update version number.
- [ ] **Verification**:
    - Validate predictor script via internal CLI tool syntax execution.
