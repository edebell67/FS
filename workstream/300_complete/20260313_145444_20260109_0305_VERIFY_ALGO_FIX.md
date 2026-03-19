# Verify Algo Script Fixes
**Date**: 2026-01-09 03:05
**Version**: V20260109_0305

## Issue
User reported that `verify_algo_execution_and_restart_02.py` was not generating base trades, unlike running the scripts manually.

## Diagnosis
The verification script was launching child processes without:
1.  **Correct Working Directory**: It relied on inherited CWD, which could be wrong if executed from the project root.
2.  **Unbuffered Output**: Logs were hidden until buffer fill/crash.
3.  **Explicit Interpreter**: Potential python environment mismatch.

## Resolution
Updated `verify_algo_execution_and_restart_02.py`:
1.  Added `cwd=folder_path` to `subprocess.Popen` calls to ensure scripts run in their local directory.
2.  Added `-u` flag for unbuffered output.
3.  Used `sys.executable` to enforce consistent python interpreter.

## Action Required
1.  **Stop ALL python processes** (including any manual `breakout.py` runs).
2.  Run `verify_algo_execution_and_restart_02.py`.
3.  Observe console for `[DEBUG] Breakout check...` logs.
4.  Check `json/live/` folder for trade files.
