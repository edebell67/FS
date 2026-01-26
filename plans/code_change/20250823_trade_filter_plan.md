### Plan: Trade Panel Filter by Created Date/Time

**Objective:** To make the "Now" button and the selection of "Strategy 12" immediately apply the filter based on the `created` timestamp of the latest closed trade for the selected product.

**Version:** 64.2.14
**Date:** 2025-08-26

---

#### 1. `tradepanel/api.py`

*   **[x] Add `fetch_latest_closed_trade_created_datetime(self, product_name: str) -> Optional[str]` method to `APIClient`.**
    *   This method should:
        *   Construct the API URL using `http://127.0.0.1:8000/api/vw_112_LatestTradeByProduct`. (2025-08-26, V64.2.14: Updated to use vw_112_LatestTradeByProduct as source for latest created date.)
        *   Execute an HTTP GET request using `_fetch_data_from_url` (non-paginated).
        *   Parse the JSON response and extract the `LatestCreatedDate` timestamp from the response.
        *   Return the `LatestCreatedDate` timestamp string or `None` if no data is found or an error occurs.
        *   **[x] Note (2025-08-25, V1.7): Changed `_sort=-created` to `_sort=created.desc` to match API expectation.**
        *   **[x] Note (2025-08-25, V1.7): Implemented datetime format conversion to `YYYY-MM-DD HH:MM:SS` for SQL compatibility.**

#### 2. `tradepanel/trade_engine.py`

*   **[x] Add `get_latest_closed_trade_created_datetime(self, product_name: str) -> Optional[str]` method to `TradeManager`.**
    *   This method will call `self.api_client.fetch_latest_closed_trade_created_datetime(product_name)`.
    *   It will return the timestamp string or `None`.

#### 3. `tradepanel/ui/main_window.py`

*   **[x] Modify `_on_now_button_click` method:**
    *   **[x] Logic implemented to call `latest_created_dt = self.manager.get_latest_closed_trade_created_datetime(selected_product)`. (2025-08-26, V64.2.14: Verified implementation uses API data or falls back to current datetime.)**
    *   **[x] If `latest_created_dt` is not `None`, update `self.app_state.trade_filter_start_datetime_var.set(latest_created_dt)`.**
    *   **[x] If `latest_created_dt` is `None`, fallback to `datetime.now().strftime("%Y-%m-%d %H:%M:%S")`.**
    *   **[x] Keep `self.trigger_manual_refresh(fetch_new=True)` and `self.manager.trigger_trade_restriction_update(selected_product)`.**

*   **[x] Modify `_on_strategy_change` method (specifically for "Strategy 12" block):**
    *   **[x] Logic implemented to call `latest_created_dt = self.manager.get_latest_closed_trade_created_datetime(selected_product)`. (2025-08-26, V64.2.14: Verified implementation uses API data or falls back to current datetime.)**
    *   **[x] If `latest_created_dt` is not `None`, update `self.app_state.trade_filter_start_datetime_var.set(latest_created_dt)`.**
    *   **[x] If `latest_created_dt` is `None`, fallback to `datetime.now().strftime("%Y-%m-%d %H:%M:%S")`.**
    *   **[x] Keep `self.trigger_manual_refresh(fetch_new=True)`.**
    *   **[x] Note (2025-08-25, V1.7): The date generation logic for "Strategy 12" is now identical to the "Now" button.**

---

#### Previous Sections (already completed and verified)

#### 1. Modify "Now" Button Command

*   **[x] In `tradepanel/ui/main_window.py`, locate the `ttk.Button` for "Now" within the `_setup_ui()` method.**
*   **[x] Modify its `command` to perform the following actions sequentially:**
    *   **[x] Update `self.app_state.trade_filter_start_datetime_var` to the current datetime (`datetime.now().strftime("%Y-%m-%d %H:%M:%S")`).**
    *   **[x] Call `self.trigger_manual_refresh(fetch_new=True)`.
**

#### 2. Add Strategy 12 Trigger

*   **[x] In `tradepanel/ui/main_window.py`, locate the `_on_strategy_change` method.**
*   **[x] Inside `_on_strategy_change`, add a conditional check: if `selected_strat_name` is "Strategy 12":**
    *   **[x] Update `self.app_state.trade_filter_start_datetime_var` to the current datetime.**
    *   **[x] Call `self.trigger_manual_refresh(fetch_new=True)`.
**

#### 3. Verify Existing Filter Application (No code changes, just confirmation)

*   [x] Confirm that `TradeManager.refresh_data_core` (in `tradepanel/trade_engine.py`) already retrieves `trade_filter_start_datetime_var` and `trade_restriction_var` from the `config` dictionary and passes them to the `APIClient`.
*   [x] Confirm that `APIClient.fetch_open_trades` and `APIClient.fetch_closed_trades` (in `tradepanel/api.py`) correctly accept and utilize the `start_datetime` parameter (populated by `trade_filter_start_datetime_var`) and that the `trade_restriction_var` is handled by the `TradeManager`'s internal logic when processing fetched data.

---

#### Additional Logging for Debugging Silent Shutdowns (Implemented 2025-08-24, V1.4)

*   **Phase 1: Add logging to `PivotApp` shutdown sequence:**
    *   [x] In `tradepanel/ui/main_window.py`, added `_on_app_close` method and bound it to `root.protocol("WM_DELETE_WINDOW", self._on_app_close)`.

    *   [x] Added `logger.info("Application is initiating graceful shutdown.")` at the beginning of `_on_app_close`.

    *   [x] Added `logger.info("Application graceful shutdown complete.")` at the end of `_on_app_close`.

    *   [x] Ensured `self.manager.stop_background_tasks()` is called within `_on_app_close`.


*   **Phase 2: Add logging around `TradeWorker` termination:**
    *   [x] In `tradepanel/ui/main_window.py`, in the `TradeWorker.run` method, added `logger.info("TradeWorker received stop signal. Exiting.")` when the `None` sentinel is received.

    *   [x] Added `logger.info("TradeWorker has stopped.")` after the `break` statement in `TradeWorker.run`.


*   **Phase 3: Add a top-level exception handler for the Tkinter main loop:**
    *   [x] In `tradepanel/ui/main_window.py`, wrapped the `self.root.mainloop()` call in a `try...except` block.

    *   [x] Added `logger.critical(f"Unhandled exception in main Tkinter loop: {e}", exc_info=True)` to log any caught exceptions.

    *   [x] Ensured cleanup (stopping background tasks and worker) is attempted before re-raising.


---

#### 4. Trade Restriction Update on Trade Closure

**Objective:** To dynamically update the `trade_restriction` field based on specific conditions when a trade is closed.

**Version:** 1.5
**Date:** 2025-08-25

*   **Conditions for Update:**
    *   **"none"**: No update to `trade_restriction` based on trade closure.

    *   **"update aft profit"**: Update `trade_restriction` if the closed trade generated a profit (`alt_net_return > 0`).

    *   **"update aft trades"**: Always update `trade_restriction` after any trade is closed, regardless of profit/loss.


*   **Implementation Details:**

    *   **`tradepanel/constants.py`**:

        *   [x] Add `TRADE_CLOSE_UPDATE_CONDITIONS: Final[List[str]] = ["none", "update aft profit", "update aft trades"]`.


    *   **`tradepanel/ui/main_window.py`**:

        *   [x] In `PivotAppState`, add `trade_close_update_condition_var: tk.StringVar`.

        *   [x] In `PivotAppState.get_current_config_dict()`, include `trade_close_update_condition_var`.

        *   [x] In `PivotApp._setup_ui()`, add a `ttk.Combobox` for `trade_close_update_condition_var` with the defined options.


    *   **`tradepanel/api.py`**:

        *   [x] Add `fetch_latest_closed_trade_restriction(self, product_name: str) -> Optional[str]` method to `APIClient`. This method should:

            *   Construct the API URL using `http://172.0.0.1:8000/api/vwCombined_trades_closed?product={product_name}&_sort=created.desc&_limit=1`.

            *   Execute an HTTP GET request.

            *   Parse the JSON response and extract `trade_restriction` from the first item.

            *   Return the `trade_restriction` value or `None`.


    *   **`tradepanel/trade_engine.py`**:

        *   [x] Modify `update_product_trade_restriction` method to use the value fetched by `APIClient.fetch_latest_closed_trade_restriction`.

        *   [x] Integrate with Trade Close Condition:

            *   [x] Retrieve the value of `trade_close_update_condition_var` from the configuration when a trade is closed.

            *   [x] Implement Conditional Update Logic:

                *   [x] If `trade_close_update_condition_var` is `"update aft profit"` AND the closed trade's `alt_net_return` is `> 0`, call `update_product_trade_restriction`.

                *   [x] If `trade_close_update_condition_var` is `"update aft trades"`, call `update_product_trade_restriction`.

                *   [x] If `trade_close_update_condition_var` is `"none"`, do not call `update_product_trade_restriction` based on this trade closure event.

---

#### 5. `NameError` Resolution (Implemented 2025-08-26, V64.2.12)

**Objective:** To resolve the `NameError: name 'config' is not defined` in `tradepanel/trade_engine.py`.

*   **Problem:** The `config` variable was not accessible within the `_update_product_trade_restriction` method.

*   **Solution:**
    *   **[x] Modify `_update_product_trade_restriction` signature in `tradepanel/trade_engine.py` to accept a `config` parameter.**
    *   **[x] Update all calls to `_update_product_trade_restriction` in `tradepanel/trade_engine.py` (within `refresh_data_core` and `execute_close_trade`) to pass the `config` object.**

---

#### 6. Forex Price Source in Simulation Mode (Implemented 2025-08-26, V64.2.13)

**Objective:** To ensure that forex prices are fetched from the simulation database when in simulation mode, preventing the fetching of live prices.

*   **Problem:** The `APIClient.fetch_forex_prices` method was not explicitly appending `?db=tradedb_sim` to the forex price endpoint in simulation mode, potentially leading to live price fetching.

*   **Solution:**
    *   **[x] Add `ENDPOINT_FOREX_PRICES_APP_SIM: Final[str] = f"{API_BASE_URL}/vw_000_fx_quotes?{SIM_DB_SUFFIX}"` to `tradepanel/constants.py`.**
    *   **[x] Modify `APIClient.fetch_forex_prices` in `tradepanel/api.py` to use `ENDPOINT_FOREX_PRICES_APP_SIM` when `self.is_simulation_mode` is `True`.**
