# TASK C1: Build quarter model, readiness metrics, and blocking queue ordering

**Workstream:** C — Quarter Close And Export
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 1
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** gemini
**UI Deliverable:** No
**Status:** [ ] Not Started
**Workstream Goal:** Convert classified transaction data into a quarter-close workflow and accountant-friendly export pack with immediate export enablement once blockers reach zero.

---

## Purpose

Represent quarter periods, compute readiness percentages, and produce the ordered Finish Now queue that drives the 10-minute close workflow.

## Input

A4 imported transactions, B3 blocker evaluation, and epic quarter readiness formulas and ordering requirements.

## Output

Quarter and QuarterMetrics services that compute totals, blocking count, readiness percentage, and ordered blocking queue for a selected quarter.

## Fields / Components

- total_txns_in_period
- blocking_txns_count
- readiness_pct
- blocking_queue

## Dependencies

- A4
- B3

## Action

Implement quarter period selection, transaction aggregation, readiness calculations, and queue ordering by uncategorised, personal missing, split missing, then duplicates.

## Verification

- [ ] A quarter with 200 transactions and 8 blockers yields a blocking count of 8 and the correct readiness percentage.
- [ ] Blocking queue ordering matches the epic order exactly.
- [ ] Export eligibility flips to enabled immediately when blocking count reaches zero.
- [ ] Quarter metrics update after each micro-decision without requiring a full re-import.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 2
- Retry scheduled at 2026-03-18 17:21:30


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\claude.CMD -p Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260314_034035_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_build_quarter_model_readiness_metrics_and_blocking_queue_ordering.md. Implement required changes in the workspace, run validations, and update checklist items. --permission-mode acceptEdits
- Return code: 1
- Stdout:
```text
You've hit your limit · resets 7pm (Europe/London)
```
- Retry scheduled at 2026-03-18 17:27:30
