# Task: Weekly Performance Table Layout Cleanup

Source: User request on 2026-04-09 with attached screenshot for `fs/weekly_performance.html`.

Task Type: implementation

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: true

## Task Summary
Adjust the weekly performance table layout in `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html` so all weekday columns are visible and correctly aligned under their headers, while reducing wasted width in the Product|Strategy, Live Trade, and Chart columns.

Context:
- UI file: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Screenshot reference: attached by user on 2026-04-09
- Existing related task: `C:\Users\edebe\eds\workstream\100_backlog\general\20260409_011513_breakout_weekly_perf_auto_promote_toggle.md`

Dependency: None

## Objective
Refine the table column sizing and spacing so the weekly view fits the full Monday-to-Sunday set on-page without misalignment or excessive whitespace.

## Requested Changes

- Ensure all days of the week are visible on the page under the appropriate column headings and aligned correctly.
- Resize the `Product | Strategy` column so it uses only the width it actually needs.
- Hide the `Gen Strategy` description text change so the descriptive strategy label is no longer shown in the table body.
- Keep the toggle buttons in place, but rename that column heading to `Live Trade`.
- Resize the `Live Trade` column to the minimum practical width for toggle controls only.
- Move the `Chart` button column closer to the `Live Trade` column.
- Move both the `Chart` and `Live Trade` columns closer to the `Product | Strategy` column.

## Acceptance Criteria

- The table displays every weekday column for the selected week without truncating the set off-screen in the normal desktop viewport shown in the screenshot.
- Day headers and day values remain horizontally aligned for every row.
- `Product | Strategy` no longer reserves unnecessary empty space.
- The former `Gen Strategy` text content is hidden, while the row-level toggle control remains available.
- The toggle column header reads `Live Trade`.
- The `Live Trade` and `Chart` columns are compact and visually grouped near `Product | Strategy`.
- No regression to existing toggle-button behavior or chart-button behavior.

## Validation

- Open `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html` in the usual local app flow.
- Verify the screenshot viewport can show the full weekday set with correct column alignment.
- Confirm toggle buttons still render and function.
- Confirm chart buttons still render and function.

## Execution Notes

- Prefer CSS/layout changes before changing data structures.
- Preserve existing interactions and event handlers.
- Record final validation evidence and outcome in this lifecycle file when work begins and completes.

## Execution Log

### 2026-04-09 00:05:58+01:00
- Task moved from `C:\Users\edebe\eds\workstream\100_todo` to `C:\Users\edebe\eds\workstream\200_inprogress`.
- Began implementation in `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`.

### 2026-04-09 00:12:00+01:00
- Updated table layout CSS to use compact fixed-width columns for rank, product|strategy, live-trade toggle, chart, weekday totals, and trades.
- Replaced the `Gen Strategy` header with `Live Trade`.
- Hid the visible gen-strategy description text in each row while preserving the toggle control and existing toggle handler.
- Pulled the `Chart` column closer to the toggle and strategy columns by reducing column widths and horizontal padding.

### 2026-04-09 00:16:00+01:00
- Live browser verification exposed a frontend rendering defect: the page only displayed the week start and end headers because `renderTable()` was iterating `currentData.date_range` instead of the full `currentData.date_labels` key set.
- Corrected `getSortedStrategies()` to derive the displayed day keys from `currentData.date_labels`, with fallback to row `daily` keys.

## Validation Results

### Source Validation
- Confirmed updated code markers in `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html` for:
  - `table-layout: fixed`
  - `Live Trade`
  - compact column classes (`col-live-trade`, `col-chart`, `col-day`, `col-total`, `col-trades`)
  - removal of visible gen-strategy text from row rendering

### Runtime Validation
- `Invoke-WebRequest -UseBasicParsing "http://localhost:5000/weekly_performance.html"` returned `200`.
- `Invoke-WebRequest -UseBasicParsing "http://localhost:5000/api/weekly_performance?product_type=forex&target_date=2026-04-09"` confirmed:
  - `date_range` only contains start/end dates
  - `date_labels` contains all seven weekday headers
  - row `daily` payload contains all seven weekday values

### Browser Validation
- Opened the live page in Playwright at `http://localhost:5000/weekly_performance.html`.
- Final post-load snapshot confirmed header row:
  - `#`
  - `Product | Strategy`
  - `Live Trade`
  - `Chart`
  - `Mon 04-06`
  - `Tue 04-07`
  - `Wed 04-08`
  - `Thu 04-09`
  - `Fri 04-10`
  - `Sat 04-11`
  - `Sun 04-12`
  - `Total`
  - `Trades`
- Final snapshot also confirmed row cells render as:
  - strategy label
  - toggle only in the `Live Trade` column
  - chart button in the adjacent `Chart` column
  - seven weekday values aligned under the seven weekday headers

## Outcome

- Requested table layout cleanup implemented.
- Additional frontend bug affecting weekday rendering identified and fixed during validation.
- Task validated against the live localhost page and ready to move to `300_complete`.
