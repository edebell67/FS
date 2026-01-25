# Plan: Replace Alt Net Columns with Win Percentages in Strategy Performance

## Goal Description
Replace the `buy alt_net` and `sell alt_net` columns in the `strategy_performance.html` table with `buyPercent` and `sellPercent`. These values should be sourced from the `_summary_net.json` file, which contains pre-calculated profitability percentages based on the `summary_net_generator.py` logic.

## User Review Required
> [!IMPORTANT]
> This change introduces a dependency on `_summary_net.json` for the Strategy Performance page. Ensure `summary_net_generator.py` is running and generating this file correctly for the selected date and mode. The columns `buy alt_net` and `sell alt_net` will be removed and replaced.

## Proposed Changes

### Trade App API
#### [MODIFY] [trade_viewer_api.py](file:///c:/Users/edebe/eds/TradeApps/breakout/trade_viewer_api.py)
*   Add a new endpoint `/api/summary_net` that serves the `_summary_net.json` file for a given `mode` and `date`. This mirrors the existing `/api/top_one` endpoint.

### Trade App Frontend
#### [MODIFY] [strategy_performance.html](file:///c:/Users/edebe/eds/TradeApps/breakout/strategy_performance.html)
*   **Table Headers**: Rename `buy alt_net` to `buyPercent` and `sell alt_net` to `sellPercent`.
*   **Data Loading**:
    *   Update `loadStats()` to fetch data from the new `/api/summary_net` endpoint in parallel with `/api/trades`.
    *   Store the fetched summary data in a global variable `summaryData`.
*   **Data Processing (`processTrades`)**:
    *   Integrate `summaryData` into the aggregation logic.
    *   For each strategy/product combination, look up the corresponding entry in `summaryData.strategies`.
    *   Extract the latest `buyPercent` and `sellPercent` from the time-series array (using the last element).
    *   Populate `s.buy_pct` and `s.sell_pct` in the stats object.
*   **Rendering (`renderTable`)**:
    *   Update the table row HTML to display `s.buy_pct` and `s.sell_pct` instead of `buy_alt` and `sell_alt`.
    *   Update cell classes/styling as appropriate (e.g., standard numeric display).
*   **Sorting (`doSort`)**:
    *   Update the sort keys to use `buy_pct` and `sell_pct`.

### Configuration
#### [MODIFY] [constants.py](file:///c:/Users/edebe/eds/TradeApps/breakout/constants.py)
*   Update version to `V20260115_1020`.

## Verification Plan

### Automated Tests
*   Verify the `/api/summary_net` returns the correct JSON content for strict and live modes.

### Manual Verification
1.  Open `strategy_performance.html`.
2.  Select "Live" mode and today's date.
3.  Verify the table shows "buyPercent" and "sellPercent" columns.
4.  Compare the values in the table with the values in `_summary_net.json` to ensure they match.
5.  Test sorting on the new columns.
6.  Test "Sim" mode if available.
