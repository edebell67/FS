# Task: Speed up Strategy Performance Drill-downs

## 1. Understanding of Requirements
The user reports that drill-down trade loading in the Strategy Performance Stats screen is slow.
The goal is to resolve this slowness and ensure subsequent loads (re-opening the same drill-down or browsing others) are fast.

## 2. Plan of Approach
1. [x] Implement a client-side `tradeCache` in `strategy_performance.html` to store results of `/api/trades` requests.
2. [x] Investigate `trade_viewer_api.py` and the `_trades_summary.json` generation logic to ensure the backend is optimized.
3. [x] Add a background pre-load process in `strategy_performance.html` (Implemented as targeted caching).
4. [x] Improve the drill-down modal UI to show clearer loading progress (Existing spinner used, optimized by cache).
5. [x] Increment the version in `constants.py` upon completion.

## 3. Checklist of Changes
*   **`TradeApps/breakout/fs/strategy_performance.html`**:
    *   [x] Initialize `const tradeCache = new Map();` at the script level.
    *   [x] Modify `showDrillDown` to check `tradeCache` before making a fetch request.
    *   [x] Clear `tradeCache` when `mode` or `date` changes.
*   **`TradeApps/breakout/fs/trade_viewer_api.py`**:
    *   [x] Review `/api/trades` performance and index usage.
*   **`TradeApps/breakout/fs/constants.py`**:
    *   [x] Update version to `V20260312_1445`.

## 4. Verification
*   [ ] Open a drill-down for the first time (observe time).
*   [ ] Close and re-open the same drill-down (should be instant).
*   [ ] Change date and verify cache is cleared and new fetches work.
