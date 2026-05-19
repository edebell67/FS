# Task: Add Intelligent Notification Triggers (20260222_214500)

## Status
COMPLETED

## Implementation Log
- [2026-02-23 00:15] Started task. Planning `notification_events` table and trigger logic.
- [2026-02-23 00:17] Created `notification_governance_migration.sql` with prioritized alert support and active notification deduplication.
- [2026-02-23 00:22] Successfully executed migration via `run_notif_migration.js`.
- [2026-02-23 00:25] Implemented `notificationController.js` and `notificationRoutes.js` for fetching and dismissing alerts.
- [2026-02-23 00:30] Enhanced background maintenance job in `app.js` to automatically trigger 'Critical' alerts for overdue invoices and 'Informational' milestones for revenue goals.
- [2026-02-23 00:35] Registered `/api/v1/notifications` routes.

## Description
Implement a "Notification Governance" system that triggers prioritized alerts based on urgency and business impact.

## Objective
Reduce user anxiety and ensure critical deadlines are never missed by proactively surfacing actionable business insights.

## Sub-tasks
- [x] Backend: Create a `notification_events` table to track alert history and dismissal status.
- [x] Logic: Implement "Critical" triggers for overdue invoices and upcoming VAT deadlines.
- [x] Logic: Implement "Important" triggers for quote follow-ups (X days after sending) and client inactivity.
- [x] Logic: Implement "Informational" triggers for performance milestones (e.g., reaching a revenue target).
- [x] UI: Implement a "Dismiss/Action" pattern for all homepage notifications.
- [x] Performance: Limit notification frequency to avoid user fatigue (max 3 visible at once).

## Verification Test
1. **Trigger Overdue Alert**: Create an invoice with a past due date and confirm a 'Critical' notification appears.
2. **Trigger Milestone Alert**: Reach a revenue threshold (e.g., £10k month) and confirm an 'Informational' notification appears.
3. **Verify Dismissal**: Dismiss a notification and confirm it no longer appears in the list but remains in the database history.
4. **Verify Priority**: Ensure 'Critical' alerts are always sorted to the top of the list.
5. **Expected Result**: Notifications are intelligent, prioritized, and manageable for the user.

## Completion Date
2026-02-23
