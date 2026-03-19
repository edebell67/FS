# Task B1: Build Capture Composition And Preview Pipeline

Source: `workstream/000_epic/bizPA.md`

Task Summary: Implement the non-committed composition state and preview generation path for monetary captures, separating editable draft data from committed financial truth and adding confirm-time orchestration.

Context:
- `bizPA/backend/src/controllers/itemController.js`
- `bizPA/backend/src/controllers/voiceController.js`
- `bizPA/backend/src/routes/itemRoutes.js`
- `bizPA/backend/src/services/businessEventLogService.js`
- `bizPA/backend/src/services/monetaryIntegrityService.js`
- `bizPA/backend/verify_monetary_integrity_rules.js`

Plan:
- [x] 1. Add composition-state creation and preview payload generation for monetary captures in the backend API and voice flow.
  - [x] Test: `node -e "require('./src/controllers/itemController'); require('./src/controllers/voiceController'); console.log('controllers_load_ok')"` from `bizPA/backend` prints `controllers_load_ok`.
  - Evidence: 2026-03-11 17:21 GMT - command printed `controllers_load_ok` after loading updated item and voice controllers.
- [x] 2. Add explicit confirm commit orchestration so confirm creates/logs the committed entity transition and queues downstream recalculation/sync work without exposing composition as final truth.
  - [x] Test: `node verify_monetary_integrity_rules.js` from `bizPA/backend` exits 0 and prints `monetary_integrity_ok`.
  - Evidence: 2026-03-11 17:21 GMT - script passed and printed `monetary_integrity_ok`, `mutation_blocked=true`, and `invalid_transition_rejected=true`.
- [x] 3. Add focused verification coverage for preview/confirm behavior and record results.
  - [x] Test: `node verify_capture_composition_flow.js` from `bizPA/backend` exits 0 and prints `capture_composition_flow_ok`.
  - Evidence: 2026-03-11 17:23 GMT - script passed and printed `capture_composition_flow_ok`, `draft_preview_isolated=true`, `confirm_emits_business_events=true`, and `confirm_enqueues_sync_push=true`.

Implementation Log:
- 2026-03-11 17:15 GMT: Read `skills/workstream-task-lifecycle/SKILL.md`, reviewed the task file, inspected `bizPA` backend routes/controllers/services, and identified that monetary captures currently create items directly while `voiceController` still writes to a legacy `items` table.
- 2026-03-11 17:18 GMT: Updated `itemController` to create monetary captures as draft compositions, build structured preview payloads, suppress committed business-event emission during composition, and add explicit confirm orchestration with sync/readiness triggering.
- 2026-03-11 17:19 GMT: Updated `voiceController` to route monetary voice captures through the draft composition pipeline and return preview payloads instead of directly committing via the legacy `items` table.
- 2026-03-11 17:20 GMT: Added `POST /api/v1/items/:id/confirm` and authored `verify_capture_composition_flow.js` to validate draft isolation plus confirm-time event/sync behavior using a fake executor.
- 2026-03-11 17:22 GMT: Fixed confirm-time amount merge logic so edited monetary fields recalculate deterministically without leaking stale gross values.

Changes Made:
- `bizPA/backend/src/controllers/itemController.js`
- Added `buildMonetaryPreviewPayload`.
- Changed `createItem` so monetary `POST /api/v1/items` requests create draft compositions and return `action_status: preview_required` with a preview contract instead of immediately creating committed financial truth.
- Added `confirmCompositionInternal` and `confirmComposition` to promote a draft monetary composition to committed state, emit business events only on confirm, record readiness recalculation, and enqueue a `sync_push` job.
- Extended insert behavior to persist `captured_at` from the composition transaction date and to suppress committed business events while in composition.
- `bizPA/backend/src/controllers/voiceController.js`
- Replaced legacy `items` table writes for monetary voice captures with the new composition pipeline and preview response.
- Updated voice undo to remove the latest draft composition from `capture_items` instead of deleting from the legacy table.
- `bizPA/backend/src/routes/itemRoutes.js`
- Added `POST /api/v1/items/:id/confirm`.
- `bizPA/backend/verify_capture_composition_flow.js`
- Added verification coverage for draft preview isolation and confirm-time event/sync orchestration.

Validation:
- 2026-03-11 17:21 GMT - `node -e "require('./src/controllers/itemController'); require('./src/controllers/voiceController'); console.log('controllers_load_ok')"` from `bizPA/backend`
- Result: Passed. Output included `controllers_load_ok`.
- 2026-03-11 17:21 GMT - `node verify_monetary_integrity_rules.js` from `bizPA/backend`
- Result: Passed. Output included `monetary_integrity_ok`.
- 2026-03-11 17:23 GMT - `node verify_capture_composition_flow.js` from `bizPA/backend`
- Result: Passed. Output included `capture_composition_flow_ok`.
- 2026-03-11 17:24 GMT - User verification requested for:
- 1. Monetary captures stay in preview/composition state and do not appear as committed business activity until confirm.
- 2. Preview payload shows entity type, counterparty, net/VAT/gross, VAT rate, category, relevant date, and confidence indicator.
- 3. Confirm commits the item and triggers downstream event/sync behavior.
- Result: Pending user pass/fail confirmation.

Risks/Notes:
- Existing readiness and inbox controllers are bank-transaction focused, so this task is implemented by preventing monetary composition records from being emitted as committed business events and by only triggering downstream work on confirm.
- User verification will still be required before the task can be moved to `300_complete` because this changes user-visible capture behavior.

Completion Status:
- Awaiting user verification — 2026-03-11 17:24 GMT


## Execution Evidence
- Agent lane: gemini
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260311_161947_bizpa_mvp_product_requirements_document_workstreamB_build_capture_composition_and_preview_pipeline.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented the monetary capture composition/preview pipeline in the backend.

Monetary `POST /api/v1/items` calls now create a draft composition and return a structured preview instead of immediately committing financial truth, with preview-building and confirm orchestration in [itemController.js](/C:/Users/edebe/eds/bizPA/backend/src/controllers/itemController.js#L36) and [itemController.js](/C:/Users/edebe/eds/bizPA/backend/src/controllers/itemController.js#L335). Confirm is exposed at [itemRoutes.js](/C:/Users/edebe/eds/bizPA/backend/src/routes/itemRoutes.js#L27) and commits the item, emits business/readiness events, and enqueues `sync_push`. Voice monetary captures now use the same draft-preview path instead of the legacy `items` table in [voiceController.js](/C:/Users/edebe/eds/bizPA/backend/src/controllers/voiceController.js#L240). I also added focused verification in [verify_capture_composition_flow.js](/C:/Users/edebe/eds/bizPA/backend/verify_capture_composition_flow.js#L1).

Validations run:
- `node -e "require('./src/controllers/itemController'); require('./src/controllers/voiceController'); console.log('controllers_load_ok')"`
- `node verify_monetary_integrity_rules.js`
- `node verify_capture_composition_flow.js`

The lifecycle file is updated and left in `Awaiting user verification` at [20260311_161947_bizpa_mvp_product_requirements_document_workstreamB_build_capture_composition_and_preview_pipeline.md](/C:/Users/edebe/eds/workstream/200_inprogress/gemini/20260311_161947_bizpa_mvp_product_requirements_document_workstreamB_build_capture_composition_and_preview_pipeline.md).

Please verify pass/fail for these three behaviors:
1. Monetary captures stay in preview/composition state and do not appear as committed activity until confirm.
2. The preview payload contains entity type, counterparty, net/VAT/gross, VAT rate, category, relevant date, and confidence indicator.
3. Confirm commits the item and triggers the downstream event/sync behavior.
```
- Stderr:
```text
view_isolated=true`, `confirm_emits_business_events=true`, and `confirm_enqueues_sync_push=true`.
+
+Implementation Log:
+- 2026-03-11 17:15 GMT: Read `skills/workstream-task-lifecycle/SKILL.md`, reviewed the task file, inspected `bizPA` backend routes/controllers/services, and identified that monetary captures currently create items directly while `voiceController` still writes to a legacy `items` table.
+- 2026-03-11 17:18 GMT: Updated `itemController` to create monetary captures as draft compositions, build structured preview payloads, suppress committed business-event emission during composition, and add explicit confirm orchestration with sync/readiness triggering.
+- 2026-03-11 17:19 GMT: Updated `voiceController` to route monetary voice captures through the draft composition pipeline and return preview payloads instead of directly committing via the legacy `items` table.
+- 2026-03-11 17:20 GMT: Added `POST /api/v1/items/:id/confirm` and authored `verify_capture_composition_flow.js` to validate draft isolation plus confirm-time event/sync behavior using a fake executor.
+- 2026-03-11 17:22 GMT: Fixed confirm-time amount merge logic so edited monetary fields recalculate deterministically without leaking stale gross values.
+
+Changes Made:
+- `bizPA/backend/src/controllers/itemController.js`
+- Added `buildMonetaryPreviewPayload`.
+- Changed `createItem` so monetary `POST /api/v1/items` requests create draft compositions and return `action_status: preview_required` with a preview contract instead of immediately creating committed financial truth.
+- Added `confirmCompositionInternal` and `confirmComposition` to promote a draft monetary composition to committed state, emit business events only on confirm, record readiness recalculation, and enqueue a `sync_push` job.
+- Extended insert behavior to persist `captured_at` from the composition transaction date and to suppress committed business events while in composition.
+- `bizPA/backend/src/controllers/voiceController.js`
+- Replaced legacy `items` table writes for monetary voice captures with the new composition pipeline and preview response.
+- Updated voice undo to remove the latest draft composition from `capture_items` instead of deleting from the legacy table.
+- `bizPA/backend/src/routes/itemRoutes.js`
+- Added `POST /api/v1/items/:id/confirm`.
+- `bizPA/backend/verify_capture_composition_flow.js`
+- Added verification coverage for draft preview isolation and confirm-time event/sync orchestration.
+
+Validation:
+- 2026-03-11 17:21 GMT - `node -e "require('./src/controllers/itemController'); require('./src/controllers/voiceController'); console.log('controllers_load_ok')"` from `bizPA/backend`
+- Result: Passed. Output included `controllers_load_ok`.
+- 2026-03-11 17:21 GMT - `node verify_monetary_integrity_rules.js` from `bizPA/backend`
+- Result: Passed. Output included `monetary_integrity_ok`.
+- 2026-03-11 17:23 GMT - `node verify_capture_composition_flow.js` from `bizPA/backend`
+- Result: Passed. Output included `capture_composition_flow_ok`.
+- 2026-03-11 17:24 GMT - User verification requested for:
+- 1. Monetary captures stay in preview/composition state and do not appear as committed business activity until confirm.
+- 2. Preview payload shows entity type, counterparty, net/VAT/gross, VAT rate, category, relevant date, and confidence indicator.
+- 3. Confirm commits the item and triggers downstream event/sync behavior.
+- Result: Pending user pass/fail confirmation.
+
+Risks/Notes:
+- Existing readiness and inbox controllers are bank-transaction focused, so this task is implemented by preventing monetary composition records from being emitted as committed business events and by only triggering downstream work on confirm.
+- User verification will still be required before the task can be moved to `300_complete` because this changes user-visible capture behavior.
+
+Completion Status:
+- Awaiting user verification — 2026-03-11 17:24 GMT

tokens used
163,138
```
