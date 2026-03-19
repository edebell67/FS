# TASK F2: Harden security performance and legal disclaimers for MVP release

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

Meet the explicit non-functional requirements for secure storage, encryption, idempotency, inbox performance, and user disclaimer visibility before release.

## Input

A3 bank integration, A4 import pipeline, E1 and E2 UI flows, and epic non-functional requirements.

## Output

Validated security and performance checklist with implemented safeguards, performance measurements, and visible disclaimer coverage.

## Fields / Components

- secure_token_storage
- encryption_in_transit
- encryption_at_rest
- inbox_load_time_ms
- disclaimer_visible

## Dependencies

- A3
- A4
- E1
- E2

## Action

Review and implement the NFR safeguards, benchmark inbox load, verify encryption and token handling paths, and place the required non-tax-advice disclaimer in relevant user flows.

## Verification

- [ ] Credentials and tokens are stored securely and are not exposed in logs or client caches.
- [ ] Encryption in transit and at rest is documented or enforced for the chosen stack.
- [ ] Inbox load is measured and meets the sub-2-second typical-device target on representative data.
- [ ] The app displays a clear disclaimer that it is not tax advice and the user remains responsible.
- [ ] Idempotent import behavior remains intact after security and performance hardening.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 2
- Retry scheduled at 2026-03-18 17:21:30


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\claude.CMD -p Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260314_034047_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamF_harden_security_performance_and_legal_disclaimers_for_mvp_release.md. Implement required changes in the workspace, run validations, and update checklist items. --permission-mode acceptEdits
- Return code: 1
- Stdout:
```text
You've hit your limit · resets 7pm (Europe/London)
```
- Retry scheduled at 2026-03-18 17:31:31
