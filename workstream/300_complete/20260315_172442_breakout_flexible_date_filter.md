# TASK: Implement Flexible Date Filter Options

**Workstream:** UI - ENHANCEMENTS
**Epic:** Kanban Dashboard
**Priority:** 2
**Status:** [x] Implemented in kanban_dashboard.py

---

## Purpose

Replace the single date picker with a more flexible date filtering system that allows users to quickly select common date ranges (this week, last week, this month, etc.) in addition to custom date range selection.

## Input

- Current single-date filter implementation
- User requirement for quick date range presets
- Existing data query/filtering logic

## Output

- Enhanced date filter UI component with:
  - Preset buttons/dropdown for common ranges
  - Custom date range picker (start date - end date)
  - Clear visual indication of selected range

## Requirements

### Preset Date Ranges
- **Today** - Current day only
- **Yesterday** - Previous day
- **This Week** - Monday to current day (or Sunday to current day based on locale)
- **Last Week** - Previous full week (Mon-Sun)
- **This Month** - 1st of current month to current day
- **Last Month** - Full previous month
- **Last 7 Days** - Rolling 7-day window
- **Last 30 Days** - Rolling 30-day window
- **Custom Range** - User-defined start and end dates

### UI/UX Considerations
1. Default selection should be "Today" or "This Week" (configurable)
2. Preset buttons should be clearly visible and quickly accessible
3. Custom range should show two date pickers (From / To)
4. Selected range should be displayed clearly in the UI
5. Filter should apply immediately on selection (or via Apply button)

### Technical Requirements
1. Update data fetching to accept date range (startDate, endDate) instead of single date
2. Ensure backend/API supports date range queries
3. Persist user's last selected range preference (localStorage)
4. Handle timezone considerations appropriately

## Action

1. Design the date filter UI component with presets and custom range
2. Implement preset date calculation logic
3. Update API calls to pass date range parameters
4. Update backend queries to filter by date range
5. Add localStorage persistence for user preference
6. Test with various date ranges and edge cases

## Verification

- [ ] All preset date ranges calculate correct start/end dates
- [ ] Custom date range picker allows selection of any valid range
- [ ] Data correctly filters based on selected date range
- [ ] User's last selection persists across page refreshes
- [ ] UI clearly shows which date range is currently active
- [ ] Edge cases handled (e.g., selecting future dates, invalid ranges)

---

## Notes

### Implementation [V20260315] - Kanban Dashboard

**File:** `workstream/kanban_dashboard.py`

**Changes Made:**
1. Replaced single date input with dropdown preset selector + custom range inputs
2. Added preset options: Today, Yesterday, This Week, Last Week, This Month, Last Month, Last 7 Days, Last 30 Days, All Time, Custom Range
3. Custom range shows From/To date pickers with Apply button
4. Added localStorage persistence with key `kanban_date_range_preset`
5. Date range displayed in compact format (e.g., "15 Mar" or "10 Mar - 15 Mar")
6. Updated `/api/tasks` endpoint to accept `startDate` and `endDate` query parameters
7. Updated date filtering logic to check if file date falls within the specified range

**Key JavaScript Functions Added:**
- `calculateDateRange(preset)` - Computes start/end dates for each preset
- `applyDatePreset()` - Handles preset selection and triggers data fetch
- `applyCustomDateRange()` - Handles custom date range selection
- `updateDateRangeDisplay()` - Updates the visual display of selected range
- `initializeDateRangeFilter()` - Initializes from localStorage or defaults to "today"
- `saveDateRangePreference()` / `loadDateRangePreference()` - localStorage persistence

**API Changes:**
- `/api/tasks` now accepts `startDate` and `endDate` query parameters (YYYY-MM-DD format)
- Backward compatible with old `?date=` single date parameter
- Date range filtering compares filename timestamp (YYYYMMDD) or file modification date

**Backward Compatibility:**
- Old `?date=YYYY-MM-DD` parameter still works (treated as single-day range)
