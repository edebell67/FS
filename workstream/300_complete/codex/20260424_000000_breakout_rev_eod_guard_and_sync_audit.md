---
Task Type: standard
Task Summary: Add EOD force-close guard to breakout_Rev.py and breakout_R_Rev.py, and document findings from Apr 23/24 carryover investigation
Dependency: None
Destination Folder: TradeApps/breakout/fs/
---

## Context

Investigation on 2026-04-24 revealed that `breakout_Rev.py` and `breakout_R_Rev.py` both override `process_new_tick` but are **missing the EOD force-close logic** present in `common.py`. This caused ~713 open trades from Apr 23 to carry over into Apr 24 (the process ran through midnight without closing them).

The base `common.py` `process_new_tick` has:
```python
else:
    if self.is_eod(current_time):   # hour >= 23
        self.close_trade(current_time, current_price, 'EOD Force Close')
        return
```

Neither `breakout_Rev.py` nor `breakout_R_Rev.py` have this block.

Additionally, neither script has the EOD entry guard:
```python
if not self.is_eod(current_time) and window_ready:
    self.check_and_enter(...)
```
— meaning they can open new trades between 23:00 and midnight.

## Findings from Investigation

### breakout_Rev.py vs breakout_R_Rev.py comparison
- Files are **in sync** — only expected differences (entry direction LONG/SHORT vs SHORT/LONG, class name, script_alias, description)
- Both import `_safe_float`, both have `[DEBUG-STARTUP]` print, both have `allow_reversal = True`
- Last committed change: V20260207_2100 (both files updated together)

### Apr 23 → Apr 24 carryover behaviour
- ~570 `breakout_Rev` and ~143 `breakout_R_Rev` op.json files remained open in Apr 23 folder as of Apr 24 morning
- These are NOT blocking new Apr 24 trades — the reversal scripts call `check_and_enter` with open trade; the old trade reverses/closes and a new one opens in the Apr 24 folder
- Apr 24 `breakout_Rev` trades started appearing from 00:01; `breakout_R_Rev` trades will appear once reversal signals fire for those products
- The `_LATEST_TRADING_DATE` global updates from tick timestamps, so new trades correctly write to the Apr 24 folder while existing open trades still write to their original Apr 23 file path

### GBPAUD_C / breakout_R_2_tp10.0_sl50.0 gap investigation
- ~9hr gap (12:34 → 21:29 Apr 23) was script downtime — ALL products stopped simultaneously at ~12:35 and restarted at ~20:58
- Exit at `01:38:51` (as seen in _trades_summary.json) corresponds to `a439d5b9` trade (entry 00:29:11)
- Virtual cl.json trades (02:12, 09:07, 10:10, 11:54) don't have trade_ids so don't appear in main summary view

## Plan

- [ ] 1. Add EOD force-close block to `breakout_Rev.py` `process_new_tick` (after `check_and_exit`, before `check_and_enter`)
  - Test: Run script past 23:00 in sim and confirm `EOD Force Close` appears in output
  - Evidence:

- [ ] 2. Apply identical EOD force-close block to `breakout_R_Rev.py` `process_new_tick`
  - Test: Diff confirms both files are in sync on EOD logic
  - Evidence:

- [ ] 3. Add EOD entry guard to `check_and_enter` call in both scripts (skip entry if hour >= 23)
  - Test: Confirm no new trades opened between 23:00–00:00 in test run
  - Evidence:

## Evidence

Objective-Delivery-Coverage: 0%
Auto-Acceptance: false

- Evidence-Type: diff
  - Artifact: planned
  - Objective-Proved: EOD guard added to both Rev scripts
  - Status: planned

## Risks/Notes

- The reversal open-trade behaviour is intentional — open trades do NOT block new entries for Rev scripts, they trigger reversals. Do not add `if self.open_trade: return` to Rev scripts' check_and_enter.
- EOD fix only prevents future carryover; existing Apr 23 open trades will close naturally via TP/SL/reversal.
