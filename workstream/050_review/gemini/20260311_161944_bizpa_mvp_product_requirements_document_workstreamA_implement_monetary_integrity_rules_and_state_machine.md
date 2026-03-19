# Task Lifecycle: bizpa monetary integrity rules and state machine

Source: `workstream/000_epic/bizPA.md`

Task Summary:
Implement a central bizPA monetary integrity policy that blocks in-place mutation of committed monetary values, rejects invalid lifecycle transitions, prevents deletion of committed monetary items, and supports explicit void/replace/supersede correction flows with traceable metadata.

Context:
- `bizPA/backend/src/services/canonicalSchemaService.js` and `bizPA/backend/src/models/canonical_entity_event_schemas.json` define the canonical entity classes and status sets from A1.
- `bizPA/backend/src/controllers/itemController.js` currently exposes the main supported create/update/delete/convert service paths for `capture_items`.
- `bizPA/backend/src/routes/itemRoutes.js` is the current API surface for item operations.
- `bizPA/backend/src/models/schema.sql` and migrations still reflect legacy capture-era statuses, so enforcement needs to preserve compatibility while introducing explicit integrity policy behavior.

Plan:
- [x] 1. Inspect the canonical schema, PRD rules, and current item controller paths to define the compatibility-safe integrity policy surface.
  - [x] Test: Manual review of `workstream/000_epic/bizPA.md`, `bizPA/backend/src/services/canonicalSchemaService.js`, `bizPA/backend/src/controllers/itemController.js`, and `bizPA/backend/src/models/schema.sql` confirms which item types are monetary, what counts as committed, and which existing routes must be guarded.
  - Evidence: Reviewed PRD sections covering committed monetary immutability, A1 canonical monetary entity definitions, the legacy `capture_items` status constraint (`draft`/`confirmed`/`reconciled`/`archived`), and the existing `PATCH`, `DELETE`, and conversion controller flows before implementation.
- [x] 2. Implement the central monetary integrity rules engine and wire it into the supported backend item flows, including explicit correction-event support.
  - [x] Test: `node verify_monetary_integrity_rules.js` from `bizPA/backend` prints `monetary_integrity_ok` and confirms mutation blocking, transition rejection, and correction metadata generation.
  - Evidence: Added `bizPA/backend/src/services/monetaryIntegrityService.js`, integrated it into `bizPA/backend/src/controllers/itemController.js`, exposed `POST /api/v1/items/:id/corrections` in `bizPA/backend/src/routes/itemRoutes.js`, added `bizPA/backend/verify_monetary_integrity_rules.js`, and added the `verify:monetary-integrity` package script. Verification output: `monetary_integrity_ok`, `mutation_blocked=true`, `invalid_transition_rejected=true`, `correction_metadata_traced=true`.
- [x] 3. Validate package/runtime integrity, record results, and request user verification for the new business-logic behavior.
  - [x] Test: `node -e "require('./src/services/monetaryIntegrityService'); require('./src/controllers/itemController'); console.log('monetary_integrity_modules_ok')"` from `bizPA/backend` prints `monetary_integrity_modules_ok`.
  - Evidence: Module-load validation passed and `npm run verify:monetary-integrity` reproduced the same integrity success output. User verification requested in this task record for the new guarded update/delete behavior plus correction endpoint semantics.

Implementation Log:
- 2026-03-11 16:47:00+00:00 Reviewed `skills/workstream-task-lifecycle/SKILL.md`, loaded the assigned task file, and converted it into the required lifecycle format with sequential plan/test placeholders.
- 2026-03-11 16:51:00+00:00 Reviewed the completed A1 schema task, the canonical schema service, the current item controller, and the legacy capture schema to identify a compatibility-safe implementation path.
- 2026-03-11 17:02:00+00:00 Added `monetaryIntegrityService.js` with committed monetary immutability rules, legacy-compatible lifecycle transition validation, archive blocking, and correction metadata builders.
- 2026-03-11 17:08:00+00:00 Refactored `createItemInternal` to support shared transactions, added reusable audit insertion, guarded `updateItem` and `archiveItem`, and implemented `applyCorrection` for explicit `void`, `replace`, and `supersede` flows.
- 2026-03-11 17:10:00+00:00 Added the correction route and a focused verification script, then executed direct and package-script validations successfully.
- 2026-03-11 17:12:00+00:00 Updated lifecycle evidence and recorded pending user-verification requirements.

Changes Made:
- Added `bizPA/backend/src/services/monetaryIntegrityService.js` to centralize:
  - monetary type detection aligned to A1 canonical schema aliases,
  - committed-state detection for current legacy item statuses,
  - immutable committed field protection,
  - status/payment-status transition validation,
  - archive blocking for committed monetary items,
  - correction request validation and audit metadata generation.
- Updated `bizPA/backend/src/controllers/itemController.js` to:
  - share audit insertion through `writeAuditEvent`,
  - allow `createItemInternal` to run inside an external transaction,
  - reject in-place committed monetary edits through `updateItem`,
  - reject delete/archive of committed monetary items through `archiveItem`,
  - add `applyCorrection` for explicit `void`, `replace`, and `supersede` correction flows that emit traceable `audit_events`.
- Updated `bizPA/backend/src/routes/itemRoutes.js` with `POST /api/v1/items/:id/corrections`.
- Added `bizPA/backend/verify_monetary_integrity_rules.js` as an executable regression check for the new rules engine.
- Updated `bizPA/backend/package.json` with `verify:monetary-integrity`.

Validation:
- `node verify_monetary_integrity_rules.js`
  - Result: `monetary_integrity_ok`
  - Result: `mutation_blocked=true`
  - Result: `invalid_transition_rejected=true`
  - Result: `correction_metadata_traced=true`
- `npm run verify:monetary-integrity`
  - Result: package script executed successfully and reproduced the same integrity verification output.
- `node -e "require('./src/services/monetaryIntegrityService'); require('./src/controllers/itemController'); console.log('monetary_integrity_modules_ok')"`
  - Result: `.env` loaded, Supabase client initialized, and `monetary_integrity_modules_ok` printed successfully.
- User verification request:
  - Please verify these behaviors and respond pass/fail for each:
  - 1. Attempting to patch a committed monetary item amount now returns a conflict with an explainable immutable-field error.
  - 2. Attempting to delete/archive a committed monetary item now returns a conflict instructing the caller to use a correction flow.
  - 3. Posting to `POST /api/v1/items/:id/corrections` with `action=void|replace|supersede` records correction metadata and, for replace/supersede, creates a replacement item.

Risks/Notes:
- The current `capture_items` table still uses legacy statuses (`draft`, `confirmed`, `reconciled`, `archived`) and does not yet persist canonical correction fields directly, so this task needs to enforce integrity without breaking existing schema assumptions.
- Correction traceability is currently persisted through `audit_events.diff_log` metadata rather than new `capture_items` columns; a later schema migration can materialize canonical fields like `void_reason`, `superseded_by`, and `commit_timestamp` on the entity itself if required.
- Because this is business-logic behavior a user can validate, the lifecycle cannot be marked complete until user verification is requested and outcome captured.

Completion Status:
- Awaiting user verification — 2026-03-11 17:12:00+00:00.


## Execution Evidence
- Agent lane: gemini
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260311_161944_bizpa_mvp_product_requirements_document_workstreamA_implement_monetary_integrity_rules_and_state_machine.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented the monetary integrity rules end-to-end in the workspace and updated the lifecycle task file to `Awaiting user verification`.

The backend now has a central policy module at [monetaryIntegrityService.js](C:/Users/edebe/eds/bizPA/backend/src/services/monetaryIntegrityService.js), guarded item flows in [itemController.js](C:/Users/edebe/eds/bizPA/backend/src/controllers/itemController.js), a correction endpoint in [itemRoutes.js](C:/Users/edebe/eds/bizPA/backend/src/routes/itemRoutes.js), and an executable verification check in [verify_monetary_integrity_rules.js](C:/Users/edebe/eds/bizPA/backend/verify_monetary_integrity_rules.js). The lifecycle record is updated at [20260311_161944_bizpa_mvp_product_requirements_document_workstreamA_implement_monetary_integrity_rules_and_state_machine.md](C:/Users/edebe/eds/workstream/200_inprogress/gemini/20260311_161944_bizpa_mvp_product_requirements_document_workstreamA_implement_monetary_integrity_rules_and_state_machine.md).

Validation passed:
- `node verify_monetary_integrity_rules.js`
- `npm run verify:monetary-integrity`
- `node -e "require('./src/services/monetaryIntegrityService'); require('./src/controllers/itemController'); console.log('monetary_integrity_modules_ok')"`

User verification is still required before this task can be closed. Please verify pass/fail for these three behaviors:
1. Patching a committed monetary item amount now returns a conflict with an immutable-field error.
2. Deleting/archiving a committed monetary item now returns a conflict directing the caller to a correction flow.
3. `POST /api/v1/items/:id/corrections` with `action=void|replace|supersede` records correction metadata, and `replace`/`supersede` also create a replacement item.
```
- Stderr:
```text
ture schema to identify a compatibility-safe implementation path.
+- 2026-03-11 17:02:00+00:00 Added `monetaryIntegrityService.js` with committed monetary immutability rules, legacy-compatible lifecycle transition validation, archive blocking, and correction metadata builders.
+- 2026-03-11 17:08:00+00:00 Refactored `createItemInternal` to support shared transactions, added reusable audit insertion, guarded `updateItem` and `archiveItem`, and implemented `applyCorrection` for explicit `void`, `replace`, and `supersede` flows.
+- 2026-03-11 17:10:00+00:00 Added the correction route and a focused verification script, then executed direct and package-script validations successfully.
+- 2026-03-11 17:12:00+00:00 Updated lifecycle evidence and recorded pending user-verification requirements.
+
+Changes Made:
+- Added `bizPA/backend/src/services/monetaryIntegrityService.js` to centralize:
+  - monetary type detection aligned to A1 canonical schema aliases,
+  - committed-state detection for current legacy item statuses,
+  - immutable committed field protection,
+  - status/payment-status transition validation,
+  - archive blocking for committed monetary items,
+  - correction request validation and audit metadata generation.
+- Updated `bizPA/backend/src/controllers/itemController.js` to:
+  - share audit insertion through `writeAuditEvent`,
+  - allow `createItemInternal` to run inside an external transaction,
+  - reject in-place committed monetary edits through `updateItem`,
+  - reject delete/archive of committed monetary items through `archiveItem`,
+  - add `applyCorrection` for explicit `void`, `replace`, and `supersede` correction flows that emit traceable `audit_events`.
+- Updated `bizPA/backend/src/routes/itemRoutes.js` with `POST /api/v1/items/:id/corrections`.
+- Added `bizPA/backend/verify_monetary_integrity_rules.js` as an executable regression check for the new rules engine.
+- Updated `bizPA/backend/package.json` with `verify:monetary-integrity`.
+
+Validation:
+- `node verify_monetary_integrity_rules.js`
+  - Result: `monetary_integrity_ok`
+  - Result: `mutation_blocked=true`
+  - Result: `invalid_transition_rejected=true`
+  - Result: `correction_metadata_traced=true`
+- `npm run verify:monetary-integrity`
+  - Result: package script executed successfully and reproduced the same integrity verification output.
+- `node -e "require('./src/services/monetaryIntegrityService'); require('./src/controllers/itemController'); console.log('monetary_integrity_modules_ok')"`
+  - Result: `.env` loaded, Supabase client initialized, and `monetary_integrity_modules_ok` printed successfully.
+- User verification request:
+  - Please verify these behaviors and respond pass/fail for each:
+  - 1. Attempting to patch a committed monetary item amount now returns a conflict with an explainable immutable-field error.
+  - 2. Attempting to delete/archive a committed monetary item now returns a conflict instructing the caller to use a correction flow.
+  - 3. Posting to `POST /api/v1/items/:id/corrections` with `action=void|replace|supersede` records correction metadata and, for replace/supersede, creates a replacement item.
+
+Risks/Notes:
+- The current `capture_items` table still uses legacy statuses (`draft`, `confirmed`, `reconciled`, `archived`) and does not yet persist canonical correction fields directly, so this task needs to enforce integrity without breaking existing schema assumptions.
+- Correction traceability is currently persisted through `audit_events.diff_log` metadata rather than new `capture_items` columns; a later schema migration can materialize canonical fields like `void_reason`, `superseded_by`, and `commit_timestamp` on the entity itself if required.
+- Because this is business-logic behavior a user can validate, the lifecycle cannot be marked complete until user verification is requested and outcome captured.
+
+Completion Status:
+- Awaiting user verification — 2026-03-11 17:12:00+00:00.

tokens used
69,976
```
