# Task: Recalculate Pair Analysis With Zero Adhoc Cost

Source: User request on 2026-04-12 to remove the built-in `-100` trade cost from the CSV and recalculate.

Task Type: analysis

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
Recompute strategy and pair-trade results from `C:\Users\edebe\Downloads\breakout_trades__2026-04-11.csv` after neutralizing the embedded `-100` cost from both `Result` and `Alt Net`.

## Results

Adjusted closed-trade standalone totals with cost set to `0`:

- `breakout_2_tp5.0_sl3.0`
  - adjusted `Result`: `-15.00`
  - adjusted `Alt Net`: `-615.00`

- `breakout_R_2_tp5.0_sl3.0`
  - adjusted `Result`: `80.00`
  - adjusted `Alt Net`: `-560.00`

- `breakout_R_Rev_2_tp5.0_sl3.0`
  - adjusted `Result`: `94.88`
  - adjusted `Alt Net`: `-1204.88`

- `breakout_Rev_2_tp5.0_sl3.0`
  - adjusted `Result`: `-347.42`
  - adjusted `Alt Net`: `-702.58`

Corrected pair formula remains:

- `pair_pnl = adjusted Result(long leg) + adjusted Alt Net(short leg)`

Adjusted pair results:

- long `breakout_2_tp5.0_sl3.0`, short `breakout_R_2_tp5.0_sl3.0` = `-575.00`
- long `breakout_2_tp5.0_sl3.0`, short `breakout_R_Rev_2_tp5.0_sl3.0` = `-1219.88`
- long `breakout_2_tp5.0_sl3.0`, short `breakout_Rev_2_tp5.0_sl3.0` = `-717.58`
- long `breakout_R_2_tp5.0_sl3.0`, short `breakout_2_tp5.0_sl3.0` = `-535.00`
- long `breakout_R_2_tp5.0_sl3.0`, short `breakout_R_Rev_2_tp5.0_sl3.0` = `-1124.88`
- long `breakout_R_2_tp5.0_sl3.0`, short `breakout_Rev_2_tp5.0_sl3.0` = `-622.58`
- long `breakout_R_Rev_2_tp5.0_sl3.0`, short `breakout_2_tp5.0_sl3.0` = `-520.12`
- long `breakout_R_Rev_2_tp5.0_sl3.0`, short `breakout_R_2_tp5.0_sl3.0` = `-465.12`
- long `breakout_R_Rev_2_tp5.0_sl3.0`, short `breakout_Rev_2_tp5.0_sl3.0` = `-607.70`
- long `breakout_Rev_2_tp5.0_sl3.0`, short `breakout_2_tp5.0_sl3.0` = `-962.42`
- long `breakout_Rev_2_tp5.0_sl3.0`, short `breakout_R_2_tp5.0_sl3.0` = `-907.42`
- long `breakout_Rev_2_tp5.0_sl3.0`, short `breakout_R_Rev_2_tp5.0_sl3.0` = `-1552.30`

Best adjusted pair, still negative:

- long `breakout_R_Rev_2_tp5.0_sl3.0`
- short `breakout_R_2_tp5.0_sl3.0`
- return `-465.12`

## Conclusion

Removing the built-in `-100` cost improves the trade economics substantially, but there is still no positive long/short pair on this CSV when the short leg is priced correctly via `Alt Net`.
