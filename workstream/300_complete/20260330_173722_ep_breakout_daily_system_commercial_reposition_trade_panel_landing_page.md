# Task Lifecycle

## Task
Implement the TradePanel landing page in `ep_007_breakout_daily_system_commercial_reposition` so the frontend matches the closed-trades leaderboard definition from the PRD and dev task documents dated 2026-03-30.

## Scope
- Replace the current broad commercial landing page with a minimal ranked board surface.
- Use closed-trade leaderboard messaging only.
- Support source-aware header copy for `twitter` and `email`.
- Show last update, last change, leaderboard rows, and CTA.
- Keep the implementation within the existing Vite React frontend.

## References
- `C:\Users\edebe\eds\workstream\000_epic\20260330_163957_trade_panel.md`
- `C:\Users\edebe\eds\workstream\100_backlog\20260330_164250_TradePanel — Dev Task.md`

## Status Log
- 2026-03-30 17:37:22: Task file created in `100_todo`.
- 2026-03-30 17:38:10: Task moved to `200_inprogress` and project structure reviewed.
- 2026-03-30 17:44:00: Replaced the prior commercial landing page with a closed-trades leaderboard page in the Vite frontend.
- 2026-03-30 17:44:00: Extended the snapshot generator to produce a combined top-20 board, movement deltas, `last_update`, `last_change`, and a pollable public JSON snapshot.

## Validation
- 2026-03-30 17:44:00: `node C:\Users\edebe\eds\ep_007_breakout_daily_system_commercial_reposition\solution\scripts\build-market-snapshot.mjs` succeeded.
- 2026-03-30 17:44:00: `npm run build` succeeded in `C:\Users\edebe\eds\ep_007_breakout_daily_system_commercial_reposition\solution\frontend`.
