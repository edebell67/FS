# TASK task_c_usage_guides: Create operator and developer usage guides

**Workstream:** C - Usage Guides
**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
**Priority:** 3
**Status:** [ ] Not Started

---

## Purpose

Provide concrete workflows for local setup, manual testing, and future implementation handoff so the empty epic can be executed consistently by multiple contributors.

## Input

Reference the root README and API docs once present. Existing integration points remain the epic root plus future implementation folders `solution/backend/` and `solution/frontend/`. Planned API endpoints from the contract should be reused in examples.

## Output

Usage guides for developers and operators covering local startup intent, sample API calls, verification flow, and expected artifacts in `verification/`.

## Existing Files to Reference

- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/api/openapi.yaml`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`

## New Files to Create

- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/guides/local-development.md`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/guides/quarterly-export-walkthrough.md`

## Action

Add `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/guides/local-development.md` and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/guides/quarterly-export-walkthrough.md`. The local development guide should explain how future services in `solution/backend/` and `solution/frontend/` are expected to be started and configured. The walkthrough should show sample calls to `POST /api/v1/bank-feeds/connect`, `POST /api/v1/imports`, `POST /api/v1/exports/quarterly`, and `GET /api/v1/exports/{exportId}`, and specify where screenshots, logs, or exported files should be placed under `verification/`.

## Verification

- [ ] Guides reference the README and API documentation instead of duplicating contracts.
- [ ] The walkthrough includes concrete request sequences for all planned endpoints.
- [ ] Verification outputs are mapped to the existing `verification/` directory.

---

## Notes

- Generated via epic augmentation on 2026-03-15T17:06:53.767960
- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:30
