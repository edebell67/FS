# Source
- Augmented task request in this lifecycle file on 2026-03-15.
- Source solution root: `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`

# Task Summary
Create a contract-first API documentation package for the bank-feed-first quarterly export MVP, covering connect, import, export, and export-status flows with OpenAPI and usage guidance aligned to the existing backend domain model.

# Context
- Solution root: `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
- Existing backend references:
  - `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\models\mvp_domain_schemas.json`
  - `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\services\openBankingAdapter.js`
  - `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\services\transactionImportService.js`
- Target docs:
  - `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\docs\api\openapi.yaml`
  - `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\docs\api\usage.md`
- Task note: the originally referenced `README.md` and `docs\README.md` files do not exist in the current workspace, so this task is anchored to the live backend/domain files above instead.

# Dependency
Dependency: None

# Plan
- [x] 1. Normalize this lifecycle file to the required workstream template and anchor the task to the concrete solution files that exist in the workspace.
  - [x] Test: `Test-Path 'C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_contract_first_api_documentation_for.md'` returned `True`, and `Select-String` confirmed the file contains `# Evidence` plus `Dependency: None`.
  - Evidence: Lifecycle file rewritten to the mandated template and anchored to the live backend/domain artifacts instead of the stale README paths.
- [x] 2. Create the contract-first API documentation package with all four planned endpoints, aligned request/response schemas, workflow examples, auth expectations, idempotency notes, and implementation-consumer integration notes.
  - [x] Test: `Test-Path` returned `True` for both target docs, `Select-String` found `/api/v1/bank-feeds/connect`, `/api/v1/imports`, `/api/v1/exports/quarterly`, and `/api/v1/exports/{exportId}` in `docs/api/openapi.yaml`, and `docs/api/usage.md` contains the connect, import, export, and export-status workflow sequence.
  - Evidence: `docs/api/openapi.yaml` and `docs/api/usage.md` created with four requested endpoints, workflow-specific examples, auth and idempotency notes, and backend/frontend integration notes.
- [x] 3. Validate the OpenAPI document parses, confirm the package matches the backend/domain context, and finalize the lifecycle evidence and completion state.
  - [x] Test: A Python `yaml.safe_load` parse of `docs/api/openapi.yaml` succeeded with `endpoint_count=4`, and `node validate_mvp_domain_schemas.js` passed in `solution/backend`.
  - Evidence: Validation output captured below confirms YAML parse success, four-path coverage, bearer auth presence, usage guide coverage, and existing backend domain-schema validation success.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\300_complete\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_contract_first_api_documentation_for.md`
  - Objective-Proved: The task lifecycle was normalized, executed, validated, and archived in the required workstream location.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\docs\api\openapi.yaml` and `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\docs\api\usage.md`
  - Objective-Proved: The requested API reference package exists at the agreed location with OpenAPI and usage guidance for the bank-feed-first quarterly export flow.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `{"yaml_available": true, "endpoint_count": 4, "has_connect": true, "has_imports": true, "has_quarterly": true, "has_export_status": true, "has_bearer_auth": true}`, `{"Exists":true,"HasConnect":true,"HasImports":true,"HasExport":true,"HasStatus":true,"HasIdempotency":true}`, and `mvp_domain_schema_ok / entities=10 / category_codes=18 / transaction_fields=14 / evidence_fields=10 / summary_fields=8`
  - Objective-Proved: The OpenAPI file parses, exposes the four required endpoints with bearer auth, the usage guide covers the workflow and idempotency guidance, and the existing backend domain schema remains valid.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `git diff --no-index -- 'NUL' 'C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\docs\api\openapi.yaml'`, `git diff --no-index -- 'NUL' 'C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\docs\api\usage.md'`, and `git status --short -- 'ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/api/openapi.yaml' 'ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/api/usage.md' 'workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_contract_first_api_documentation_for.md'`
  - Objective-Proved: The workspace contains the new API documentation package and the updated lifecycle file.
  - Status: captured

# Implementation Log
- 2026-03-15 17:06:53: Task generated via epic augmentation.
- 2026-03-18 17:21:29: Retry scheduled.
- 2026-03-19 17:00: Began task execution under Codex, loaded the required lifecycle skill, and inspected the existing backend/domain files.
- 2026-03-19 17:08: Located the live solution references and confirmed the task's `README.md` source paths are stale in the current workspace.
- 2026-03-19 17:18: Created `docs/api/openapi.yaml` with the four requested endpoints, contract schemas, examples, auth semantics, idempotency guidance, and implementation notes.
- 2026-03-19 17:20: Created `docs/api/usage.md` documenting the client sequence from bank connection through quarterly export download.
- 2026-03-19 17:27: Removed an accidental import-status link from the OpenAPI response so the contract stays scoped to the four requested endpoints.
- 2026-03-19 17:32:14: Captured validation outputs, updated evidence, and archived the task to `workstream/300_complete/codex`.
- 2026-03-19 17:43: Re-opened the task context from the `.result.md` transcript artifact, verified the archived lifecycle file is the active source of truth, and re-ran the package validations in the current workspace.

# Changes Made
- Added `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\docs\api\openapi.yaml` with:
  - `POST /api/v1/bank-feeds/connect`
  - `POST /api/v1/imports`
  - `POST /api/v1/exports/quarterly`
  - `GET /api/v1/exports/{exportId}`
- Added request/response schemas for bank feed connection, import submission, quarterly export creation, export status retrieval, and shared error responses.
- Added workflow-specific request/response examples, bearer auth expectations, and `Idempotency-Key` header guidance.
- Added `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\docs\api\usage.md` with sequence, client examples, error semantics, idempotency notes, and consumer integration notes.
- Rewrote this lifecycle file to the required workstream template and recorded the stale README path mismatch as a documented note rather than a hidden assumption.

# Validation
- 2026-03-19: Lifecycle template validation:
  - `{"Exists":true,"HasEvidence":true,"HasDependency":true}`
- 2026-03-19: API package presence and workflow coverage validation:
  - `{"OpenApiExists":true,"UsageExists":true,"Connect":true,"Imports":true,"Quarterly":true,"ExportStatus":true,"UsageSequence":true,"UsageConnect":true,"UsageImports":true,"UsageExport":true,"UsageStatus":true}`
- 2026-03-19: OpenAPI parse validation executed with Python because `ConvertFrom-Yaml` is unavailable in this PowerShell environment:
  - `{"yaml_available": true, "endpoint_count": 4, "has_connect": true, "has_imports": true, "has_quarterly": true, "has_export_status": true, "has_bearer_auth": true}`
- 2026-03-19: Example and integration-note spot-check on `openapi.yaml`:
  - `{"ConnectExamples":4,"HasIdempotencyHeader":true,"HasBackendNote":true,"HasFrontendNote":true}`
- 2026-03-19: Existing backend schema validation:
  - `mvp_domain_schema_ok`
  - `entities=10`
  - `category_codes=18`
  - `transaction_fields=14`
  - `evidence_fields=10`
  - `summary_fields=8`
- 2026-03-19: Diff/status evidence capture:
  - `git diff --no-index` created new-file diffs for `docs/api/openapi.yaml` and `docs/api/usage.md`
  - `git status --short` reported:
    - `?? ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/api/openapi.yaml`
    - `?? ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/api/usage.md`
    - `?? workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_contract_first_api_documentation_for.md`
- 2026-03-19: Lifecycle archive validation:
  - `{"InProgressExists":false,"CompleteExists":true}`
  - `git status --short` after archive reported:
    - `?? ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/api/openapi.yaml`
    - `?? ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docs/api/usage.md`
    - `?? workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_contract_first_api_documentation_for.md`
- 2026-03-19: Current-workspace rerun from the requested `.result.md` artifact:
  - `{"TranscriptArtifactExists":true,"ArchivedLifecycleExists":true,"ApiDocFolderExists":true}`
  - `{"yaml_available": true, "endpoint_count": 4, "has_connect": true, "has_imports": true, "has_quarterly": true, "has_export_status": true, "has_bearer_auth": true}`
  - `mvp_domain_schema_ok`
  - `entities=10`
  - `category_codes=18`
  - `transaction_fields=14`
  - `evidence_fields=10`
  - `summary_fields=8`

# Risks/Notes
- The repository has extensive unrelated in-progress changes; this task is limited to the quarterly export MVP documentation subtree and its lifecycle file.
- The source README paths named in the original task are stale in the current workspace, so this implementation uses the live backend/domain artifacts as the authoritative references.
- No OpenAPI linter is installed in the workspace. YAML parsing plus targeted content checks were used as the contract validation path.
- `workstream/200_inprogress/codex/...md.result.md` is a transcript artifact from a prior execution, not the active lifecycle file. The archived `.md` file in `workstream/300_complete/codex` remains the authoritative task record.

# Completion Status
- Complete on 2026-03-19 17:32:14. Auto-acceptance criteria met with `Objective-Delivery-Coverage: 100%` and `Auto-Acceptance: true`.
