# Task: Harden Structured Transaction Schema (20260222_214000)

## Status
COMPLETE

## Description
Harden the database schema and backend logic to ensure every financial record contains all required structural transaction fields.

## Objective
Enable bizPA to support robust financial reporting and VAT compliance by enforcing a comprehensive transaction data model.

## Sub-tasks
- [x] Database: Update `capture_items` table to include `net_amount`, `vat_amount`, `gross_amount`, `vat_rate`, `vat_type`, and `quarter_ref`.
- [x] Logic: Update `itemController.js` to automatically calculate `gross_amount` and `vat_amount` if only two values are provided.
- [x] Logic: Implement `vat_type` detection (Input for receipts, Output for invoices).
- [x] Logic: Add logic to auto-assign a `quarter_ref` (e.g., Q1-2026) based on the transaction date.
- [x] Logic: Ensure `counterparty` (Client/Supplier) is consistently tracked for all transaction types.

## Verification Test
1. **Create Transaction**: Use the API to create a new receipt with a `net_amount` of 100 and a `vat_rate` of 20%.
2. **Verify Calculation**: Query the database to ensure `vat_amount` is 20 and `gross_amount` is 120.
3. **Verify Metadata**: Confirm `vat_type` is 'Input' and `quarter_ref` is correctly assigned based on the current date.
4. **Expected Result**: All fields are correctly populated and calculated. **PASSED**.

## Completion Date
2026-02-22 21:45
