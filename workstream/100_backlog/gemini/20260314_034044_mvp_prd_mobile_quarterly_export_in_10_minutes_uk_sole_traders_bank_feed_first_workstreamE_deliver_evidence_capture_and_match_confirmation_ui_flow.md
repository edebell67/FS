# TASK E3: Deliver evidence capture and match confirmation UI flow

**Workstream:** E — Mobile UX And Voice
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 2
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** codex
**UI Deliverable:** Yes
**Status:** [ ] Not Started
**Workstream Goal:** Provide the mobile-first screens and voice-assisted workflows that make quarterly triage and close achievable in minutes.

---

## Purpose

Allow users to attach receipts, review the top three candidate bank matches, and confirm or defer the link through a simple bottom-sheet flow.

## Input

D1 evidence ingestion, D2 candidate matching, D3 confirmation handlers, and epic evidence UX requirements.

## Output

Mobile evidence flow with receipt capture entrypoint, candidate bottom sheet, match reason chips, and No match or Later actions.

## Fields / Components

- receipt_capture
- candidate_card
- match_reason_chip
- confirm_action
- no_match_action

## Dependencies

- D1
- D2
- D3

## Action

Implement the evidence attach workflow and confirmation-first candidate selection UI for inbox or quarter-close contexts.

## Verification

- [ ] Provide or update a simple local access/start script that launches the app locally, prints the localhost URL, and is documented for evidence matching verification.
- [ ] Smoke-test the local startup path and confirm the evidence UI loads without immediate crashes.
- [ ] Capture screenshots of the candidate match bottom sheet in a working state in the epic verification folder.
- [ ] Each candidate shows merchant, date, amount, and match-reason chips with the first candidate visually prominent.
- [ ] User can confirm a match or choose No match or Later without creating export blockers.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.
- UI delivery requirements were expanded per `skills/ui-delivery-viewability/SKILL.md`.


## Retry History
Retry-Count: 2
- Retry scheduled at 2026-03-18 17:21:30


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\claude.CMD -p Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260314_034044_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_evidence_capture_and_match_confirmation_ui_flow.md. Implement required changes in the workspace, run validations, and update checklist items. --permission-mode acceptEdits
- Return code: 1
- Stdout:
```text
You've hit your limit · resets 7pm (Europe/London)
```
- Retry scheduled at 2026-03-18 17:30:31
