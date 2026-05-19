# Task: Periodic Market Update Generator (20260224_134000)

## Task Summary
Implement a script or endpoint process to generate the `_market_update.json` file on a recurring interval. Use the `strategy-boxing-battle-pulse` and `strategy-battle-punchy-updates` skill templates to generate a boxing ring-style live narrative.

## Context
- The Breakout UI has a "PERIODIC MARKET UPDATE" panel.
- The UI relies on `_market_update.json` containing specific keys: totals, windows (last 30m, prev 30m), headline, narrative, etc.
- Currently, this reads "Waiting for periodic generation".

## Sub-tasks
- [x] Read trades data (either via Postgres `vw_trades_all` or local files).
- [x] Calculate block metrics (Total Net, Last 30m, Prev 30m, Open Pressure, imbalance).
- [x] Determine the "Likely Winner" and Strategy Dominators.
- [x] Formulate narrative exactly matching the "Boxing Battle Pulse" format.
- [x] Serialize and write the output to `fs/json/live/YYYY-MM-DD/_market_update.json` and append to `_market_update_history.json`.
- [x] Hook into the API application's background processing thread (or an external runner script) to run every 5 minutes.
- [x] Increment `Constants.py` to `V20260224_1340` as requested.
- [x] Write the completed status here when done.

## Associated Plan
`C:\Users\edebe\eds\plans\20260224_1340_V20260224_1340_periodic_market_update.md`

## Status
COMPLETE
