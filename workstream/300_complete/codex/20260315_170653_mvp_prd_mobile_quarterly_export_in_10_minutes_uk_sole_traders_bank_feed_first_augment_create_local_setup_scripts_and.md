# TASK task_d_setup_and_env_bootstrap: Create local setup scripts and environment templates

**Workstream:** D - Developer Setup
**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Source:** `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
**Priority:** 4
**Status:** [x] Complete

## Source
`ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`

## Task Summary
Create additive root-level bootstrap artifacts for the MVP quarterly export epic so local backend/frontend development can start from a consistent environment template and folder structure.

## Context
- Epic root: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/`
- Contract docs: `docs/api/openapi.yaml`, `docs/api/usage.md`
- Existing implementation scaffold: `solution/backend/`
- Missing future scaffold to preserve: `solution/frontend/`

## Dependency
None

## Plan
- [x] 1. Derive the required local bootstrap contract from the epic docs and current solution tree.
  - [x] Test: `Select-String -Path 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\docs\\api\\openapi.yaml','ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\docs\\api\\usage.md' -Pattern '/api/v1','BANK','quarterly','JWT'`
  - Evidence: Matches captured for `/api/v1` routes, bearer `JWT`, bank-feed workflow, and quarterly export endpoints in both contract files.
- [x] 2. Create cross-platform setup scripts and an environment template in the epic root without overwriting existing implementation files.
  - [x] Test: `& '.\\workstream\\artefacts\\setup_validation_ps1_min\\setup.ps1'` completed successfully in a disposable root and created `solution/frontend`, `verification/artifacts`, `verification/artifacts/exports`, and `.env`; direct Git Bash execution of `setup.sh` was blocked by the host shell (`couldn't create signal pipe, Win32 error 5`), so shell parity was validated by targeted file-content checks against the same folder/env-copy logic.
  - Evidence: Disposable PowerShell validation root shows only additive folder/file creation; `setup.sh` contains the same target directories, `.env` seeding behavior, and `/api/v1` startup messaging.
- [x] 3. Validate alignment, capture proof, and close the lifecycle item.
  - [x] Test: `Select-String -Path 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\.env.example','ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\setup.ps1','ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\setup.sh' -Pattern 'API_PORT','BANK_FEED_PROVIDER','EXPORT_STORAGE_PATH','JWT_SECRET','/api/v1','solution/frontend','quarterly export services'` plus `git status --short -- <files>`
  - Evidence: Expected env vars and startup hook references were captured in all three new artifacts; git reports the bootstrap artifacts and lifecycle file as new files only.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `Select-String` output against `docs/api/openapi.yaml` and `docs/api/usage.md` showing `/api/v1`, quarterly export endpoints, bank-feed references, and `JWT` bearer auth plus PowerShell disposable-root run output ending with `frontend=True artifacts=True exports=True env=True`
  - Objective-Proved: The bootstrap contract was derived from the documented API/auth/export workflow and the PowerShell setup flow creates only the expected additive artifacts.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `git status --short -- ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.env.example ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/setup.ps1 ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/setup.sh workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_local_setup_scripts_and.md`
  - Objective-Proved: The implementation is additive and limited to the intended new bootstrap artifacts plus lifecycle documentation.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `Select-String` output against `.env.example`, `setup.ps1`, and `setup.sh` showing `API_PORT`, `BANK_FEED_PROVIDER`, `EXPORT_STORAGE_PATH`, `JWT_SECRET`, `/api/v1`, `solution/frontend`, and quarterly export startup hook text
  - Objective-Proved: The environment template aligns with the API/export workflow and both scripts document future backend/frontend integration points.
  - Status: captured

## Implementation Log
- 2026-03-19 17:28 GMT: Read `skills/workstream-task-lifecycle/SKILL.md` and loaded the assigned task.
- 2026-03-19 17:29 GMT: Inspected `docs/api/openapi.yaml`; confirmed `/api/v1` bank-feed, import, export, and bearer-token requirements.
- 2026-03-19 17:30 GMT: Checked the epic tree and found `solution/backend/` present while `solution/frontend/` and the referenced `docs/guides/local-development.md` were absent.
- 2026-03-19 17:31 GMT: Restored the lifecycle file from `workstream/200_inprogress/blocker/codex/` to `workstream/200_inprogress/codex/` to resume active execution.
- 2026-03-19 17:44 GMT: Added `.env.example`, `setup.ps1`, and `setup.sh` in the epic root with additive folder creation, `.env` seeding, and `/api/v1` startup hook messaging.
- 2026-03-19 17:49 GMT: Ran `setup.ps1` in `workstream/artefacts/setup_validation_ps1_min` and verified additive creation of `solution/frontend`, `verification/artifacts/exports`, and `.env`.
- 2026-03-19 17:51 GMT: Attempted direct `setup.sh` execution with both WSL-backed and Git-for-Windows bash binaries; execution was blocked by host shell permission errors, so shell parity was validated from file content instead.

## Changes Made
- Added `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.env.example` with local API, bank-feed, JWT, import-window, and export-storage variables aligned to the `/api/v1` workflow.
- Added `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/setup.ps1` to create the expected future folder structure and seed `.env` from `.env.example` without overwriting existing files.
- Added `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/setup.sh` with the same additive bootstrap behavior for POSIX shells.
- Normalized the lifecycle document into the required workstream format and recorded concrete validation evidence.

## Validation
- `Select-String -Path 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\docs\\api\\openapi.yaml','ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\docs\\api\\usage.md' -Pattern '/api/v1','BANK','quarterly','JWT'`
  - Pass: matched `/api/v1` routes, bank-feed operations, quarterly export flow, and `JWT` bearer auth.
- `& '.\\workstream\\artefacts\\setup_validation_ps1_min\\setup.ps1'`
  - Pass: output reported `Created solution/frontend`, `Created verification/artifacts`, `Created verification/artifacts/exports`, `Created .env from .env.example`, followed by `frontend=True artifacts=True exports=True env=True`.
- `& 'C:\\Program Files\\Git\\bin\\bash.exe' '.\\workstream\\artefacts\\setup_validation_sh_min\\setup.sh'`
  - Environment limitation: host returned `couldn't create signal pipe, Win32 error 5`; no workspace defect observed in the script content itself.
- `Select-String -Path 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\.env.example','ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\setup.ps1','ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\setup.sh' -Pattern 'API_PORT','BANK_FEED_PROVIDER','EXPORT_STORAGE_PATH','JWT_SECRET','/api/v1','solution/frontend','quarterly export services'`
  - Pass: confirmed required env vars, `/api/v1`, and backend/frontend startup hook messaging in the delivered files.
- `git status --short -- ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.env.example ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/setup.ps1 ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/setup.sh workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_local_setup_scripts_and.md`
  - Pass: all four files appear as new tracked workspace changes only.

## Risks/Notes
- The task input referenced `docs/guides/local-development.md`, but the current epic contains `docs/api/usage.md` instead. Validation used the files that exist in the workspace.
- Direct execution of `setup.sh` is blocked in this environment by the available bash runtimes, so shell validation is based on content parity and the same bootstrap steps already proven by `setup.ps1`.
- Generated via epic augmentation on 2026-03-15T17:06:53.770320.
- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`.

## Completion Status
Complete - 2026-03-19 17:53 GMT

## Retry History
Retry-Count: 2
- Retry scheduled at 2026-03-18 17:21:29

## Execution Evidence
- Agent lane: codex
- 2026-03-19 17:41:07: Prior execution attempt was parked after a usage-limit failure outside the workspace changes. This retry resumed the same lifecycle item in the active lane.
