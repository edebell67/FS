# Task: Verify Individual Indices Metals Trade Net Return Formula

## Source
- User Directive: 2026-03-26

## Task Summary
Verify at the individual trade level that `net_return` in `*cld.json` is correctly calculated from entry and exit prices for representative `indices` and `metals` trades.

## Context
- Need trade-level validation rather than summary reconciliation.

## Goal
Confirm whether the price difference and contract valuation used in `cld` trade records are correct for specific `indices` and `metals` trades.

## Plan
- [x] 1. Inspect representative `cld` records for indices and metals.
- [x] 2. Trace the code path that computes `gross_pnl_pips` and `net_return`.
- [x] 3. Recompute trade-level values from entry and exit prices.
- [x] 4. Report whether the per-trade calculations are correct.

## Implementation Log
- **2026-03-26 22:40**: Task created and representative `NQ` and `SI` `cld` records inspected for trade-level fields.
- **2026-03-26 22:46**: Traced active PnL logic in `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`. Verified `net_return` is derived from price difference, dynamic product pip multiplier, dynamic product pip value, minus commission and any product-type adhoc costs.
- **2026-03-26 22:49**: Loaded `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json` values for `NQ` and `SI`. Derived `pip_value = 10.0` for both products. Verified `indices` and `metals` adhoc costs are `0`, so net is effectively `gross_pnl_pips * 10 - 5`.
- **2026-03-26 22:54**: Manually checked representative trades:
  - `NQ` TP trade: price move `10.0` points on a SHORT with multiplier `2` gives `20` pips, so `20 * 10 - 5 = 195`, matching the CLD record.
  - `NQ` SL trade: price move `-2.5` points on a LONG with multiplier `2` gives `-5` pips, so `-5 * 10 - 5 = -55`, matching the CLD record.
  - `SI` TP and SL examples also matched exactly after applying multiplier `500` and pip value `10`.
- **2026-03-26 22:59**: Ran a targeted audit over all weekly `breakout_R_2_tp20.0_sl5.0` CLD records for `NQ` and `SI` from `2026-03-19` to `2026-03-26`. Results: `NQ` checked `325` trades with `0` mismatches; `SI` checked `560` trades with `0` mismatches.

## Findings
- The individual trade math is correct for the checked `indices` and `metals` CLD records.
- For the high-return strategies reviewed, every checked `NQ` and `SI` trade had a `gross_pnl_pips` and `net_return` that matched the entry/exit price calculation exactly.
- For both `NQ` and `SI`, the effective formula is:
  - `gross_pnl_pips = (exit_price - entry_price) * pip_multiplier`, negated for `SHORT`
  - `net_return = gross_pnl_pips * pip_value - 5`
- Derived product settings:
  - `NQ`: `pip_multiplier=2`, `pip_value=10`
  - `SI`: `pip_multiplier=500`, `pip_value=10`
- Since trade-level math checks out, unusually high totals are not being caused by incorrect per-trade price valuation.

## Validation
- Code checked:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- Example trade records checked:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\indices\2026-03-26\breakout_R_2_tp20.0_sl5.0_*.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\2026-03-26\breakout_R_2_tp20.0_sl5.0_*.json`
- Targeted audit result:
  - `indices / NQ / breakout_R_2_tp20.0_sl5.0`: `325` checked, `0` mismatches
  - `metals / SI / breakout_R_2_tp20.0_sl5.0`: `560` checked, `0` mismatches

## Outcome
Trade-level net-return calculations for the reviewed `indices` and `metals` trades are correct. The concern does not appear to be a bad entry/exit price calculation on individual CLD records.
