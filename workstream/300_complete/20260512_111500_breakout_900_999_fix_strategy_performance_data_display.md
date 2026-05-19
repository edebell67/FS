## Task
- Investigate and fix strategy_performance.html which is currently not displaying any data.
- Ensure the API and UI are correctly pulling data from the new X:\eds workspace.
- Identify if the issue is in the frontend fetch logic, the backend API response, or missing background generator data.

## Task Type
- investigative / fix-followup

## Destination Folder
- workstream/300_complete

## Dependency
- TradeApps/breakout/fs/trade_viewer_api.py
- TradeApps/breakout/fs/strategy_performance.html
- TradeApps/breakout/fs/paths.py
- X:\eds drive availability

## Plan
1. [x] Check API response for /api/stats_summary.
   - Test: `Invoke-WebRequest http://127.0.0.1:5000/api/stats_summary?mode=live&date=2026-05-12&product_type=forex&limit=3&view=top&sort_key=total_net&sort_dir=desc&include_dist=false`
   - Evidence: Windows-host API returned HTTP 200 with populated `data` and `snapshot`.
2. [x] Verify `_summary_net.json` exists on X: drive for the target date.
   - Test: PowerShell `Test-Path X:\eds\TradeApps\breakout\fs\json\live\forex\2026-05-12\_summary_net.json`.
   - Evidence: Found file, size 5,316,222 bytes.
3. [x] Identify frontend/backend fault boundary.
   - Evidence: API returned populated JSON. Served page returned HTTP 200. Source had a startup race: `loadStats()` ran before `/api/config` populated the Product Type dropdown.
4. [x] Implement fixes.
   - `strategy_performance.html`: wait for config/product-type initialization before calling `loadStats()`.
   - `paths.py`: make Windows drive path normalization OS-aware so WSL/Linux does not treat `X:\eds` / `x:\eds` as relative local folders.
5. [x] Verify display path and syntax.
   - Evidence: Served `strategy_performance.html` contains the new config-before-stats marker.
   - Evidence: Python `py_compile` passed for `paths.py` under WSL and Windows Python.
   - Evidence: Extracted strategy page JS passed `node --check`.

## Evidence
- Objective: Restore performance data visibility.
- Delivery: Initial dashboard stats load now waits for the configured product type before requesting `/api/stats_summary`.
- Coverage: Core performance dashboard startup load and X:\eds path handling.
- Auto-Acceptance:
  - `X:\eds\TradeApps\breakout\fs\json\live\forex\2026-05-12\_summary_net.json` exists and is non-empty.
  - `http://127.0.0.1:5000/api/stats_summary?...` returns HTTP 200 and populated rows.
  - `http://127.0.0.1:5000/strategy_performance.html` returns HTTP 200 and includes the fix marker.

## Implementation Log
- 2026-05-13: Located the referenced task at `C:\Users\edebe\eds\workstream\200_inprogress\20260512_111500_breakout_900_999_fix_strategy_performance_data_display.md`.
- 2026-05-13: Confirmed Windows-host API returns data from the X:\eds summary file.
- 2026-05-13: Fixed frontend startup ordering in `strategy_performance.html` so stats are fetched after config/product type initialization.
- 2026-05-13: Hardened `paths.py` for WSL/Linux handling of Windows drive paths.

## Changes Made
- `TradeApps/breakout/fs/strategy_performance.html`
  - Replaced config/stats parallel startup with config-first initialization, then `loadStats()`.
- `TradeApps/breakout/fs/paths.py`
  - Added OS-independent Windows drive detection using `ntpath`/regex.
  - Added WSL `/mnt/<drive>/...` mapping fallback for Windows drive paths.
  - Prevented accidental relative directories named like `x:\eds` from being accepted as data roots on POSIX.

## Validation
- WSL: `/usr/bin/python3 -m py_compile paths.py` passed.
- Windows: `py -3` compiled/imported `paths.py`; `DATA_EDS_ROOT` resolved to `X:\eds`, exists true; `BREAKOUT_JSON_ROOT` exists true.
- API: Windows `Invoke-WebRequest` to `/api/stats_summary` returned HTTP 200 with populated performance rows.
- Served page: Windows `Invoke-WebRequest` to `/strategy_performance.html` returned HTTP 200 and included the fix marker.
- JS syntax: extracted inline script from `strategy_performance.html` and ran `node --check`; exit code 0.

## Risks/Notes
- The local WSL environment cannot currently access the Windows mapped X: drive as `/mnt/x`; PowerShell can access `X:\eds` and the running Windows API is reading it correctly.
- If running the Flask API inside WSL against X:\eds, mount the Windows X: drive into WSL or configure a Linux-accessible data root.
- Browser-level visual verification from this sandbox could not connect to the Windows localhost, but Windows PowerShell verified the API and served page.

## Completion Status
- Complete.
