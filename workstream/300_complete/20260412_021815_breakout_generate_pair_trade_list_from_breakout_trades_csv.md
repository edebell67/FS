# Task: Generate Pair-Trade List From breakout_trades CSV

Source: User request on 2026-04-12 to provide the actual trades from the supplied CSV that deliver the positive return.

Task Type: analysis

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
From `C:\Users\edebe\Downloads\breakout_trades__2026-04-11.csv`, generate the actual trade list for the profitable long/short strategy spread and report the resulting realized return.

## Validation Plan
- Select the best closed-trade pair from the prior analysis.
- Build the executable trade list by keeping the long-leg trades as-is and inverting the short-leg trades.
- Export the trade list in timestamp order.
- Verify the summed contribution matches the spread return.

## Execution Log

### 2026-04-12 02:18
- Chose the best realized pair from the previous CSV analysis:
  - long `breakout_R_2_tp5.0_sl3.0`
  - short `breakout_Rev_2_tp5.0_sl3.0`
- Restricted to `Status = CLOSED` so the output reflects realized returns only.

### 2026-04-12 02:20
- Generated a transformed pair-trade CSV where:
  - long-leg trades are copied as-is
  - short-leg trades are inverted (`LONG -> SHORT`, `SHORT -> LONG`)
  - `Contribution = Result` for long-leg trades
  - `Contribution = -Result` for inverted short-leg trades
- Sorted all resulting trades by timestamp and added running cumulative contribution.

## Validation Results

### Output File
- `C:\Users\edebe\eds\misc\pair_trades_long_breakout_R_2_short_breakout_Rev_2_2026-04-11.csv`

### Verification
- Output trade count: `51`
- Total realized pair return: `2327.42`
- This matches the previously computed closed-only spread return for:
  - long `breakout_R_2_tp5.0_sl3.0`
  - short `breakout_Rev_2_tp5.0_sl3.0`

### First Rows
- `00:01:16 | LONG_STRATEGY | breakout_R_2_tp5.0_sl3.0 | LONG | -135.00 | cum -135.00`
- `01:15:14 | LONG_STRATEGY | breakout_R_2_tp5.0_sl3.0 | LONG | -55.00 | cum -190.00`
- `01:15:14 | SHORT_STRATEGY_INVERTED | breakout_Rev_2_tp5.0_sl3.0 | LONG | +135.00 | cum -55.00`
- `01:52:19 | LONG_STRATEGY | breakout_R_2_tp5.0_sl3.0 | LONG | -135.00 | cum -190.00`
- `02:18:16 | SHORT_STRATEGY_INVERTED | breakout_Rev_2_tp5.0_sl3.0 | SHORT | +111.84 | cum -78.16`

## Notes

- This output is a transformed analytical trade list, not a broker-ready order file.
- It represents the strategy spread implementation directly from the supplied CSV:
  - copy `breakout_R_2_tp5.0_sl3.0`
  - invert `breakout_Rev_2_tp5.0_sl3.0`
