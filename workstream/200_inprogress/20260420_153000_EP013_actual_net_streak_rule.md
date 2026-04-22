# Task: [EP_013] Anticipatory Switching Rule (3 Consecutive Losses) Implementation

## Status
- **Epic:** EP_013 - Simulation Test Trades
- **Epic Folder:** `C:\Users\edebe\eds\epics\ep_013_simulation_test_trades\`
- **Status:** In Progress
- **Started:** 2026-04-20 15:30:00
- **Version:** V20260420_1530

## Objective
Implement an anticipatory switching rule in the GBP/USD simulation: If the active strategy loses 3 times in a row, switch to the other strategy (`net` <-> `alt`).

## Description
To avoid entering a losing streak just as a background strategy becomes profitable (the "catch-22" of the previous rule), this rule switches the active trade allocation based on recent performance history rather than absolute profitability.

## Artifacts Location (Epic 013)
- **Root:** `C:\Users\edebe\eds\epics\ep_013_simulation_test_trades\`
- **Scripts:** `..\scripts\gbp_breakout_sim.py`
- **Data:** `..\data\intraday_gbp_prices_2_days.csv`

## Checklist
- [ ] Implement state tracking for `current_active_strategy` and `consecutive_losses`.
- [ ] Implement toggle logic after 3 consecutive losses.
- [ ] Update simulation loop to use the state-based allocation.
- [ ] Update simulation print output formatting.
- [ ] Update `Constants.py` to `V20260420_1530`.

## Progress Log
### 2026-04-20 15:35 - Task Created
- New anticipatory switching plan approved.
- Linked to Epic 013.
