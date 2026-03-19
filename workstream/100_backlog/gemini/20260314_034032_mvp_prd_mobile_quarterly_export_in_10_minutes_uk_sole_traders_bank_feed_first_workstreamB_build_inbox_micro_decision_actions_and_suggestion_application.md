# TASK B2: Build inbox micro-decision actions and suggestion application

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

## Action

Implement the command handlers for all core micro-decisions, including suggestion acceptance, manual override, split updates, and duplicate dismiss or merge resolution.

## Verification

- [ ] Each supported micro-decision updates classification state and audit history correctly.
- [ ] A transaction can be moved from unresolved to resolved when the required fields are supplied.
- [ ] Duplicate resolution supports both dismiss and merge outcomes without data loss.
- [ ] Manual overrides are distinguishable from automated suggestions for later PDF audit counts.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
