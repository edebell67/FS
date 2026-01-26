# Dashboard Enhancements Plan (2025-09-30)

This document outlines the plan to implement dashboard enhancements for the Algo Zone Viewer, including column visibility, conditional highlighting, and new trend-based styling.

## 1. Understanding of Requirements

The goal is to modify the 'algo_zone_viewer' dashboard to improve readability and provide quick visual cues for changes in key metrics.

## 2. Plan of Approach

1.  **CSS Modifications (style.css)**: Hide specified columns using 'display: none;'.
2.  **JavaScript Modifications (script.js)**: Implement conditional highlighting and trend-based styling for relevant cells.
    *   Introduce a helper function for applying base highlighting (green/red for positive values).
    *   Modify updateZoneCountsTable to store previous values for comparison.
    *   Modify updateRowCells to compare current and previous values for trend-based styling (bold/deep green for increase, bold/deep red for decrease).
    *   Modify createRowElement to ensure initial rendering is correct.

## 3. List of Changes

*   **'algo_zone_viewer/static/style.css'**:
    *   [x] Add CSS rules to hide "Beyond Target (Buy)" (2nd column) and "Beyond Target (Sell)" (13th column).
    *   [x] Add CSS rules to hide "Beyond Stop (Buy)" (6th column) and "Beyond Stop (Sell)" (9th column).
    *   [x] Add new CSS classes for deep green and deep red bold fonts.

*   **'algo_zone_viewer/static/script.js'**:
    *   [x] Modify updateZoneCountsTable to store the current item data in rowElement.dataset.previousItem for comparison in subsequent updates.
    *   [x] Modify createRowElement to ensure rowElement.dataset.previousItem is set on initial row creation.
    *   [x] Implement a helper function applyHighlighting to apply base green/red highlighting for positive values.
    *   [x] Modify createRowElement to call applyHighlighting for darkgreen_buy, green_buy, darkgreen_sell, and green_sell.
    *   [x] Modify updateRowCells to call applyHighlighting for darkgreen_buy, green_buy, darkgreen_sell, and green_sell.
    *   [x] **New**: In updateRowCells, implement logic to compare current darkgreen_buy and darkgreen_sell values with their previousItem counterparts.
    *   [x] **New**: Apply a new CSS class (e.g., highlight-deep-green-bold) to darkgreen_buy or darkgreen_sell cells if the current value is greater than the previous value.
    *   [x] **New**: Apply a new CSS class (e.g., highlight-deep-red-bold) to darkgreen_buy or darkgreen_sell cells if the current value is less than the previous value.
    *   [x] Ensure existing highlighting logic for red_buy and red_sell remains intact.
    *   [x] **New**: Display per-row up/down arrows in dark green columns by comparing each timestamp with its immediate predecessor.

## 4. Verification

*   Visually inspect the dashboard to confirm:
    *   Specified columns are hidden.
    *   Correct cells are highlighted green/red based on positive values.
    *   'Dark Green' cells show bold deep green/red font based on value increase/decrease, with accompanying arrows indicating direction versus the prior timestamp.

## 5. Rollback Plan

*   Revert style.css to its state before these changes.
*   Revert script.js to its state before these changes.

---
