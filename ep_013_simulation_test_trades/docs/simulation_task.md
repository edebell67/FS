# Task: [EP_013] GBP/USD Breakout Strategy Simulation

## Status
- **Epic:** EP_013 - Simulation Test Trades
- **Epic Folder:** `C:\Users\edebe\eds\epics\ep_013_simulation_test_trades\`
- **Status:** In Progress
- **Started:** 2026-04-20 14:00:00
- **Version:** V20260420_1445

## Objective
Simulate a breakout strategy against 2 days of intraday GBP/USD price data to evaluate performance and its reverse (Alt Net) performance including commissions.

## Artifacts Location (Epic 013)
- **Root:** `C:\Users\edebe\eds\epics\ep_013_simulation_test_trades\`
- **Scripts:** `..\scripts\`
- **Data:** `..\data\`
- **Docs:** `..\docs\`

## Trading Parameters
- **Pair:** GBP/USD
- **Trade Size:** 100,000 units (1 standard lot)
- **Pip Value:** $10.00
- **Commission:** $5 Entry / $5 Exit ($10 total per round trip)
- **Take Profit (TP):** 30 pips ($300 gross)
- **Stop Loss (SL):** 10 pips ($100 gross)
- **Price Window:** Last 5 distinct price points (Breakout signal)

## Simulation Logic
- **Entry:** Trigger BUY if price > MAX of last 5 distinct prices. Trigger SELL if price < MIN of last 5 distinct prices.
- **Net Return:** (Gross Pips - 1.0 Pip Commission) * $10.
- **Alt Net Return:** Reverse position of the strategy, also subtracting 1.0 Pip Commission.
- **Cumulative Columns:** `cum_net` and `cum_alt_net` tracking running totals.

## Progress Log
### 2026-04-20 14:05 - Initial Simulation Run
- **Total Trades:** 493
- **Strategy Net P&L:** -$630.00
- **Win Rate:** 27.2%
- **Observation:** High noise in the 5-point window results in frequent SL hits.

### 2026-04-20 14:15 - Alt Net Implementation (with commissions)
- **Reverse (Alt) Net P&L:** -$9,230.00
- **Observation:** Reverse trade performs significantly worse due to the drag of commissions on 493 trades and the fact that 30-pip moves occur often enough to hurt the reverse position more than the 10-pip gains help it.

### 2026-04-20 14:30 - Added Cumulative Tracking
- Modified `_tmp_sim_test.py` to include `Cum Net $` and `Cum Alt Net $`.
- Verified first 20 trades match expected math.

## Next Steps
- [ ] Run full 2-day simulation with cumulative tracking.
- [ ] Test with larger window sizes (10, 20, 50) to filter noise.
- [ ] Evaluate performance without commission to see raw edge.
