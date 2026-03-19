# TASK G2: Add Sync Conflict Guardrails And Health Telemetry

**Source**: `workstream/000_epic/bizPA.md`
**Workstream**: G - Sync And Notifications
**Epic**: bizPA MVP Product Requirements Document
**Priority**: 1
**Suggested Agent**: gemini
**UI Deliverable**: No
**Status**: In Progress
**Workstream Goal**: Provide resilient local-first continuity, backup, and operational alerts without corrupting financial truth.

## Task Summary

Implement sync conflict handling and telemetry so acceptable non-financial changes resolve predictably, immutable financial truth is blocked from silent overwrite, and governance consumers can inspect sync health.

## Context

- Existing sync push/pull controller: `bizPA/backend/src/controllers/syncController.js`
- Existing envelope/conflict helpers: `bizPA/backend/src/services/syncEnvelopeService.js`
- Existing sync payload validation: `bizPA/backend/src/services/syncValidationService.js`
- Existing monetary integrity rules from A2: `bizPA/backend/src/services/monetaryIntegrityService.js`
- Existing sync verification: `bizPA/backend/verify_sync_service.js`

## Plan

- [x] 1. Expand sync conflict policy so non-financial records can follow a defined resolution path while financially sensitive records remain explicitly blocked.
  - [x] Test: `node bizPA/backend/verify_sync_service.js` passes and confirms both permissive and blocked conflict paths.
  - Evidence: `verify_sync_service=PASS` with `{"normalized_changes":1,"conflict_checks":3,"envelope_changes":1}` after adding stale non-financial LWW handling plus explicit financial and tenant conflict metadata.
- [x] 2. Add sync health telemetry generation and expose backlog, error rate, and last successful sync details through the sync API surface.
  - [x] Test: `node bizPA/backend/verify_sync_health_telemetry.js` passes and confirms telemetry fields for tenant scope, backlog size, error rate, and last successful sync.
  - Evidence: `verify_sync_health_telemetry=PASS` with `{"backlog_size":2,"error_rate":0.25,"last_successful_sync":"2026-03-11T20:05:30.000Z","tenant_scope":"00000000-0000-0000-0000-000000000000"}` after adding sync run telemetry builders, `/sync/health`, and push/pull telemetry payloads.
- [x] 3. Run end-to-end technical validation and update this lifecycle record with concrete results, file changes, and verification status.
  - [x] Test: `node bizPA/backend/verify_sync_service.js && node bizPA/backend/verify_sync_health_telemetry.js` both pass with recorded output snippets.
  - Evidence: Combined verification rerun passed; sync modules also loaded successfully with `sync_modules_ok` after requiring the updated controller and route.

## Implementation Log

- 2026-03-11 16:20:05Z - Task file received in `workstream/200_inprogress/gemini`.
- 2026-03-11 20:26:39Z - Read `skills/workstream-task-lifecycle/SKILL.md` and converted this file to the required lifecycle format before code edits.
- 2026-03-11 20:26:39Z - Inspected sync app client, backend sync controller, sync envelope service, sync validation service, and monetary integrity verification to define the implementation surface.
- 2026-03-11 20:26:39Z - Updated `syncEnvelopeService.js` to classify tenant-scope conflicts, block immutable monetary updates with explicit resolution metadata, and discard stale non-financial writes with a server-wins last-write-wins policy.
- 2026-03-11 20:26:39Z - Ran `node bizPA/backend/verify_sync_service.js`; verification passed.
- 2026-03-11 20:30:08Z - Added `syncHealthService.js`, telemetry migration SQL, `/api/v1/sync/health`, and telemetry payloads on sync push/pull responses with best-effort persistence into `sync_run_telemetry`.
- 2026-03-11 20:30:08Z - Ran `node bizPA/backend/verify_sync_health_telemetry.js`; verification passed.
- 2026-03-11 20:31:23Z - Re-ran both sync verification scripts and loaded the updated sync controller/route modules successfully.
- 2026-03-11 20:31:23Z - User verification requested for observable sync conflict and telemetry behavior; pending pass/fail response.

## Changes Made

- `bizPA/backend/src/services/syncEnvelopeService.js`
  - Added `conflict_type` and `resolution_strategy` to sync result envelopes.
  - Added stale version detection for non-financial records using record timestamps.
  - Added explicit metadata for tenant mismatch and immutable monetary conflict outcomes.
- `bizPA/backend/verify_sync_service.js`
  - Added verification coverage for acceptable non-financial stale-write resolution and richer blocked conflict metadata.
- `bizPA/backend/src/services/syncHealthService.js`
  - Added sync run telemetry builders, issue sampling, persistence helper, and health snapshot aggregation.
- `bizPA/backend/src/controllers/syncController.js`
  - Added telemetry generation for pull and push flows.
  - Added `getHealth` endpoint handler.
  - Made telemetry persistence best-effort so sync itself still completes if telemetry storage is unavailable.
- `bizPA/backend/src/routes/syncRoutes.js`
  - Added `GET /api/v1/sync/health`.
- `bizPA/backend/src/models/sync_health_telemetry_migration.sql`
  - Added `sync_run_telemetry` schema and indexes for dashboard queries.
- `bizPA/backend/verify_sync_health_telemetry.js`
  - Added verification for backlog size, error rate, tenant scope, and last successful sync aggregation.

## Validation

- 2026-03-11 20:26:39Z - `node bizPA/backend/verify_sync_service.js`
  - Result: PASS
  - Key output: `verify_sync_service=PASS`
  - Key output: `{"normalized_changes":1,"conflict_checks":3,"envelope_changes":1}`
- 2026-03-11 20:30:08Z - `node bizPA/backend/verify_sync_health_telemetry.js`
  - Result: PASS
  - Key output: `verify_sync_health_telemetry=PASS`
  - Key output: `{"backlog_size":2,"error_rate":0.25,"last_successful_sync":"2026-03-11T20:05:30.000Z","tenant_scope":"00000000-0000-0000-0000-000000000000"}`
- 2026-03-11 20:31:23Z - `node bizPA/backend/verify_sync_service.js; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }; node bizPA/backend/verify_sync_health_telemetry.js`
  - Result: PASS
  - Key output: `verify_sync_service=PASS`
  - Key output: `verify_sync_health_telemetry=PASS`
- 2026-03-11 20:31:23Z - `node -e "require('./src/controllers/syncController'); require('./src/routes/syncRoutes'); console.log('sync_modules_ok')"`
  - Result: PASS
  - Key output: `sync_modules_ok`
- 2026-03-11 20:31:23Z - User verification requested:
  - Acceptable non-financial conflicts should return a resolved success path using server-wins last-write-wins metadata instead of silently overwriting newer server data.
  - Financially sensitive immutable conflicts should return explicit blocked conflict metadata that points callers to a correction flow.
  - `GET /api/v1/sync/health` and sync push/pull responses should expose `backlog_size`, `error_rate`, `last_successful_sync`, and `tenant_scope`.
  - Pending user pass/fail response.

## Risks/Notes

- Current sync API has no dedicated telemetry endpoint; this task will likely add telemetry to the existing sync route surface unless the backend structure forces a separate route.
- Financial conflict rules must stay aligned with A2 monetary integrity semantics rather than creating a second source of truth.
- Because this changes observable API behavior, final completion may require explicit user verification before moving to `300_complete`.

## Completion Status

Awaiting user verification - 2026-03-11 20:31:23Z


## Execution Evidence
- Agent lane: gemini
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260311_162005_gemini_bizpa_mvp_product_requirements_document_workstreamG_add_sync_conflict_guardrails_and_health_telemetry.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented the sync guardrails and telemetry changes in the backend.

Key changes:
- [syncEnvelopeService.js](C:/Users/edebe/eds/bizPA/backend/src/services/syncEnvelopeService.js) now distinguishes acceptable non-financial stale writes from blocked financial conflicts. Non-financial stale updates resolve with explicit server-wins LWW metadata; immutable committed monetary updates remain blocked with correction-flow guidance.
- [syncHealthService.js](C:/Users/edebe/eds/bizPA/backend/src/services/syncHealthService.js), [syncController.js](C:/Users/edebe/eds/bizPA/backend/src/controllers/syncController.js), and [syncRoutes.js](C:/Users/edebe/eds/bizPA/backend/src/routes/syncRoutes.js) now emit sync telemetry on push/pull and expose `GET /api/v1/sync/health`.
- Added telemetry schema in [sync_health_telemetry_migration.sql](C:/Users/edebe/eds/bizPA/backend/src/models/sync_health_telemetry_migration.sql), plus verification coverage in [verify_sync_service.js](C:/Users/edebe/eds/bizPA/backend/verify_sync_service.js) and [verify_sync_health_telemetry.js](C:/Users/edebe/eds/bizPA/backend/verify_sync_health_telemetry.js).

Validation passed:
- `node bizPA/backend/verify_sync_service.js`
- `node bizPA/backend/verify_sync_health_telemetry.js`
- module load check for updated sync controller/routes

I also updated the lifecycle file and checklist in [20260311_162005_gemini_bizpa_mvp_product_requirements_document_workstreamG_add_sync_conflict_guardrails_and_health_telemetry.md](C:/Users/edebe/eds/workstream/200_inprogress/gemini/20260311_162005_gemini_bizpa_mvp_product_requirements_document_workstreamG_add_sync_conflict_guardrails_and_health_telemetry.md). It is left in `200_inprogress` with `Awaiting user verification`, per the lifecycle skill.

Please verify these three behaviors and reply `pass` or `fail` for each:
1. Non-financial stale conflicts resolve as a successful server-wins LWW outcome, not a silent overwrite.
2. Financially sensitive immutable conflicts return an explicit blocked conflict with correction-flow guidance.
3. Sync responses and `GET /api/v1/sync/health` expose `backlog_size`, `error_rate`, `last_successful_sync`, and `tenant_scope`.
```
- Stderr:
```text
cHealthService.js`, telemetry migration SQL, `/api/v1/sync/health`, and telemetry payloads on sync push/pull responses with best-effort persistence into `sync_run_telemetry`.
+- 2026-03-11 20:30:08Z - Ran `node bizPA/backend/verify_sync_health_telemetry.js`; verification passed.
+- 2026-03-11 20:31:23Z - Re-ran both sync verification scripts and loaded the updated sync controller/route modules successfully.
+- 2026-03-11 20:31:23Z - User verification requested for observable sync conflict and telemetry behavior; pending pass/fail response.
+
+## Changes Made
+
+- `bizPA/backend/src/services/syncEnvelopeService.js`
+  - Added `conflict_type` and `resolution_strategy` to sync result envelopes.
+  - Added stale version detection for non-financial records using record timestamps.
+  - Added explicit metadata for tenant mismatch and immutable monetary conflict outcomes.
+- `bizPA/backend/verify_sync_service.js`
+  - Added verification coverage for acceptable non-financial stale-write resolution and richer blocked conflict metadata.
+- `bizPA/backend/src/services/syncHealthService.js`
+  - Added sync run telemetry builders, issue sampling, persistence helper, and health snapshot aggregation.
+- `bizPA/backend/src/controllers/syncController.js`
+  - Added telemetry generation for pull and push flows.
+  - Added `getHealth` endpoint handler.
+  - Made telemetry persistence best-effort so sync itself still completes if telemetry storage is unavailable.
+- `bizPA/backend/src/routes/syncRoutes.js`
+  - Added `GET /api/v1/sync/health`.
+- `bizPA/backend/src/models/sync_health_telemetry_migration.sql`
+  - Added `sync_run_telemetry` schema and indexes for dashboard queries.
+- `bizPA/backend/verify_sync_health_telemetry.js`
+  - Added verification for backlog size, error rate, tenant scope, and last successful sync aggregation.
+
+## Validation
+
+- 2026-03-11 20:26:39Z - `node bizPA/backend/verify_sync_service.js`
+  - Result: PASS
+  - Key output: `verify_sync_service=PASS`
+  - Key output: `{"normalized_changes":1,"conflict_checks":3,"envelope_changes":1}`
+- 2026-03-11 20:30:08Z - `node bizPA/backend/verify_sync_health_telemetry.js`
+  - Result: PASS
+  - Key output: `verify_sync_health_telemetry=PASS`
+  - Key output: `{"backlog_size":2,"error_rate":0.25,"last_successful_sync":"2026-03-11T20:05:30.000Z","tenant_scope":"00000000-0000-0000-0000-000000000000"}`
+- 2026-03-11 20:31:23Z - `node bizPA/backend/verify_sync_service.js; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }; node bizPA/backend/verify_sync_health_telemetry.js`
+  - Result: PASS
+  - Key output: `verify_sync_service=PASS`
+  - Key output: `verify_sync_health_telemetry=PASS`
+- 2026-03-11 20:31:23Z - `node -e "require('./src/controllers/syncController'); require('./src/routes/syncRoutes'); console.log('sync_modules_ok')"`
+  - Result: PASS
+  - Key output: `sync_modules_ok`
+- 2026-03-11 20:31:23Z - User verification requested:
+  - Acceptable non-financial conflicts should return a resolved success path using server-wins last-write-wins metadata instead of silently overwriting newer server data.
+  - Financially sensitive immutable conflicts should return explicit blocked conflict metadata that points callers to a correction flow.
+  - `GET /api/v1/sync/health` and sync push/pull responses should expose `backlog_size`, `error_rate`, `last_successful_sync`, and `tenant_scope`.
+  - Pending user pass/fail response.
+
+## Risks/Notes
+
+- Current sync API has no dedicated telemetry endpoint; this task will likely add telemetry to the existing sync route surface unless the backend structure forces a separate route.
+- Financial conflict rules must stay aligned with A2 monetary integrity semantics rather than creating a second source of truth.
+- Because this changes observable API behavior, final completion may require explicit user verification before moving to `300_complete`.
+
+## Completion Status
+
+Awaiting user verification - 2026-03-11 20:31:23Z

tokens used
169,602
```
