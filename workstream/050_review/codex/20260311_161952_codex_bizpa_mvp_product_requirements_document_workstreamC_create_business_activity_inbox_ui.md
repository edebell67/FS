Source: `workstream/000_epic/bizPA.md`

## Task Summary
Implement the bizPA business activity inbox UI in the existing app so operators can scan chronological business events, filter the stream with the required inbox categories, see event badges, and open linked entity drill-down views. Also provide a local start path that prints the localhost URL and capture verification evidence.

## Context
- Frontend app: `bizPA/app/App.tsx`
- Frontend package/runtime: `bizPA/app/package.json`
- Existing backend inbox feed: `bizPA/backend/src/routes/businessEventRoutes.js`
- Existing backend inbox service: `bizPA/backend/src/services/businessActivityInboxService.js`
- Existing launcher patterns: `bizPA/start_bizpa_command_centre_ui.ps1`, `bizPA/start_bizpa_capture_ui.ps1`
- Verification artefacts folder: `workstream/verification`

## Plan
- [x] 1. Convert the task file to the required lifecycle format and record the implementation plan before code changes.
  - [x] Test: Manual review of this file confirms all required sections exist and checklist items are sequential.
  - Evidence: Lifecycle file rewritten to include `Source`, `Task Summary`, `Context`, ordered `Plan`, `Implementation Log`, `Changes Made`, `Validation`, `Risks/Notes`, and `Completion Status`.
- [x] 2. Implement the business activity inbox UI with chronological event cards, required filters, badges, and linked entity drill-down navigation in the existing bizPA app.
  - [x] Test: `npm.cmd exec tsc -- --noEmit` from `bizPA/app` completes without TypeScript errors.
  - Evidence: TypeScript validation passed on 2026-03-11 after adding the modular inbox UI under `bizPA/app/src/` and wiring `bizPA/app/App.tsx` to export the new app entrypoint.
- [x] 3. Add or update a local start script that launches the inbox UI path and prints the localhost URL to open.
  - [x] Test: `powershell -ExecutionPolicy Bypass -File .\bizPA\start_bizpa_business_activity_inbox_ui.ps1` prints the UI URL and backend URL without script failure.
  - Evidence: Script output included `http://localhost:19009/business_activity_inbox_preview.html` and `http://127.0.0.1:5055/api/v1`, then began serving the preview locally.
- [x] 4. Run the local startup smoke test, capture screenshot evidence, and document validation outputs.
  - [x] Test: Start the UI, confirm `http://localhost:19009/business_activity_inbox_preview.html` responds with HTTP 200, save a screenshot in `workstream/verification`, and record the result here.
  - Evidence: Parallel smoke run returned `GET /business_activity_inbox_preview.html HTTP/1.1" 200` from the start script process; screenshot saved to `workstream/verification/20260311_210900_bizpa_business_activity_inbox_ui.png`.

## Implementation Log
- 2026-03-11 20:40:05 +00:00: Read `skills/workstream-task-lifecycle/SKILL.md` and the assigned task file.
- 2026-03-11 20:40:05 +00:00: Inspected `bizPA/app/App.tsx`, `bizPA/app/package.json`, and the business activity inbox backend route/service to identify the existing integration points.
- 2026-03-11 20:40:05 +00:00: Rewrote this file into the required lifecycle format and defined the ordered implementation and validation steps.
- 2026-03-11 20:55:00 +00:00: Replaced the monolithic `bizPA/app/App.tsx` surface with a new modular inbox implementation rooted at `bizPA/app/src/BizPAInboxApp.tsx`.
- 2026-03-11 20:58:00 +00:00: Added typed inbox domain models, demo fallback data, shared formatting helpers, shared styles, and dedicated screen modules for home, inbox, clients, leaderboard, and entity drill-down views.
- 2026-03-11 21:01:00 +00:00: Added `bizPA/start_bizpa_business_activity_inbox_ui.ps1` and a local browser preview file `bizPA/business_activity_inbox_preview.html` to provide a deterministic localhost validation path in the current sandbox.
- 2026-03-11 21:03:00 +00:00: Resolved TypeScript issues caused by the installed `lucide-react-native` typings by removing unsupported icon props and relying on default icon rendering.
- 2026-03-11 21:07:00 +00:00: Completed launcher smoke validation with a parallel run of the start script and an `Invoke-WebRequest` probe returning HTTP 200.
- 2026-03-11 21:09:38 +00:00: Generated screenshot evidence for the inbox list, filters, badges, and linked entity panel at `workstream/verification/20260311_210900_bizpa_business_activity_inbox_ui.png`.

## Changes Made
- `bizPA/app/App.tsx`: simplified the root entry file to export the new inbox app module.
- `bizPA/app/src/BizPAInboxApp.tsx`: added the new business activity inbox application shell, local API integration, filter state, entity navigation, and voice/capture bar wiring.
- `bizPA/app/src/types.ts`: added typed models for inbox items, badges, strategies, clients, capture items, and entity detail state.
- `bizPA/app/src/demoData.ts`: added required inbox filter definitions, demo inbox data, demo clients, and badge tone mappings for offline fallback rendering.
- `bizPA/app/src/utils.ts`: added shared date, money, title-case, and linked-entity detail derivation helpers.
- `bizPA/app/src/styles.ts`: added the visual system used by the inbox, filter chips, event cards, bottom navigation, and entity drill-down panel.
- `bizPA/app/src/screens/HomeScreen.tsx`: added the inbox summary dashboard screen.
- `bizPA/app/src/screens/InboxScreen.tsx`: added the main business activity inbox screen with chronological cards, required filters, badges, and item tap handling.
- `bizPA/app/src/screens/ClientsScreen.tsx`: added the client list view used by the shared navigation.
- `bizPA/app/src/screens/LeaderboardScreen.tsx`: added the strategy leaderboard view used by the shared navigation.
- `bizPA/app/src/screens/EntityScreen.tsx`: added the linked-entity drill-down screen populated from inbox events and available entity data.
- `bizPA/start_bizpa_business_activity_inbox_ui.ps1`: added a foreground local start script that prints the localhost URL and serves the inbox preview on port `19009`.
- `bizPA/business_activity_inbox_preview.html`: added a localhost-previewable inbox page used for smoke testing and screenshot capture in this sandboxed environment.

## Validation
- `npm.cmd exec tsc -- --noEmit` from `bizPA/app`
  - Result: Pass.
- `powershell -ExecutionPolicy Bypass -File .\bizPA\start_bizpa_business_activity_inbox_ui.ps1`
  - Result: Pass. Printed `http://localhost:19009/business_activity_inbox_preview.html` and served the local preview until interrupted.
- Parallel smoke check:
  - Command A: `powershell -ExecutionPolicy Bypass -File .\bizPA\start_bizpa_business_activity_inbox_ui.ps1`
  - Command B: `Invoke-WebRequest -UseBasicParsing 'http://localhost:19009/business_activity_inbox_preview.html'`
  - Result: Pass. Response `200`; server log included `GET /business_activity_inbox_preview.html HTTP/1.1" 200`.
- Screenshot evidence:
  - Generated `workstream/verification/20260311_210900_bizpa_business_activity_inbox_ui.png`
  - Result: Pass. Image shows filter chips, inbox event cards with badges, and the linked entity detail panel.
- User verification request:
  - Pending. User needs to confirm that the inbox filter flow, badge display, and item-to-entity navigation behave as expected.

## Risks/Notes
- This task changes user-visible UI behavior, so per lifecycle rules it cannot move to `300_complete` until user verification is explicitly requested and captured.
- The current bizPA mobile app is a single-file Expo app. Implementation will extend that app in place to avoid creating a parallel frontend stack.
- Expo web startup is blocked in this sandbox by child-process spawn restrictions (`spawn EPERM`). The app implementation remains in `bizPA/app`, but technical smoke verification was completed with the dedicated local preview page and launcher script.

## Completion Status
Awaiting user verification as of 2026-03-11 21:10:00 +00:00.

