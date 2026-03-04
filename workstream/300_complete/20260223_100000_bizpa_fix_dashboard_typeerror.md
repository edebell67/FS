# Task: Bug Fix - TypeError in Dashboard Totals Calculation (20260223_100000)

## Status
COMPLETED

## Sub-tasks
- [x] Bug (Web): Updated `App.jsx` to use `parseFloat(i.amount)` in the `reduce` function for Invoices.
- [x] Bug (Web): Confirmed that `statsController` already uses `parseFloat` for summary data.
- [x] Mobile Audit: Verified that `App.tsx` (mobile) already uses `parseFloat(i.amount)` correctly.
- [x] Verification: Dashboard now loads without `TypeError`.

## Implementation Log
- [2026-02-23 10:00] Task created.
- [2026-02-23 10:05] Fixed string-to-number coercion bug in `App.jsx`.
- [2026-02-23 10:10] Bumped web version to v1.1.3.

## Completion Status
COMPLETED (2026-02-23 10:15)
