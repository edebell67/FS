# Breakout Optimize Weekly Performance Auto Refresh To Update Data Only

- Status: Complete
- Created: 2026-04-09 21:00:23
- Project: breakout
- Owner: Codex

## Request

Modify `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html` so auto-refresh updates only the underlying data/state instead of refreshing the whole page.

## Scope

- Keep the existing auto-refresh control behavior.
- Ensure auto-refresh uses incremental data refresh only.
- Avoid full browser page reloads.
- Preserve current filters, selected week, sort state, and UI control state during refresh.

## Acceptance Criteria

1. Auto-refresh does not perform `window.location.reload()` or equivalent full-page reload behavior.
2. Only data-bound content updates during refresh.
3. Existing page state remains intact while auto-refresh is running.
4. No duplicate refresh timers or redundant render loops are introduced.

## Notes

- Prefer reusing the existing `fetchData()` and render pipeline.
- If any current code path is still doing a full reload, replace it with data-only refresh behavior.

## Progress Log

- 2026-04-10 00:10:12: Verified the page was not doing a browser reload, but auto-refresh still felt heavy because it showed the loading overlay and rebuilt the full table each cycle.
- 2026-04-10 00:10:12: Updated auto-refresh calls to run in silent mode with `showOverlay: false`.
- 2026-04-10 00:10:12: Added in-place row patching for auto-refresh so the table structure is reused when the date columns are unchanged.

## Validation

- 2026-04-10 00:10:45: Confirmed there is no `window.location.reload`, `window.location`, or meta refresh path in `weekly_performance.html`.
- 2026-04-10 00:10:45: Confirmed auto-refresh now calls `fetchData({ useCache: false, refreshActivations: true, showOverlay: false, patchRowsOnly: true })`.
- 2026-04-10 00:10:45: Confirmed `renderTable(options)` supports `patchRowsOnly` and only falls back to a full table rebuild when the date-column structure changes.

## Outcome

`weekly_performance.html` now performs quiet data-only auto-refresh in practice: no full page reload, no loading overlay during timer refresh, and in-place row/cell updates when the weekly table structure has not changed. Manual refresh/navigation paths still retain the normal overlay behavior.
