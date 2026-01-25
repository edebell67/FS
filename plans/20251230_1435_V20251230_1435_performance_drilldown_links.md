# Plan for Commission Update and Strategy Stats Enhancement (V20251230_1435)

## 1. Understanding of Requirements
1.  **Commission Update**:
    *   Change base commission from $10 to $5 in `common.py`.
    *   Set commission to $10 for products ending in `_C` (previously $20 logic existed).
2.  **Strategy Performance Enhancement**:
    *   Enable "Total Net" column values to link to a drill-down (showing all trades).
    *   In the drill-down modal, sort trades by Entry Time in descending order.
    *   Insert an "Exit Time" column next to "Entry Time".
    *   Format "Exit Time" as `hh:mm:ss` only.

## 2. Plan of Approach
1.  **Modify `common.py`**:
    *   Update `COMMISSION_USD` default to `5.0`.
    *   Refine `calculate_pnl` to set commission to `$10` for `_C` trades.
2.  **Modify `strategy_performance.html`**:
    *   Update `renderTable` to make "Total Net" clickable.
    *   Update `showDrillDown` to:
        *   Accept `direction='all'` to show all trades for a strategy.
        *   Sort the `filtered` trade array by `entry_time` descending.
        *   Update the table header to include "Exit Time" after "Entry Time".
        *   Update the table body loop to include exit time formatted as `hh:mm:ss`.
        *   Adjust the empty state `colspan`.
3.  **Update Version**: Change `constants.py` to `V20251230_1435`.

## 3. List of Changes
*   **`TradeApps/breakout/common.py`**:
    *   [x] Change `COMMISSION_USD` default to `5.0`.
    *   [x] Update `calculate_pnl` commission logic for `_C` trades.
*   **`TradeApps/breakout/strategy_performance.html`**:
    *   [x] Make `Total Net` clickable in `renderTable`.
    *   [x] Implement `direction='all'` and descending sort in `showDrillDown`.
    *   [x] Add and format `Exit Time` column in `showDrillDown`.
*   **`TradeApps/breakout/constants.py`**:
    *   [x] Update `VERSION` to `V20251230_1435`.

## 4. Verification Plan
*   Load stats page and click a "Total Net" value.
*   Verify the modal shows Buy/Sell trades sorted by time descending.
*   Verify the new "Exit Time" column exists and shows `hh:mm:ss`.
*   Confirm commission calculations in logs/pnl if possible.
