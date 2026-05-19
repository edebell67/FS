# Task: Verify Energy Trade Net Return Formula

## Source
- User Directive: 2026-03-26

## Task Summary
Verify at the individual trade level that `net_return` in `energy` `*cld.json` records is correctly calculated from entry and exit prices for representative `CL` trades.

## Goal
Confirm whether the price difference and contract valuation used in `energy` CLD trade records are correct.

## Plan
- [x] 1. Inspect representative `CL` `cld` records.
- [x] 2. Trace the code path and config values used for `CL` PnL.
- [x] 3. Recompute trade-level values from entry and exit prices.
- [x] 4. Report whether the per-trade calculations are correct.

## Implementation Log
- **2026-03-26 23:11**: Task created and `CL` energy config values identified for validation.
- **2026-03-26 23:13**: Loaded representative `CL` `cld` records for `breakout_R_2_tp20.0_sl5.0` and manually verified both SL and TP examples against entry/exit price movement.
- **2026-03-26 23:15**: Confirmed active PnL logic in `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py` and `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`. Derived `CL` settings: `min_move=0.01`, `min_value=10`, `pip_multiplier=100`, `pip_value=10`, commission `$5`, energy adhoc cost `0`.
- **2026-03-26 23:17**: Ran a targeted audit over all weekly `CL breakout_R_2_tp20.0_sl5.0` CLD records from `2026-03-19` to `2026-03-26`. Result: `240` checked, `0` mismatches.

## Findings
- The individual `energy` trade math is correct for the checked `CL` CLD records.
- Effective formula for `CL`:
  - `gross_pnl_pips = (exit_price - entry_price) * 100`, negated for `SHORT`
  - `net_return = gross_pnl_pips * 10 - 5`
- Manual sample checks matched exactly:
  - SHORT `94.75 -> 94.80` gives `-5` pips and `-55`
  - SHORT `94.42 -> 94.22` gives `20` pips and `195`
- Weekly audit for the high-return `energy` strategy showed no mismatches.

## Validation
- Code checked:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- Example trade records checked:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\energy\2026-03-26\breakout_R_2_tp20.0_sl5.0_19de831f_CL_20260326_170929_2_0.00015_20.0_5.0_cld.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\energy\2026-03-26\breakout_R_2_tp20.0_sl5.0_1808808c_CL_20260326_193219_2_0.00015_20.0_5.0_cld.json`
- Audit result:
  - `energy / CL / breakout_R_2_tp20.0_sl5.0`: `240` checked, `0` mismatches

## Outcome
Energy trade-level net-return calculations for the reviewed `CL` trades are correct.
