# Add Exit Time Column to Drilldown Trades

**Source**: User request

## Task Summary
Add an explicit exit time column to the FXPilot dashboard drilldown trades table in `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`, formatted consistently with entry time and showing a dash for open trades.

## Context
- Dashboard URL: `http://172.22.108.121:3001/`
- Frontend file: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
- API endpoint: `TradeApps/breakout/piphunter/landing_page/server.py` route `/api/strategy-trades`
- Related data flow: inline `fetchStrategyTrades()` helper in `forex-dashboard_1.jsx`

## Dependency
Dependency: None

## Plan
- [x] 1. Inspect the drilldown trade table and confirm the strategy-trades payload carries exit time.
  - [x] Test: `Get-Content -Path 'TradeApps\breakout\piphunter\landing_page\forex-dashboard_1.jsx' | Select-Object -First 80` and `Get-Content -Path 'TradeApps\breakout\piphunter\landing_page\server.py' | Select-Object -Skip 100 -First 160` should show the drilldown fetch helper and `/api/strategy-trades` returning `exit_time`.
  - [x] Evidence: `forex-dashboard_1.jsx` inline helper reads `exit_time`; `server.py` route includes `'exit_time': trade.get('exit_time')` for closed trades and `None` for open trades.
- [x] 2. Patch the drilldown trade table to show an explicit Exit Time column using the same formatter pattern as Entry Time and preserve the trade fields passed through from `/api/strategy-trades`.
  - [x] Test: `Get-Content -Path 'TradeApps\breakout\piphunter\landing_page\forex-dashboard_1.jsx' | Select-Object -Skip 480 -First 180` should show `ENTRY TIME` / `EXIT TIME` headers plus `formatTradeDateTime(t.closeTime)`, and the fetch helper should include `exitReason` and related API fields.
  - [x] Evidence: patched JSX now defines `formatTradeDateTime()`, renders `EXIT TIME`, uses `formatTradeDateTime(t.closeTime)`, and preserves `entry_price`, `exit_price`, `exit_reason`, `bias_at_open`, and `bias_latest`.
- [x] 3. Run targeted validation and record any blockers plus required user verification.
  - [x] Test: `npm run build` and `node .\node_modules\vite\bin\vite.js build` from `TradeApps\breakout\piphunter\landing_page` should complete without frontend build errors; if blocked by environment, record the exact failure and request user verification of the visible change.
  - [x] Evidence: `npm run build` failed because `vite` was not resolved in PATH; direct `node .\node_modules\vite\bin\vite.js build` failed because optional dependency `@rollup/rollup-win32-x64-msvc` is missing. User verification requested for the visible drilldown change.

## Evidence
Objective-Delivery-Coverage: 80%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
  - Objective-Proved: The drilldown trade table now exposes an explicit exit-time column and uses a safe date/time formatter with `-` fallback for open trades.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `Get-Content -Path 'TradeApps\breakout\piphunter\landing_page\forex-dashboard_1.jsx' | Select-Object -First 40` and `Get-Content -Path 'TradeApps\breakout\piphunter\landing_page\forex-dashboard_1.jsx' | Select-Object -Skip 480 -First 180`
  - Objective-Proved: The fetch helper preserves exit-time-related fields from `/api/strategy-trades`, and the rendered table headers/cells include `EXIT TIME` using the shared formatter.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `npm run build` and `node .\node_modules\vite\bin\vite.js build` in `TradeApps\breakout\piphunter\landing_page`
  - Objective-Proved: Build validation was attempted and the remaining blocker is environment-specific dependency resolution rather than the functional code path patched here.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Pending user verification in the FXPilot drilldown UI at `http://172.22.108.121:3001/`
  - Objective-Proved: Confirms the Exit Time column is visible in the live drilldown modal, aligned with the table, and displays `-` for open trades.
  - Status: planned

## Implementation Log
- 2026-03-19 00:00: Read `skills/workstream-task-lifecycle/ SKILL.md` and this task file before making changes.
- 2026-03-19 00:00: Inspected `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` and found the drilldown uses `TradeTable` plus an inline `fetchStrategyTrades()` helper.
- 2026-03-19 00:00: Confirmed `TradeApps/breakout/piphunter/landing_page/server.py` route `/api/strategy-trades` already returns `exit_time` for closed trades and `None` for open trades.
- 2026-03-19 00:00: Patched `forex-dashboard_1.jsx` to preserve full strategy-trade fields from the API, add a reusable `formatTradeDateTime()` helper, rename the drilldown time headers to `ENTRY TIME` and `EXIT TIME`, and render exit time with a dash fallback.
- 2026-03-19 00:00: Attempted local frontend build validation; build is currently blocked by missing local Vite/Rollup runtime dependencies.
- 2026-03-19 00:00: Recorded user-visible verification as still required before this task can be closed.

## Changes Made
- Updated `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
- In `fetchStrategyTrades()`:
  - Preserved `entry_price`, `exit_price`, `exit_reason`, `bias_at_open`, and `bias_latest` from `/api/strategy-trades`
- Added `formatTradeDateTime(timestamp)`:
  - Returns `-` for null/invalid timestamps
  - Formats timestamps with `toLocaleString("en-GB", { day, month, hour, minute })`
- Updated `TradeTable` drilldown headers:
  - `OPENED` -> `ENTRY TIME`
  - `EXIT` -> `EXIT TIME`
- Updated `TradeTable` rows:
  - Entry time now uses `formatTradeDateTime(t.openTime)`
  - Exit time now uses `formatTradeDateTime(t.closeTime)`

## Validation
- `Get-Content -Path 'TradeApps\breakout\piphunter\landing_page\server.py' | Select-Object -Skip 100 -First 160`
  - Result: confirmed `/api/strategy-trades` returns `exit_time` and `None` for open trades.
- `Get-Content -Path 'TradeApps\breakout\piphunter\landing_page\forex-dashboard_1.jsx' | Select-Object -First 40`
  - Result: confirmed the inline fetch helper preserves `exitTime`, `exitReason`, pricing, and bias fields.
- `Get-Content -Path 'TradeApps\breakout\piphunter\landing_page\forex-dashboard_1.jsx' | Select-Object -Skip 480 -First 180`
  - Result: confirmed `ENTRY TIME` and `EXIT TIME` headers and `formatTradeDateTime()` usage in trade rows.
- `npm run build` in `TradeApps\breakout\piphunter\landing_page`
  - Result: failed with `'vite' is not recognized as an internal or external command`.
- `node .\node_modules\vite\bin\vite.js build` in `TradeApps\breakout\piphunter\landing_page`
  - Result: failed with missing optional dependency `@rollup/rollup-win32-x64-msvc`.
- User verification request
  - Pending: verify in the FXPilot drilldown UI that:
    - Exit Time column is visible
    - Times are readable and match entry-time formatting
    - Open trades display `-`
    - Column alignment is acceptable

## Risks/Notes
- Local build validation is incomplete because the landing-page workspace has a broken frontend toolchain dependency state (`vite` resolution and missing Rollup optional package).
- This task changes user-visible drilldown output, so manual verification is still required before moving the file to `workstream/300_complete`.
- No backend change was required because `/api/strategy-trades` already exposes `exit_time`.

## Completion Status
**Awaiting user verification** - 2026-03-19 00:00

## Execution Evidence
- Agent lane: claude
- Command: `cmd /c echo claude processing 20260302_035617_claude_pipHunter_drilldown_exit_time_column.md`
- Return code: 0
- Stdout:
```text
claude processing 20260302_035617_claude_pipHunter_drilldown_exit_time_column.md
```

## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
