# Task: Breakout FS _summary_net.json Chronological Accumulation
**Status:** [ ] To Do
**Priority:** 1 (High)
**Created:** 2026-03-10

## Source
- User Request: "i have little confidence in the data from _summary_net.json... the historical information on the chart changes.. this should never be the case as history is closed trades"
- The issue arises because the legacy `summary_net_generator.py` processes historical trades from disk sorted by their filenames. Because the filenames contain the *entry* time, a long-running trade that closes late can incorrectly be processed before a short-running trade that opened slightly later but closed quickly. Since P&L is accumulated into a running total, doing this out of the actual `exit_time` order corrupts the trajectory (equity curve) of the historical series exactly as observed by the user, particularly on restart.

## Plan
- [x] 1. Refactor `process_trade_file` in `summary_net_generator.py` to allow passing in pre-loaded JSON dictionaries.
- [x] 2. Update the `_cld.json` initialization loop so it pre-loads all files into memory, extracts their actual `exit_time` (or `entry_time`), and explicitly sorts them chronologically *before* accumulating their P&L totals.
- [x] 3. Ensure the newly closed `_cl.json` files in the live stream also receive the same `exit_time` sorting treatment to maintain absolutely pristine sequential accumulation.

## Implementation Log
- **2026-03-10 23:48:** Task created.
- **2026-03-10 23:51:** Separated `process_trade_file` IO logic from core processing into a dictionary-driven `process_trade_dict()`. 
- **2026-03-10 23:51:** Replaced sequential alphabetical processing with an explicitly parsed array `tuples` mapping `exit_time` values. P&L points are now plotted and accumulated strictly in historical sequence.
- **2026-03-11 01:00:** Discovered & fixed an additional UI-side bug inside `multi_chart_v2.js` and `multi_chart_v3.js` where the accessor referenced `pt.buy` instead of the required `pt.buy_net` property when charting split directional traces.

## Issue Summary & Fixes Applied

### 1. The Time-Travel Bug (Backend - Fixed)
**Problem:** The `summary_net_generator.py` rebuilt history by reading the trade `.json` files in alphabetical order of their filenames. Because the file names are stamped with `entry_time`, a trade that stayed open for hours would be mathematically added to the running `total_net` *before* a 10-minute scalp trade that actually closed much earlier. When the UI sorted these out-of-order `net` sums by actual time, it created massive fake vertical spikes and drops (jumps/time-travel). This was especially noticeable on script restart.
**Fix:** The python generator now reads the internal `exit_time` directly from the trade JSON properties and rigidly sorts every trade chronologically into an exact sequence *before* applying the profit/loss to the running total.
**Expectation:** The historical line will now trace perfectly flat horizontal steps and perfectly vertical leaps aligned to exactly when each trade finalized its balance, without ever deviating or jumping differently upon restart. Note: This applies going forward (Current Date) entirely unless backfilled previously.

### 2. The Split-Chart Metric Bug (Frontend - Fixed)
**Problem:** The JS charts for Split View `[b]` and `[s]` in versions v2 and v3 were calling for `pt.buy` instead of the correct `pt.buy_net` backend metric field.
**Fix:** Updated `getMetricValueV2()` and `getMetricValueV3()` globally in all variants to correctly fallback to `pt.buy_net` and `pt.sell_net`.
**Expectation:** Toggling the Split/Combo views (especially for V2 and V3) will now correctly map the true directional P&L without drawing flat 0 lines or errors. 

## Completion Status
COMPLETE