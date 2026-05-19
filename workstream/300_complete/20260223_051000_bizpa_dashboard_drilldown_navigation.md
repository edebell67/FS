# Task: Improve Dashboard Drill-down Navigation (20260223_051000)

## Status
COMPLETED

## Task Summary
Correct the drill-down behavior for dashboard cards. Clicking "Invoices" or "Receipts" should navigate to the Activity tab with a pre-applied filter for that specific type, rather than showing the full unfiltered feed.

## Context
- User reported: "drill down from invoice and receipt cards shows a Activity Feed Page.. expected invoice to go to Invoice page and receipt to Receipt page"
- The app currently uses a unified "Activity" tab for all transactions.

## Sub-tasks
- [x] Logic: Added `activityTypeFilter` state to `App.jsx` and `App.tsx`.
- [x] UI (Web): Updated `renderActivity` to filter items based on `activityTypeFilter`.
- [x] UI (Web): Added a "Show All" button when a filter is active in the Activity tab.
- [x] UI (Web): Updated dashboard card click handlers to set the appropriate filter.
- [x] UI (Web): Ensured clicking "Activity" in the bottom nav resets the filter to "All".
- [x] Mobile: Ported the same filtered drill-down logic to the mobile app.
- [x] Verification: Confirmed "Invoices" card shows only invoices in the activity feed.

## Implementation Log
- [2026-02-23 05:10] Task created.
- [2026-02-23 05:15] Implemented filtered activity logic in Web `App.jsx`.
- [2026-02-23 05:25] Implemented filtered activity logic in Mobile `App.tsx` and restored the performance grid.
- [2026-02-23 05:35] Triggered new production build v1.1.2.
- [2026-02-23 05:55] **Build Finished Successfully.**

## Completion Status
COMPLETED (2026-02-23 06:00)
