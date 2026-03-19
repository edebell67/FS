# TASK: bizPA Multi-Slot Voice Filtering (Client & Date)

Source: `000_epic/20260301_235500_bizPA_UI_UX_and_Navigation_Refinement.md`

## Task Summary
Enable advanced voice-driven filtering in the bizPA UI so invoice and expense queries can combine entity type, client name, and date range criteria, including `today`, `this week`, and `last week`.

## Context
- Affected Files: `bizPA/backend/src/services/voiceCaptureParserService.js`, `bizPA/backend/verify_voice_capture_parser.js`, `bizPA/frontend/src/App.jsx`
- Systems: Voice query parsing, Activity timeline filtering, rendered list grouping
- Current State: Query handling previously set one filter at a time, and backend query parsing only resolved exact date hints like `today` rather than period phrases such as `this week` or `last week`.

## Dependency
Dependency: None

## Plan
- [x] 1. Inspect the current voice parsing and Activity filtering flow to identify slot shape and filtering gaps.
  - [x] Test: `rg -n "executeVoiceAction|timePeriodFilter|view_invoices|view_expenses|today|this week|last week|date_hint" bizPA/frontend/src/App.jsx bizPA/backend/src/services/voiceCaptureParserService.js` should show the current handlers and parser coverage.
  - Evidence: `rg` confirmed `executeVoiceAction` only set `activityTypeFilter` and `searchQuery`, while `voiceCaptureParserService.js` handled `today` but not `this week` or `last week`.
- [x] 2. Implement combined client/date/type voice filtering across backend slot extraction and frontend Activity rendering.
  - [x] Test: `rg -n "parseTimePeriodHint|time_period|openActivityView|matchesActivityTimePeriod|ACTIVITY_TIME_PERIOD_OPTIONS" bizPA/backend/src/services/voiceCaptureParserService.js bizPA/backend/verify_voice_capture_parser.js bizPA/frontend/src/App.jsx` should show period-slot extraction, parser assertions, and combined Activity filter wiring.
  - Evidence: `rg` confirmed `parseTimePeriodHint` plus `time_period` slot emission in the backend, new parser assertions in `verify_voice_capture_parser.js`, and `openActivityView` / `matchesActivityTimePeriod` / `ACTIVITY_TIME_PERIOD_OPTIONS` in `App.jsx`.
- [x] 3. Validate parser behavior and frontend build stability, then finalize evidence and status.
  - [x] Test: `npm run verify:voice-capture` in `bizPA/backend` and `npm run build` in `bizPA/frontend` should both pass.
  - Evidence: Backend verification printed `voice_capture_parser_ok` and `query_period_filters_ok=true`; frontend build compiled successfully and emitted `build\\static\\js\\main.7ab0b0e5.js`.

## Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `rg -n "parseTimePeriodHint|time_period|openActivityView|matchesActivityTimePeriod|ACTIVITY_TIME_PERIOD_OPTIONS" bizPA/backend/src/services/voiceCaptureParserService.js bizPA/backend/verify_voice_capture_parser.js bizPA/frontend/src/App.jsx`
  - Objective-Proved: Backend now emits voice period slots for `today`, `this week`, and `last week`, and the frontend now applies type, client, and period filters together in the Activity view.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `npm run verify:voice-capture` in `bizPA/backend`; `npm run build` in `bizPA/frontend`
  - Objective-Proved: Parser behavior and React build both pass after the slot and filtering changes.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `bizPA Activity view voice flow`
  - Objective-Proved: User-visible behavior can be reviewed by triggering voice invoice/expense queries with client and date phrases in the Activity view.
  - Status: planned

## Implementation Log
- 2026-03-16 17:32:42 +00:00: Read `skills/workstream-task-lifecycle/SKILL.md` and normalized this task file to the required lifecycle structure.
- 2026-03-16 17:32:42 +00:00: Inspected `bizPA/frontend/src/App.jsx` and `bizPA/backend/src/services/voiceCaptureParserService.js`; confirmed frontend applied only one filter path and backend query parsing lacked `this week` / `last week` period extraction.
- 2026-03-16 17:38:39 +00:00: Implemented backend query-period parsing and legacy slot emission for `today`, `this week`, and `last week`; added parser verification coverage for period queries.
- 2026-03-16 17:38:39 +00:00: Implemented shared Activity filter application in `App.jsx`, added period filter state and selector, and aligned Activity grouping with the same date precedence used by filtering.
- 2026-03-16 17:40:40 +00:00: Fixed counterparty cleanup so phrases like `Acme this week` resolve to client `Acme` plus period `this_week`; reran parser validation successfully.
- 2026-03-16 17:41:13 +00:00: Captured implementation evidence and prepared the task for user-visible verification.

## Changes Made
- `bizPA/backend/src/services/voiceCaptureParserService.js`
  - Added `parseTimePeriodHint`, plus week-bound helpers, to derive `today`, `this_week`, and `last_week`.
  - Added `time_period` to query/search/summary parse results and legacy slots.
  - Tightened counterparty cleanup so period phrases are not absorbed into `client_name`.
- `bizPA/backend/verify_voice_capture_parser.js`
  - Added assertions for invoice and expense query parsing with `this week` and `last week`.
- `bizPA/frontend/src/App.jsx`
  - Added `timePeriodFilter` state, `openActivityView`, and date-range matching helpers.
  - Updated `executeVoiceAction` so voice invoice/expense commands apply type, client search, and time period together.
  - Added an Activity date-range selector and empty-state messaging.
  - Changed Activity grouping to use the same effective date precedence used for time-range filtering.

## Validation
- 2026-03-16 17:32:42 +00:00: `rg -n "executeVoiceAction|timePeriodFilter|view_invoices|view_expenses|today|this week|last week|date_hint" bizPA/frontend/src/App.jsx bizPA/backend/src/services/voiceCaptureParserService.js`
  - Result: Pass. Located the Activity voice action handler and confirmed parser support for `today` only.
- 2026-03-16 17:41:13 +00:00: `rg -n "parseTimePeriodHint|time_period|openActivityView|matchesActivityTimePeriod|ACTIVITY_TIME_PERIOD_OPTIONS" bizPA/backend/src/services/voiceCaptureParserService.js bizPA/backend/verify_voice_capture_parser.js bizPA/frontend/src/App.jsx`
  - Result: Pass. Confirmed backend period-slot wiring, parser verification coverage, and frontend combined filter helpers and controls.
- 2026-03-16 17:40:40 +00:00: `npm run verify:voice-capture` in `bizPA/backend`
  - Result: Pass. Output included `voice_capture_parser_ok`, `entity_mapping_ok=true`, `composition_contract_ok=true`, and `query_period_filters_ok=true`.
- 2026-03-16 17:38:39 +00:00: `npm run build` in `bizPA/frontend`
  - Result: Pass. React build compiled successfully and emitted `build\static\js\main.7ab0b0e5.js`.
- 2026-03-16 17:41:13 +00:00: User verification requested for voice Activity queries using:
  - `Show invoices for <client> this week`
  - `Show expenses for <client> last week`
  - `Show invoices for <client> today`
  - Expected: Activity tab opens with type, client search, and date-range filters applied together.

## Risks/Notes
- The Activity list can contain multiple date-like fields (`transaction_date`, `relevant_date`, `due_date`, `created_at`); filtering now uses deterministic precedence `transaction_date -> relevant_date -> due_date -> created_at`.
- This task changes visible Activity behavior, so it should remain in review until the user confirms the voice-filter flow in the UI.

## Completion Status
AWAITING USER VERIFICATION - 2026-03-16 17:41:13 +00:00


## Execution Evidence
- Agent lane: gemini
- Command: cmd /c echo gemini processing 20260301_235501_gemini_bizpa_voice_client_date_filtering.md
- Return code: 0
- Stdout:
```text
gemini processing 20260301_235501_gemini_bizpa_voice_client_date_filtering.md
```
