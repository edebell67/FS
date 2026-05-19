# Task: Fix Frequency Explorer Data Loading and Robust Date Resolution

## 1. Context and Problem
The user's objective is to fix the Frequency Explorer data loading issue for `forex/2026-03-18/_frequency.json`. The application auto-resolves the "latest date" to `2026-03-18`, but the `_frequency.json` file for `forex` has not been generated yet for that date. This causes a JSON parsing error when the server returns a 404 HTML response instead of JSON.

## 2. Plan of Approach
1.  **Backend Enhancment (`trade_viewer_api.py`)**: Update the `/api/dates` endpoint to support an optional `file` query parameter. If provided, the API will only return dates where that specific file exists.
2.  **Frontend Enhancement (`frequency_explorer.html`)**: Update `getLatestDate` to pass the `file` name of the current data source and improve error handling in `fetchData`.
3.  **Validation**: Verify that for `forex`, the latest date resolved is now `2026-03-17`.
4.  **Version Update**: Bump version to `V20260318_1055`.

## 3. Progress Tracking
- [x] Update `trade_viewer_api.py` with `file` check in `/api/dates`.
- [x] Update `frequency_explorer.html` to pass `file` in `getLatestDate`.
- [x] Improve error banner in `frequency_explorer.html`.
- [x] Update `constants.py` to `V20260318_1055`.
- [x] Final verification.

## 4. Work Log
- 2026-03-18 00:55: Starting task.
- 2026-03-18 01:05: Implemented backend `file` filter in `/api/dates`.
- 2026-03-18 01:06: Updated frontend `getLatestDate` to pass filename for smarter date resolution.
- 2026-03-18 01:07: Enhanced error messaging for missing data files.
- 2026-03-18 01:08: Task completed.
