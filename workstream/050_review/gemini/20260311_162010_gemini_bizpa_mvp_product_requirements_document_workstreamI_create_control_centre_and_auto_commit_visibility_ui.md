# TASK I3: Create Control Centre And Auto Commit Visibility UI

Source: `workstream/000_epic/bizPA.md`

## Task Summary
Implement the bizPA admin control centre UI and persistent operator-visible auto-commit indicators so governance, policy caps, sync health, queue backlog, session visibility, and risky-mode state are obvious in the local demo app.

## Context
- App surface: `bizPA/frontend/src/App.jsx`
- Governance helpers: `bizPA/frontend/src/governance.js`
- Local launch scripts: `bizPA/start_bizpa_command_centre_ui.ps1`, `bizPA/command_centre_ui_smoke.ps1`
- Verification artefacts: `workstream/verification`

## Plan
- [x] 1. Update the command-centre route and shared app shell to expose a dedicated control centre screen with governance, role, sync-health, queue, and session visibility widgets.
  - [x] Test: `npm.cmd test -- --runInBand` from `bizPA/frontend` with `CI=true` passes with governance/control-centre coverage and no failing suites.
  - Evidence: `PASS src/controlCentre.test.js`, `PASS src/governance.test.js`, `Test Suites: 2 passed, 2 total`, `Tests: 6 passed, 6 total`.
- [x] 2. Add persistent auto-commit visibility across the shared app and capture flow, including clear banners/badges and capture-specific risky-mode cues.
  - [x] Test: `npm.cmd test -- --runInBand` from `bizPA/frontend` with `CI=true` still passes after the visibility updates.
  - Evidence: Global header badge and banner plus capture-mode panel implemented in `bizPA/frontend/src/App.jsx`; Jest remained green with `6 passed, 6 total`.
- [x] 3. Validate the local startup path, capture a control-centre screenshot in `workstream/verification`, and update the task verification checklist with concrete URLs and outputs.
  - [x] Test: `powershell -ExecutionPolicy Bypass -File .\bizPA\command_centre_ui_smoke.ps1` completes, prints the local URL/status lines, and writes a screenshot file without an immediate crash.
  - Evidence: `COMMAND_CENTRE_URL=http://127.0.0.1:3001/?commandCentreDemo=1&tab=control`, `FRONTEND_STATUS=200`, `BACKEND_STATUS=200`, `SCREENSHOT=C:\Users\edebe\eds\workstream\verification\20260311_203500_bizpa_control_centre_auto_commit.png`.

## Implementation Log
- 2026-03-11 20:41 Europe/London: Read `skills/workstream-task-lifecycle/SKILL.md` and the task brief. Confirmed the task requires lifecycle-file updates before edits and user verification before final completion.
- 2026-03-11 20:43 Europe/London: Inspected `bizPA` launch scripts, `bizPA/frontend/package.json`, `bizPA/frontend/src/App.jsx`, and `bizPA/frontend/src/governance.js` to determine the existing governance UI baseline and startup path.
- 2026-03-11 20:46 Europe/London: Found existing governance controls embedded in the quarter/readiness screen plus a command-centre launch script, but no dedicated control-centre tab and no app-wide persistent auto-commit visibility across capture workflows.
- 2026-03-11 20:48 Europe/London: Added `bizPA/frontend/src/controlCentre.js` and `bizPA/frontend/src/controlCentre.test.js` to centralize auto-commit visibility, queue backlog, and control-centre summary logic with direct Jest coverage.
- 2026-03-11 20:53 Europe/London: Updated `bizPA/frontend/src/App.jsx` to add a dedicated `control` tab, admin/system-health widgets, session visibility cards, persistent auto-commit banner/badge, and a capture-mode panel that links back to the control centre.
- 2026-03-11 20:54 Europe/London: Updated `bizPA/start_bizpa_command_centre_ui.ps1` and `bizPA/command_centre_ui_smoke.ps1` to open `http://127.0.0.1:3001/?commandCentreDemo=1&tab=control` directly and capture the control-centre screenshot.
- 2026-03-11 20:55 Europe/London: First frontend test attempt with `npm.cmd test -- --watch=false --runInBand` failed because CRA requires `--watchAll` outside git; reran with `CI=true` to force one-shot Jest execution.
- 2026-03-11 20:58 Europe/London: Executed the smoke script successfully; frontend and backend both returned HTTP 200 and the screenshot artefact was created in `workstream/verification`.

## Changes Made
- Added `bizPA/frontend/src/controlCentre.js` with pure helpers and demo telemetry/session data for:
  - auto-commit banner and mode-badge copy,
  - queue backlog summarization,
  - control-centre summary health metrics.
- Added `bizPA/frontend/src/controlCentre.test.js` covering backlog counts, governed-mode visibility copy, and control-centre metric aggregation.
- Updated `bizPA/frontend/src/App.jsx` to:
  - create a dedicated `control` tab in the shared navigation,
  - default the command-centre demo route to the control-centre tab,
  - surface persistent auto-commit status in the header and global banner,
  - add a capture-screen risky-mode panel so auto-commit stays obvious during capture workflows,
  - render dedicated control-centre sections for role management, policy caps, feature toggles, sync health, queue backlog, session visibility, and governance audit.
- Updated `bizPA/start_bizpa_command_centre_ui.ps1` so the printed local access URL opens the dedicated control-centre route directly.
- Updated `bizPA/command_centre_ui_smoke.ps1` so the smoke run opens the dedicated control-centre route and writes screenshot evidence to `workstream/verification/20260311_203500_bizpa_control_centre_auto_commit.png`.

## Validation
- `CI=true npm.cmd test -- --runInBand` from `bizPA/frontend`
  - Result: Pass.
  - Evidence: `PASS src/controlCentre.test.js`, `PASS src/governance.test.js`, `Test Suites: 2 passed, 2 total`, `Tests: 6 passed, 6 total`.
- `powershell -ExecutionPolicy Bypass -File .\bizPA\command_centre_ui_smoke.ps1`
  - Result: Pass.
  - Evidence: `COMMAND_CENTRE_URL=http://127.0.0.1:3001/?commandCentreDemo=1&tab=control`, `FRONTEND_STATUS=200`, `BACKEND_STATUS=200`.
- Screenshot verification:
  - Result: Pass.
  - Evidence: `C:\Users\edebe\eds\workstream\verification\20260311_203500_bizpa_control_centre_auto_commit.png` exists; `Length=160216`.
- User verification requested:
  - Open `http://127.0.0.1:3001/?commandCentreDemo=1&tab=control` and confirm pass/fail for:
  - 1. Dedicated control centre view is visible with policy, sync, queue, session, and audit sections.
  - 2. Auto-commit status is obvious in the header/banner and remains obvious on the Capture tab.
  - 3. The Capture tab clearly indicates governed/manual mode and links back to the control centre.

## Risks/Notes
- This task changes user-visible UI behavior, so completion must remain pending until explicit user verification is requested per lifecycle rules.
- Existing launch scripts already target `http://127.0.0.1:3001/?commandCentreDemo=1`; implementation should preserve or improve that access path.

## Verification Checklist
- [x] A start script is present that launches the control centre UI locally and prints the access URL.
- [x] The task documents the localhost URL to open for the governance or control centre screen.
- [x] Running the start script completes a startup smoke test without immediate crash.
- [x] A screenshot is captured showing the control centre and visible auto-commit state in the verification folder.
- [x] Auto-commit state remains visually obvious during capture-related workflows.
- [x] Provide or update a simple local access/start script that prints the localhost URL for this UI.
- [x] Smoke-test the local startup path and confirm the UI loads without an immediate crash.
- [x] Capture screenshot evidence of the working UI in the epic verification folder.

## Completion Status
Awaiting user verification - 2026-03-11 20:59 Europe/London


## Execution Evidence
- Agent lane: gemini
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260311_162010_gemini_bizpa_mvp_product_requirements_document_workstreamI_create_control_centre_and_auto_commit_visibility_ui.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented the control-centre and auto-commit visibility work in [App.jsx](C:/Users/edebe/eds/bizPA/frontend/src/App.jsx), with supporting helpers/tests in [controlCentre.js](C:/Users/edebe/eds/bizPA/frontend/src/controlCentre.js) and [controlCentre.test.js](C:/Users/edebe/eds/bizPA/frontend/src/controlCentre.test.js). The app now has a dedicated `Control` tab, persistent auto-commit header/banner visibility, and a capture-screen mode panel so risky mode stays obvious during capture workflows.

The local launch path now opens the control-centre route directly via [start_bizpa_command_centre_ui.ps1](C:/Users/edebe/eds/bizPA/start_bizpa_command_centre_ui.ps1) and the smoke harness in [command_centre_ui_smoke.ps1](C:/Users/edebe/eds/bizPA/command_centre_ui_smoke.ps1). Verified:
- `CI=true npm.cmd test -- --runInBand` in `bizPA/frontend`: 2 suites passed, 6 tests passed
- `powershell -ExecutionPolicy Bypass -File .\bizPA\command_centre_ui_smoke.ps1`: frontend `200`, backend `200`
- Screenshot captured at [20260311_203500_bizpa_control_centre_auto_commit.png](C:/Users/edebe/eds/workstream/verification/20260311_203500_bizpa_control_centre_auto_commit.png)

The lifecycle file is updated and set to awaiting verification at [20260311_162010_gemini_bizpa_mvp_product_requirements_document_workstreamI_create_control_centre_and_auto_commit_visibility_ui.md](C:/Users/edebe/eds/workstream/200_inprogress/gemini/20260311_162010_gemini_bizpa_mvp_product_requirements_document_workstreamI_create_control_centre_and_auto_commit_visibility_ui.md).

Verify these and send pass/fail:
1. Open `http://127.0.0.1:3001/?commandCentreDemo=1&tab=control` and confirm the control centre shows policy, sync, queue, session, and audit sections.
2. Confirm auto-commit status is obvious in the header/banner.
3. Open the `Capture` tab and confirm the governed/manual mode panel is obvious and links back to the control centre.
```
- Stderr:
```text
creenshot.
+- 2026-03-11 20:55 Europe/London: First frontend test attempt with `npm.cmd test -- --watch=false --runInBand` failed because CRA requires `--watchAll` outside git; reran with `CI=true` to force one-shot Jest execution.
+- 2026-03-11 20:58 Europe/London: Executed the smoke script successfully; frontend and backend both returned HTTP 200 and the screenshot artefact was created in `workstream/verification`.
+
+## Changes Made
+- Added `bizPA/frontend/src/controlCentre.js` with pure helpers and demo telemetry/session data for:
+  - auto-commit banner and mode-badge copy,
+  - queue backlog summarization,
+  - control-centre summary health metrics.
+- Added `bizPA/frontend/src/controlCentre.test.js` covering backlog counts, governed-mode visibility copy, and control-centre metric aggregation.
+- Updated `bizPA/frontend/src/App.jsx` to:
+  - create a dedicated `control` tab in the shared navigation,
+  - default the command-centre demo route to the control-centre tab,
+  - surface persistent auto-commit status in the header and global banner,
+  - add a capture-screen risky-mode panel so auto-commit stays obvious during capture workflows,
+  - render dedicated control-centre sections for role management, policy caps, feature toggles, sync health, queue backlog, session visibility, and governance audit.
+- Updated `bizPA/start_bizpa_command_centre_ui.ps1` so the printed local access URL opens the dedicated control-centre route directly.
+- Updated `bizPA/command_centre_ui_smoke.ps1` so the smoke run opens the dedicated control-centre route and writes screenshot evidence to `workstream/verification/20260311_203500_bizpa_control_centre_auto_commit.png`.
+
+## Validation
+- `CI=true npm.cmd test -- --runInBand` from `bizPA/frontend`
+  - Result: Pass.
+  - Evidence: `PASS src/controlCentre.test.js`, `PASS src/governance.test.js`, `Test Suites: 2 passed, 2 total`, `Tests: 6 passed, 6 total`.
+- `powershell -ExecutionPolicy Bypass -File .\bizPA\command_centre_ui_smoke.ps1`
+  - Result: Pass.
+  - Evidence: `COMMAND_CENTRE_URL=http://127.0.0.1:3001/?commandCentreDemo=1&tab=control`, `FRONTEND_STATUS=200`, `BACKEND_STATUS=200`.
+- Screenshot verification:
+  - Result: Pass.
+  - Evidence: `C:\Users\edebe\eds\workstream\verification\20260311_203500_bizpa_control_centre_auto_commit.png` exists; `Length=160216`.
+- User verification requested:
+  - Open `http://127.0.0.1:3001/?commandCentreDemo=1&tab=control` and confirm pass/fail for:
+  - 1. Dedicated control centre view is visible with policy, sync, queue, session, and audit sections.
+  - 2. Auto-commit status is obvious in the header/banner and remains obvious on the Capture tab.
+  - 3. The Capture tab clearly indicates governed/manual mode and links back to the control centre.
+
+## Risks/Notes
+- This task changes user-visible UI behavior, so completion must remain pending until explicit user verification is requested per lifecycle rules.
+- Existing launch scripts already target `http://127.0.0.1:3001/?commandCentreDemo=1`; implementation should preserve or improve that access path.
+
+## Verification Checklist
+- [x] A start script is present that launches the control centre UI locally and prints the access URL.
+- [x] The task documents the localhost URL to open for the governance or control centre screen.
+- [x] Running the start script completes a startup smoke test without immediate crash.
+- [x] A screenshot is captured showing the control centre and visible auto-commit state in the verification folder.
+- [x] Auto-commit state remains visually obvious during capture-related workflows.
+- [x] Provide or update a simple local access/start script that prints the localhost URL for this UI.
+- [x] Smoke-test the local startup path and confirm the UI loads without an immediate crash.
+- [x] Capture screenshot evidence of the working UI in the epic verification folder.
+
+## Completion Status
+Awaiting user verification - 2026-03-11 20:59 Europe/London

tokens used
94,941
```
