# Breakout Add Auto Refresh Toggle To Weekly Performance Html

- Status: Todo
- Created: 2026-04-09 16:36:50
- Project: breakout
- Owner: Codex

## Request

Apply auto-refresh behavior to `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`.

## Scope

- Add an `Auto Refresh` checkbox or toggle to the weekly performance page UI.
- When enabled, the page should automatically refresh its data every few seconds.
- When disabled, auto-refresh should stop.
- Keep manual refresh behavior intact if one already exists.

## Acceptance Criteria

1. `weekly_performance.html` includes a visible auto-refresh control.
2. Turning the control on starts periodic data refresh.
3. Turning the control off stops periodic refresh.
4. Refresh cadence is every few seconds and does not require a full page reload unless the existing page architecture requires it.
5. Any interval/timer is cleaned up properly to avoid duplicate refresh loops.

## Notes

- Prefer refreshing the page data/function already used by the screen instead of forcing a full browser reload.
- Final implementation should document the exact refresh interval chosen.

## Progress Log

- 2026-04-09 20:58:45: Added an `Auto Refresh` toggle UI to `weekly_performance.html`.
- 2026-04-09 20:58:45: Implemented a single managed refresh loop that calls the existing `fetchData()` path with cache bypass enabled.
- 2026-04-09 20:58:45: Persisted the toggle state in `localStorage` so the page restores the user preference on reload.

## Validation

- 2026-04-09 20:58:56: Verified `weekly_performance.html` contains the `Auto Refresh` toggle control and managed timer functions.
- 2026-04-09 20:58:56: Confirmed refresh interval is set to 5 seconds via `AUTO_REFRESH_INTERVAL_MS = 5000`.

## Outcome

`weekly_performance.html` now includes an `Auto Refresh` toggle. When enabled, it refreshes weekly performance data every 5 seconds using the existing page data fetch logic without requiring a full browser reload. When disabled, the interval is cleared so duplicate loops do not accumulate.
