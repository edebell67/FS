# TASK F3: Build end-to-end MVP acceptance and regression suite

**Workstream:** F — Quality Metrics And Compliance
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 1
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** general
**UI Deliverable:** No
**Status:** [ ] Not Started
**Workstream Goal:** Prove the MVP meets its speed, completion, confidence, and compliance expectations through measurable telemetry and robust validation.

---

## Purpose

Lock the epic acceptance tests into automated or repeatable verification so the MVP can be reviewed and regression-tested with confidence.

## Input

Completed ingestion, classification, quarter, export, evidence, and voice workflows across prior tasks.

## Output

End-to-end test scenarios and fixtures covering quarter-close, export, evidence confirmation, and voice undo acceptance criteria.

## Fields / Components

- fixture_transaction_count
- blocking_count
- expected_exports
- voice_test_phrase
- evidence_match_state

## Dependencies

- C4
- D3
- E4
- F2

## Action

Create deterministic test data and regression scenarios that exercise the full MVP from imported transactions through export generation and evidence or voice workflows.

## Verification

- [ ] A scenario with 200 transactions and 8 blockers shows the correct items-left count before resolution.
- [ ] Resolving the 8 blockers enables export immediately and generates all four artifacts.
- [ ] Evidence attachment requires user confirmation of the match or explicit No match handling.
- [ ] Voice 'Category: Travel' applies successfully and is undoable with one tap.
- [ ] Regression coverage includes duplicate handling, split percentages, and empty-evidence export cases.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
