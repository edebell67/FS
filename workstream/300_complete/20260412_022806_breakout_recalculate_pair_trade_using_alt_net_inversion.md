# Task: Recalculate Pair Trade Using Alt Net Inversion

Source: User correction on 2026-04-12 that pair-trade inversion must use `Alt Net` from `C:\Users\edebe\Downloads\breakout_trades__2026-04-11.csv` because it already includes spread and commission.

Task Type: analysis

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
Recompute the strategy spread analysis and transformed trade list using `Result` for the long leg and `Alt Net` for the inverted short leg.

## Validation Plan
- Recalculate pair totals on closed trades only.
- Identify the best pair under the corrected inversion rule.
- Regenerate the transformed trade file with `Alt Net`-based contributions.
- Verify totals match the corrected pair return.

## Execution Log

### 2026-04-12 02:29
- Recomputed standalone closed-trade totals from `C:\Users\edebe\Downloads\breakout_trades__2026-04-11.csv`.
- Applied corrected spread rule:
  - long-leg contribution uses `Result`
  - inverted short-leg contribution uses `Alt Net`

### 2026-04-12 02:30
- Computed every ordered long/short pair using:
  - `pair_pnl = sum(Result for long model) + sum(Alt Net for short model)`

## Validation Results

### Standalone Closed Totals
- `breakout_2_tp5.0_sl3.0`
  - `Result = -2115.00`
  - `Alt Net = -2715.00`

- `breakout_R_2_tp5.0_sl3.0`
  - `Result = -1520.00`
  - `Alt Net = -2160.00`

- `breakout_R_Rev_2_tp5.0_sl3.0`
  - `Result = -3605.12`
  - `Alt Net = -4904.88`

- `breakout_Rev_2_tp5.0_sl3.0`
  - `Result = -3847.42`
  - `Alt Net = -4202.58`

### Corrected Pair Results

- Long `breakout_2_tp5.0_sl3.0`, short `breakout_R_2_tp5.0_sl3.0`: `-4275.00`
- Long `breakout_2_tp5.0_sl3.0`, short `breakout_R_Rev_2_tp5.0_sl3.0`: `-7019.88`
- Long `breakout_2_tp5.0_sl3.0`, short `breakout_Rev_2_tp5.0_sl3.0`: `-6317.58`
- Long `breakout_R_2_tp5.0_sl3.0`, short `breakout_2_tp5.0_sl3.0`: `-4235.00`
- Long `breakout_R_2_tp5.0_sl3.0`, short `breakout_R_Rev_2_tp5.0_sl3.0`: `-6424.88`
- Long `breakout_R_2_tp5.0_sl3.0`, short `breakout_Rev_2_tp5.0_sl3.0`: `-5722.58`
- Long `breakout_R_Rev_2_tp5.0_sl3.0`, short `breakout_2_tp5.0_sl3.0`: `-6320.12`
- Long `breakout_R_Rev_2_tp5.0_sl3.0`, short `breakout_R_2_tp5.0_sl3.0`: `-5765.12`
- Long `breakout_R_Rev_2_tp5.0_sl3.0`, short `breakout_Rev_2_tp5.0_sl3.0`: `-7807.70`
- Long `breakout_Rev_2_tp5.0_sl3.0`, short `breakout_2_tp5.0_sl3.0`: `-6562.42`
- Long `breakout_Rev_2_tp5.0_sl3.0`, short `breakout_R_2_tp5.0_sl3.0`: `-6007.42`
- Long `breakout_Rev_2_tp5.0_sl3.0`, short `breakout_R_Rev_2_tp5.0_sl3.0`: `-8752.30`

### Best Corrected Pair
- Best, but still negative:
  - long `breakout_R_2_tp5.0_sl3.0`
  - short `breakout_2_tp5.0_sl3.0`
  - return: `-4235.00`

## Conclusion

- Under the corrected executable inversion rule using `Alt Net`, no pair from this CSV produces a positive return.
- The earlier positive result was invalid because it inverted `Result` arithmetically and ignored the spread/commission already represented by `Alt Net`.
