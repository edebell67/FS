# Task: Update System Health Live Feed Check To Use Multiple FX Endpoints

## Source
- User Directive: 2026-03-27

## Task Summary
Update the live system-health price-feed check so it tries multiple configured live FX endpoints and passes if any one of them returns valid data.

## Goal
For live mode, check these endpoints in order and mark the feed healthy if any one responds with rows:
- `http://127.0.0.1:8001/api/vw_000_fx_quotes`
- `http://127.0.0.1:8002/api/vw_000_fx_quotes`
- `http://127.0.0.1:8000/api/vw_000_fx_quotes?db=tradedb`

## Plan
- [x] 1. Locate the current health-check endpoint logic.
- [x] 2. Patch the live feed check to try all requested endpoints.
- [x] 3. Verify the health API result locally.
- [x] 4. Record the outcome.

## Implementation Log
- **2026-03-27 00:46**: Task created and current health-check logic identified in `trade_viewer_api.py`.
- **2026-03-27 00:47**: Updated live health-check logic to try these endpoints in sequence and stop on first successful rowset:
  - `http://127.0.0.1:8001/api/vw_000_fx_quotes`
  - `http://127.0.0.1:8002/api/vw_000_fx_quotes`
  - `http://127.0.0.1:8000/api/vw_000_fx_quotes?db=tradedb`
- **2026-03-27 00:47**: Preserved existing sim-mode behavior using the sim FX endpoint on port `8001`.
- **2026-03-27 00:47**: Verified `http://127.0.0.1:5000/api/system_health?mode=all` now returns `live.checks.price_feed = true`, `feed_latency_sec = 1`, and `healthy = true`.

## Findings
- The live health check now passes if any one of the requested live FX endpoints is healthy.
- Current post-change API result shows:
  - `live.checks.price_feed = true`
  - `live.checks.feed_latency_sec = 1`
  - `live.healthy = true`

## Validation
- Updated file:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Confirmed endpoint list in code:
  - `http://127.0.0.1:8001/api/vw_000_fx_quotes`
  - `http://127.0.0.1:8002/api/vw_000_fx_quotes`
  - `http://127.0.0.1:8000/api/vw_000_fx_quotes?db=tradedb`
- Runtime verification:
  - `Invoke-RestMethod http://127.0.0.1:5000/api/system_health?mode=all`

## Outcome
The `Price Feed Connection` health check for live mode now uses the requested fallback behavior and reports healthy when any one of the approved live FX endpoints is available.
