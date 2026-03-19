# TASK D3: Create Tax Readiness UI

Source: `workstream/000_epic/bizPA.md`

## Task Summary

Implement the bizPA tax readiness UI for the active quarter so a user can see readiness percentage, outstanding issues, severity mix, quarter context, drill into blockers, and jump directly into corrective actions. Deliver a local start path that prints the localhost URL, run a startup smoke test, and capture screenshot evidence.

## Context

- Frontend shell: `bizPA/frontend/src/App.jsx`
- Existing launch scripts: `bizPA/start_bizpa_command_centre_ui.ps1`, `bizPA/command_centre_ui_smoke.ps1`
- Verification artefacts: `workstream/verification`
- Readiness payload source: `bizPA/backend/src/services/readinessService.js`

## Original Task Brief

- Workstream: D - Tax Readiness Engine
- Epic: bizPA MVP Product Requirements Document
- Priority: 1
- Suggested Agent: claude
- UI Deliverable: Yes
- Workstream Goal: Continuously calculate an explainable quarter-readiness score for the active quarter only.

Provide a visible readiness dashboard for the current quarter, including percentage, issue count, severity, and drill-down actions.

Fields / Components:
- readiness_percentage
- issues_remaining
- severity_breakdown
- issue_action_links
- quarter_label

Dependencies:
- D1
- D2

## Plan

- [x] 1. Convert this task file to lifecycle format and define the implementation/validation sequence.
  - [x] Test: Open `workstream/200_inprogress/claude/20260311_161957_claude_bizpa_mvp_product_requirements_document_workstreamD_create_tax_readiness_ui.md` and confirm all required lifecycle sections plus ordered checklist are present.
  - [x] Evidence: This file now contains `Source`, `Task Summary`, `Context`, `Plan`, `Implementation Log`, `Changes Made`, `Validation`, `Risks/Notes`, and `Completion Status`.
- [x] 2. Implement the active-quarter tax readiness UI and supporting demo-safe data handling in the bizPA frontend.
  - [x] Test: `npm.cmd run build` from `C:\Users\edebe\eds\bizPA\frontend` completes without errors.
  - [x] Evidence: `react-scripts build` completed successfully on 2026-03-11 with production bundle output under `bizPA/frontend/build`.
- [x] 3. Add or update a local readiness start path and an automated smoke/screenshot validation path that prints the localhost URL.
  - [x] Test: Run the readiness smoke script and confirm it reports the readiness URL, HTTP 200 frontend status, and screenshot path.
  - [x] Evidence: `tax_readiness_ui_smoke.ps1` returned `READINESS_URL=http://127.0.0.1:3002/?readinessDemo=1&tab=quarter`, `FRONTEND_STATUS=200`, and `SCREENSHOT=C:\Users\edebe\eds\workstream\verification\20260311_201500_bizpa_tax_readiness_ui.png`.
- [x] 4. Capture verification evidence, update this lifecycle file with results, and request user verification for the UI behaviour.
  - [x] Test: Screenshot exists in `workstream/verification` and this task file records validation results plus explicit user-verification request.
  - [x] Evidence: Screenshot file `workstream/verification/20260311_201500_bizpa_tax_readiness_ui.png` exists at 137199 bytes with timestamp 2026-03-11 20:25:45.

## Implementation Log

- 2026-03-11 20:13 GMT: Read `skills/workstream-task-lifecycle/SKILL.md`, reviewed the assigned task file, and mapped the task to the existing bizPA frontend quarter screen plus existing launch/smoke script patterns.
- 2026-03-11 20:14 GMT: Rewrote this task file into lifecycle format before code changes, per repository and skill requirements.
- 2026-03-11 20:16 GMT: Implemented a dedicated readiness demo report, historical snapshot contrast, severity breakdown helpers, and a redesigned active-quarter readiness workspace in `bizPA/frontend/src/App.jsx`.
- 2026-03-11 20:18 GMT: Added `bizPA/start_bizpa_tax_readiness_ui.ps1` and `bizPA/tax_readiness_ui_smoke.ps1` to provide a stable local launch URL and automated smoke/screenshot capture path on port 3002.
- 2026-03-11 20:19 GMT: Ran `npm.cmd run build` in `bizPA/frontend`; build passed.
- 2026-03-11 20:20 GMT: First smoke run reached the frontend but failed at screenshot capture because the initial Chrome process handle was not bound to a visible window.
- 2026-03-11 20:24 GMT: Hardened the smoke script to discover the real Chrome window process with an accessible `MainWindowHandle` before capture.
- 2026-03-11 20:25 GMT: Re-ran the readiness smoke script successfully; frontend returned HTTP 200 and screenshot evidence was captured.
- 2026-03-11 20:27 GMT: Updated checklist evidence and prepared explicit user-verification request; task remains pending user confirmation per lifecycle rules.

## Changes Made

- `bizPA/frontend/src/App.jsx`
  - Added a deterministic `readinessDemo` query mode so the readiness UI can launch locally without backend dependency for smoke validation.
  - Replaced the old minimal quarter card with a full readiness workspace showing active-quarter score, quarter label, issue count, severity breakdown, issue drill-down, corrective action buttons, and explicit historical snapshot separation.
  - Added helper functions and demo data structures for readiness report rendering and historical snapshot context.
- `bizPA/start_bizpa_tax_readiness_ui.ps1`
  - Added a dedicated local start script that launches the readiness UI on port `3002` and prints the exact localhost URL to open.
- `bizPA/tax_readiness_ui_smoke.ps1`
  - Added an automated smoke script that starts the readiness UI, verifies HTTP 200 on the readiness URL, and captures a screenshot into `workstream/verification`.

## Validation

- `npm.cmd run build` in `C:\Users\edebe\eds\bizPA\frontend`
  - Result: Pass
  - Key output: `Compiled successfully.` and bundle emitted to `build\`
- `powershell -ExecutionPolicy Bypass -File 'C:\Users\edebe\eds\bizPA\tax_readiness_ui_smoke.ps1'`
  - Result: Pass
  - Key output:
    - `READINESS_URL=http://127.0.0.1:3002/?readinessDemo=1&tab=quarter`
    - `FRONTEND_STATUS=200`
    - `SCREENSHOT=C:\Users\edebe\eds\workstream\verification\20260311_201500_bizpa_tax_readiness_ui.png`
- User verification requested on 2026-03-11 20:27 GMT
  - Please verify:
    - active-quarter readiness is clearly labelled and separated from historical snapshots
    - readiness percentage, issue count, and severity breakdown are visible
    - issue drill-down rows show corrective actions and navigate as expected
    - local start path `bizPA/start_bizpa_tax_readiness_ui.ps1` prints the readiness URL and opens the UI without immediate crash

## Risks/Notes

- This is a user-visible UI change, so final lifecycle completion requires user verification per the lifecycle skill.
- The repo has many unrelated uncommitted changes; this task will avoid reverting or modifying unrelated files.
- The smoke/start path intentionally uses `readinessDemo=1` on port `3002` so verification is stable even when the backend is not running; the live UI still consumes the real readiness payload when demo mode is absent.

## Completion Status

Awaiting user verification - 2026-03-11 20:27 GMT


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260311_161957_claude_bizpa_mvp_product_requirements_document_workstreamD_create_tax_readiness_ui.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented the tax-readiness UI in [App.jsx](C:/Users/edebe/eds/bizPA/frontend/src/App.jsx). The quarter screen now shows active-quarter readiness, issue count, severity breakdown, blocker drill-down with corrective actions, and a separate historical snapshot section so archived quarters are clearly reference-only.

Added a dedicated launch path in [start_bizpa_tax_readiness_ui.ps1](C:/Users/edebe/eds/bizPA/start_bizpa_tax_readiness_ui.ps1) and an automated smoke/screenshot script in [tax_readiness_ui_smoke.ps1](C:/Users/edebe/eds/bizPA/tax_readiness_ui_smoke.ps1). The local readiness URL is `http://127.0.0.1:3002/?readinessDemo=1&tab=quarter`. Screenshot evidence was captured at [20260311_201500_bizpa_tax_readiness_ui.png](C:/Users/edebe/eds/workstream/verification/20260311_201500_bizpa_tax_readiness_ui.png). The lifecycle file is updated at [20260311_161957_claude_bizpa_mvp_product_requirements_document_workstreamD_create_tax_readiness_ui.md](C:/Users/edebe/eds/workstream/200_inprogress/claude/20260311_161957_claude_bizpa_mvp_product_requirements_document_workstreamD_create_tax_readiness_ui.md).

Validation passed:
- `npm.cmd run build` in `bizPA/frontend`
- `powershell -ExecutionPolicy Bypass -File C:\Users\edebe\eds\bizPA\tax_readiness_ui_smoke.ps1`
- Smoke output confirmed `FRONTEND_STATUS=200` and the readiness URL above

This task is left as awaiting user verification, per the lifecycle rule for UI changes. Please verify pass/fail for:
- active-quarter readiness is clearly separated from historical snapshots
- readiness percentage, issue count, and severity breakdown are visible
- issue drill-down actions behave as expected
- [start_bizpa_tax_readiness_ui.ps1](C:/Users/edebe/eds/bizPA/start_bizpa_tax_readiness_ui.ps1) prints the URL and launches without an immediate crash
```
- Stderr:
```text
mestamp 2026-03-11 20:25:45.
+
+## Implementation Log
+
+- 2026-03-11 20:13 GMT: Read `skills/workstream-task-lifecycle/SKILL.md`, reviewed the assigned task file, and mapped the task to the existing bizPA frontend quarter screen plus existing launch/smoke script patterns.
+- 2026-03-11 20:14 GMT: Rewrote this task file into lifecycle format before code changes, per repository and skill requirements.
+- 2026-03-11 20:16 GMT: Implemented a dedicated readiness demo report, historical snapshot contrast, severity breakdown helpers, and a redesigned active-quarter readiness workspace in `bizPA/frontend/src/App.jsx`.
+- 2026-03-11 20:18 GMT: Added `bizPA/start_bizpa_tax_readiness_ui.ps1` and `bizPA/tax_readiness_ui_smoke.ps1` to provide a stable local launch URL and automated smoke/screenshot capture path on port 3002.
+- 2026-03-11 20:19 GMT: Ran `npm.cmd run build` in `bizPA/frontend`; build passed.
+- 2026-03-11 20:20 GMT: First smoke run reached the frontend but failed at screenshot capture because the initial Chrome process handle was not bound to a visible window.
+- 2026-03-11 20:24 GMT: Hardened the smoke script to discover the real Chrome window process with an accessible `MainWindowHandle` before capture.
+- 2026-03-11 20:25 GMT: Re-ran the readiness smoke script successfully; frontend returned HTTP 200 and screenshot evidence was captured.
+- 2026-03-11 20:27 GMT: Updated checklist evidence and prepared explicit user-verification request; task remains pending user confirmation per lifecycle rules.
+
+## Changes Made
+
+- `bizPA/frontend/src/App.jsx`
+  - Added a deterministic `readinessDemo` query mode so the readiness UI can launch locally without backend dependency for smoke validation.
+  - Replaced the old minimal quarter card with a full readiness workspace showing active-quarter score, quarter label, issue count, severity breakdown, issue drill-down, corrective action buttons, and explicit historical snapshot separation.
+  - Added helper functions and demo data structures for readiness report rendering and historical snapshot context.
+- `bizPA/start_bizpa_tax_readiness_ui.ps1`
+  - Added a dedicated local start script that launches the readiness UI on port `3002` and prints the exact localhost URL to open.
+- `bizPA/tax_readiness_ui_smoke.ps1`
+  - Added an automated smoke script that starts the readiness UI, verifies HTTP 200 on the readiness URL, and captures a screenshot into `workstream/verification`.
+
+## Validation
+
+- `npm.cmd run build` in `C:\Users\edebe\eds\bizPA\frontend`
+  - Result: Pass
+  - Key output: `Compiled successfully.` and bundle emitted to `build\`
+- `powershell -ExecutionPolicy Bypass -File 'C:\Users\edebe\eds\bizPA\tax_readiness_ui_smoke.ps1'`
+  - Result: Pass
+  - Key output:
+    - `READINESS_URL=http://127.0.0.1:3002/?readinessDemo=1&tab=quarter`
+    - `FRONTEND_STATUS=200`
+    - `SCREENSHOT=C:\Users\edebe\eds\workstream\verification\20260311_201500_bizpa_tax_readiness_ui.png`
+- User verification requested on 2026-03-11 20:27 GMT
+  - Please verify:
+    - active-quarter readiness is clearly labelled and separated from historical snapshots
+    - readiness percentage, issue count, and severity breakdown are visible
+    - issue drill-down rows show corrective actions and navigate as expected
+    - local start path `bizPA/start_bizpa_tax_readiness_ui.ps1` prints the readiness URL and opens the UI without immediate crash
+
+## Risks/Notes
+
+- This is a user-visible UI change, so final lifecycle completion requires user verification per the lifecycle skill.
+- The repo has many unrelated uncommitted changes; this task will avoid reverting or modifying unrelated files.
+- The smoke/start path intentionally uses `readinessDemo=1` on port `3002` so verification is stable even when the backend is not running; the live UI still consumes the real readiness payload when demo mode is absent.
+
+## Completion Status
+
+Awaiting user verification - 2026-03-11 20:27 GMT

tokens used
127,021
```
