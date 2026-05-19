# Task: Implement Multi-Tenant User Switching for Grouping Verification (20260223_130000)

## Status
COMPLETED

## Task Summary
Enable multi-user testing by implementing a "User Switcher" in the dashboard. This allows verification that data (Invoices, Receipts, Bookings) is correctly isolated and grouped by user ID across the backend and frontend.

## Context
- **Root Cause**: Previously, the system defaulted to a single hard-coded user ID, making it impossible to test multi-tenant grouping.
- **Fix**: Created 3 test identities (Default, Alice, Bob), implemented a backend middleware to switch identity via headers, and added a visual selector in the Web UI.

## Sub-tasks
- [x] Database: Created `add_test_users.sql` and initialized Alice (`1111...`) and Bob (`2222...`).
- [x] Backend: Implemented `userMiddleware.js` to extract `user_id` from the custom `X-User-ID` header.
- [x] Backend: Registered `userMiddleware` in `src/app.js` and fixed a missing `db` import.
- [x] Frontend: Added a **User Context Selector** (Avatar dropdown) in the main header.
- [x] Frontend: Synchronized all `axios` requests to automatically include the `X-User-ID` of the selected user.
- [x] Frontend: Persisted the selected user to `localStorage` to survive page refreshes.
- [x] Verification: Switch to Alice, log a £50 spend, switch to Bob, and verify the spend is hidden.

## Implementation Log
- [2026-02-23 13:00] Task created.
- [2026-02-23 13:10] Applied database migration for test users.
- [2026-02-23 13:20] Implemented backend identity middleware.
- [2026-02-23 13:30] Integrated User Switcher into Web UI v1.1.6.

## Completion Status
COMPLETED (2026-02-23 13:45)
