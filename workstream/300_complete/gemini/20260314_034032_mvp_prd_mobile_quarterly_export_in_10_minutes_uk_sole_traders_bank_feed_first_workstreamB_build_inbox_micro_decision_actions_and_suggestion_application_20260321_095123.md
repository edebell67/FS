# TASK B2: Build inbox micro-decision actions and suggestion application

**Workstream:** B â€” Classification And Rules
**Epic:** MVP PRD â€” Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 1
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** gemini
**UI Deliverable:** No
**Status:** IN_PROGRESS
**Workstream Goal:** Turn imported transactions into resolved or blocking items using fast micro-decisions, rules, and complete edit traceability.

---

## Purpose

Support the MVP triage actions that resolve transactions quickly through taps or later voice intents.

## Input

B1 classification model, category taxonomy, and epic inbox action requirements. 

## Output

Application services or APIs for category assignment, business/personal tagging, split percentage updates, and duplicate resolution state changes.

## Fields / Components

- suggested_category
- manual_override
- business_personal
- split_business_pct
- duplicate_resolution

## Dependencies

- B1

## Plan
- [ ] 1. Update SQL migration `transaction_classification_migration.sql` to include `duplicate_of_txn_id` and `duplicate_resolution`.
  - Test: Check table schema after migration.
  - Evidence: SQL command output.
- [ ] 2. Update `MemoryTransactionImportStore.js` to support new fields and transaction-aware updates.
  - Test: Run existing tests to ensure no regressions.
  - Evidence: Test output.
- [ ] 3. Implement action handlers in `transactionImportService.js`:
  - `acceptCategorySuggestion`
  - `overrideCategory`
  - `setBusinessPersonal`
  - `updateSplit`
  - `resolveDuplicate`
  - Test: Call each action and verify classification state and audit log.
  - Evidence: Log output or test verification.
- [ ] 4. Update version number in `Constants.py` files.
  - Test: Read files to confirm update.
  - Evidence: `cat` output.
- [ ] 5. Create and run a comprehensive verification script `verify_inbox_actions.js`.
  - Test: Run script and verify 100% pass rate.
  - Evidence: Script output.

## Evidence
- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `verify_inbox_actions.js` output
  - Objective-Proved: Core micro-decisions and audit history correctly implemented.
  - Status: planned

## Implementation Log
- 2026-03-21 10:00: Initialised task B2 and created plan.

## Completion Status
IN_PROGRESS
