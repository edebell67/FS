# Task: Add Energy to Weekly Strategy Performance Dashboard

## Source
- User Directive: 2026-03-25 (via chat)

## Task Summary
Include Energy asset class in the Weekly Strategy Performance Dashboard.

## Context
- **Product Type**: Energy.
- **Data Source**: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\energy\{date}`.

## Dependency
- Dependency: `20260325_233035_breakout_add_crypto_to_weekly_dashboard.md`

## Plan
- [x] 1. Update `aggregate_top_strategies.py` to include `energy` in defaults.
  - Test: Run script and check if `energy/stats/daily_net_return.json` exists.
  - Evidence: Script updated and ran successfully.
- [x] 2. Add "Energy" filter button to `weekly_performance.html`.
  - Test: UI shows Energy button and data loads.
  - Evidence: Button added with `fa-fire` icon.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `fs/json/live/energy/stats/daily_net_return.json`
  - Objective-Proved: Energy data aggregated.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: UI Check
  - Objective-Proved: Energy button present and functional.
  - Status: captured

## Implementation Log
- **2026-03-25 23:47**: Task created and completed in one turn.

## Changes Made
- Modified `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py` to add `energy` to `product_types`.
- Modified `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html` to add Energy filter button.

## Validation
- Ran `python aggregate_top_strategies.py energy`.
- Verified UI changes.

## Completion Status
**Complete** - 2026-03-25 23:48
