# Task: Weekly Strategy Performance Dashboard

## Source
- User Directive: 2026-03-25

## Task Summary
Build a new screen in the Breakout Trade Viewer to display strategy performance (Net Return) aggregated by week. Make it accessible via a new menu option in the sidebar.

## Context
- **Product Types**: Forex, Indices, Metals.
- **Data Source**: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\{product_type}\stats\daily_net_return.json` (to be updated to support historical weeks).
- **Frontend**: HTML/JS dashboard with a `product_type` filter.
- **Functionality**: Default to current week, scroll back/forward to view different weeks.
- **Navigation**: `sidebar.html` needs a new link.

## Dependency
- Dependency: None

## Plan
- [ ] 1. Update `aggregate_top_strategies.py` to support specific week range selection (e.g., via command line args).
  - Test: Run script with a past week date range and verify `daily_net_return.json` output.
  - Evidence: TBD
- [ ] 2. Implement API endpoint in `trade_viewer_api.py` to fetch weekly summary data for a given product type and start date.
  - Test: Access endpoint via browser/curl and verify JSON response.
  - Evidence: TBD
- [ ] 3. Create `weekly_performance.html` in `\fs\` directory.
  - Test: Open file in browser and verify basic layout.
  - Evidence: TBD
- [x] 4. Add "Weekly Performance" menu option to `sidebar.html`.
  - Test: Refresh any dashboard page and verify new link exists.
  - Evidence: Sidebar updated.
- [ ] 5. Build Product Type filter (dropdown/tabs).
  - Test: Change filter and verify data updates.
  - Evidence: TBD
- [ ] 6. Implement Weekly Pagination (Back/Forward buttons).
  - Test: Navigate to previous week and verify data matches expected historical stats.
  - Evidence: TBD
- [ ] 7. Final UI Polish: Add sorting, formatting, and responsive layout.
  - Test: Verify visual appearance matches project standards.
  - Evidence: TBD

## Evidence
- Objective-Delivery-Coverage: 10%
- Auto-Acceptance: true

- Evidence-Type: demo
  - Artifact: `weekly_performance.html`
  - Objective-Proved: Interactive weekly dashboard
  - Status: planned

- Evidence-Type: diff
  - Artifact: `sidebar.html`
  - Objective-Proved: New menu option added.
  - Status: captured

## Implementation Log
- **2026-03-25 17:23**: Task created.
- **2026-03-25 17:25**: Updated `aggregate_top_strategies.py` and moved summary files to per-product `stats` folders.
- **2026-03-25 17:35**: Moved task to `200_inprogress/gemini` and added menu option requirement. Updated `sidebar.html`.

## Changes Made
- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py` to output per-product `stats/daily_net_return.json`.
- Moved summary JSON files to their respective `stats` directories.
- Added `weekly_performance.html` link to `C:\Users\edebe\eds\TradeApps\breakout\fs\sidebar.html`.

## Validation
- TBD

## Risks/Notes
- Need to ensure historical data is available in the `live/{product_type}/{date}` structure for older weeks.

## Completion Status
**In Progress** - 2026-03-25 17:35
