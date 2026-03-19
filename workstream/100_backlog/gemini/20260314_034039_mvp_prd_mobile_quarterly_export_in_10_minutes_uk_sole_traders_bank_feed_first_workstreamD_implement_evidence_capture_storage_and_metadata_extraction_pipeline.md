# TASK D1: Implement evidence capture storage and metadata extraction pipeline

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

Store receipt or invoice evidence, extract best-effort metadata, and persist extraction confidence for later matching suggestions.

## Input

A1 Evidence schema and epic evidence capture requirements.

## Output

Evidence ingestion pipeline with file storage, evidence records, extracted amount/date/merchant metadata, and confidence scoring.

## Fields / Components

- evidence_id
- type
- captured_at
- doc_date
- merchant
- amount
- storage_link
- extraction_confidence

## Dependencies

- A1

## Action

Build evidence upload or capture intake, persist evidence files and metadata, and run best-effort extraction for downstream candidate matching.

## Verification

- [ ] Evidence can be stored and retrieved with a durable storage link and metadata record.
- [ ] Extraction output captures amount, date, merchant, and confidence when available.
- [ ] Evidence ingestion failures do not block transaction export flows.
- [ ] Evidence records are available for later matching suggestions even when extraction is partial.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 2
- Retry scheduled at 2026-03-18 17:21:30


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\claude.CMD -p Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline.md. Implement required changes in the workspace, run validations, and update checklist items. --permission-mode acceptEdits
- Return code: 1
- Stdout:
```text
You've hit your limit · resets 7pm (Europe/London)
```
- Retry scheduled at 2026-03-18 17:29:30
