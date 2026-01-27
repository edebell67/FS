# Plan: Fix Standard Dashboard Drilldown [V20260126_1305]

This plan fixes the empty trade drilldown issue in the standard dashboard caused by product name suffixes (e.g., `EURAUD_C`) not matching SQL database symbols (e.g., `EURAUD`).

## 1. Requirements
*   **Fix SQL Query**: Clean product names before querying the SQL View.
*   **Indices Check**: Ensure the mapping for "Total Net" is correct across different metrics.

## 2. Plan of Approach

### A. JavaScript Logic Update (`multi_chart.js`)
*   **`showTradeDrilldown()`**: 
    *   Strip `_C`, `_O`, etc., from the product name using `split('_')[0]`.
    *   Add defensive logging for the fetch URL to aid future debugging.
*   **Versioning**: Update reference to `V20260126_1305`.

## 3. Checklist
*   [ ] `multi_chart.js`: `showTradeDrilldown` product cleaning added.
*   [ ] `constants.py`: Version updated to `V20260126_1305`.

## 4. Verification
*   Open standard dashboard.
*   Double-click `EURAUD_C` card.
*   Confirm trade list loads correctly from SQL.
