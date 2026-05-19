# TASK B4: Implement simple merchant rules for recurring categorisation defaults

**Workstream:** B � Classification And Rules
**Epic:** MVP PRD � Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 2
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** gemini
**UI Deliverable:** No
**Status:** [x] Complete
**Workstream Goal:** Turn imported transactions into resolved or blocking items using fast micro-decisions, rules, and complete edit traceability.

---

## Purpose

Reduce future triage volume by applying user-defined merchant patterns to later transactions while preserving override capability.

## Input

A1 Rule entity, B1 classification model, B2 action handling, and epic merchant rule scope.

## Output

Rule creation, storage, and application service that maps merchant patterns to category and optional default business or split values.

## Fields / Components

- merchant_pattern
- category_code
- default_business_personal
- default_split_business_pct
- rule_source

## Dependencies

- B1
- B2

## Action

Implement rule creation from user actions, merchant matching on import or refresh, and safe application of suggested defaults to applicable transactions.       

## Plan
- [x] 1. Create SQL migration for `merchant_rules` table.
  - Test: Check if migration file is created correctly.
  - Evidence: `merchant_rules_migration.sql` created.
- [x] 2. Update memory store for testing.
  - Test: Check if `upsertRule` and `listRules` work.
  - Evidence: Passed in `testMerchantRules.js`.
- [x] 3. Implement `merchantRuleService.js`.
  - Test: Verify matching logic (longest pattern, case-insensitive).
  - Evidence: Passed in `testMerchantRules.js`.
- [x] 4. Integrate rules into import flow.
  - Test: Import transaction and check if rule is applied.
  - Evidence: Passed in `testMerchantRules.js`.
- [x] 5. Verify audit and override.
  - Test: Override auto-classification and check audit trail.
  - Evidence: Passed in `testMerchantRules.js`.

## Verification

- [x] A rule can be saved from a user classification decision and applied to future matching merchants.
- [x] Automatic rule application remains auditable and user-overridable.        
- [x] False-positive rule application can be corrected without corrupting historical audit data.
- [x] Rule application measurably reduces unresolved item counts in repeated import scenarios.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `node src/testing/testMerchantRules.js` output showing 11/11 passed.
  - Objective-Proved: Full implementation of merchant rules with audit and override.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\services\merchantRuleService.js`
  - Objective-Proved: Service implementation.
  - Status: captured

---

## Implementation Log
- 2026-03-22 17:30: Created `merchant_rules_migration.sql`.
- 2026-03-22 17:35: Updated `MemoryTransactionImportStore.js` with Rule support.
- 2026-03-22 17:40: Implemented `merchantRuleService.js` with substring matching logic.
- 2026-03-22 17:45: Integrated `merchantRuleService` into `transactionImportService.js` (V20260322_1730).
- 2026-03-22 17:50: Created and ran `testMerchantRules.js`, all 11 scenarios passed.
- 2026-03-22 17:55: Updated version to `V20260322_1730` in `Constants.py`.

## Completion Status
COMPLETE - 2026-03-22 18:00
