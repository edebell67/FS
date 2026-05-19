# Task: Test Invert Losing Strategy Hypothesis For 2026-04-10 NQ tp20 sl50

Source: User request on 2026-04-12 to test the hypothesis of inverting the losing strategy using `C:\Users\edebe\Downloads\breakout_trades__2026-04-10.csv`.

Task Type: analysis

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
Use the supplied `2026-04-10` breakout trades CSV to test whether inverting the losing `tp20/sl50` strategy yields positive returns for the two NQ strategies shown in the chart.

## Validation Plan
- Isolate the two strategies from the CSV.
- Compute closed-trade `Result` and `Alt Net` totals.
- Compute corrected pair outcome using `Result` for the long leg and `Alt Net` for the inverted leg.
- Report whether the hypothesis holds and provide the executable interpretation.

## Results

Closed trades only from `C:\Users\edebe\Downloads\breakout_trades__2026-04-10.csv`:

- `breakout_2_tp20.0_sl50.0`
  - count: `31`
  - `Result`: `-3755.00`
  - `Alt Net`: `2825.00`
  - adjusted zero-cost `Result`: `-655.00`
  - adjusted zero-cost `Alt Net`: `5925.00`

- `breakout_R_2_tp20.0_sl50.0`
  - count: `11`
  - `Result`: `2145.00`
  - `Alt Net`: `-2475.00`
  - adjusted zero-cost `Result`: `3245.00`
  - adjusted zero-cost `Alt Net`: `-1375.00`

## Hypothesis Test

Losing strategy in the chart:
- `breakout_2_tp20.0_sl50.0`

Winning strategy in the chart:
- `breakout_R_2_tp20.0_sl50.0`

Correct executable interpretation:
- trade the winner normally using `Result`
- invert the loser using `Alt Net`

### Pair Outcome

Raw:
- `2145.00 + 2825.00 = 4970.00`

Zero-cost adjusted:
- `3245.00 + 5925.00 = 9170.00`

## Conclusion

For this `2026-04-10` NQ `tp20/sl50` sample, the hypothesis works.

- The loser is genuinely invertible here:
  - `breakout_2_tp20.0_sl50.0` has `Result = -3755.00`
  - but `Alt Net = 2825.00`

- The winner is also positive:
  - `breakout_R_2_tp20.0_sl50.0` has `Result = 2145.00`

- So:
  - inverting the loser alone would have been profitable
  - combining long winner + inverted loser would have been strongly profitable
