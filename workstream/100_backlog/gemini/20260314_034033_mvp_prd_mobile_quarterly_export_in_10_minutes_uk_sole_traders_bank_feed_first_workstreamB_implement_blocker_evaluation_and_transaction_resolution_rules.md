# TASK B3: Implement blocker evaluation and transaction resolution rules

**Workstream:** B — Classification And Rules
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 1
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** gemini
**UI Deliverable:** No
**Status:** [ ] Not Started
**Workstream Goal:** Turn imported transactions into resolved or blocking items using fast micro-decisions, rules, and complete edit traceability.

---

## Purpose

Encode the exact blocking-export logic so readiness metrics and Finish Now queues are deterministic and traceable.

## Input

A1 schemas, B1 classification state, B2 action outcomes, and epic blocking rules.

## Output

Rule service that marks transactions as resolved, blocking, or non-blocking and exposes blocker reason codes.

## Fields / Components

- missing_category
- missing_business_personal
- split_pct_missing
- duplicate_unresolved
- is_blocking_export

## Dependencies

- B1
- B2

## Action

Build the rules engine that evaluates transaction state against the MVP export blockers while keeping missing evidence explicitly non-blocking.

## Verification

- [ ] Transactions are marked RESOLVED only when all required fields are present per epic rules.
- [ ] Evidence or receipt absence never creates a blocking state.
- [ ] Reason codes are emitted so queues can be ordered and UI can explain why an item blocks export.
- [ ] Rule outputs are deterministic for the same transaction state.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
