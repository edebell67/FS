# Preserve Drilldown State on Auto-Refresh

Source: PipHunter Dashboard - FXPilot Landing Page

## Task Summary
Preserve the selected strategy drilldown during the 30-second dashboard auto-refresh so users do not have to reopen the drilldown during analysis. Date changes must still reset the drilldown.

## Context
- Dashboard URL: `http://172.22.108.121:3001/`
- Source file: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
- Auto-refresh interval: `30000` ms

## Dependency
Dependency: None

## Original Task Intake
- User expands a strategy to view trade drilldown.
- Auto-refresh triggers after 30 seconds.
- Drilldown collapses because `selectedId` and `strategyTrades` were reset inside `loadData`.
- Expected behavior: preserve drilldown on refresh, but still reset on date change.

## Plan
- [x] 1. Separate date-change resets from interval refreshes inside the dashboard data loader.
  - [x] Test: Inspect the updated `loadData` flow in `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` and confirm `setSelectedId(null)` only runs when the selected date changes or the selected strategy disappears from refreshed results.
  - [x] Evidence: `previousSelectedDateRef` and `selectedIdRef` were added, `dateChanged` now gates the reset path, and missing selected strategies are cleared in the refreshed strategy list diff.
- [x] 2. Re-trigger selected strategy trade loading after each successful main refresh without collapsing the drilldown.
  - [x] Test: Inspect the updated drilldown fetch effect and confirm it depends on a refresh signal produced by the main data load rather than on clearing selection state.
  - [x] Evidence: `strategyTradesRefreshKey` increments after successful main refresh and the strategy-trade effect now depends on `[selectedId, selectedDate, strategyTradesRefreshKey, strategies]`.
- [x] 3. Run technical validation available in the current environment and record the user verification request required for this UI change.
  - [x] Test: Run `@'...@ | node -` with `@babel/parser` against `forex-dashboard_1.jsx` and confirm parse success; run `npm run build` and `node .\node_modules\vite\bin\vite.js build` to capture the current environment limitation.
  - [x] Evidence: Babel parser returned `Babel parse OK`; Vite and Rollup validation are blocked because the checked-in `node_modules` tree contains Linux-native packages on this Windows host.

## Evidence
Objective-Delivery-Coverage: 85%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `git -C TradeApps diff -- breakout/piphunter/landing_page/forex-dashboard_1.jsx`
  - Objective-Proved: The dashboard now preserves drilldown state across auto-refresh, only resets on date change, and refreshes selected strategy trades after the main data load.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
  - Objective-Proved: The modified JSX parses successfully in the current environment.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `http://172.22.108.121:3001/`
  - Objective-Proved: User can verify that expanded drilldown stays open after the next 30-second refresh and still resets after changing the date.
  - Status: planned

## Implementation Log
- 2026-03-19 16:31: Loaded `skills/workstream-task-lifecycle/SKILL.md` and this task file, then reviewed the dashboard component and current worktree state.
- 2026-03-19 16:34: Updated `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` to stop clearing selection on every refresh, track the selected strategy in a ref, and create a refresh key for selected strategy trade reloads.
- 2026-03-19 16:35: Added a guard to clear the drilldown only if the selected strategy disappears from refreshed strategy data.
- 2026-03-19 16:35: Attempted `npm run build`; this failed because the local `vite` command is not executable in the current environment.
- 2026-03-19 16:35: Attempted `node .\node_modules\vite\bin\vite.js build`; this failed because Rollup's Windows native optional dependency is missing from the current `node_modules`.
- 2026-03-19 16:36: Ran Babel parser validation for `forex-dashboard_1.jsx`; parsing succeeded with `Babel parse OK`.
- 2026-03-19 16:36: Recorded a required user verification request for the UI behavior change and left the task in progress pending that confirmation.

## Changes Made
- Added `previousSelectedDateRef` in `forex-dashboard_1.jsx` so the dashboard only resets `selectedId` and `strategyTrades` when `selectedDate` changes.
- Added `selectedIdRef` so the refresh cycle can preserve or clear the current drilldown based on refreshed strategy availability without relying on stale interval-closure state.
- Added `strategyTradesRefreshKey` so the selected strategy's trade drilldown re-fetches after each successful main dashboard refresh while keeping the drilldown open.
- Updated the selected strategy trade effect dependencies to include the refresh key and live strategy data.

## Validation
- `npm run build`
  - Result: failed
  - Summary: `'vite' is not recognized as an internal or external command, operable program or batch file.`
- `node .\node_modules\vite\bin\vite.js build`
  - Result: failed
  - Summary: `Cannot find module @rollup/rollup-win32-x64-msvc`; the current `node_modules` tree contains incompatible optional native packages for this Windows environment.
- `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
  - Result: passed
  - Summary: `Babel parse OK`
- User verification requested on 2026-03-19 16:36 UTC:
  - Expand a strategy drilldown on the dashboard.
  - Wait for the 30-second auto-refresh.
  - Confirm the same drilldown remains open and its trade data refreshes.
  - Change the selected date and confirm the drilldown resets.

## Risks/Notes
- Full production build validation is currently blocked by cross-platform dependency drift in `TradeApps/breakout/piphunter/landing_page/node_modules`.
- This task changes user-visible behavior, so completion requires user verification per the lifecycle gate.
- If the refreshed strategy list no longer contains the selected strategy, the drilldown still closes intentionally.

## Completion Status
Awaiting user verification - 2026-03-19 16:36:51 +00:00

## Historical Execution Evidence
- Agent lane: claude
- Command: `cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`
- Return code: `0`
- Stdout: `claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`

## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
