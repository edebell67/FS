# Task: Add Chart Column to Weekly Performance Dashboard

## Source
- User Directive: 2026-04-07

## Task Summary
Modify `fs\\weekly_performance.html` to add a \"Chart\" column at the end of each row. This column will contain a button that, when clicked, sends the selected strategy and product to the Multi-Chart view (`multi_chart.html`), matching the functionality found in `strategy_performance.html`.

## Context
- **Page**: `C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\weekly_performance.html`
- **Reference**: `C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\strategy_performance.html` (for CSS and handoff logic)
- **Tooling**: Uses `BroadcastChannel` and `localStorage` for cross-tab communication.

## Plan
- [x] 1. **Add UI Element**: Update the table header in `weekly_performance.html` to include a \"Chart\" column.
- [x] 2. **Add Handoff Logic**:
  - [x] Port `sendSummarySelectionToMultiChart` from `strategy_performance.html`.
  - [x] Port `buildModelName` dependency.
  - [x] Port `toLocalDateIso` or ensure date handling is consistent.
- [x] 3. **Update Rendering**: Update the `renderTable` function to generate the \"Chart\" button in the new column for every row.
- [x] 4. **Validation**:
  - [x] Verify the button appears correctly.
  - [x] Verify clicking the button opens `multi_chart.html` (or focuses an existing tab) and loads the correct strategy/product series.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-08 17:35:00

