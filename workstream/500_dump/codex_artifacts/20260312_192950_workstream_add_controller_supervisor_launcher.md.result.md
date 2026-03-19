# TASK H1: Create Homepage Command Centre UI

## Source
- Source epic path: `workstream/000_epic/bizPA.md`
- Workstream: `H — Homepage Command Centre`
- Original task brief: replace the passive homepage with a business command centre that answers what needs attention today and provides a central capture action.

## Task Summary
Implement the MVP homepage in the `bizPA` web frontend as an operator dashboard with a momentum bar, attention panel, compact performance grid, insight feed, and a central capture call to action. Add a local start path that prints the homepage URL, run a startup smoke test, capture screenshot evidence, and update this lifecycle file with validation results.

## Context
- Frontend app: `bizPA/frontend`
- Existing launch scripts: `bizPA/start_bizpa_capture_ui.ps1`, `bizPA/capture_ui_smoke.ps1`
- Verification artefacts folder: `workstream/verification`
- Primary affected file expected: `bizPA/frontend/src/App.jsx`

## Plan
- [x] 1. Convert the task into the required lifecycle format and document the ordered execution plan.
  - [x] Test: `Get-Content -Raw "C:\Users\edebe\eds\workstream\200_inprogress\codex\20260311_162007_codex_bizpa_mvp_product_requirements_document_workstreamH_create_homepage_command_centre_ui.md"` returns lifecycle sections including `Plan`, `Implementation Log`, `Validation`, and `Completion Status`.
  - Evidence: `Get-Content -Raw ...create_homepage_command_centre_ui.md` returned `Plan`, `Implementation Log`, `Validation`, and `Completion Status` after the lifecycle rewrite at 2026-03-11 19:17 GMT.
- [x] 2. Implement the homepage command centre UI in the `bizPA` web frontend without breaking existing navigation and capture flows.
  - [x] Test: `npm.cmd run build` in `C:\Users\edebe\eds\bizPA\frontend` completes successfully.
  - Evidence: Build completed on 2026-03-11 19:58 GMT with `Compiled successfully.` and emitted `build\static\js\main.2b8e5e8e.js`.
- [x] 3. Provide a local homepage start path and smoke validation path that print the localhost URL, boot the UI, and capture a verification screenshot.
  - [x] Test: homepage start script prints the command centre localhost URL; smoke script returns HTTP 200 for the frontend and writes a screenshot into `C:\Users\edebe\eds\workstream\verification`.
  - Evidence: `start_bizpa_command_centre_ui.ps1` printed `http://127.0.0.1:3001/?commandCentreDemo=1`. `command_centre_ui_smoke.ps1` returned `FRONTEND_STATUS=200`, `BACKEND_STATUS=200`, and wrote `C:\Users\edebe\eds\workstream\verification\20260311_193500_bizpa_homepage_command_centre.png`. Visual fidelity of the desktop screenshot remains environment-sensitive and is called out below.
- [x] 4. Record implementation details, validation outputs, verification artefacts, and the user-verification request in this lifecycle file.
  - [x] Test: this file includes completed checklist evidence, validation command summaries, screenshot path, localhost URL, and explicit user verification request.
  - Evidence: Lifecycle file updated on 2026-03-11 20:21 GMT with the implemented file list, validation outputs, screenshot path, localhost URL, and a verification request for homepage behaviour confirmation.

## Implementation Log
- 2026-03-11 19:15 GMT: Read `skills/workstream-task-lifecycle/SKILL.md`, loaded the active task file, and inspected the `bizPA` frontend/backend structure plus existing start/smoke scripts.
- 2026-03-11 19:17 GMT: Rewrote this task file into the required lifecycle format before code changes.
- 2026-03-11 19:29 GMT: Reworked `bizPA/frontend/src/App.jsx` so the `home` tab becomes a command-centre layout with hero momentum block, attention list, compact performance grid, insight feed, and a central capture CTA.
- 2026-03-11 19:38 GMT: Added `bizPA/start_bizpa_command_centre_ui.ps1` to print the homepage command centre URL and launch the frontend/backend locally on port `3001` and `5056`.
- 2026-03-11 19:40 GMT: Added `bizPA/command_centre_ui_smoke.ps1` to boot the local stack, wait for HTTP readiness, and capture screenshot evidence into `workstream/verification`.
- 2026-03-11 19:58 GMT: Ran `npm.cmd run build` in `bizPA/frontend`; build passed.
- 2026-03-11 20:00 GMT: Ran the new start script and confirmed the printed homepage command centre URL.
- 2026-03-11 20:20 GMT: Ran the smoke script and captured screenshot file `C:\Users\edebe\eds\workstream\verification\20260311_193500_bizpa_homepage_command_centre.png`.
- 2026-03-11 20:21 GMT: Prepared user verification request covering homepage attention clarity and central capture flow.

## Changes Made
- `bizPA/frontend/src/App.jsx`
  - Added homepage command-centre styling and helpers for formatted currency and period deltas.
  - Added `commandCentreDemo` URL support for deterministic homepage validation.
  - Replaced the simple home dashboard with:
    - a hero momentum panel,
    - a central capture action,
    - an attention-required panel driven by blockers, notifications, unpaid invoices, and upcoming items,
    - a compact performance grid,
    - a smart insight feed with live or fallback signals.
- `bizPA/start_bizpa_command_centre_ui.ps1`
  - New local launch script that starts backend/frontend services and prints the homepage command centre URL: `http://127.0.0.1:3001/?commandCentreDemo=1`.
- `bizPA/command_centre_ui_smoke.ps1`
  - New startup smoke script that launches the stack, validates HTTP readiness, and captures screenshot evidence to `workstream/verification`.

## Validation
- 2026-03-11 19:18 GMT
  - Command: `Get-Content -Raw "C:\Users\edebe\eds\workstream\200_inprogress\codex\20260311_162007_codex_bizpa_mvp_product_requirements_document_workstreamH_create_homepage_command_centre_ui.md"`
  - Result: lifecycle sections present after rewrite.
- 2026-03-11 19:58 GMT
  - Command: `npm.cmd run build`
  - Working directory: `C:\Users\edebe\eds\bizPA\frontend`
  - Result: pass; `Compiled successfully.`
- 2026-03-11 20:00 GMT
  - Command: `powershell -ExecutionPolicy Bypass -File "C:\Users\edebe\eds\bizPA\start_bizpa_command_centre_ui.ps1"`
  - Result: pass; printed:
    - `Homepage command centre URL: http://127.0.0.1:3001/?commandCentreDemo=1`
    - `Base frontend URL: http://127.0.0.1:3001`
    - `Backend health URL: http://127.0.0.1:5056/api/health`
- 2026-03-11 20:20 GMT
  - Command: `powershell -ExecutionPolicy Bypass -File "C:\Users\edebe\eds\bizPA\command_centre_ui_smoke.ps1"`
  - Result: pass; returned `FRONTEND_STATUS=200`, `BACKEND_STATUS=200`, and `SCREENSHOT=C:\Users\edebe\eds\workstream\verification\20260311_193500_bizpa_homepage_command_centre.png`.
- 2026-03-11 20:21 GMT
  - User verification requested:
    - Verify that the homepage clearly answers what needs attention today.
    - Verify that the central capture action opens the capture workspace.
    - Verify that the performance grid and insight feed feel correct for the homepage.
  - Outcome: Pending user response.

## Risks/Notes
- This is a user-visible UI task, so per lifecycle rules the task cannot be moved to `300_complete` until user verification is requested and outcome is captured.
- Existing `bizPA` startup scripts target the capture flow on port `3001`; the new homepage path uses a dedicated script and the deterministic demo URL `?commandCentreDemo=1` for validation.
- The smoke screenshot was captured from the local desktop workflow rather than a browser automation library; HTTP readiness and screenshot file creation both passed, but the desktop capture can pick up the foreground window in this environment. User visual verification on `http://127.0.0.1:3001/?commandCentreDemo=1` remains the reliable acceptance check.

## Completion Status
- Awaiting user verification — 2026-03-11 20:21 GMT

