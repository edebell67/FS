---
Task Type: standard
Task Summary: Fix breakout_Rev and breakout_R_Rev not generating window 3 and 4 trades
Dependency: None
---

## Context

Investigation triggered by user report that "most strategies not executing new trades" and specifically that breakout_Rev and breakout_R_Rev were only generating window 2 trades across ALL dates from 2026-04-01 onwards (confirmed working in 2026-03-25 and earlier).

## Root Cause

Regression introduced in commit `f4afe6a918` (2026-03-24 "feat(breakout): implement social automation, historical logging, and unified treemap").

`calculate_pnl()` return signature was changed from 4 to 5 values (added `adhoc_cost_usd`), but two call sites were missed:

- `common.py:1705` — inside `_trigger_grid_live_activation()`
- `common.py:2411` — inside `display_open_trade_status()`

Both still unpacked 4 values:
```python
gross_pnl, net_pnl_usd, _, alt_net_pnl_usd = self.calculate_pnl(...)
```

This raised `ValueError: too many values to unpack` on every tick where a processor had an open trade.

## Blast Radius

The main loop wraps the entire `for processor in processors_map[product]:` inside a single try/except. So when processor N crashes, processors N+1 onwards are silently skipped for that tick.

Processor order is window 2 → window 3 → window 4. Window 2 processors are almost always in a trade (Rev strategy reverses continuously). So window 2 crashes the loop on nearly every tick, window 3 and 4 never receive ticks, and therefore never generate trades.

## Fix Applied

Added 5th unpack position to both call sites (`common.py`):

```python
# Line 1705
gross_pnl, net_pnl_usd, _, alt_net_pnl_usd, _ = self.calculate_pnl(...)

# Line 2411
gross_pnl, net_pnl_usd, _, alt_net_pnl_usd, _ = self.calculate_pnl(...)
```

## Plan

- [x] Identify root cause — `calculate_pnl` 5-value return, 2 missed unpack sites
- [x] Fix `common.py:1705` — add 5th `_` to unpack
- [x] Fix `common.py:2411` — add 5th `_` to unpack
- [x] Verify no remaining 4-value unpacks remain

## Evidence

- `breakout_Rev_3/4` and `breakout_R_Rev_3/4`: 0 trades every day from 2026-04-01 to 2026-04-23
- Same scripts in 2026-03-16 to 2026-03-25: hundreds of trades per day
- Breaking commit: `f4afe6a918` dated 2026-03-24
- Fix restores 5-value unpack alignment with `calculate_pnl` signature

Objective-Delivery-Coverage: 100%
