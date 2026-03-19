## Source
- `workstream/000_epic/bizPA.md`

## Task Summary
Implement the accountant-ready export package builder for bizPA so a selected snapshot version can be re-exported into a reproducible package containing a structured CSV, VAT summary document, integrity report, snapshot metadata, and packaged download artifact.

## Context
- Existing export flow lives in `bizPA/backend/src/controllers/exportController.js`.
- Canonical export fields and snapshot contract live in `bizPA/backend/src/models/canonical_entity_event_schemas.json`.
- Snapshot creation currently exists as a business event log action in `bizPA/backend/src/controllers/businessEventController.js` and `bizPA/backend/src/services/businessEventLogService.js`.
- This task depends conceptually on Workstream A1 canonical schema discipline and E1 snapshot records; current implementation will use immutable snapshot payloads stored in snapshot events so the export builder can operate deterministically.

## Plan
- [x] 1. Inspect the current export controller, snapshot event flow, and canonical schema contract to define the minimal snapshot-backed package builder surface.
  - [x] Test: `rg -n "exportQuarterlyPack|createSnapshot|recordSnapshotCreated|\"snapshot\"|\"export_column\"" bizPA/backend/src`
  - Evidence: Command returned the expected implementation anchors in `src/controllers/exportController.js`, `src/controllers/businessEventController.js`, `src/services/businessEventLogService.js`, `src/routes/exportRoutes.js`, and canonical export field mappings in `src/models/canonical_entity_event_schemas.json`.
- [x] 2. Implement a deterministic snapshot export package builder service and wire the quarterly export endpoint to support snapshot-based package generation.
  - [x] Test: `node -e "require('./src/services/exportPackageBuilderService')"`, run from `bizPA/backend`, and pass when the module loads without throwing.
  - Evidence: Command exited `0` with no output, confirming the new service module loads successfully.
- [x] 3. Add focused regression coverage proving package completeness, canonical CSV column alignment, and reproducible re-export behavior for the same snapshot.
  - [x] Test: `node verify_export_package_builder.js`, run from `bizPA/backend`, and pass when all export package assertions succeed.
  - Evidence: Command output `verify_export_package_builder=PASS`.
- [x] 4. Run route-level and schema validation relevant to the new export flow, then update this file with exact results and request user verification.
  - [x] Test: `npm run validate:canonical-schemas`, run from `bizPA/backend`, and pass when canonical schema validation succeeds after the export changes.
  - Evidence: Command output `canonical_schema_ok`, `vat_classification_ok`, and `quarter_boundary_ok`.

## Implementation Log
- 2026-03-11 18:xx - Read `skills/workstream-task-lifecycle/SKILL.md` and the assigned task file.
- 2026-03-11 18:xx - Inspected existing bizPA quarterly export, snapshot event logging, and canonical schema definitions to determine the implementation path.
- 2026-03-11 18:xx - Reworked the task file into the required lifecycle template with ordered checklist steps, explicit tests, and evidence placeholders before code edits.
- 2026-03-11 18:xx - Added `src/services/exportPackageBuilderService.js` to normalize immutable snapshot payloads, enforce canonical export column order, build the accountant-ready files, compute deterministic hashes, and fetch snapshot payloads from `snapshot_created` business events.
- 2026-03-11 18:xx - Updated `src/controllers/exportController.js` so `GET /api/v1/export/quarterly-pack?snapshot_id=<id>` now builds a snapshot-based package while preserving the legacy period-based export path.
- 2026-03-11 18:xx - Added `verify_export_package_builder.js` and `test_fixtures/export_package_snapshot_fixture.json` to prove package completeness, canonical CSV alignment, and reproducible re-export behavior.
- 2026-03-11 18:xx - Ran module-load, package-builder, and canonical schema validation checks; all passed.

## Changes Made
- Added `bizPA/backend/src/services/exportPackageBuilderService.js`.
- Updated `bizPA/backend/src/controllers/exportController.js`.
- Added `bizPA/backend/verify_export_package_builder.js`.
- Added `bizPA/backend/test_fixtures/export_package_snapshot_fixture.json`.
- New behavior:
  - `GET /api/v1/export/quarterly-pack` now supports `snapshot_id` and builds the export from immutable snapshot event metadata.
  - The package contains `structured_csv.csv`, `vat_summary_document.pdf`, `integrity_report.json`, `snapshot_metadata.json`, and `package_manifest.json`.
  - Structured CSV columns now follow the canonical export column order from schema A1.
  - Package contents are deterministic for the same snapshot payload, with stable per-file SHA-256 hashes and package manifest checksum.
- Snapshot assumptions:
  - The snapshot export path expects the `snapshot_created` event metadata to carry the snapshot payload directly or under `metadata.snapshot`, including canonical transaction records.

## Validation
- `rg -n "exportQuarterlyPack|createSnapshot|recordSnapshotCreated|\"snapshot\"|\"export_column\"" bizPA/backend/src`
  - Passed. Confirmed the export controller, snapshot event flow, and canonical schema mappings used for this task.
- `node -e "require('./src/services/exportPackageBuilderService')"` (run in `bizPA/backend`)
  - Passed. Exit code `0`.
- `node verify_export_package_builder.js` (run in `bizPA/backend`)
  - Passed. Output: `verify_export_package_builder=PASS`
- `npm run validate:canonical-schemas` (run in `bizPA/backend`)
  - Passed. Output included `canonical_schema_ok`, `monetary_types=invoice,receipt_expense,payment,quote,monetary_booking`, `event_types=15`, `vat_classification_ok`, `quarter_boundary_ok`.
- 2026-03-11 18:xx - User verification requested for the new snapshot-based export behavior:
  - Verify that a known snapshot can be exported through `GET /api/v1/export/quarterly-pack?snapshot_id=<snapshot_id>`.
  - Verify that the zip contents are accountant-ready for your expected downstream consumer.
  - Verify that re-exporting the same snapshot yields the same file set and expected metadata.

## Risks/Notes
- Snapshot persistence from Workstream E1 is not yet represented as a dedicated table in the current backend. The implementation will therefore anchor export reproducibility on immutable snapshot payloads carried by snapshot business events unless a stronger in-repo store already exists.
- Because this changes export output behavior, final lifecycle completion requires explicit user verification per the skill gate.
- If existing snapshot events do not yet include canonical transaction arrays in their metadata, the new `snapshot_id` export path will return a server error until E1 writes the expected immutable payload.

## Completion Status
- Awaiting user verification.


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260311_162002_claude_bizpa_mvp_product_requirements_document_workstreamF_implement_accountant_ready_export_package_builder.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented the snapshot-based accountant export builder in [exportPackageBuilderService.js](/C:/Users/edebe/eds/bizPA/backend/src/services/exportPackageBuilderService.js) and wired it into [exportController.js](/C:/Users/edebe/eds/bizPA/backend/src/controllers/exportController.js). `GET /api/v1/export/quarterly-pack?snapshot_id=<snapshot_id>` now builds a deterministic zip from immutable snapshot event metadata, with `structured_csv.csv`, `vat_summary_document.pdf`, `integrity_report.json`, `snapshot_metadata.json`, and `package_manifest.json`.

I added focused regression coverage in [verify_export_package_builder.js](/C:/Users/edebe/eds/bizPA/backend/verify_export_package_builder.js) with fixture data in [export_package_snapshot_fixture.json](/C:/Users/edebe/eds/bizPA/backend/test_fixtures/export_package_snapshot_fixture.json). The lifecycle file was updated and is now marked awaiting verification at [20260311_162002_claude_bizpa_mvp_product_requirements_document_workstreamF_implement_accountant_ready_export_package_builder.md](/C:/Users/edebe/eds/workstream/200_inprogress/claude/20260311_162002_claude_bizpa_mvp_product_requirements_document_workstreamF_implement_accountant_ready_export_package_builder.md).

Validation passed:
- `node -e "require('./src/services/exportPackageBuilderService')"`
- `node verify_export_package_builder.js`
- `npm run validate:canonical-schemas`

Verification needed from you before this can be closed:
1. Call `GET /api/v1/export/quarterly-pack?snapshot_id=<snapshot_id>` against a real snapshot event.
2. Confirm the zip contents are acceptable for your accountant workflow.
3. Confirm re-exporting the same snapshot gives the same file set and expected metadata.

One risk remains: the new `snapshot_id` path expects snapshot event metadata to already contain the immutable snapshot payload, including canonical transaction records.
```
- Stderr:
```text
shot event logging, and canonical schema definitions to determine the implementation path.
+- 2026-03-11 18:xx - Reworked the task file into the required lifecycle template with ordered checklist steps, explicit tests, and evidence placeholders before code edits.
+- 2026-03-11 18:xx - Added `src/services/exportPackageBuilderService.js` to normalize immutable snapshot payloads, enforce canonical export column order, build the accountant-ready files, compute deterministic hashes, and fetch snapshot payloads from `snapshot_created` business events.
+- 2026-03-11 18:xx - Updated `src/controllers/exportController.js` so `GET /api/v1/export/quarterly-pack?snapshot_id=<id>` now builds a snapshot-based package while preserving the legacy period-based export path.
+- 2026-03-11 18:xx - Added `verify_export_package_builder.js` and `test_fixtures/export_package_snapshot_fixture.json` to prove package completeness, canonical CSV alignment, and reproducible re-export behavior.
+- 2026-03-11 18:xx - Ran module-load, package-builder, and canonical schema validation checks; all passed.
+
+## Changes Made
+- Added `bizPA/backend/src/services/exportPackageBuilderService.js`.
+- Updated `bizPA/backend/src/controllers/exportController.js`.
+- Added `bizPA/backend/verify_export_package_builder.js`.
+- Added `bizPA/backend/test_fixtures/export_package_snapshot_fixture.json`.
+- New behavior:
+  - `GET /api/v1/export/quarterly-pack` now supports `snapshot_id` and builds the export from immutable snapshot event metadata.
+  - The package contains `structured_csv.csv`, `vat_summary_document.pdf`, `integrity_report.json`, `snapshot_metadata.json`, and `package_manifest.json`.
+  - Structured CSV columns now follow the canonical export column order from schema A1.
+  - Package contents are deterministic for the same snapshot payload, with stable per-file SHA-256 hashes and package manifest checksum.
+- Snapshot assumptions:
+  - The snapshot export path expects the `snapshot_created` event metadata to carry the snapshot payload directly or under `metadata.snapshot`, including canonical transaction records.
+
+## Validation
+- `rg -n "exportQuarterlyPack|createSnapshot|recordSnapshotCreated|\"snapshot\"|\"export_column\"" bizPA/backend/src`
+  - Passed. Confirmed the export controller, snapshot event flow, and canonical schema mappings used for this task.
+- `node -e "require('./src/services/exportPackageBuilderService')"` (run in `bizPA/backend`)
+  - Passed. Exit code `0`.
+- `node verify_export_package_builder.js` (run in `bizPA/backend`)
+  - Passed. Output: `verify_export_package_builder=PASS`
+- `npm run validate:canonical-schemas` (run in `bizPA/backend`)
+  - Passed. Output included `canonical_schema_ok`, `monetary_types=invoice,receipt_expense,payment,quote,monetary_booking`, `event_types=15`, `vat_classification_ok`, `quarter_boundary_ok`.
+- 2026-03-11 18:xx - User verification requested for the new snapshot-based export behavior:
+  - Verify that a known snapshot can be exported through `GET /api/v1/export/quarterly-pack?snapshot_id=<snapshot_id>`.
+  - Verify that the zip contents are accountant-ready for your expected downstream consumer.
+  - Verify that re-exporting the same snapshot yields the same file set and expected metadata.
+
+## Risks/Notes
+- Snapshot persistence from Workstream E1 is not yet represented as a dedicated table in the current backend. The implementation will therefore anchor export reproducibility on immutable snapshot payloads carried by snapshot business events unless a stronger in-repo store already exists.
+- Because this changes export output behavior, final lifecycle completion requires explicit user verification per the skill gate.
+- If existing snapshot events do not yet include canonical transaction arrays in their metadata, the new `snapshot_id` export path will return a server error until E1 writes the expected immutable payload.
+
+## Completion Status
+- Awaiting user verification.

tokens used
219,949
```
