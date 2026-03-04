# TASK: Resolve Continuous Connection Errors (MetaMask/Backend Sync)

## 1. Problem Description
The user is experiencing continuous error displays in the browser console and potentially the UI. 
- **Console Error**: `chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/scripts/inpage.js:1:63510` (MetaMask extension interference).
- **Backend Errors**: `404 Not Found` for new Milestone 3 endpoints (`/api/v1/calendar`, `/revenue`, `/diary`, `/teams/my`).

## 2. Root Cause Analysis
- **MetaMask**: The extension is injecting `inpage.js` and failing to connect to its own provider, causing "noise" in the console.
- **Backend Stale State**: The backend process (PID 29896) is still running the old version of `app.js` which does not have the Milestone 3 routes bound, leading to `404` errors when the UI attempts to fetch new data.

## 3. Action Plan (Checklist)
- [ ] **Step 1: Restart Backend Process**
  - Kill existing Node process (External/User action required due to safety constraints).
  - Restart with `npm start` in `bizPA/backend`.
- [ ] **Step 2: Verify Endpoints**
  - Use `curl` or `test_api_query.py` to confirm `/api/v1/calendar` returns 200 OK.
- [ ] **Step 3: Handle MetaMask Noise**
  - Update `App.jsx` to include a global error boundary or silence specific extension-related console logs if they affect UX.
- [ ] **Step 4: Validate UI Recovery**
  - Refresh `http://localhost:3005` and verify "Schedule" and "Diary" tabs load without 404s.

## 4. Log of Findings (2026-02-24 15:19)
- Playwright snapshot confirms UI is rendered but 404s are firing every 30 seconds due to `fetchAllData` polling stale backend routes.
- MetaMask error confirmed as non-app code but persistent.
