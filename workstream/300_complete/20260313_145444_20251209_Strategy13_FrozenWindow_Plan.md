# Plan to Implement "Frozen Window" Logic for Strategy13

## 1. Understanding of Requirements

The user identified a flaw in the initial `Strategy13` implementation: the price history window was continuously rolling, making it difficult for a true breakout to occur. The desired behavior, as demonstrated by `breakout.py`, is for the price history window to "freeze" (stop updating) once it is full and the strategy is awaiting a trade entry. The window should only clear and begin rebuilding after a trade initiated by `Strategy13` is closed.

## 2. Plan of Approach

The `Strategy13` class in `s13.py` will be modified to incorporate class-level flags that manage the state of the price history window and trade activity. This will involve:

1.  **Class-level state variables:** Introducing `has_open_trade_from_this_strategy` and `is_window_built` (both booleans) to track the strategy's trade status and the price history window's completeness.
2.  **`__init__` method refinement:** Ensuring proper initialization and dynamic adjustment of the `price_history` deque's `maxlen` based on the configured `window_size`. Also, initializing the new state flags.
3.  **`evaluate` method state machine:** Implementing a multi-phase logic within `evaluate` to:
    *   Detect trade closures and trigger a window reset.
    *   Conditionally manage the `price_history` (building it up, then freezing it).
    *   Only allow trade entry checks when the window is built and no trade is open.
    *   Update logging to reflect the various states of the window and trade activity.

## 3. List of Changes

*   **`algo_viewer/tradepanel/strategies/s13.py`**:
    *   [x] **Class Definition:**
        *   Add `has_open_trade_from_this_strategy: bool = False`
        *   Add `is_window_built: bool = False`
    *   [x] **`__init__` method:**
        *   Ensure `Strategy13.price_history` `maxlen` is dynamically set by `self.window_size`.
        *   Implement logic to reset `has_open_trade_from_this_strategy` and `is_window_built` when `window_size` changes.
        *   Add initial checks to align `has_open_trade_from_this_strategy` and `is_window_built` based on current active trades and history length.
    *   [x] **`evaluate` method:**
        *   **Phase 1 (State Update & Closure Detection):**
            *   Capture `previous_has_open_trade` before updating `Strategy13.has_open_trade_from_this_strategy` with the current `has_own_open_trade`.
            *   If `previous_has_open_trade` was `True` and `has_own_open_trade` is now `False`, clear `Strategy13.price_history` and set `Strategy13.is_window_built = False` (trade closure and window reset).
        *   **Phase 2 (Manage Price History Window):**
            *   If `current_price` is valid:
                *   If no trade is open (`not Strategy13.has_open_trade_from_this_strategy`) AND the window is not yet built (`not Strategy13.is_window_built`), append `current_price` to `price_history`.
                *   If `price_history` reaches `self.window_size`, set `Strategy13.is_window_built = True`.
                *   Log debug messages for building, freezing (due to trade open), and freezing (due to built window awaiting entry).
            *   Else (`current_price` is `None`), log a message indicating no price data.
        *   **Phase 3 (Main Entry Logic):**
            *   Modify the main `if` condition for trade entry to: `if not Strategy13.has_open_trade_from_this_strategy and current_price is not None and Strategy13.is_window_built:`
            *   Adjust logging messages in this section (`S13 Eval:`, `NO SIGNAL`, `Entry Conditions NOT met`) to be more explicit about the window state.
    *   [x] **Update Logging:** Ensure all relevant log messages clearly indicate the state of the price window (building, frozen, reset) and the trade status.