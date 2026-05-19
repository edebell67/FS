# Gemini Coder - Plan for Alt P&L Calculation Rework (2025-12-07)

## 1. Understanding of Requirements

The `alt_pnl` calculation in `simple_trend_trader.py` needs to be updated to a specific formula provided by the user, incorporating a dynamically calculated `total_spread_cost`. Additionally, for historical data analysis, the bid and ask prices at both the entry and exit points of a trade must be explicitly captured and stored in the trade object.

**New `alt_pnl` Formula:**
`alt_net_pips = -(gross_pips of original trade) - commission_pips - total_spread_cost_pips`

**Definition of `total_spread_cost_pips`:**
`total_spread_cost_pips = (spread_at_entry_pips) + (spread_at_exit_pips)`
Where `spread_at_entry_pips = (Entry Ask Price - Entry Bid Price) / PIP_SIZE` and `spread_at_exit_pips = (Exit Ask Price - Exit Bid Price) / PIP_SIZE`.

**Historical Data Capture:**
The `current_trade` and `reverse_trade` objects must store:
*   `'Entry Bid Price'`
*   `'Entry Ask Price'`
*   `'Exit Bid Price'`
*   `'Exit Ask Price'`

## 2. Plan of Approach

The implementation will involve modifying trade opening and closing functions to capture and store the required bid/ask prices, and then updating the `alt_pnl` calculation to use the new formula based on these stored values. The changes will be applied to `simple_trend_trader.py`.

## 3. List of Changes

**File: `C:\Users\edebe\eds\Trades\simple_trend_trader.py`**

### Phase 0: Setup & Backup
- [ ] Create a timestamped backup of `C:\Users\edebe\eds\Trades\simple_trend_trader.py`. (E.g., `simple_trend_trader.py_20251207_HHMMSS`)
- [ ] Create and save this plan document as `C:\Users\edebe\eds\plans\20251207_alt_pnl_rework.md`.

### Phase 1: Data Capture - Bid/Ask at Entry
- [ ] **Modify `open_new_trade` function:**
    - [ ] Update its signature to accept `bid_at_entry` and `ask_at_entry`.
    - [ ] Add `'Entry Bid Price'` and `'Entry Ask Price'` to the `current_trade` dictionary initialization.
    - Tag: `20251207_01`
- [ ] **Modify `open_reverse_trade` function:**
    - [ ] Update its signature to accept `bid_at_entry` and `ask_at_entry`.
    - [ ] Add `'Entry Bid Price'` and `'Entry Ask Price'` to the `reverse_trade` dictionary initialization.
    - Tag: `20251207_01`
- [ ] **Update calls to `open_new_trade` in `check_for_signals`:**
    - [ ] Pass the current `bid_price` and `ask_price` (from `get_latest_price`) as `bid_at_entry` and `ask_at_entry`.
    - Tag: `20251207_01`
- [ ] **Update calls to `open_reverse_trade` in `check_for_signals`:**
    - [ ] Pass the current `bid_price` and `ask_price` (from `get_latest_price`) as `bid_at_entry` and `ask_at_entry`.
    - Tag: `20251207_01`

### Phase 2: Data Capture - Bid/Ask at Exit
- [ ] **Modify `close_current_trade` function:**
    - [ ] Update its signature to accept `bid_at_exit` and `ask_at_exit`.
    - [ ] Add `'Exit Bid Price'` and `'Exit Ask Price'` to the `current_trade` dictionary update (`current_trade.update(...)`).
    - Tag: `20251207_01`
- [ ] **Modify `close_reverse_trade` function:**
    - [ ] Update its signature to accept `bid_at_exit` and `ask_at_exit`.
    - [ ] Add `'Exit Bid Price'` and `'Exit Ask Price'` to the `reverse_trade` dictionary update (`reverse_trade.update(...)`).
    - Tag: `20251207_01`
- [ ] **Update calls to `close_current_trade` in `check_for_signals`:**
    - [ ] Pass the current `bid_price` and `ask_price` (from `get_latest_price`) as `bid_at_exit` and `ask_at_exit`.
    - Tag: `20251207_01`
- [ ] **Update calls to `close_reverse_trade` in `check_for_signals`:**
    - [ ] Pass the current `bid_price` and `ask_price` (from `get_latest_price`) as `bid_at_exit` and `ask_at_exit`.
    - Tag: `20251207_01`

### Phase 3: Implement `alt_pnl` Calculation
- [ ] **Modify `close_current_trade` function:**
    - [ ] Retrieve `gross_pips` (of the actual trade) and `commission_pips` from the initial `calculate_pnl` call.
    - [ ] Retrieve `'Entry Bid Price'`, `'Entry Ask Price'`, `'Exit Bid Price'`, `'Exit Ask Price'` from the `current_trade` object.
    - [ ] Calculate `spread_at_entry_pips = (current_trade.get('Entry Ask Price', 0.0) - current_trade.get('Entry Bid Price', 0.0)) / PIP_SIZE`.
    - [ ] Calculate `spread_at_exit_pips = (current_trade.get('Exit Ask Price', 0.0) - current_trade.get('Exit Bid Price', 0.0)) / PIP_SIZE`.
    - [ ] Calculate `total_spread_cost_pips = spread_at_entry_pips + spread_at_exit_pips`.
    - [ ] Calculate `alt_net_pips` using the formula: `alt_net_pips = -gross_pips - commission_pips - total_spread_cost_pips`.
    - [ ] Calculate `alt_net_usd` from `alt_net_pips`.
    - [ ] **Remove the previous problematic `alt_net_pips = -gross_pips - commission_pips` override and the preceding `calculate_pnl` call that was meant for alt_pnl.**
    - Tag: `20251207_01`
- [ ] **Modify `close_reverse_trade` function:**
    - [ ] Apply the same logic as in `close_current_trade` to the `reverse_trade` object.
    - Tag: `20251207_01`

### Phase 4: Data Loading & Backward Compatibility
- [ ] **Modify `load_trade_state_and_params` function:**
    - [ ] Ensure `'Entry Bid Price'`, `'Entry Ask Price'`, `'Exit Bid Price'`, `'Exit Ask Price'` are handled gracefully (initialized to `0.0` or sensible defaults for calculations) for old trade JSON files that might not contain these new fields. This prevents crashes when loading historical data.
    - Tag: `20251207_01`

### Phase 5: Version Update
- [ ] Update the `VERSION` in `simple_trend_trader.py` (if an existing version constant is available, otherwise add one for tracking this change).
    - Tag: `20251207_01`

---

## 4. Verification

After implementing these changes, verification will involve:
*   Running the script and opening/closing trades.
*   Checking the saved JSON trade log files to ensure `Entry Bid Price`, `Entry Ask Price`, `Exit Bid Price`, and `Exit Ask Price` are correctly stored.
*   Verifying that `alt_net_pips` and `alt_net_usd` are calculated correctly according to the new formula, especially for the example scenario leading to -7 pips (as per user's example).
*   Testing with older trade log files (that lack the new bid/ask fields) to ensure they load without errors.
