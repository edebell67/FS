# Task: [EP_013] Dynamic Rule Strategy (Actual Net) Implementation

## Status
- **Epic:** EP_013 - Simulation Test Trades
- **Epic Folder:** `C:\Users\edebe\eds\epics\ep_013_simulation_test_trades\`
- **Status:** In Progress
- **Started:** 2026-04-20 15:00:00
- **Version:** V20260420_1500

## Objective
Enhance the GBP/USD simulation to support a dynamic choice between the breakout strategy and its reverse for every trade, tracking the "actual" performance.

## Description
The user wants to experiment with different rules to decide whether to take the primary strategy signal (`net`) or the reverse (`alt_net`) for each individual trade. This task implements the necessary columns and a placeholder rule function for these experiments.

## Artifacts Location (Epic 013)
- **Root:** `C:\Users\edebe\eds\epics\ep_013_simulation_test_trades\`
- **Scripts:** `..\scripts\gbp_breakout_sim.py`
- **Data:** `..\data\intraday_gbp_prices_2_days.csv`

## Checklist
- [ ] Implement `evaluate_trade_rule()` placeholder in `gbp_breakout_sim.py`.
- [ ] Add `actual_net` column logic.
- [ ] Add `cum_actual_net` column logic.
- [ ] Update simulation print output formatting.
- [ ] Update `Constants.py` to `V20260420_1500`.

## Progress Log
### 2026-04-20 15:05 - Task Created
- Initial plan approved and workstream started.
- Linked to Epic 013.
