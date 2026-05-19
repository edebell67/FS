# Plan: Sync Live Selection & L-Trade Highlighting [V20260126_1320]

This plan synchronizes the Live Trading selection functionality from V3 to all Multi-Chart dashboards and implements a new "L-Trade" visual marking process for JSON-backed charts.

## 1. Requirements
*   **Live Selection Sync**: Apply V3 `toggleLiveMode` and `loadGridLiveStatus` to Standard and V2.
*   **L-Trade Marking**: For JSON charts, identify the "Top Performer" in a Live card and highlight its actual Live trades (from SQL) on the JSON chart line.
*   **Datasource Integrity**: Charts stay JSON-backed; SQL is only used to "mark" the live points.

## 2. Plan of Approach

### A. Core Logic (`multi_chart.js`)
*   **Ranking Enhancement**: Update `applyRankSelection` to automatically toggle Live Mode for the top results if requested (or simplify to manual toggle).
*   **Leader Identification**: In `updateCharts`, for every "Live" group, calculate which model has the highest P&L.
*   **L-Trade Fetch**: For that Leader, fetch its Live trades from `vwCombined_trades_output_top200` (on-demand side-fetch).
*   **Point Marking**: 
    *   Iterate through the Leader's JSON-based dataset.
    *   If a point's timestamp matches a Live trade (within a small tolerance), set `pointStyle: 'rectRounded'`, `pointRadius: 6`, and `pointBorderColor: 'white'`.
    *   This creates a clear visual distinction for "L-Trades".

### B. V2 Sync (`multi_chart_v2.js`)
*   Apply the same "Live Leader" marking to the chart series.

### C. Versioning
*   Update `constants.py` to `V20260126_1320`.

## 3. Checklist
*   [ ] `multi_chart.js`: `updateCharts` modified to identify Best performer and fetch L-Trade markers.
*   [ ] `multi_chart.js`: Dataset configurator updated to apply `pointRadius` and styles for Live trades.
*   [ ] `multi_chart_v2.js`: Synchronized with same logic.
*   [ ] `constants.py`: Version updated.

## 4. Verification
*   Open Standard dashboard.
*   Toggle a card to `LIVE: ON`.
*   Note the "Leader" dataset.
*   Confirm white pulsing markers (or distinct points) appear on the JSON line for trades that exist as "Live" in SQL.
