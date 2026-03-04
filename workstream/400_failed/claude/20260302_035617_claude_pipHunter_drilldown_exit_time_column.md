# Add Exit Time Column to Drilldown Trades

**Source**: User request

## Task Summary
Add an exit time column to the trades table displayed in the drilldown modal of the FXPilot dashboard.

## Context
- **Dashboard URL**: `http://172.22.108.121:3001/`
- **Frontend File**: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
- **API Endpoint**: `/api/strategy-trades` in `server.py`

## Current State
The drilldown modal shows trades with columns including:
- Trade ID
- Direction
- Entry Time
- Entry Price
- Exit Price
- Exit Reason
- P&L Pips
- Net Return
- Status

**Missing**: Exit Time column

## Implementation
1. Locate the drilldown modal trades table in `forex-dashboard_1.jsx`
2. Add "Exit Time" column header
3. Add exit_time data cell for each trade row
4. Format the time appropriately (same format as Entry Time)
5. Handle null/empty values for open trades

## API Data
The `/api/strategy-trades` endpoint already returns `exit_time` field for each trade:
```json
{
  "exit_time": "2026-02-27T22:00:50.308274",
  ...
}
```

## Validation
- [ ] Exit Time column visible in drilldown modal
- [ ] Times displayed in readable format
- [ ] Open trades show empty/dash for exit time
- [ ] Column aligns properly with other columns

## Completion Status
**Pending**
