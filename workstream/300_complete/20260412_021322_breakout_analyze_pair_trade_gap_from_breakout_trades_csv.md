# Task: Analyze Pair-Trade Gap From breakout_trades CSV

Source: User request on 2026-04-12 to use `C:\Users\edebe\Downloads\breakout_trades__2026-04-11.csv` to determine how going long one strategy and short another could profit from the gap.

Task Type: analysis

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
Use the provided CSV to compute relative strategy pair results for the four BTC breakout variants and identify whether inverting one strategy against another would have produced positive returns.

## Validation Plan
- Load and inspect the CSV structure.
- Compute standalone strategy totals from the CSV.
- Compute long/short pair totals by inverting the short-leg strategy.
- Report best positive combinations and any caveats in interpretation.

## Execution Log

### 2026-04-12 02:13
- Loaded `C:\Users\edebe\Downloads\breakout_trades__2026-04-11.csv`.
- Confirmed the file contains four BTC strategy variants:
  - `breakout_2_tp5.0_sl3.0`
  - `breakout_R_2_tp5.0_sl3.0`
  - `breakout_R_Rev_2_tp5.0_sl3.0`
  - `breakout_Rev_2_tp5.0_sl3.0`

### 2026-04-12 02:16
- Computed standalone totals using the `Result` column.
- Computed both:
  - all rows including currently open marked-to-market trades
  - closed-only rows

### 2026-04-12 02:18
- Computed pair-trade totals for every ordered long/short combination using:
  - `pair_pnl = pnl(long_leg_strategy) - pnl(short_leg_strategy_original)`
- This models copying the long-leg strategy as-is and inverting every trade from the short-leg strategy with equal notional sizing.

## Validation Results

### CSV Shape
- Source file:
  - `C:\Users\edebe\Downloads\breakout_trades__2026-04-11.csv`
- Columns observed:
  - `Time, Model, Product, Type, Signal, Result, Alt Net, Total, Exit, Status, Live`

### Standalone Strategy Totals

Using `Result`:

- `breakout_2_tp5.0_sl3.0`
  - all rows: 22 trades, `-2210.48`
  - closed only: 21 trades, `-2115.00`

- `breakout_R_2_tp5.0_sl3.0`
  - all rows: 17 trades, `-1605.05`
  - closed only: 16 trades, `-1520.00`

- `breakout_R_Rev_2_tp5.0_sl3.0`
  - all rows: 37 trades, `-3605.12`
  - closed only: 37 trades, `-3605.12`

- `breakout_Rev_2_tp5.0_sl3.0`
  - all rows: 35 trades, `-3847.42`
  - closed only: 35 trades, `-3847.42`

### Pair Results

Closed-only pair P&L:

- Long `breakout_R_2_tp5.0_sl3.0`, short `breakout_Rev_2_tp5.0_sl3.0`: `+2327.42`
- Long `breakout_R_2_tp5.0_sl3.0`, short `breakout_R_Rev_2_tp5.0_sl3.0`: `+2085.12`
- Long `breakout_2_tp5.0_sl3.0`, short `breakout_Rev_2_tp5.0_sl3.0`: `+1732.42`
- Long `breakout_2_tp5.0_sl3.0`, short `breakout_R_Rev_2_tp5.0_sl3.0`: `+1490.12`
- Long `breakout_R_Rev_2_tp5.0_sl3.0`, short `breakout_Rev_2_tp5.0_sl3.0`: `+242.30`
- Long `breakout_R_2_tp5.0_sl3.0`, short `breakout_2_tp5.0_sl3.0`: `+595.00`

All-rows pair P&L including the two still-open marked trades:

- Long `breakout_R_2_tp5.0_sl3.0`, short `breakout_Rev_2_tp5.0_sl3.0`: `+2242.38`
- Long `breakout_R_2_tp5.0_sl3.0`, short `breakout_R_Rev_2_tp5.0_sl3.0`: `+2000.07`
- Long `breakout_2_tp5.0_sl3.0`, short `breakout_Rev_2_tp5.0_sl3.0`: `+1636.94`
- Long `breakout_2_tp5.0_sl3.0`, short `breakout_R_Rev_2_tp5.0_sl3.0`: `+1394.64`
- Long `breakout_R_Rev_2_tp5.0_sl3.0`, short `breakout_Rev_2_tp5.0_sl3.0`: `+242.30`
- Long `breakout_R_2_tp5.0_sl3.0`, short `breakout_2_tp5.0_sl3.0`: `+605.43`

## Interpretation

- The best performer in this sample is `breakout_R_2_tp5.0_sl3.0`.
- The worst performer is `breakout_Rev_2_tp5.0_sl3.0`.
- So the strongest simple spread in this file is:
  - long `breakout_R_2_tp5.0_sl3.0`
  - short `breakout_Rev_2_tp5.0_sl3.0`

On this CSV, that spread is positive because the long leg loses materially less than the shorted leg loses in its original direction.

## Caveats

- This is a strategy-inversion spread model, not a synchronous hedge model.
- The calculation assumes equal notional sizing and independent execution of all trades from both strategies.
- Trade counts differ across models, so the spread includes timing and frequency differences as well as signal quality differences.
- Because all legs are on BTC, real execution would still need portfolio-level exposure controls to avoid unintended net directional BTC risk when the legs are not naturally offsetting at the same time.
