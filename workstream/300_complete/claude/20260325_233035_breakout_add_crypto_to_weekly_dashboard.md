# Task: Add Crypto to Weekly Strategy Performance Dashboard

## Source
- User Directive: 2026-03-25

## Task Summary
Extend the Weekly Strategy Performance Dashboard to include Crypto data. This involves updating the aggregation logic, the background workers, and the UI filters.

## Context
- **Product Type**: Crypto.
- **Data Source**: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\crypto\{date}`.
- **Files Affected**:
  - `fs/tools/aggregate_top_strategies.py`
  - `fs/weekly_performance.html`
  - `fs/json/live/crypto/stats/` (new directory)

## Dependency
- Dependency: `20260325_172300_breakout_weekly_strategy_performance_screen.md` (Base implementation complete)

## Plan
- [ ] 1. Update `aggregate_top_strategies.py` to include `crypto` in the default product types list.
  - Test: Run script manually and verify `fs/json/live/crypto/stats/daily_net_return.json` is created.
  - Evidence: TBD
- [ ] 2. Add "Crypto" filter button to `weekly_performance.html`.
  - Test: Refresh page and verify Crypto button appears and loads crypto data.
  - Evidence: TBD
- [ ] 3. Verify Date Logic: Crypto trades 7 days a week, unlike Forex/Indices/Metals (5 days).
  - Test: Check if `get_trading_days` needs adjustment for crypto to show all 7 days if required, or keep 6 for consistency.
  - Evidence: TBD

## Evidence
- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `fs/json/live/crypto/stats/daily_net_return.json`
  - Objective-Proved: Crypto aggregation logic working.
  - Status: planned

- Evidence-Type: screenshot
  - Artifact: UI with Crypto filter active.
  - Objective-Proved: UI support for Crypto.
  - Status: planned

## Implementation Log
- **2026-03-25 23:30**: Task created.

## Changes Made
- None yet.

## Validation
- TBD

## Risks/Notes
- Crypto trading hours differ from traditional markets. Current dashboard logic assumes a 6-day "trading week" (looking back from target). Need to decide if Crypto should show 7 days.

## Completion Status
**Backlog** - 2026-03-25 23:30
