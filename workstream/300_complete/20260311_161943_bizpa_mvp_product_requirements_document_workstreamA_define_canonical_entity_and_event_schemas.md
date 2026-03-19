# Task Lifecycle: bizpa canonical entity and event schemas

Source: `workstream/epic/bizPA.md`

Task Summary:
Define the canonical MVP schema contract for bizPA monetary entities, non-monetary entities, quarter snapshots, and immutable business events. Deliver a versioned machine-readable schema, supporting field dictionary, validation helpers, and executable checks that later workstreams can consume as the shared source of truth.

Context:
- `bizPA/backend/src/models` contains the backend schema and migration artifacts.
- `bizPA/backend/src/services` contains reusable backend domain helpers.
- `bizPA/docs` contains product-facing schema and field dictionary documentation.
- Existing files `bizPA/docs/json_schema_definitions.md` and `bizPA/docs/core_entity_dictionary.md` reflect older capture-era structures and needed canonical redirection for the quarterly MVP.

Plan:
- [x] 1. Inspect the epic, PRD-aligned backend files, and existing docs to define the canonical MVP entity/event scope.
  - [x] Test: Manual review of `workstream/epic/bizPA.md`, `bizPA/backend/src/controllers/itemController.js`, `bizPA/backend/src/controllers/exportController.js`, and `bizPA/backend/src/controllers/vatController.js` confirms required monetary fields, quarter handling, and export/snapshot expectations are captured.
  - Evidence: Reviewed PRD sections 9-17 plus backend references to `quarter_ref`, export columns, snapshot pack requirements, and invoice lifecycle fields before implementation.
- [x] 2. Implement the canonical schema artifacts, field dictionary, and validation helpers in the bizPA workspace.
  - [x] Test: `node validate_canonical_schemas.js` from `bizPA/backend` returns `canonical_schema_ok` and lists all required monetary/non-monetary entity sets.
  - Evidence: Added `bizPA/backend/src/models/canonical_entity_event_schemas.json`, `bizPA/backend/src/services/canonicalSchemaService.js`, `bizPA/backend/validate_canonical_schemas.js`, `bizPA/docs/canonical_entity_event_schemas.md`, and `bizPA/docs/canonical_field_dictionary.md`; updated `bizPA/backend/package.json` plus supersession notes in the older docs.
- [x] 3. Validate JSON/package integrity, capture results, and close the lifecycle task.
  - [x] Test: `node -e "JSON.parse(require('fs').readFileSync('C:/Users/edebe/eds/bizPA/backend/src/models/canonical_entity_event_schemas.json','utf8')); JSON.parse(require('fs').readFileSync('C:/Users/edebe/eds/bizPA/backend/package.json','utf8')); console.log('json_parse_ok')"` prints `json_parse_ok`.
  - Evidence: JSON schema artifact and backend package manifest both parsed successfully after edits; lifecycle record updated with command results and moved to complete.

Implementation Log:
- 2026-03-11 16:20: Reviewed `skills/workstream-task-lifecycle/SKILL.md` and loaded the assigned task file.
- 2026-03-11 16:24: Inspected the bizPA epic plus backend controller/model references to reconcile the newer quarterly/export MVP with the older capture-only docs.
- 2026-03-11 16:34: Authored a new machine-readable canonical schema artifact covering monetary entities, non-monetary entities, event types, quarter reference conventions, and shared field mappings.
- 2026-03-11 16:37: Added a reusable backend schema service with entity/event validation helpers and quarter derivation logic for future workstreams.
- 2026-03-11 16:39: Added human-readable schema and field dictionary docs and marked older docs as superseded for the quarterly MVP path.
- 2026-03-11 16:41: Added backend script `validate:canonical-schemas` and executed validation successfully.
- 2026-03-11 16:44: Recorded validation evidence and prepared lifecycle completion.

Changes Made:
- Added versioned canonical schema source at `bizPA/backend/src/models/canonical_entity_event_schemas.json`.
- Added reusable validation/lookup helpers at `bizPA/backend/src/services/canonicalSchemaService.js`.
- Added executable regression check at `bizPA/backend/validate_canonical_schemas.js`.
- Added canonical documentation at `bizPA/docs/canonical_entity_event_schemas.md`.
- Added export/snapshot field mapping reference at `bizPA/docs/canonical_field_dictionary.md`.
- Updated `bizPA/backend/package.json` with `validate:canonical-schemas`.
- Added supersession pointers in `bizPA/docs/json_schema_definitions.md` and `bizPA/docs/core_entity_dictionary.md`.

Validation:
- `node validate_canonical_schemas.js`
  - Result: `canonical_schema_ok`
  - Result: `monetary_types=invoice,receipt_expense,payment,quote,monetary_booking`
  - Result: `non_monetary_types=note,attachment,booking,client,supplier,reminder,snapshot`
  - Result: `event_types=15`
- `npm run validate:canonical-schemas`
  - Result: script executed successfully and reproduced the same `canonical_schema_ok` output.
- `node -e "JSON.parse(require('fs').readFileSync('C:/Users/edebe/eds/bizPA/backend/src/models/canonical_entity_event_schemas.json','utf8')); JSON.parse(require('fs').readFileSync('C:/Users/edebe/eds/bizPA/backend/package.json','utf8')); console.log('json_parse_ok')"`
  - Result: `json_parse_ok`
- User verification request: Not required for this task because the deliverable is schema/documentation/validation infrastructure with no direct UI behavior change.

Risks/Notes:
- The existing runtime still uses legacy names such as `quarter_ref` and mixed status sets in controllers and SQL; this task defines the canonical target contract but does not migrate all runtime consumers yet.
- `deriveQuarterReference` currently uses UTC when computing the label in the helper module; downstream implementation work should swap this to tenant-local logic where tenant timezone context exists.
- Repo worktree already contained extensive unrelated modifications and untracked files; those were left untouched.

Completion Status:
- Complete — 2026-03-11 16:44:24+00:00
