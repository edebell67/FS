---
Task Type: standard
Task Summary: Fix breakout main loop performance bottlenecks and add signal audit logging
Dependency: 20260423_190000_breakout_fix_rev_window3_window4_trade_generation.md
---

## Context

Follow-on to the window 3/4 trade generation fix. After restarting scripts, the main trading loop was hanging for 25–30 seconds per iteration instead of polling every 5 seconds. Signal logging was also only going to stdout (ephemeral). This task covers three improvements applied to `common.py` and all four breakout scripts.

## Changes Made

### 1. Signal audit logging — all 4 breakout scripts
Added `_audit_signal_event('breakout_detected', ...)` call at the threshold-crossing point in `check_and_enter` for all scripts. Removed per-tick noisy debug prints ("Breakout check: price=...", "No breakout", "Building window").

Files: `breakout.py`, `breakout_R.py`, `breakout_Rev.py`, `breakout_R_Rev.py`

Each signal event persists to `json/live/forex/{date}/_signal_audit.json` with: `signal`, `price`, `long_threshold`, `short_threshold`, `window_size`, `strategy`, `product`.

### 2. Price logging per tick — `common.py`
Added `[PRICES]` log line after each successful quote fetch showing all product prices in one line:
```
[HH:MM:SS] [PRICES] {'EUR': '1.16830', 'GBP': '1.34640', ...}
```

### 3. Main loop performance — `common.py`

Three bottlenecks identified and throttled:

| Call | Before | After |
|------|--------|-------|
| `_perform_auto_activation_check` | Every 10s (scans 3500 files) | Every 60s |
| `_perform_cld_auto_archive` | Every tick (globs 800+ .cld files) | Every 60s (same gate as activation check) |
| `_perform_auto_activation_check` file scan | `rglob('*.json')` = all 3940 files | `glob('*_op.json')` + `glob('*_cl.json')` only |

Also previously fixed (in prior task): `_load_persisted_state` changed from `glob('*.json')` to `glob('*_op.json')`.

Result: loop now ticks every ~5–10s instead of hanging 25–30s per iteration.

## Evidence

- `breakout_Rev_2_*` trades on EURNZD_C at 21:39 ✅
- `breakout_Rev_2_*` trades on GBPEUR_C at 21:41 ✅  
- `breakout_Rev_3_tp3.0_sl3.0_*` on CAD at 21:49 ✅ (window 3 confirmed)
- Price log showing 12 forex products updating every ~5s ✅

Objective-Delivery-Coverage: 100%
