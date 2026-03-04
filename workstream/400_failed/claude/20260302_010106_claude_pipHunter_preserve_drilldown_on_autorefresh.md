# Preserve Drilldown State on Auto-Refresh

**Source**: PipHunter Dashboard - FXPilot Landing Page

## Task Summary
When viewing trade drilldown for a strategy, the auto-refresh (every 30 seconds) causes the drilldown to close, forcing user to re-expand. The drilldown state should be preserved across data refreshes.

## Context
- **Dashboard URL**: `http://172.22.108.121:3001/`
- **Source File**: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
- **Auto-refresh interval**: 30 seconds (line 1173)

## Problem Description
1. User expands a strategy to view trade drilldown
2. Auto-refresh triggers after 30 seconds
3. Drilldown collapses/closes
4. User must re-click to expand again
5. Poor UX - interrupts analysis workflow

## Root Cause (Likely)
The `loadData` function in useEffect (line 1131-1175) resets state:
- `setSelectedId(null)` on line 1135 clears the selected strategy
- `setStrategyTrades([])` on line 1136 clears trade data

This happens on every refresh, not just date changes.

## Implementation Steps
- [ ] Only reset `selectedId` when date actually changes, not on interval refresh
- [ ] Preserve expanded strategy state across refreshes
- [ ] Re-fetch strategy trades after main data refresh if a strategy is selected
- [ ] Consider using `useRef` to track if this is initial load vs refresh

## Proposed Fix
```javascript
// Track if date changed vs just refresh
const prevDateRef = useRef(selectedDate);

useEffect(() => {
  const loadData = async () => {
    const dateChanged = prevDateRef.current !== selectedDate;
    prevDateRef.current = selectedDate;

    if (dateChanged) {
      setSelectedId(null);  // Only reset on date change
      setStrategyTrades([]);
    }
    // ... rest of fetch logic
  };
}, [selectedDate]);
```

## Validation
- Expand a strategy drilldown
- Wait for auto-refresh (30s)
- Drilldown should remain open with updated data
- Changing date should still reset the view

## Risks/Notes
- Need to handle case where selected strategy no longer exists after refresh
- May need to re-fetch strategy trades after main refresh

## Completion Status
**Pending**
