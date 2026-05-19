Source: None
Task Summary: Restore `market_prices_api` startup under the failing `C:\Python313` environment by handling the FastAPI/Starlette router signature mismatch and documenting the dependency constraint.
Context: `market_prices_api/api.py`, `market_prices_api/requirements.txt`, Python 3.13 user-site packages (`fastapi 0.110.0`, `starlette 1.0.0`).
Dependency: None

Plan:
- [x] 1. Reproduce the failure in the same Python 3.13 environment and identify the incompatible dependency behavior.
  - [x] Test: `& 'C:\Python313\python.exe' main.py`
  - Evidence: Captured traceback showing `TypeError: Router.__init__() got an unexpected keyword argument 'on_startup'` with `fastapi=0.110.0` and `starlette=1.0.0`.
- [x] 2. Patch `market_prices_api` to tolerate the incompatible router signature and record the expected dependency range.
  - [x] Test: `& 'C:\Python313\python.exe' -c "import api; print(api.app.title)"`
  - Evidence: Command returned `Market Prices API` after adding a Starlette router compatibility shim, migrating startup/shutdown to lifespan, and pinning `starlette>=0.36.3,<0.37.0`.
- [x] 3. Validate the app boots far enough to complete FastAPI startup in the failing interpreter.
  - [x] Test: `& 'C:\Python313\python.exe' main.py`
  - Evidence: Startup log reached `INFO:     Application startup complete.` and `INFO:     Uvicorn running on http://0.0.0.0:8002`.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `& 'C:\Python313\python.exe' main.py` traceback reproduced on 2026-03-27
  - Objective-Proved: Reproduces the reported startup failure in the target interpreter before the fix.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `market_prices_api/api.py`, `market_prices_api/requirements.txt`
  - Objective-Proved: Shows the compatibility shim and dependency constraint added for the fix.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `& 'C:\Python313\python.exe' -c "import api; print(api.app.title)"` and `& 'C:\Python313\python.exe' main.py`
  - Objective-Proved: Confirms the API imports and starts successfully after the fix.
  - Status: captured

Implementation Log:
- 2026-03-27 12:48:39 Europe/London: Created lifecycle file for the FastAPI/Starlette startup compatibility bugfix.
- 2026-03-27 12:49:00 Europe/London: Confirmed the failing interpreter was `C:\Python313\python.exe` with `fastapi 0.110.0` and `starlette 1.0.0`; reproduced the original `Router.__init__` failure.
- 2026-03-27 12:51:00 Europe/London: Added a compatibility shim in `api.py` so FastAPI can instantiate Starlette routers when `on_startup` and `on_shutdown` are no longer accepted.
- 2026-03-27 12:52:00 Europe/London: Replaced `@app.on_event(...)` handlers with a lifespan context manager because Starlette 1.0 also removes `add_event_handler`.
- 2026-03-27 12:52:30 Europe/London: Pinned `fastapi` and `starlette` in `requirements.txt` to document the supported dependency window and prevent future incompatible installs.
- 2026-03-27 12:52:40 Europe/London: Validated successful import and full application startup in the previously failing interpreter.

Changes Made:
- Added `_patch_starlette_router_for_fastapi_compat()` in `market_prices_api/api.py` to normalize Starlette router initialization across older and newer signatures.
- Added an application `lifespan` context manager in `market_prices_api/api.py` and moved fetcher startup/shutdown into it.
- Updated `market_prices_api/requirements.txt` to pin `fastapi>=0.110.0,<0.111.0` and `starlette>=0.36.3,<0.37.0`.

Validation:
- `& 'C:\Python313\python.exe' -c "import sys, inspect; from starlette.routing import Router; import fastapi, starlette; print(sys.executable); print(f'fastapi={fastapi.__version__}'); print(f'starlette={starlette.__version__}'); print(inspect.signature(Router.__init__))"`
  - Result: Confirmed target interpreter `C:\Python313\python.exe`, `fastapi=0.110.0`, `starlette=1.0.0`, and a router signature without `on_startup`.
- `& 'C:\Python313\python.exe' main.py`
  - Result before fix: Failed with `TypeError: Router.__init__() got an unexpected keyword argument 'on_startup'`.
- `& 'C:\Python313\python.exe' -c "import api; print(api.app.title)"`
  - Result after fix: Printed `Market Prices API`.
- `& 'C:\Python313\python.exe' main.py`
  - Result after fix: Reached `Application startup complete` and began serving on `http://0.0.0.0:8002`; remaining warnings were network/file-access issues from fetchers, not FastAPI startup failures.

Risks/Notes:
- The Python 3.13 environment is using `fastapi 0.110.0` with `starlette 1.0.0`, which is outside FastAPI 0.110's supported Starlette range.
- The repo worktree is already dirty; changes must remain scoped to this task's files.
- The compatibility shim keeps the app bootable even if Starlette 1.0 is present, but the preferred long-term state is still to reinstall dependencies from `requirements.txt` so the environment matches the supported range.

Completion Status:
- Complete - 2026-03-27 12:52:40 Europe/London
