# Dashboard Performance and Drilldown Data Fix

**Source**: PipHunter Dashboard - FXPilot Landing Page

## Task Summary
Two issues reported after initial drilldown fix:
1. Very slow loading of dashboard
2. Trades displayed in drilldown still not matching summary data in some cases

## Context
- **Dashboard URL**: `http://172.22.108.121:3001/`
- **API Server**: `http://172.22.108.121:5050/api`
- **Previous Fix**: Added trade deduplication in server.py (completed task 20260302_005742)
- **Source Files**:
  - API: `TradeApps/breakout/piphunter/landing_page/server.py`
  - Frontend: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
  - Data Service: `TradeApps/breakout/piphunter/landing_page/src/api/dataService.js`

## Issue 1: Slow Dashboard Loading

### Potential Causes
1. API endpoints taking too long to respond
2. Multiple parallel API calls blocking each other
3. Large JSON payloads being transferred
4. File scanning in server.py too slow (glob patterns)
5. No caching - every request scans files fresh

### Investigation Steps
- [ ] Profile API response times for each endpoint
- [ ] Check Flask server logs for slow requests
- [ ] Measure payload sizes
- [ ] Check if file scanning can be optimized

## Issue 2: Drilldown Still Not Matching Summary

### Potential Causes
1. Deduplication not catching all cases
2. Different strategies/products have different data patterns
3. `_top20.json` calculated differently than trade aggregation
4. Trade files from multiple dates not being included
5. Live trades being counted differently

### Investigation Steps
- [ ] Test with multiple strategies to find failing cases
- [ ] Compare exact calculation in _top20.json generation vs API aggregation
- [ ] Check if issue is specific to certain strategies/products
- [ ] Verify deduplication logic handles all edge cases

## Implementation Steps
- [ ] Add timing logs to API endpoints
- [ ] Optimize file scanning (cache file list, use more specific globs)
- [ ] Add API response caching for expensive operations
- [ ] Fix any remaining drilldown calculation mismatches
- [ ] Consider pagination for large trade lists

## Validation
- Dashboard loads within 3 seconds
- All drilldown totals match summary data exactly
- No duplicate trades in any drilldown view

## Risks/Notes
- May need to refactor how _top20.json is generated to ensure consistency
- Caching needs invalidation strategy

## Completion Status
**Pending**
