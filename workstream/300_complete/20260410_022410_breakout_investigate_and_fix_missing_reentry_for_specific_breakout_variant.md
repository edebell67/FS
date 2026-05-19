# Breakout Investigate And Fix Missing Reentry For Specific Breakout Variant

- Status: Complete
- Started: 2026-04-10 02:24:10
- Completed: 2026-04-10 02:36:00
- Project: breakout
- Owner: Codex

## Request

Investigate and fix the recurring defect where one specific breakout strategy variant does not reopen after closing, even though sibling variants with the same entry logic do reopen on the same product and time window.

## Concrete Case

- Product: `GBPNZD_C`
- Affected strategy: `breakout_2_tp10.0_sl20.0`
- Sibling evidence: `breakout_2_tp3.0_sl20.0` reopened later at `2026-04-10T00:44:00.915579`
- Expectation: because `breakout.py` entry logic depends on window size and pip buffer, not TP/SL, `breakout_2_tp10.0_sl20.0` should also have reopened once flat.

## Plan

1. Trace close lifecycle and `open_trade` clearing in `common.py`.
2. Compare persisted and runtime state assumptions for sibling `breakout_2` variants.
3. Identify why the affected variant remained logically blocked from re-entry.
4. Implement a fix and validate against the known failure mode.

## Findings

- `breakout.py` entry logic does not use `tp_pips` or `sl_pips`; it only uses `window_size`, `pip_buffer`, `price_history`, and `current_price`.
- The missing `GBPNZD_C / breakout_2_tp10.0_sl20.0` re-entry was not a file-save issue. `_trades_summary.json` and the day folder both show no later file for that exact script.
- The real divergence came from runtime state: `BaseBreakoutStrategy.process_new_tick()` cleared `price_history` on every close and did not keep `price_history` updating while a trade was open.
- That means sibling variants with different TP/SL values drifted into different local windows after they closed at different times. One variant could still see a later breakout while another had already thrown away or frozen the context needed to detect it.

## Fix

- Changed `BaseBreakoutStrategy.process_new_tick()` to preserve the rolling price window across closes and continue appending prices every tick.
- Changed `BreakoutStrategyWithReversal.process_new_tick()` in `breakout_rev.py` to follow the same rolling-window behavior.
- Changed `BreakoutReversalContrarianStrategy.process_new_tick()` in `breakout_R_Rev.py` to follow the same rolling-window behavior.
- Entry checks now run against the prior rolling window, then the current tick is appended, which keeps breakout detection based on recent market context instead of reset-on-close behavior.

## Coverage

- `breakout.py`: covered via `BaseBreakoutStrategy.process_new_tick()`
- `breakout_R.py`: covered via `BaseBreakoutStrategy.process_new_tick()`
- `breakout_Rev.py`: directly patched
- `breakout_R_Rev.py`: directly patched

## Validation

1. `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\breakout.py C:\Users\edebe\eds\TradeApps\breakout\fs\breakout_R.py C:\Users\edebe\eds\TradeApps\breakout\fs\breakout_Rev.py C:\Users\edebe\eds\TradeApps\breakout\fs\breakout_R_Rev.py`
   - Passed.
2. In-memory regression script against `BaseBreakoutStrategy`
   - Confirmed a TP close no longer clears `price_history`.
   - Confirmed `check_and_enter(...)` can run immediately after close using the preserved rolling window.
