# TASK B2: Implement Voice Parsing For Core Monetary And Note Intents

**Source**: `workstream/000_epic/bizPA.md`
**Task Summary**: Implement a rule-first voice parser for bizPA MVP utterances so invoice, receipt, quote, payment, booking, and note speech inputs are normalized into structured candidate payloads with confidence scoring and explicit review fallback when extraction is uncertain.

## Context

- `bizPA/backend/src/controllers/voiceController.js`
- `bizPA/backend/src/controllers/itemController.js`
- `bizPA/backend/src/services/monetaryIntegrityService.js`
- `bizPA/backend/verify_capture_composition_flow.js`
- `bizPA/backend/package.json`

## Plan

- [x] 1. Inspect the current voice endpoint, capture composition flow, and payload contract to identify the MVP parser touchpoints and expected normalized fields.
  - [x] Test: Review `bizPA/backend/src/controllers/voiceController.js`, `bizPA/backend/src/controllers/itemController.js`, and `bizPA/backend/verify_capture_composition_flow.js`; pass when the supported capture entity types, preview contract, and missing extraction gaps are identified.
  - Evidence: Confirmed the existing flow used `voiceController.processVoice()` -> `itemController.createItemInternal()` -> `buildMonetaryPreviewPayload()` for monetary drafts, while capture-slot extraction only reliably populated `amount` and partial dates. Capture client extraction was missing for non-query flows, there was no normalized parser result contract, and low-confidence review behavior was not explicit.
- [x] 2. Implement the core voice parsing rules, extraction, confidence scoring, and fallback metadata for invoice, receipt, quote, payment, booking, and note utterances.
  - [x] Test: `node verify_voice_capture_parser.js` from `bizPA/backend` prints `voice_capture_parser_ok` and confirms correct entity mapping plus explicit review signaling for low-confidence utterances.
  - Evidence: Added `bizPA/backend/src/services/voiceCaptureParserService.js` and `bizPA/backend/verify_voice_capture_parser.js`. Verification output: `voice_capture_parser_ok`, `entity_mapping_ok=true`, `low_confidence_review_ok=true`, `composition_contract_ok=true`.
- [x] 3. Wire parser output into the voice processing endpoint so monetary flows and uncertain note flows return composition-aligned payloads and preview/review actions without breaking existing capture behavior.
  - [x] Test: `node verify_capture_composition_flow.js` from `bizPA/backend` prints `capture_composition_flow_ok`.
  - Evidence: Updated `bizPA/backend/src/controllers/voiceController.js` to consume the parser service, return `parser_result` metadata, and emit `review_required` responses with composition payloads when extraction is uncertain. Existing monetary composition verification still passed with output `capture_composition_flow_ok`, `draft_preview_isolated=true`, `confirm_emits_business_events=true`, and `confirm_enqueues_sync_push=true`.
- [x] 4. Run final technical validation, record results, and request user verification for the user-visible voice behavior before marking the task complete.
  - [x] Test: `node -e "const controller=require('./src/controllers/voiceController'); console.log(typeof controller.parseIntent === 'function' && typeof controller.processVoice === 'function' ? 'voice_controller_exports_ok' : 'voice_controller_exports_bad')"` from `bizPA/backend` prints `voice_controller_exports_ok`.
  - Evidence: Export check passed with `voice_controller_exports_ok`. User verification request recorded in `Validation`: please verify pass/fail for invoice/receipt/quote/payment/note voice parsing and confirm that low-confidence inputs now stop at explicit review instead of continuing toward commit.

## Implementation Log

- 2026-03-11 17:46 GMT: Loaded `skills/workstream-task-lifecycle/SKILL.md`, opened this task file, and converted it to the required lifecycle structure with ordered checklist gates.
- 2026-03-11 17:49 GMT: Inspected the existing bizPA backend voice route, monetary composition preview helper, and composition verification harness to establish the current payload contract and parser gaps.
- 2026-03-11 17:55 GMT: Added a dedicated rule-first parser service for capture intents with normalized fields, composition payload synthesis, confidence scoring, missing-field detection, and explicit review reasons.
- 2026-03-11 17:58 GMT: Updated `voiceController.processVoice()` to use parser results, preserve existing navigation/query intents, return `review_required` responses for uncertain capture/note inputs, and attach parser metadata to preview responses.
- 2026-03-11 18:01 GMT: Added the executable parser verifier, registered the package script, fixed a payment counterparty extraction bug exposed by the verifier, and reran the technical validations successfully.

## Changes Made

- Added `bizPA/backend/src/services/voiceCaptureParserService.js` to centralize:
  - intent classification for invoice, receipt, quote, payment, booking, and note utterances
  - extraction of `counterparty_name`, `description`, `amount`, `vat_hint`, and `date_hint`
  - confidence scoring, missing-field detection, and review/fallback decisions
  - normalized `composition_payload` output aligned to the existing item-composition contract
- Updated `bizPA/backend/src/controllers/voiceController.js` to:
  - route `parseIntent()` through the new parser service while preserving the legacy `{ intent, slots, confidence }` shape
  - return `parser_result` metadata on voice responses
  - return `action_status: review_required` with `review_reason`, `missing_fields`, and `composition_payload` when parsing is uncertain
  - keep existing preview creation for confident monetary captures and execute confident note/booking flows
- Added `bizPA/backend/verify_voice_capture_parser.js` as a focused regression check for entity mapping, review behavior, and payload-contract conformance.
- Updated `bizPA/backend/package.json` with `verify:voice-capture`.

## Validation

- `node verify_voice_capture_parser.js`
  - Result: Pass
  - Output: `voice_capture_parser_ok`, `entity_mapping_ok=true`, `low_confidence_review_ok=true`, `composition_contract_ok=true`
- `node verify_capture_composition_flow.js`
  - Result: Pass
  - Output: `capture_composition_flow_ok`, `draft_preview_isolated=true`, `confirm_emits_business_events=true`, `confirm_enqueues_sync_push=true`
- `node -e "const controller=require('./src/controllers/voiceController'); console.log(typeof controller.parseIntent === 'function' && typeof controller.processVoice === 'function' ? 'voice_controller_exports_ok' : 'voice_controller_exports_bad')"`
  - Result: Pass
  - Output: `voice_controller_exports_ok`
- 2026-03-11 18:02 GMT: User verification requested for the following behaviors:
  - invoice, receipt, quote, payment, and note sample utterances map to the expected entity type
  - low-confidence parses stop in explicit review mode before commit
  - parser-backed voice responses provide the expected composition/review payloads for manual correction

## Risks/Notes

- The current task changes user-visible voice behavior, so per lifecycle rules the file should remain `Awaiting user verification` after technical validation until the user confirms pass/fail on the implemented behaviors.
- Existing `voiceController` also supports navigation and inbox-style intents. The parser refactor should preserve those paths while strengthening capture-specific extraction.

## Completion Status

**State**: Awaiting user verification
**Last Updated**: 2026-03-11 18:02 GMT


## Execution Evidence
- Agent lane: gemini
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260311_161948_bizpa_mvp_product_requirements_document_workstreamB_implement_voice_parsing_for_core_monetary_and_note_intents.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented the voice parsing work in the bizPA backend. The main change is a dedicated parser service at [voiceCaptureParserService.js](C:/Users/edebe/eds/bizPA/backend/src/services/voiceCaptureParserService.js#L1) that classifies invoice, receipt, quote, payment, booking, and note utterances, extracts `counterparty_name`/`description`/`amount`/`vat_hint`/`date_hint`, scores confidence, and marks uncertain parses for review. The voice endpoint now consumes that parser in [voiceController.js](C:/Users/edebe/eds/bizPA/backend/src/controllers/voiceController.js#L15), returns `parser_result`, and emits `action_status: review_required` with a composition-aligned payload when extraction is weak instead of pushing ahead toward commit.

I added an executable verifier at [verify_voice_capture_parser.js](C:/Users/edebe/eds/bizPA/backend/verify_voice_capture_parser.js#L1) and registered it in [package.json](C:/Users/edebe/eds/bizPA/backend/package.json#L14). Technical validation passed:
`node verify_voice_capture_parser.js`
`node verify_capture_composition_flow.js`
`node -e "const controller=require('./src/controllers/voiceController'); ..."`
The lifecycle file is updated with evidence and left in the required awaiting-verification state at [20260311_161948_bizpa_mvp_product_requirements_document_workstreamB_implement_voice_parsing_for_core_monetary_and_note_intents.md](C:/Users/edebe/eds/workstream/200_inprogress/gemini/20260311_161948_bizpa_mvp_product_requirements_document_workstreamB_implement_voice_parsing_for_core_monetary_and_note_intents.md#L75).

Please verify pass/fail for these three behaviors:
1. Invoice, receipt, quote, payment, and note sample utterances map to the expected entity type.
2. Low-confidence utterances now stop in explicit review mode before commit.
3. Voice responses now include the expected composition/review payload for manual correction.

Once you confirm that, the task can be moved to `300_complete`.
```
- Stderr:
```text
low-confidence inputs now stop at explicit review instead of continuing toward commit.
+
+## Implementation Log
+
+- 2026-03-11 17:46 GMT: Loaded `skills/workstream-task-lifecycle/SKILL.md`, opened this task file, and converted it to the required lifecycle structure with ordered checklist gates.
+- 2026-03-11 17:49 GMT: Inspected the existing bizPA backend voice route, monetary composition preview helper, and composition verification harness to establish the current payload contract and parser gaps.
+- 2026-03-11 17:55 GMT: Added a dedicated rule-first parser service for capture intents with normalized fields, composition payload synthesis, confidence scoring, missing-field detection, and explicit review reasons.
+- 2026-03-11 17:58 GMT: Updated `voiceController.processVoice()` to use parser results, preserve existing navigation/query intents, return `review_required` responses for uncertain capture/note inputs, and attach parser metadata to preview responses.
+- 2026-03-11 18:01 GMT: Added the executable parser verifier, registered the package script, fixed a payment counterparty extraction bug exposed by the verifier, and reran the technical validations successfully.
+
+## Changes Made
+
+- Added `bizPA/backend/src/services/voiceCaptureParserService.js` to centralize:
+  - intent classification for invoice, receipt, quote, payment, booking, and note utterances
+  - extraction of `counterparty_name`, `description`, `amount`, `vat_hint`, and `date_hint`
+  - confidence scoring, missing-field detection, and review/fallback decisions
+  - normalized `composition_payload` output aligned to the existing item-composition contract
+- Updated `bizPA/backend/src/controllers/voiceController.js` to:
+  - route `parseIntent()` through the new parser service while preserving the legacy `{ intent, slots, confidence }` shape
+  - return `parser_result` metadata on voice responses
+  - return `action_status: review_required` with `review_reason`, `missing_fields`, and `composition_payload` when parsing is uncertain
+  - keep existing preview creation for confident monetary captures and execute confident note/booking flows
+- Added `bizPA/backend/verify_voice_capture_parser.js` as a focused regression check for entity mapping, review behavior, and payload-contract conformance.
+- Updated `bizPA/backend/package.json` with `verify:voice-capture`.
+
+## Validation
+
+- `node verify_voice_capture_parser.js`
+  - Result: Pass
+  - Output: `voice_capture_parser_ok`, `entity_mapping_ok=true`, `low_confidence_review_ok=true`, `composition_contract_ok=true`
+- `node verify_capture_composition_flow.js`
+  - Result: Pass
+  - Output: `capture_composition_flow_ok`, `draft_preview_isolated=true`, `confirm_emits_business_events=true`, `confirm_enqueues_sync_push=true`
+- `node -e "const controller=require('./src/controllers/voiceController'); console.log(typeof controller.parseIntent === 'function' && typeof controller.processVoice === 'function' ? 'voice_controller_exports_ok' : 'voice_controller_exports_bad')"`
+  - Result: Pass
+  - Output: `voice_controller_exports_ok`
+- 2026-03-11 18:02 GMT: User verification requested for the following behaviors:
+  - invoice, receipt, quote, payment, and note sample utterances map to the expected entity type
+  - low-confidence parses stop in explicit review mode before commit
+  - parser-backed voice responses provide the expected composition/review payloads for manual correction
+
+## Risks/Notes
+
+- The current task changes user-visible voice behavior, so per lifecycle rules the file should remain `Awaiting user verification` after technical validation until the user confirms pass/fail on the implemented behaviors.
+- Existing `voiceController` also supports navigation and inbox-style intents. The parser refactor should preserve those paths while strengthening capture-specific extraction.
+
+## Completion Status
+
+**State**: Awaiting user verification
+**Last Updated**: 2026-03-11 18:02 GMT

tokens used
82,909
```
