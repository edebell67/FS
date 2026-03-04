# Task: bizPA Refine Unpaid Data Linking (20260224_134500)

## Task Summary
Refine the "Unpaid" dashboard indicators to link to a specifically filtered view of unpaid invoices, rather than just all invoices.

## Context
- bizPA v1.1.7 has general type-based filtering for dashboard numbers.
- "Unpaid" currently links to the general 'invoice' activity filter.
- Goal: Clicking "Unpaid" should filter Activity by `type='invoice'` AND `payment_status != 'paid'`.

## Sub-tasks
- [x] UI: Add `paymentStatusFilter` state to `App.jsx`.
- [x] UI: Update `renderActivity` to respect `paymentStatusFilter`.
- [x] UI: Update "Unpaid" indicator in Momentum Bar to set `paymentStatusFilter('unpaid')`.
- [x] UI: Update "Invoices" card in Performance Grid to set `paymentStatusFilter('unpaid')`.
- [x] Verification: Confirm only unpaid/overdue/draft invoices show when clicking the link.

## Implementation Log
- [2026-02-24 13:45] Task initialized.
- [2026-02-24 13:50] Added `paymentStatusFilter` state to `App.jsx`.
- [2026-02-24 13:55] Updated `renderActivity` to filter items where `payment_status !== 'paid'`.
- [2026-02-24 14:00] Updated Momentum Bar and Performance Grid to set the new filter.
- [2026-02-24 14:05] Verified that clicking "Weekly Momentum" or "Show All" clears the filter.

## Changes Made
- `bizPA/frontend/src/App.jsx`:
    - Added `paymentStatusFilter` state.
    - Updated filtering logic in `renderActivity`.
    - Integrated filter state into all dashboard click handlers.

## Validation
- Browser testing: Clicking "Unpaid" successfully navigates to Activity and hides any (simulated) paid invoices.
- Confirmed "Show All" restores full list.

## Risks/Notes
- Logic relies on `payment_status` being correctly set to 'paid' when closed.

## Completion Status
COMPLETED (2026-02-24 14:10)
