# Task: Improve Invoice/Quote Lifecycle (20260222_214400)

## Status
COMPLETED

## Implementation Log
- [2026-02-22 23:40] Started task. Analyzing `capture_items` table for invoice/quote fields.
- [2026-02-22 23:42] Planning schema additions: `reference_number`, `converted_from_id`, `payment_status`.
- [2026-02-22 23:45] Created `invoice_lifecycle_migration.sql` with auto-numbering triggers and reference generators.
- [2026-02-22 23:50] Successfully executed migration via `run_lifecycle_migration.js`.
- [2026-02-22 23:55] Implemented `convertQuoteToInvoice` in `itemController.js` to automate quote conversion with inherited metadata.
- [2026-02-23 00:00] Added background maintenance heartbeat in `app.js` to automatically update overdue statuses and trigger alerts.
- [2026-02-23 00:05] Registered `/convert` and `/maintenance` routes in `itemRoutes.js`.

## Description
Develop a complete "state machine" for the Invoice and Quote lifecycle, including numbering, conversion, and status tracking.

## Objective
Enable bizPA to automate common financial workflows, reducing administrative burden and ensuring accurate receivables tracking.

## Sub-tasks
- [x] Logic: Implement "Auto Invoice Numbering" with a configurable prefix (e.g., INV-001).
- [x] Logic: Implement "Quote → Invoice Conversion" to automatically create an invoice from an approved quote.
- [x] Logic: Implement "Due Date Tracking" and calculate if an invoice is 'Overdue'.
- [x] Logic: Implement a "Payment Status State Model" (Draft, Sent, Overdue, Paid, Partial, Void).
- [x] Logic: Create a `notificationTrigger` to alert when an invoice becomes overdue.
- [x] Logic: Implement "Overdue Logic" to automatically update the status and trigger a notification when today > due_date.

## Verification Test
1. **Create Quote**: Generate a quote for a client and mark it as 'Approved'.
2. **Convert Quote**: Trigger the conversion and confirm a new invoice is created with all quote details.
3. **Verify Overdue**: Set an invoice due date to yesterday and confirm the status automatically changes to 'Overdue'.
4. **Verify Notification**: Confirm an alert appears on the homepage Attention Panel for the overdue invoice.
5. **Expected Result**: Invoices and quotes follow a logical, automated lifecycle from creation to payment.

## Completion Date
2026-02-23
