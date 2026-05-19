# Market Prices API FastAPI-Starlette Startup Compatibility

## Source
User traceback during conversation 1dc8e4c5-47c8-4ca9-9bc9-8cb42900b7de

## Task Summary
Fix the `market_prices_api` startup failure caused by an incompatible FastAPI and Starlette combination so the service can boot cleanly under the current environment or fail with a controlled actionable message.

## Requirements
1. Identify the startup failure cause in `market_prices_api`.
2. Implement a local fix or compatibility guard for the FastAPI/Starlette mismatch.
3. Preserve existing API endpoints and fetcher lifecycle behavior.
4. Add or tighten dependency guidance so the environment does not silently drift into the broken combination again.
5. Validate that the application module imports and the service startup path no longer crashes with the current error.

## Context
- `market_prices_api/api.py`
- `market_prices_api/main.py`
- `market_prices_api/requirements.txt`
- Installed environment currently reports `fastapi 0.110.0`, `starlette 1.0.0`, `uvicorn 0.42.0`

## Dependency
None

## Plan

- [x] 1. Inspect the installed dependency versions and the FastAPI app bootstrap path.
  - [x] Test: Run an inline Python probe to print installed versions and reproduce the failing `api` import path; pass condition is confirming the exact `Router.__init__()` `on_startup` incompatibility.
  - Evidence: `fastapi 0.110.0`, `starlette 1.0.0`, `uvicorn 0.42.0`, and `TypeError: Router.__init__() got an unexpected keyword argument 'on_startup'` were captured from the `sys.path.insert(0, os.path.abspath('market_prices_api')); import api` reproduction.

- [x] 2. Patch the app startup path with a compatibility fix or explicit guard.
  - [x] Test: Import `api:app` successfully in the local environment; pass condition is `IMPORT_OK FastAPI` and `PKG_IMPORT_OK FastAPI` after the patch.
  - Evidence: `market_prices_api/api.py` now applies a narrow Starlette router constructor shim, uses a FastAPI lifespan context for fetcher startup/shutdown, and supports both package-relative and script-local imports.

- [x] 3. Update dependency metadata to document or constrain the supported package range.
  - [x] Test: Inspect `market_prices_api/requirements.txt`; pass condition is a tested version boundary matching the validated local environment.
  - Evidence: `market_prices_api/requirements.txt` now constrains `fastapi>=0.110.0,<0.111.0`, `starlette>=1.0.0,<1.1.0`, and `uvicorn>=0.42.0,<0.43.0`.

- [x] 4. Validate service startup via the existing entry point.
  - [x] Test: Run `python market_prices_api/main.py --host 127.0.0.1 --port 8002` in a short-lived subprocess and query `http://127.0.0.1:8002/api/health`; pass condition is `Application startup complete.` plus HTTP 200 with health payload keys.
  - Evidence: Startup logs showed all three fetchers starting, Uvicorn reached `Application startup complete.`, and `/api/health` returned `status=healthy` with `cache`, `fetchers`, `status`, and `timestamp`.

## Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false

- Evidence-Type: test_output
  - Artifact: Inline Python probe output capturing `fastapi 0.110.0`, `starlette 1.0.0`, `uvicorn 0.42.0`, plus the original `TypeError: Router.__init__() got an unexpected keyword argument 'on_startup'`.
  - Objective-Proved: Confirms the original failure cause and the exact incompatible API surface.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `market_prices_api/api.py`
  - Objective-Proved: The API now boots with a Starlette 1.x constructor shim, lifespan-managed fetcher lifecycle, and import compatibility for both `api:app` and `market_prices_api.api`.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `market_prices_api/requirements.txt`
  - Objective-Proved: Dependency guidance is pinned to the tested FastAPI, Starlette, and Uvicorn version range used for validation.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: Import verification output `IMPORT_OK FastAPI` and `PKG_IMPORT_OK FastAPI`.
  - Objective-Proved: The application module import path no longer crashes with the original FastAPI/Starlette startup error.
  - Status: captured

- Evidence-Type: demo
  - Artifact: `python market_prices_api/main.py --host 127.0.0.1 --port 8002` followed by `GET http://127.0.0.1:8002/api/health` returning HTTP 200 and `status=healthy`.
  - Objective-Proved: The service startup path works through the existing entry point and exposes the expected health endpoint.
  - Status: captured

- Evidence-Type: user_feedback
  - Artifact: Pending user verification request for normal workflow startup and endpoint checks.
  - Objective-Proved: Final acceptance from the user environment for the API behavior after the compatibility fix.
  - Status: planned

## Implementation Log
- 2026-03-28 18:49 — Task created from traceback showing FastAPI/Starlette startup incompatibility in `market_prices_api`.
- 2026-03-28 18:49 — Moved from `workstream/100_todo` to `workstream/200_inprogress/codex` when implementation work began.
- 2026-03-28 18:52 — Reproduced the failure under `fastapi 0.110.0` and `starlette 1.0.0`; confirmed FastAPI still passes legacy `on_startup` / `on_shutdown` kwargs into Starlette’s `Router.__init__`.
- 2026-03-28 18:54 — Kept the narrow router constructor compatibility shim, preserved fetcher lifecycle through a FastAPI lifespan context, and added package-relative import fallback for `market_prices_api.api`.
- 2026-03-28 18:55 — Updated `market_prices_api/requirements.txt` to the validated `fastapi`, `starlette`, and `uvicorn` range used in the current environment.
- 2026-03-28 18:55 — Verified both `import api` and `import market_prices_api.api` succeed and no longer raise the original startup error.
- 2026-03-28 18:55 — Started the service through `market_prices_api/main.py`, observed all fetchers start, and confirmed `/api/health` returned HTTP 200 with `status=healthy`.

## Changes Made
- `market_prices_api/api.py`: preserved the existing endpoint surface, kept the Starlette router constructor compatibility shim, used a lifespan context for fetcher startup/shutdown, and added package-relative import fallback for `price_cache` and `fetchers`.
- `market_prices_api/requirements.txt`: aligned dependency bounds with the validated local environment by constraining FastAPI, Starlette, and Uvicorn to the tested range.

## Validation
- `@' import fastapi, starlette, uvicorn; print(...) '@ | python -` reported `fastapi 0.110.0`, `starlette 1.0.0`, and `uvicorn 0.42.0`.
- `@' sys.path.insert(0, os.path.abspath("market_prices_api")); import api '@ | python -` originally reproduced `TypeError: Router.__init__() got an unexpected keyword argument 'on_startup'`.
- `@' sys.path.insert(0, os.path.abspath("market_prices_api")); import api; print("IMPORT_OK", type(api.app).__name__) '@ | python -` passed after the patch.
- `@' import market_prices_api.api as api; print("PKG_IMPORT_OK", type(api.app).__name__) '@ | python -` passed after the package import fallback was added.
- Inline subprocess verification of `python market_prices_api/main.py --host 127.0.0.1 --port 8002` reached `Application startup complete.` and `GET http://127.0.0.1:8002/api/health` returned HTTP 200 with `status=healthy`, `cache`, `fetchers`, and `timestamp`.
- 2026-03-28 18:56 — User verification requested in final response for normal workflow startup and endpoint behavior.

## Risks/Notes
- The Starlette router shim is intentionally narrow: it only absorbs FastAPI’s legacy constructor kwargs when they are empty and raises a controlled error if future code tries to rely on legacy startup/shutdown lists again.
- The service was validated with a short-lived local boot and health check. Final acceptance is still pending user verification in the normal runtime environment.
- The workspace is currently untracked by Git in this environment, so evidence references file contents and command output instead of a repository diff.

## Completion Status
Awaiting user verification — 2026-03-28 18:56
