# TASK F1: Instrument MVP analytics and quarter-close funnel metrics

**Workstream:** F — Quality Metrics And Compliance
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 2
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** general
**UI Deliverable:** No
**Status:** [ ] Not Started
**Workstream Goal:** Prove the MVP meets its speed, completion, confidence, and compliance expectations through measurable telemetry and robust validation.

---

## Purpose

Capture the product metrics defined in the epic so the team can measure time-to-export, completion rate, blocker counts, and voice success.

## Input

User flows from onboarding, inbox, quarter close, evidence matching, voice actions, and export completion.

## Output

Analytics event taxonomy, metric aggregation logic, and dashboards or reports for MVP success metrics.

## Fields / Components

- quarter_opened_at
- export_generated_at
- blocking_items_count
- voice_intent_success
- quarter_started
- quarter_exported

## Dependencies

- C4
- E4

## Action

Instrument key events and derive the median quarter-close duration, completion rate, average blockers after 30 days, and voice success rate for MVP reporting.

## Verification

- [ ] Events exist to calculate each epic metric without ambiguous joins or missing timestamps.
- [ ] Time from opening the quarter screen to export generation can be computed accurately.
- [ ] Voice success can distinguish successful application without edit from failed or corrected attempts.
- [ ] Analytics instrumentation does not log secrets or raw bank credentials.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
