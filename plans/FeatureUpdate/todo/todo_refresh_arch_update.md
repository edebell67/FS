### 1. Plan of Approach

The current system uses a fixed-interval refresh loop. If the refresh rate is set to 5 seconds, the UI will always have a latency of up to 5 seconds, even if the data changes instantly on the server. Simply decreasing this interval to a very low number (e.g., <1 second) would be inefficient. The application would spend most of its time fetching and processing the full dataset, even when nothing has changed, which would strain the backend and potentially cause the UI to become sluggish.

A more robust and performant solution involves three key architectural enhancements:

1.  **Implement a WebSocket Client:** Instead of the application repeatedly *polling* the server for changes, the server should *push* changes to the application the moment they happen. This is the most effective way to reduce latency. A WebSocket provides a persistent, two-way communication channel perfect for this. The backend would need a corresponding WebSocket server to broadcast trade events.

2.  **Transition to Incremental Data Updates:** When an event is received via the WebSocket (e.g., a trade's P&L changes), the payload should contain only the data that has changed (a "delta"). For example, `{"event": "pnl_update", "trade_id": 123, "new_pnl": 55.50}`. The `TradeManager` would then update only that specific trade in its internal list, rather than re-fetching and re-processing the entire list of all trades.

3.  **Enable Granular UI Updates:** The UI refresh logic needs to be ableto update individual elements instead of redrawing large panels. For example, upon receiving a `pnl_update` event for trade 123, the UI should be able to find the specific label displaying the P&L for that trade and update its text directly, leaving all other UI elements untouched. This is far more efficient than a full redraw and prevents UI flickering.

By combining these three approaches, the application can display changes in near real-time with minimal performance impact, as work is only done when data actually changes.

### 2. Checklist of Changes

Here is a detailed checklist of the necessary code modifications to implement this plan.

*   **Backend Prerequisite (Informational)**
    *   A WebSocket server needs to be created on the backend that can broadcast trade events (e.g., `new_trade`, `trade_closed`, `pnl_update`). This plan assumes such an endpoint can be made available.

*   **`C:/Users/edebe/eds/algo_viewer/tradepanel/api.py`**
    *   [ ] Create a new `WebSocketClient` class responsible for connecting to the backend WebSocket server.
    *   [ ] This client will run in its own background thread, continuously listening for incoming messages.
    *   [ ] When a message (an event) is received, it will be placed into a thread-safe queue for the `TradeManager` to process.
    *   [ ] Add a comment: `# 2025-07-29: WebSocket client for real-time updates.`

*   **`C:/Users/edebe/eds/algo_viewer/tradepanel/trade_engine.py`**
    *   [ ] In `TradeManager.__init__`, initialize and start the new `WebSocketClient`.
    *   [ ] Create a new background thread in `TradeManager` that continuously checks the WebSocket message queue.
    *   [ ] Create new handler methods within `TradeManager` to process the delta updates, for example:
        *   `_handle_pnl_update(data)`: Finds the specific trade in `self.active_trades_list` and updates its P&L.
        *   `_handle_new_trade(data)`: Adds a new trade to `self.active_trades_list`.
        *   `_handle_trade_closed(data)`: Removes a trade from `self.active_trades_list` and moves it to history.
    *   [ ] After processing an event, the `TradeManager` will notify the UI to perform a *granular* update.
    *   [ ] The existing polling refresh (`refresh_data_core`) can be kept as a periodic full-sync mechanism (e.g., every 5 minutes) to ensure data consistency, but its frequency would be greatly reduced.
    *   [ ] Add a comment: `# 2025-07-29: Integrated WebSocket event handling for incremental updates.`

*   **`C:/Users/edebe/eds/algo_viewer/tradepanel/ui/main_window.py`**
    *   [ ] In `PivotApp`, modify the way active trade rows are created. Each row (or the labels within it) will need to be stored in a dictionary, keyed by `trade_id`. For example: `self.active_trade_widgets[trade_id] = {'pnl_label': pnl_label_widget, ...}`.
    *   [ ] Create new UI update methods that can be called by the `TradeManager` to perform granular updates, for example:
        *   `update_single_trade_pnl(trade_id, new_pnl)`: This method will look up the correct P&L label in the dictionary and update its text.
        *   `add_new_trade_row(trade_data)`: Creates and displays a single new row for a new trade.
        *   `remove_trade_row(trade_id)`: Finds and destroys the widgets for a closed trade.
    *   [ ] The main `_start_ui_auto_refresh` loop will be simplified or repurposed for less frequent, full UI syncs, with the primary UI updates being triggered by events from the `TradeManager`.
    *   [ ] Add a comment: `# 2025-07-29: Refactored UI for granular, event-driven updates.`

*   **`C:/Users/edebe/eds/algo_viewer/tradepanel/constants.py`**
    *   [ ] Increment the `VERSION` string to `64.4.0` (as this is a significant architectural change).
    *   [ ] Add a comment: `#2025-07-29: Planning for WebSocket integration.`

### 3. Confirmation

This is a significant architectural change that will improve performance and responsiveness. Please review the plan and confirm if you would like me to proceed.