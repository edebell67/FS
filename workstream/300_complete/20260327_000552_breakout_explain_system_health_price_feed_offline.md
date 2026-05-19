# Task: Explain Why System Health Shows Price Feed Connection Offline

## Source
- User Directive: 2026-03-27

## Task Summary
Trace the `System Health` logic to explain why the UI currently shows `Price Feed Connection: Offline`.

## Goal
Identify the exact backend condition that produces the `Offline` status in the health UI.

## Plan
- [x] 1. Locate the UI and API code for system health.
- [x] 2. Read the backend health-check logic for feed connectivity.
- [x] 3. Check the current runtime condition that triggered `Offline`.
- [x] 4. Explain the result clearly.

## Implementation Log
- **2026-03-27 00:05**: Task created. Located `system_health.html` and `/api/system_health` implementation in `trade_viewer_api.py`.
- **2026-03-27 00:07**: Confirmed frontend shows `Offline` whenever `data.checks.price_feed` is false in `system_health.html`.
- **2026-03-27 00:08**: Traced backend logic in `trade_viewer_api.py`. For live mode, the health check probes only `http://127.0.0.1:8001/api/vw_000_fx_quotes`.
- **2026-03-27 00:09**: Verified current runtime state with PowerShell:
  - `http://127.0.0.1:8001/api/vw_000_fx_quotes` => connection refused
  - `http://127.0.0.1:8002/api/vw_000_futures_quotes` => returning live rows

## Findings
- `Price Feed Connection: Offline` is being caused by the live health check probing port `8001` and getting a refused connection.
- The health check is not using the futures feed on port `8002` for that row.
- So the page is currently reporting:
  - FX feed endpoint on `8001`: down/unreachable
  - futures feed endpoint on `8002`: up and returning data
- This means the health indicator is endpoint-specific, not a full “any live market feed is available” check.

## Validation
- UI mapping:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\system_health.html`
- Backend logic:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Runtime checks:
  - `Invoke-RestMethod http://127.0.0.1:8001/api/vw_000_fx_quotes` => refused connection
  - `Invoke-RestMethod http://127.0.0.1:8002/api/vw_000_futures_quotes` => live data returned

## Outcome
The `Offline` status is correct for the specific FX endpoint the health page checks. It does not mean every live quote source is down; your futures quote source on `8002` is currently responding.
