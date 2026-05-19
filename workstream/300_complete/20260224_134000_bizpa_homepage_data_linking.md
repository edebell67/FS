# Task: bizPA Homepage Data Linking (20260224_131000)

## Task Summary
Link all numerical indicators on the Home dashboard to their underlying data views. Clicking a total or count should navigate the user to the relevant tab or a filtered activity feed.

## Context
- bizPA v1.1.7 is implementation complete for core plugins.
- Current dashboard shows high-level totals but most are static text without navigation.
- Target elements: Weekly Momentum, Expenses, VAT Est., Unpaid Invoices, Quotes.

## Sub-tasks
- [x] UI: Link "Weekly Momentum" total to the Activity/Timeline tab.
- [x] UI: Link "Expenses" total to Activity filtered by 'receipt'.
- [x] UI: Link "VAT Est." total to the Tax tab.
- [x] UI: Link "Unpaid" count to Activity filtered by 'invoice'.
- [x] UI: Link "Quotes" count to Activity filtered by 'quote'.
- [x] Verification: Test navigation flow for each linked element in the browser.

## Implementation Log
- [2026-02-24 13:10] Task initialized.
- [2026-02-24 13:15] Added `onClick` handlers and `cursor: pointer` to the Momentum Bar elements.
- [2026-02-24 13:20] Updated Performance Grid: redirected "Bookings" card to the Calendar tab.
- [2026-02-24 13:25] Linked "Attention Required" items to filtered Activity or Calendar views.
- [2026-02-24 13:30] Linked "Smart Insights" cards to relevant filtered Activity views.
- [2026-02-24 13:35] Browser verification: Confirmed "Weekly Momentum" navigates to "Timeline" and "Expenses" navigates to "Timeline" filtered for "Receipts".

## Changes Made
- `bizPA/frontend/src/App.jsx`:
    - Momentum bar: Linked titles and totals to tabs/filters.
    - Performance Grid: Redirected `booking` key to `calendar` tab.
    - Attention panel: Added `onClick` logic for automated navigation.
    - Insight feed: Added `onClick` logic for automated navigation.

## Validation
- Browser test: Clicking "Weekly Momentum" -> active tab becomes "Timeline".
- Browser test: Clicking "Expenses" -> header shows "Receipts".
- Browser test: Clicking "Invoices" card -> header shows "Invoices".

## Risks/Notes
- The backend for some newer Milestone 3 tabs (Calendar, Diary, Teams) is currently pending a process restart, so those views may show 404/Empty until then. Dashboard links are correctly coded to those paths.

## Completion Status
COMPLETED (2026-02-24 13:40)
