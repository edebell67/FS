# TASK C4: Assemble final quarterly pack and export delivery flow

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

Package all four export artifacts into a single user-triggered flow with traceable metadata, consistent naming, and completion logging.

## Input

C2 CSV exports, C3 summary and PDF outputs, and quarter export gating from C1.

## Output

Export orchestration flow that builds the Quarterly Pack, stores or shares artifacts, and records export completion metadata.

## Fields / Components

- export_id
- quarter_id
- generated_at
- artifact_paths
- readiness_pct_at_export

## Dependencies

- C2
- C3

## Action

Implement the end-to-end export command that validates readiness, generates all artifacts, packages them coherently, and records the export event for analytics.

## Verification

- [ ] Export produces all four required artifacts in one completion flow.
- [ ] The export command refuses to run while blocking transactions remain.
- [ ] Artifact names, timestamps, and traceability metadata are consistent across a single pack.
- [ ] Export completion is logged for funnel and completion-rate metrics.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
