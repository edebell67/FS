# TASK J2: Launch Landing Page

**Source:** `workstream/epic/Autonomous Trading Signal Platform.md`

## Task Summary

Make the landing page publicly accessible for the Autonomous Trading Signal Platform workstream.

## Context

- `DataInsights/src/main.py` controls FastAPI startup and public route exposure.
- `DataInsights/src/routers/landing.py` contains landing-page HTML routes.
- `DataInsights/src/services/landing/renderer.py` manages template rendering.
- `DataInsights/src/templates/` contains HTML templates for landing experiences.
- `DataInsights/tests/test_landing_page.py` covers landing-page regressions.

## Plan

- [x] 1. Add a public landing-page entry route that renders without requiring a lead-specific page code.
  - [x] Test: `$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py -k public` passes and confirms the public landing HTML is returned.
  - Evidence: `2 passed, 5 deselected`; assertions confirmed `/` returns HTTP 200 and includes `Autonomous Trading Signal Platform` plus `Open API docs`.
- [x] 2. Make application startup resilient enough for the public landing page to load even when the database is unavailable.
  - [x] Test: `$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py -k startup` passes and confirms `/` still responds when startup DB health checks fail.
  - Evidence: `1 passed, 6 deselected`; test patched `health_check` to raise `RuntimeError("database unavailable")` and still received HTTP 200 from `/`.
- [x] 3. Run the focused landing-page regression suite and record implementation/validation details.
  - [x] Test: `$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py` passes.
  - Evidence: `7 passed`; landing-page unit coverage now includes public route rendering and startup-resilience behavior.

## Implementation Log

- 2026-03-09 14:36 GMT: Read `skills/workstream-task-lifecycle/SKILL.md` and loaded the task stub from `workstream/200_inprogress/codex/20260309_120091_codex_workstreamJ_launch_landing_page.md`.
- 2026-03-09 14:37 GMT: Inspected `DataInsights` landing router, FastAPI app wiring, templates, tests, and epic context for Workstream J2.
- 2026-03-09 14:42 GMT: Identified two blockers to “publicly accessible”: no generic public landing entry route and startup failure when Postgres health checks fail.
- 2026-03-09 14:45 GMT: Added a new public landing renderer/template and mounted a root `/` landing route in `DataInsights/src/routers/landing.py`.
- 2026-03-09 14:47 GMT: Updated `DataInsights/src/main.py` startup/shutdown handling to log and continue when DB health checks or scheduler start/shutdown fail.
- 2026-03-09 14:49 GMT: Extended `DataInsights/tests/test_landing_page.py` with public-route and startup-failure coverage, then ran focused pytest validation successfully.

## Changes Made

- Added `render_public_landing()` to `DataInsights/src/services/landing/renderer.py`.
- Added a public root route `GET /` to `DataInsights/src/routers/landing.py`.
- Added `DataInsights/src/templates/public_landing.html` for a generic public-facing marketing entry page.
- Changed `DataInsights/src/main.py` startup to tolerate DB health-check failures and scheduler startup failures by logging warnings instead of aborting app boot.
- Changed `DataInsights/src/main.py` shutdown to tolerate scheduler shutdown errors without crashing termination.
- Updated `DataInsights/tests/test_landing_page.py` to:
  - set repo-local import path for direct pytest runs,
  - verify the public landing page returns expected marketing content,
  - verify the root landing page still loads when startup DB health checks fail.

## Validation

- Passed: `$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py -k public`
- Passed: `$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py -k startup`
- Passed: `$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py`
- Warning-only output observed during pytest:
  - Pytest reported unknown config option `asyncio_mode` in the current environment.
  - FastAPI emitted existing `on_event` deprecation warnings.
  - Pydantic emitted existing class-based config deprecation warnings.
- User verification requested: confirm the public landing page at `/` is the intended public entrypoint and the content/CTA copy is acceptable for launch.

## Risks/Notes

- Scope is limited to making a public landing entrypoint available and resilient at app startup; no production hosting or domain cutover is included in this task file.
- Existing lead-specific landing routes under `/i/{page_code}` still require database-backed content.

## Completion Status

Awaiting user verification — 2026-03-09 14:49 GMT


## Execution Evidence
- Agent lane: codex
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/codex\20260309_120091_codex_workstreamJ_launch_landing_page.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented the landing-page launch task in `DataInsights`. The app now exposes a public root landing page at `/` via [landing.py](/C:/Users/edebe/eds/DataInsights/src/routers/landing.py#L22), renders it through [renderer.py](/C:/Users/edebe/eds/DataInsights/src/services/landing/renderer.py#L34), and uses the new template [public_landing.html](/C:/Users/edebe/eds/DataInsights/src/templates/public_landing.html). I also made startup more resilient in [main.py](/C:/Users/edebe/eds/DataInsights/src/main.py#L71) so a failed DB health check no longer prevents the public page from loading.

Validation passed with:
`$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py -k public`
`$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py -k startup`
`$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py`

The lifecycle file is updated with checklist evidence and is currently marked awaiting user verification at [20260309_120091_codex_workstreamJ_launch_landing_page.md](/C:/Users/edebe/eds/workstream/200_inprogress/codex/20260309_120091_codex_workstreamJ_launch_landing_page.md#L17). Verify two things before this moves to complete: `1.` `/` is the intended public entrypoint, and `2.` the current landing-page copy/CTAs are acceptable for launch.
```
- Stderr:
```text
ing a lead-specific page code.
+  - [x] Test: `$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py -k public` passes and confirms the public landing HTML is returned.
+  - Evidence: `2 passed, 5 deselected`; assertions confirmed `/` returns HTTP 200 and includes `Autonomous Trading Signal Platform` plus `Open API docs`.
+- [x] 2. Make application startup resilient enough for the public landing page to load even when the database is unavailable.
+  - [x] Test: `$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py -k startup` passes and confirms `/` still responds when startup DB health checks fail.
+  - Evidence: `1 passed, 6 deselected`; test patched `health_check` to raise `RuntimeError("database unavailable")` and still received HTTP 200 from `/`.
+- [x] 3. Run the focused landing-page regression suite and record implementation/validation details.
+  - [x] Test: `$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py` passes.
+  - Evidence: `7 passed`; landing-page unit coverage now includes public route rendering and startup-resilience behavior.
+
+## Implementation Log
+
+- 2026-03-09 14:36 GMT: Read `skills/workstream-task-lifecycle/SKILL.md` and loaded the task stub from `workstream/200_inprogress/codex/20260309_120091_codex_workstreamJ_launch_landing_page.md`.
+- 2026-03-09 14:37 GMT: Inspected `DataInsights` landing router, FastAPI app wiring, templates, tests, and epic context for Workstream J2.
+- 2026-03-09 14:42 GMT: Identified two blockers to “publicly accessible”: no generic public landing entry route and startup failure when Postgres health checks fail.
+- 2026-03-09 14:45 GMT: Added a new public landing renderer/template and mounted a root `/` landing route in `DataInsights/src/routers/landing.py`.
+- 2026-03-09 14:47 GMT: Updated `DataInsights/src/main.py` startup/shutdown handling to log and continue when DB health checks or scheduler start/shutdown fail.
+- 2026-03-09 14:49 GMT: Extended `DataInsights/tests/test_landing_page.py` with public-route and startup-failure coverage, then ran focused pytest validation successfully.
+
+## Changes Made
+
+- Added `render_public_landing()` to `DataInsights/src/services/landing/renderer.py`.
+- Added a public root route `GET /` to `DataInsights/src/routers/landing.py`.
+- Added `DataInsights/src/templates/public_landing.html` for a generic public-facing marketing entry page.
+- Changed `DataInsights/src/main.py` startup to tolerate DB health-check failures and scheduler startup failures by logging warnings instead of aborting app boot.
+- Changed `DataInsights/src/main.py` shutdown to tolerate scheduler shutdown errors without crashing termination.
+- Updated `DataInsights/tests/test_landing_page.py` to:
+  - set repo-local import path for direct pytest runs,
+  - verify the public landing page returns expected marketing content,
+  - verify the root landing page still loads when startup DB health checks fail.
+
+## Validation
+
+- Passed: `$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py -k public`
+- Passed: `$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py -k startup`
+- Passed: `$env:PYTHONPATH='.'; pytest -q tests/test_landing_page.py`
+- Warning-only output observed during pytest:
+  - Pytest reported unknown config option `asyncio_mode` in the current environment.
+  - FastAPI emitted existing `on_event` deprecation warnings.
+  - Pydantic emitted existing class-based config deprecation warnings.
+- User verification requested: confirm the public landing page at `/` is the intended public entrypoint and the content/CTA copy is acceptable for launch.
+
+## Risks/Notes
+
+- Scope is limited to making a public landing entrypoint available and resilient at app startup; no production hosting or domain cutover is included in this task file.
+- Existing lead-specific landing routes under `/i/{page_code}` still require database-backed content.
+
+## Completion Status
+
+Awaiting user verification — 2026-03-09 14:49 GMT

tokens used
141,318
```

# User Feedback
User Verified: PASS
