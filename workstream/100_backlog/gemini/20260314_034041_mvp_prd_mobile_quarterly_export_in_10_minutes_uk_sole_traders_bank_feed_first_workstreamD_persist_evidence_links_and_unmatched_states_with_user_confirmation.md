# TASK D3: Persist evidence links and unmatched states with user confirmation

**Workstream:** D — Evidence Matching
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 2
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** gemini
**UI Deliverable:** No
**Status:** [ ] Not Started
**Workstream Goal:** Allow optional receipt evidence to be captured, extracted, and matched to bank transactions without ever becoming an export blocker.

---

## Purpose

Record confirmed evidence-to-transaction links, confirmation metadata, and explicit no-match or later decisions for audit-friendly exports.

## Input

D2 candidate service, A1 EvidenceLink schema, and epic confirmation requirements.

## Output

EvidenceLink persistence and workflow handlers for confirm, no match, and later outcomes.

## Fields / Components

- evidence_id
- bank_txn_id
- user_confirmed
- confirmed_at
- method
- link_confidence

## Dependencies

- D2

## Action

Implement the commands that confirm a candidate, defer matching, or mark no match while updating evidence-related queue items and export linkage data.

## Verification

- [ ] A confirmed match creates an EvidenceLink with user confirmation metadata.
- [ ] Choosing No match or Later preserves the evidence record without blocking quarter export.
- [ ] Confirmed links remove the related evidence task from any active queue.
- [ ] EvidenceIndex.csv can reflect confirmed and unmatched evidence states correctly.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 2
- Retry scheduled at 2026-03-18 17:21:30


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\claude.CMD -p Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260314_034041_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_persist_evidence_links_and_unmatched_states_with_user_confirmation.md. Implement required changes in the workspace, run validations, and update checklist items. --permission-mode acceptEdits
- Return code: 1
- Stdout:
```text
You've hit your limit · resets 7pm (Europe/London)
```
- Retry scheduled at 2026-03-18 17:29:30
