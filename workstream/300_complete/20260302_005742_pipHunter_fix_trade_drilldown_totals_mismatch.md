# Fix Trade Drilldown Totals Mismatch

**Source**: PipHunter Dashboard - FXPilot Landing Page

## Task Summary
When drilling down into a strategy's trades, the displayed trades do not show all trades - causing the sum of displayed trade net values to not match the summarized total net shown in the leaderboard.

## Context
- **Dashboard URL**: `http://172.22.108.121:3001/`
- **API Server**: `http://172.22.108.121:5050/api`
- **Source Files**:
  - Frontend: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
  - API: `TradeApps/breakout/piphunter/landing_page/server.py`
  - Data Service: `TradeApps/breakout/piphunter/landing_page/src/api/dataService.js`

## Problem Description
1. User selects a strategy from the leaderboard (shows total_net = X)
2. Drilldown loads trades via `/api/strategy-trades` endpoint
3. Sum of displayed trades' net values ≠ X (the summarized total)
4. Some trades appear to be missing from the drilldown view

## Potential Causes
1. **API filtering issue**: `/api/strategy-trades` not returning all trades for the strategy
2. **Date mismatch**: Trades from previous days not included
3. **File scanning issue**: Not all `*_cld.json` files being scanned
4. **Product filter**: Trades filtered by product when they shouldn't be
5. **Pagination**: Trades being paginated but not all pages loaded
6. **Data source mismatch**: Summary using different data source than drilldown

## Investigation Steps
- [x] Compare trade count from `_top20.json` vs `/api/strategy-trades` response
- [x] Check if all `*_cld.json` files are being scanned for the strategy
- [x] Verify product parameter handling in API
- [x] Check if live trades are included in drilldown

## Root Cause
**Duplicate trades**: API was returning trades from both `*_cld.json` (closed trades) AND `_live_trades.json` without deduplication. The same trade_id appeared twice when a trade existed in both files.

Example: Strategy `breakout_R_Rev_2_tp20.0_sl5.0` with product `CAD`
- `_top20.json`: 12 trades, total_net 780.00
- API before fix: 17 trades (5 duplicates)
- API after fix: 12 trades, sum 780.00

## Implementation Log

### 2026-03-02 01:15
- Identified duplicate trades in API response (17 vs expected 12)
- Found trade_ids 139-143 appearing twice (once from cld files, once from live_trades)
- Added deduplication logic to `server.py` lines 201-211
- Deduplication prefers closed trades (with exit_time) over live versions

## Changes Made
- **File**: `TradeApps/breakout/piphunter/landing_page/server.py`
- **Lines**: 201-211 (added deduplication block)
- **Logic**: Uses dict keyed by trade_id, prefers version with exit_time

## Validation
- [x] Trade count: 12 (matches _top20.json)
- [x] Sum net_return: 780.00 (matches _top20.json total_net)
- [x] API tested and verified working

## Completion Status
**COMPLETE** - 2026-03-02
