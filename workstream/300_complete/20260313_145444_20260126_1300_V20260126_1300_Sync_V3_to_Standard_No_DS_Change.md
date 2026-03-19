# Plan: Sync V2/V3 Functionality to Multi-Chart (Standard) [V20260126_1300]

This plan synchronizes all premium investigative and UI features from Multi-Chart V2 & V3 to the standard dashboard, while strictly maintaining the JSON-based datasource for the primary charts.

## 1. Requirements
*   **Aesthetics**: Sync CSS for live trading pulses, premium legends, and the detailed loading progress bar.
*   **Functionality**:
    *   **Live Sync**: Indicate which models are currently "Live" in the legend using a pulsing dot.
    *   **Advanced Ranking**: Support ranking by "Trade Count" as well as "Total Net".
    *   **Drilldown**: 9-column investigative modal with sorting (Restored "Result" column).
    *   **Loading UX**: Animated loading bar for data fetches.
*   **Constraint**: NO change to the primary chart datasource (maintained as JSON).

## 2. Plan of Approach

### A. UI Refinement (`multi_chart.html`)
*   **CSS**: Inject the Live Trading styles, refined Legend styles, and Loading Overlay styles.
*   **Controls**: Add the `Rank By` selector to the Management section.
*   **Loading**: Add the `loading-overlay` and `loader-bar` structure.

### B. Logic Synchronization (`multi_chart.js`)
*   **Live Grid Sync**: Implement `loadGridLiveStatus()` to fetch the active trading list from the SQL backend.
*   **Legend Indicators**: Update the chart card generation to check the live status and add the pulse animation.
*   **Ranking**: Update `applyRankSelection` to look at `trade_count` when requested.
*   **Drilldown**: Re-implement the on-demand SQL fetch for the drilldown modal (9 columns, functional sorting).
*   **Loading UX**: Hook `showLoader` and `hideLoader` into the fetch cycle.

## 3. Checklist
*   [ ] `multi_chart.html` CSS and UI components added.
*   [ ] `multi_chart.js` `loadGridLiveStatus` added.
*   [ ] `multi_chart.js` legend item live indicators added.
*   [ ] `multi_chart.js` Advanced Ranking (by trades) added.
*   [ ] `multi_chart.js` Loading bar logic added.
*   [ ] `constants.py` version updated to `V20260126_1300`.

## 4. Verification
*   Confirm charts still load from JSON.
*   Confirm live models show a pulsing dot in the legend.
*   Confirm double-click opens the detailed drilldown.
*   Confirm ranking by "Trades" works.
