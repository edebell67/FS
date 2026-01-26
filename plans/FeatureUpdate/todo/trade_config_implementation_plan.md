# Trade Configuration Management Implementation Plan

**Date**: 2025-11-24  
**Target File**: `simple_trend_trader.py`  
**Objective**: Implement config_trade.json for saving/loading multiple trade strategies

## Implementation Checklist

### Part 1: Create Plan Document
- [x] Create plan document at `C:\Users\edebe\eds\plans\FeatureUpdate\trade_config_implementation_plan.md`

### Part 2: Configuration File Management

- [ ] **Step 1**: Define constant `TRADE_CONFIG_PATH` for `config_trade.json` location
  - Location: After line 31 (near other config paths)
  - Value: `os.path.join(os.path.dirname(__file__), 'config_trade.json')`

- [ ] **Step 2**: Create `load_trade_configs()` function
  - Location: After `load_app_config()` function (around line 120)
  - Returns: `dict` of trade configurations keyed by TRADE_TITLE
  - Handles: File not found, JSON decode errors
  - Default: Returns empty dict `{}`

- [ ] **Step 3**: Create `save_trade_configs(configs)` function
  - Location: After `load_trade_configs()`
  - Parameter: `configs` - dict of trade configurations
  - Action: Write to `config_trade.json` with indent=4
  - Error handling: Print error message if save fails

### Part 3: Startup UI Overhaul

- [ ] **Step 4**: Create `select_or_create_trade_config()` function
  - Location: After `get_user_inputs()` function
  - Sub-tasks:
    - [ ] Load all saved configs using `load_trade_configs()`
    - [ ] Display numbered list of saved TRADE_TITLEs
    - [ ] Add option "[N] Create a New Trade Strategy" (where N = len(configs) + 1)
    - [ ] Prompt user for choice
    - [ ] Handle invalid input gracefully

- [ ] **Step 5**: Implement "Select Existing Strategy" logic
  - Sub-tasks:
    - [ ] Retrieve selected config parameters
    - [ ] Check if trade is already active by looking in OPEN_TRADES_FOLDER
      - Look for files matching pattern: `trade_{TRADE_TITLE}_No*.json`
    - [ ] If active: Print message and exit script gracefully
    - [ ] If not active: Load parameters into global variables
      - Set: PRODUCT_SYMBOL, PRICE_CACHE_SIZE, BUFFER_X
      - Set: TARGET_PROFIT_PIPS, TARGET_LOSS_PIPS
      - Set: TARGET_PROFIT_USD, TARGET_LOSS_USD
      - Set: TRADE_TITLE, REVERSE_TRADE_TITLE
      - Set: COMMISSION_PER_TRADE_USD
      - Set: price_cache maxlen

- [ ] **Step 6**: Implement "Create New Strategy" logic
  - Sub-tasks:
    - [ ] Call original `get_user_inputs()` function
    - [ ] After TRADE_TITLE is generated, create config dict with all parameters
    - [ ] Add new config to main configs dict (keyed by TRADE_TITLE)
    - [ ] Call `save_trade_configs()` to persist

- [ ] **Step 7**: Modify `run_trading_simulation()`
  - Location: Line 831 (where `get_user_inputs()` is currently called)
  - Action: Replace `get_user_inputs()` with `select_or_create_trade_config()`
  - Ensure: Rest of function continues unchanged

## Testing Plan

1. **Test New Strategy Creation**:
   - Run script, select "Create New"
   - Verify config_trade.json is created with correct parameters
   - Verify trade runs normally

2. **Test Strategy Selection**:
   - Run script again, select existing strategy
   - Verify parameters are loaded correctly
   - Verify trade runs with loaded parameters

3. **Test Active Trade Detection**:
   - Start a trade (leave it open)
   - Run script again, select same strategy
   - Verify script exits gracefully with message

4. **Test Multiple Strategies**:
   - Create 2-3 different strategies
   - Verify all are saved and listed correctly
   - Verify each can be selected and run independently

## Safety Considerations

- **No Breaking Changes**: All existing functionality preserved
- **Backward Compatible**: Script works even if config_trade.json doesn't exist
- **Graceful Degradation**: Errors in config file don't crash the script
- **Data Integrity**: Existing open/closed trade JSON files remain untouched
