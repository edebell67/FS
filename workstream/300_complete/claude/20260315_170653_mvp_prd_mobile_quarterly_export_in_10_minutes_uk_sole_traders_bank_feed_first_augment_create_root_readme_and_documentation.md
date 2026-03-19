# TASK task_a_docs_readme_foundation: Create root README and documentation index for the quarterly export MVP

**Workstream:** A - Documentation Foundation
**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
**Priority:** 1
**Status:** [ ] Not Started

---

## Purpose

Establish the primary entry point for the empty solution so future backend, frontend, and infrastructure work has a shared project map and onboarding flow.

## Input

Existing integration points: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/workstreams/`. No existing code files or APIs are present yet.

## Output

A root `README.md` plus `docs/README.md` that describe architecture intent, directory responsibilities, planned API surface, setup expectations, and links to future implementation areas under `solution/backend/` and `solution/frontend/`.

## Existing Files to Reference

- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/workstreams/`

## New Files to Create

- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/README.md`

## Action

Add `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md` and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/README.md`. Document the intended user flow for UK sole traders: connect bank feed, categorise transactions, generate quarterly export in under 10 minutes. Reference the existing epic folders as integration points, and explicitly point future backend work to `solution/backend/` and UI work to `solution/frontend/`. Include a section listing the planned contract-first endpoints: `POST /api/v1/bank-feeds/connect`, `POST /api/v1/imports`, `GET /api/v1/exports/{exportId}`, and `POST /api/v1/exports/quarterly`.

## Verification

- [ ] `README.md` exists at the epic root and links to `docs/README.md`.
- [ ] Documentation names the existing `solution/`, `deploy/`, `verification/`, and `workstreams/` directories.
- [ ] README includes the four planned API endpoints and explains their role in the MVP flow.

---

## Notes

- Generated via epic augmentation on 2026-03-15T17:06:53.761953
- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:30
