# TASK B4: Implement simple merchant rules for recurring categorisation defaults

**Workstream:** B — Classification And Rules
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 2
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** gemini
**UI Deliverable:** No
**Status:** [ ] Not Started
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

## Verification

- [ ] A rule can be saved from a user classification decision and applied to future matching merchants.
- [ ] Automatic rule application remains auditable and user-overridable.
- [ ] False-positive rule application can be corrected without corrupting historical audit data.
- [ ] Rule application measurably reduces unresolved item counts in repeated import scenarios.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
