# TASK C3: Generate QuarterlySummary.csv and QuarterlyPack.pdf

**Workstream:** C — Quarter Close And Export
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 1
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** gemini
**UI Deliverable:** No
**Status:** [ ] Not Started
**Workstream Goal:** Convert classified transaction data into a quarter-close workflow and accountant-friendly export pack with immediate export enablement once blockers reach zero.

---

## Purpose

Create the summary outputs required for quarter handoff, including category totals, unresolved counts, audit counts, readiness, and evidence coverage.

## Input

C1 quarter metrics, B1 classifications, C2 detailed exports, and epic PDF content requirements.

## Output

QuarterlySummary.csv and QuarterlyPack.pdf with period totals, category highlights, readiness state, audit counts, and evidence coverage metrics.

## Fields / Components

- period_start
- period_end
- category_code
- category_name
- total_in
- total_out
- count
- unresolved_count

## Dependencies

- C1
- C2

## Action

Implement summary aggregation and PDF rendering logic for the required 1-2 page accountant-friendly pack.

## Verification

- [ ] QuarterlySummary.csv totals reconcile with detailed transaction export data.
- [ ] QuarterlyPack.pdf shows period, totals, readiness, category highlights, audit counts, and evidence coverage.
- [ ] PDF readiness is 100% at export time and export is blocked otherwise.
- [ ] Generated artifacts are readable and suitable for handoff without proprietary tool dependencies.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 2
- Retry scheduled at 2026-03-18 17:21:30


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\claude.CMD -p Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260314_034037_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_quarterlysummary_csv_and_quarterlypack_pdf.md. Implement required changes in the workspace, run validations, and update checklist items. --permission-mode acceptEdits
- Return code: 1
- Stdout:
```text
You've hit your limit · resets 7pm (Europe/London)
```
- Retry scheduled at 2026-03-18 17:29:30
