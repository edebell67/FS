# TASK task_e_containerisation: Create Docker and compose scaffolding for backend, frontend, and supporting services

**Workstream:** E - Containerisation
**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Source:** Augmentation of existing solution at `ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
**Priority:** 5
**Status:** [ ] Not Started

---

## Purpose

Prepare consistent local and CI runtime scaffolding so implementation teams can drop service code into known containers without redesigning deployment layout later.

## Input

Anchor to the existing epic root and future service directories `solution/backend/` and `solution/frontend/`. Reuse environment variables from `.env.example` and expose the documented `/api/v1` endpoints through the backend container.

## Output

Root-level Docker assets for local orchestration and a deployment baseline that future code can plug into.

## Existing Files to Reference

- `ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.env.example`
- `ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/setup.sh`
- `ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`

## New Files to Create

- `ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
- `ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/backend/Dockerfile`
- `ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/frontend/Dockerfile`

## Action

Create `ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`, `ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/backend/Dockerfile`, and `ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/frontend/Dockerfile`. Compose should define placeholder `backend`, `frontend`, and optional `db`/`mock-bank-feed` services, mount `verification/artifacts/` for exported outputs, and reserve routing for the contract endpoints under `/api/v1`.

## Verification

- [ ] `docker-compose.yml` references only additive paths under the epic root.
- [ ] Backend and frontend Dockerfiles point at the required `solution/backend/` and `solution/frontend/` directories.
- [ ] Compose wiring includes environment variables and volumes consistent with setup scripts and verification artifacts.

---

## Notes

- Generated via epic augmentation on 2026-03-15T17:06:53.771899
- Builds on existing solution: `ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:30
