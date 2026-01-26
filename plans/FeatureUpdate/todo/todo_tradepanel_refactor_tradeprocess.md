# Gemini Coder - Plan for TradePanel Refactoring (Centralized Trade Execution)

This document outlines the plan to refactor TradePanel's internal flow to centralize trade execution through TradeEngine's API.

## 1. Understanding of Requirements

The core requirement is to shift trade execution responsibility from TradePanel to TradeEngine. TradePanel will no longer directly create or close trades. Instead, it will send "trade instruction" messages to TradeEngine via a new API endpoint. TradePanel will then consume trade status updates (open and closed trades) from TradeEngine's existing APIs to maintain its internal state and update its UI.

**Key Objectives:**
*   TradePanel issues trade-execution instructions to TradeEngine.
*   TradePanel maintains full visibility over the life-cycle of trades it instructed TradeEngine to execute.
*   Existing analytics, dashboards, and strategy-selection features in TradePanel are preserved.
*   New API endpoints and message formats for the new flow are defined.
*   An MVP feature set for a new web/mobile client (plugging into the same APIs) is defined.

**Out of Scope:**
*   Changes to TradeEngine's core signal generation or risk engine (except for the new instruction endpoint).
*   Broker/order-routing logic (remains inside TradeEngine).

## 2. Plan of Approach

**Objective:** Refactor TradePanel to centralize trade execution through TradeEngine via a new API-driven flow.

### Phase 1: Define API Contracts and Client-Side API Calls

*   **`tradepanel/constants.py`**:
    *   [ ] Add `ENDPOINT_TRADE_INSTRUCTION: Final[str] = f"{API_BASE_URL}/trade/instruction"`.
    *   [ ] Add `ENDPOINT_GET_OPEN_TRADES_NEW: Final[str] = f"{API_BASE_URL}/trades/open_new"`.
    *   [ ] Add `ENDPOINT_GET_CLOSED_TRADES_NEW: Final[str] = f"{API_BASE_URL}/trades/closed_new"`.
    *   [ ] Add `ENDPOINT_ACTIVE_TRADES_SESSION: Final[str] = f"{API_BASE_URL}/vw_106_active_trades"`.
    *   [ ] Add `ENDPOINT_CLOSED_TRADES_SESSION: Final[str] = f"{API_BASE_URL}/vw_107_closed_trades"`.

*   **`tradepanel/api.py`**:
    *   [ ] Add a new method `send_trade_instruction` to send trade execution requests to TradeEngine.
    *   [ ] Add new methods `fetch_open_trades_new` and `fetch_closed_trades_new` to retrieve trade lists from TradeEngine. These will be used by TradePanel's TradeManager to update its internal state.
    *   [ ] Add `fetch_active_trades_session(self, session_id: str) -> pd.DataFrame`.
    *   [ ] Add `fetch_closed_trades_session(self, session_id: str) -> pd.DataFrame`.

### Phase 2: Refactor TradePanel's TradeManager to be a Client of TradeEngine's API

*   **`tradepanel/strategies/base.py`**:
    *   [ ] Update `TradeManagerInterface` to replace `execute_automated_buy_trade` and `execute_automated_sell_trade` with `send_trade_instruction`.

*   **`tradepanel/trade_engine.py`**:
    *   [ ] Modify `TradeManager.refresh_data_core()`:
        *   Change `self.api_client.fetch_open_trades()` and `self.api_client.fetch_closed_trades()` calls to `self.api_client.fetch_open_trades_new()` and `self.api_client.fetch_closed_trades_new()`. This makes TradePanel's TradeManager a client of TradeEngine's trade state.
        *   After fetching, update `self.active_trades_list` and `self.session_closed_trade_history` based on the data received from the API. This is crucial for TradePanel to maintain visibility.
        *   **NEW:** Update the data fetching logic for `self.active_trades_list` and `self.session_closed_trade_history` to use `self.api_client.fetch_active_trades_session(self.session_guid)` and `self.api_client.fetch_closed_trades_session(self.session_guid)` respectively. This will replace the previous `fetch_open_trades_new` and `fetch_closed_trades_new` for populating the main trade section.
    *   [ ] Modify `TradeManager._check_and_trigger_stop_loss_profit_target()`:
        *   Replace direct calls to `self.execute_close_trade()` with calls to `self.send_trade_instruction()` (for closing trades).
    *   [ ] Add a new method `send_trade_instruction()` to `TradeManager`. This method will act as the intermediary, calling `api_client.send_trade_instruction()`. The actual execution (`execute_automated_buy_trade`/`sell_trade`) will happen on the `TradeEngine` side (which is assumed to be the external API server).
    *   [ ] Modify `TradeManager.clear_all_trades_data()`:
        *   This will iterate through active trades and send a close instruction for each.

### Phase 3: Update TradePanel's UI and Strategies to Use the New Flow

*   **`tradepanel/strategies/*.py` (all strategy files)**:
    *   [ ] Modify `evaluate()` methods to replace direct calls to `self.trade_manager.execute_automated_buy_trade()` and `self.trade_manager.execute_automated_sell_trade()` with `self.trade_manager.send_trade_instruction()`.
    *   [ ] Adjust parameters to match the new `send_trade_instruction` signature (e.g., explicitly pass `action="buy"` or `action="sell"`).
    *   [ ] Replace direct calls to `self.trade_manager.execute_close_trade()` with `self.trade_manager.send_trade_instruction()` (for closing trades).

*   **`tradepanel/ui/main_window.py`**:
    *   [ ] Modify `execute_manual_buy_trade()` and `execute_manual_sell_trade()`:
        *   Replace direct calls to `self.manager.execute_automated_buy_trade()` and `self.manager.execute_automated_sell_trade()` with `self.manager.send_trade_instruction()`.
    *   [ ] Modify `execute_manual_close_trade()`:
        *   Replace direct calls to `self.manager.execute_close_trade()` with `self.manager.send_trade_instruction()` (for closing trades).
    *   [ ] `update_product_trade_panel()` will now display data from `self.manager.active_trades_list` and `self.manager.session_closed_trade_history` which are populated by API calls. No direct changes to this method's logic, but its data source changes.

## 3. List of Changes (Checklist)

**`tradepanel/constants.py`**
- [x] Add `ENDPOINT_TRADE_INSTRUCTION`
- [x] Add `ENDPOINT_GET_OPEN_TRADES_NEW`
- [x] Add `ENDPOINT_GET_CLOSED_TRADES_NEW`
- [ ] Add `ENDPOINT_ACTIVE_TRADES_SESSION`
- [ ] Add `ENDPOINT_CLOSED_TRADES_SESSION`

**`tradepanel/api.py`**
- [x] Add `send_trade_instruction` method.
- [x] Add `fetch_open_trades_new` method.
- [x] Add `fetch_closed_trades_new` method.
- [ ] Add `fetch_active_trades_session` method.
- [ ] Add `fetch_closed_trades_session` method.

**`tradepanel/strategies/base.py`**
- [x] Modify `TradeManagerInterface` to replace `execute_automated_buy_trade` and `execute_automated_sell_trade` with `send_trade_instruction`.

**`tradepanel/trade_engine.py`**
- [x] Modify `TradeManager.refresh_data_core` to use `api_client.fetch_open_trades_new` and `api_client.fetch_closed_trades_new`.
- [x] Modify `TradeManager._check_and_trigger_stop_loss_profit_target` to use `self.send_trade_instruction` for closing trades.
- [x] Add `TradeManager.send_trade_instruction` method.
- [x] Modify `TradeManager.clear_all_trades_data` to send close instructions for each trade.

**`tradepanel/strategies/s00b.py`**
- [x] Replace `tm.execute_automated_buy_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s00bs.py`**
- [x] Replace `self.trade_manager.execute_automated_buy_trade` and `self.trade_manager.execute_automated_sell_trade` with `self.trade_manager.send_trade_instruction`.
- [x] Replace `self.trade_manager.execute_close_trade` with `self.trade_manager.send_trade_instruction`.

**`tradepanel/strategies/s00s.py`**
- [x] Replace `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s01.py`**
- [x] Replace `tm.execute_automated_sell_trade`, `tm.execute_automated_buy_trade`, and `tm.execute_close_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s012.py`**
- [x] Replace `tm.execute_automated_sell_trade`, `tm.execute_automated_buy_trade`, and `tm.execute_close_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s02.py`**
- [x] Replace `tm.execute_automated_sell_trade` and `tm.execute_automated_buy_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s03.py`**
- [x] Replace `tm.execute_automated_buy_trade` and `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s04.py`**
- [x] Replace `tm.execute_automated_buy_trade`, `tm.execute_automated_sell_trade`, and `tm.execute_close_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s05.py`**
- [x] Replace `tm.execute_automated_buy_trade` and `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s06.py`**
- [x] Replace `tm.execute_close_trade`, `tm.execute_automated_buy_trade`, and `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`. (This is where the last operation failed, so this file and subsequent ones are pending).

**`tradepanel/strategies/s061.py`**
- [x] Replace `tm.execute_automated_buy_trade` and `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s07.py`**
- [x] Replace `tm.execute_close_trade`, `tm.execute_automated_buy_trade`, and `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s08.py`**
- [x] Replace `tm.execute_automated_buy_trade` and `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s08p.py`**
- [x] Replace `tm.execute_close_trade`, `tm.execute_automated_buy_trade`, and `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s08r.py`**
- [x] Replace `tm.execute_close_trade`, `tm.execute_automated_buy_trade`, and `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s08s.py`**
- [x] Replace `tm.execute_close_trade`, `tm.execute_automated_buy_trade`, and `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s08sr.py`**
- [x] No direct trade execution calls, so no changes needed here.

**`tradepanel/strategies/s09.py`**
- [x] Replace `tm.execute_automated_buy_trade` with `tm.send_trade_instruction`.
- [x] Replace `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s10.py`**
- [x] Replace `tm.execute_automated_buy_trade` with `tm.send_trade_instruction`.
- [x] Replace `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s11.py`**
- [x] Replace `tm.execute_close_trade` with `tm.send_trade_instruction`.
- [x] Replace `tm.execute_automated_buy_trade` with `tm.send_trade_instruction`.
- [x] Replace `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/strategies/s11p.py`**
- [x] Replace `tm.execute_close_trade` with `tm.send_trade_instruction`.
- [x] Replace `tm.execute_automated_buy_trade` with `tm.send_trade_instruction`.
- [x] Replace `tm.execute_automated_sell_trade` with `tm.send_trade_instruction`.

**`tradepanel/ui/main_window.py`**
- [x] Modify `execute_manual_buy_trade` to use `self.manager.send_trade_instruction`.
- [x] Modify `execute_manual_sell_trade` to use `self.manager.send_trade_instruction`.
- [x] Modify `execute_manual_close_trade` to use `self.manager.send_trade_instruction`.
- [x] `update_product_trade_panel` will now display data from `self.manager.active_trades_list` and `self.manager.session_closed_trade_history` which are populated by API calls. No direct changes to this method's logic, but its data source changes.

## 4. MVP Feature Set for New Web/Mobile Client

The new web/mobile client will act as a user interface to the TradeEngine, leveraging the same API endpoints that TradePanel now uses.

**Core Features (MVP):**
1.  **Real-time Trade Display:**
    *   View a list of all currently open trades (product, type, quantity, entry price, current P&L).
    *   View a list of recently closed trades (product, type, quantity, entry/exit prices, final P&L, close reason).
    *   Filter trades by product.
2.  **Manual Trade Execution:**
    *   Buttons to manually initiate BUY and SELL trades for a selected product and quantity.
    *   Input fields for quantity and commission.
3.  **Trade Management:**
    *   Ability to manually close an open trade.
4.  **Basic Performance Overview:**
    *   Display total P&L for open trades.
    *   Display total P&L for closed trades.
5.  **Strategy Selection & Configuration (Read-Only for MVP):**
    *   View the currently active strategy.
    *   View the current configuration parameters of the active strategy (e.g., stop-loss, profit target, thresholds).
    *   (Future: Ability to change strategy and parameters via UI).
6.  **Connection Status Indicator:**
    *   Indicate whether the client is successfully connected to the TradeEngine API.

**Technical Considerations:**
*   The client will make HTTP requests to the TradeEngine API endpoints.
*   Data will be received in JSON format.
*   Authentication/Authorization (future consideration, not MVP).

## 5. API Server Integration: `tbl_trade_links` and Trade Details UI

This section details the integration with the `tbl_trade_links` table in the API server and the subsequent UI update to display trade details.

*   **Task 5.1: API Server `tbl_trade_links` Integration (Backend)**
    *   [ ] Ensure the API server function receiving the payload from `tradepanel.api.send_trade_instruction` correctly maps and inserts data into `tbl_trade_links` with the following fields:
        *   `session_id` (from `instruction_payload['session_id']`)
        *   `message_id` (from `instruction_payload['instruction_id']`)
        *   `product` (from `instruction_payload['product']`)
        *   `action` (from `instruction_payload['action']`)
        *   `trade_quantity` (from `instruction_payload['quantity']`)
        *   `executed` (default to 0, managed by TradeEngine)
        *   `created` (default to `SYSUTCDATETIME()`, managed by DB)
        *   `guid` (from `instruction_payload['trade_id']` for close, or `NEWID()` for open, managed by DB/TradeEngine)
        *   `send_order` (derived from `config.get('csv_gen_rule_var')` and `config.get('apply_csv_rule_at_signal_level')` in `TradeManager.send_trade_instruction`)
        *   `json_field` (captures all other details from `instruction_payload['config']`, `entry_log_details`, `close_log_details`, etc.)

*   **Task 5.2: UI Update for Trade Details (Replacing `tksheet`)**
    *   [ ] **Define New API Endpoint for Trade Details:**
        *   Add `ENDPOINT_TRADE_DETAILS: Final[str] = f"{API_BASE_URL}/trade/details"` to `tradepanel/constants.py`.
    *   [ ] **Implement `fetch_trade_details` in `APIClient`:**
        *   Add a new method `fetch_trade_details(self, trade_id: int) -> Optional[Dict[str, Any]]` to `tradepanel/api.py` to fetch specific trade details from `ENDPOINT_TRADE_DETAILS`.
    *   [ ] **Modify `update_product_trade_panel` in `main_window.py`:**
        *   Replace the `tksheet` widget (`self.product_trade_history_sheet`) with a `tk.Text` widget or similar text-based display for trade history.
        *   Update the logic to fetch trade details using `self.manager.api_client.fetch_trade_details()` for each trade in the history.
        *   Display the fetched trade details in a formatted text list within the new widget. (Further granular details for display formatting will be addressed in a subsequent step).