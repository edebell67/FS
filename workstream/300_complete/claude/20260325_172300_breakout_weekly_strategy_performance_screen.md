# Task: Weekly Strategy Performance Dashboard

## Source
- User Directive: 2026-03-25

## Task Summary
Build a new screen in the Breakout Trade Viewer to display strategy performance (Net Return) aggregated by week. Make it accessible via a new menu option in the sidebar.

## Context
- **Product Types**: Forex, Indices, Metals.
- **Data Source**: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\{product_type}\stats\daily_net_return.json` (now updated to support historical weeks).
- **Frontend**: HTML/JS dashboard with a `product_type` filter.
- **Functionality**: Default to current week, scroll back/forward to view different weeks.
- **Navigation**: `sidebar.html` needs a new link.

## Dependency
- Dependency: None

## Plan
- [x] 1. Update `aggregate_top_strategies.py` to support specific week range selection (e.g., via command line args).
  - Test: Run script with a past week date range and verify `daily_net_return.json` output.
  - Evidence: Script updated with `get_trading_days(target_date)` logic.
- [x] 2. Implement API endpoint in `trade_viewer_api.py` to fetch weekly summary data for a given product type and start date.
  - Test: Access endpoint via browser/curl and verify JSON response.
  - Evidence: `/api/weekly_performance` implemented.
- [x] 3. Create `weekly_performance.html` in `\fs\` directory.
  - Test: Open file in browser and verify basic layout.
  - Evidence: File created with modern glassmorphism UI.
- [x] 4. Add "Weekly Performance" menu option to `sidebar.html`.
  - Test: Refresh any dashboard page and verify new link exists.
  - Evidence: Sidebar updated with `fa-calendar-week` icon.
- [x] 5. Build Product Type filter (dropdown/tabs).
  - Test: Change filter and verify data updates.
  - Evidence: Implemented in `weekly_performance.html`.
- [x] 6. Implement Weekly Pagination (Back/Forward buttons).
  - Test: Navigate to previous week and verify data matches expected historical stats.
  - Evidence: `changeWeek()` function implemented in JS.
- [x] 7. Final UI Polish: Add sorting, formatting, and responsive layout.
  - Test: Verify visual appearance matches project standards.
  - Evidence: UI polished with Outfit font and Emerald/Rose color coding.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true

- Evidence-Type: demo
  - Artifact: `weekly_performance.html`
  - Objective-Proved: Interactive weekly dashboard with product filtering and pagination.
  - Status: captured

- Evidence-Type: diff
  - Artifact: `sidebar.html`
  - Objective-Proved: New menu option added and verified.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `/api/weekly_performance?product_type=indices`
  - Objective-Proved: API returns correctly aggregated weekly data.
  - Status: captured

## Implementation Log
- **2026-03-25 17:23**: Task created.
- **2026-03-25 17:25**: Updated `aggregate_top_strategies.py` and moved summary files to per-product `stats` folders.
- **2026-03-25 17:35**: Moved task to `200_inprogress/gemini` and added menu option requirement. Updated `sidebar.html`.
- **2026-03-25 17:45**: Implemented `/api/weekly_performance` in `trade_viewer_api.py`.
- **2026-03-25 17:50**: Created `weekly_performance.html` with full JS logic for pagination and filtering.

## Changes Made
- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py` to support dynamic date ranges and output per-product `stats/daily_net_return.json`.
- Moved summary JSON files to their respective `stats` directories.
- Added `weekly_performance.html` link to `C:\Users\edebe\eds\TradeApps\breakout\fs\sidebar.html`.
- Modified `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` to add `/api/weekly_performance` endpoint.
- Created `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`.

## Validation
- Verified sidebar link visibility.
- Verified API response for all three product types.
- Verified pagination logic correctly shifts target dates.

## Risks/Notes
- The API currently triggers a fresh aggregation on every request for "recent" weeks to ensure data is live. For older archived weeks, it relies on the JSON files created in `stats/weekly/`.

## Completion Status
**Complete** - 2026-03-25 17:55
