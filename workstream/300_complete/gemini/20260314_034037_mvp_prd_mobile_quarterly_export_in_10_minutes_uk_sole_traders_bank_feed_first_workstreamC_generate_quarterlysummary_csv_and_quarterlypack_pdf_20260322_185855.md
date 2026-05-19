# TASK C3: Generate QuarterlySummary.csv and QuarterlyPack.pdf

**Workstream:** C � Quarter Close And Export
**Epic:** MVP PRD � Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 1
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** gemini
**UI Deliverable:** No
**Status:** IN_PROGRESS
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

## Plan

- [ ] 1. Update \solution/backend/src/services/exportService.js\ with PDF generation logic.
  - Test: Run unit test for PDF generation.
  - Evidence: File existence check.
- [ ] 2. Update \solution/backend/src/services/packOrchestrationService.js\ to coordinate PDF creation.
  - Test: Run integration test for full export flow.
  - Evidence: List of generated artifacts showing .pdf file.
- [ ] 3. Create and run \erify_C3_outputs.js\.
  - Test: Check CSV reconciliation and PDF readiness.
  - Evidence: Verification script output.

## Evidence
- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: Verification script output
  - Objective-Proved: technical correctness
  - Status: planned
- Evidence-Type: file_output
  - Artifact: QuarterlySummary.csv
  - Objective-Proved: summary data availability
  - Status: planned
- Evidence-Type: file_output
  - Artifact: QuarterlyPack.pdf
  - Objective-Proved: accountant-friendly summary availability
  - Status: planned

## Implementation Log
- 2026-03-22 18:55: Started task.
- 2026-03-22 19:05: Moved task to 200_inprogress.
- 2026-03-22 19:06: Defined plan and updated task file.

## Validation
- Awaiting execution.

## Risks/Notes
- Need to ensure Edge is available for PDF conversion.

## Completion Status
- In Progress
