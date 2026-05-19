# Task: Build Accountant-Ready Export (20260222_214600)

## Status
COMPLETED

## Implementation Log
- [2026-02-23 00:45] Started task. Planning CSV export mappings for Xero and QuickBooks.
- [2026-02-23 00:47] Researching standard column headers for major accounting software.
- [2026-02-23 00:55] Implemented `exportController.js` with mapping logic for Xero (UK standard), QuickBooks, and Generic formats.
- [2026-02-23 01:00] Added support for date range and VAT quarter filtering in exports.
- [2026-02-23 01:05] Registered `/api/v1/export` routes.
- [2026-02-23 01:15] Installed `archiver` library.
- [2026-02-23 01:20] Implemented `exportVATPack` to bundle CSV data and original receipt images into a single ZIP for accountant submission.

## Description
Develop an "Accountant-Ready" CSV/Excel export engine that provides structured financial data compatible with major accounting software.

## Objective
Enable bizPA to seamlessly integrate with professional accounting workflows, simplifying tax filing for sole traders.

## Sub-tasks
- [x] Export: Implement a "Xero-compatible CSV" export with all required transaction mapping.
- [x] Export: Implement a "QuickBooks-compatible CSV" export with standard column headers.
- [x] Export: Implement a "Generic Structured Export" (Excel/CSV) for general use.
- [x] Logic: Filter exports by date range and/or VAT quarter.
- [x] UI: Create a "Tax & Export" tab to provide one-click access to all financial reports.
- [x] Logic: Package all receipts/invoices as a downloadable "VAT Pack" (structured CSV + original image attachments).

## Verification Test
1. **Fetch Transactions**: Create a mix of receipts and invoices for a single quarter.
2. **Generate Export**: Trigger a "Xero-compatible CSV" export for that quarter.
3. **Verify Columns**: Open the CSV and confirm all 12+ structured transaction fields (Net, VAT, Gross, Counterparty, etc.) are present.
4. **Verify Attachments**: Ensure the "VAT Pack" includes a zip file with both the CSV and the corresponding image files.
5. **Expected Result**: Export files are accurate and follow the specific schema for external accounting software.

## Completion Date
2026-02-23
