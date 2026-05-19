---
Task Type: standard
Task Summary: Add EOD force-close guard to breakout_Rev.py and breakout_R_Rev.py process_new_tick, and document findings from Apr 23/24 carryover investigation
Dependency: None
Destination Folder: TradeApps/breakout/fs/
---

## Context

Investigation on 2026-04-24 found that `breakout_Rev.py` and `breakout_R_Rev.py` both override `process_new_tick` but were missing the EOD force-close logic present in `common.py`. This caused ~713 open trades from Apr 23 to carry over into Apr 24 (the process ran through midnight without closing positions).

Additionally, the entry guard (`not self.is_eod`) was also missing, meaning new trades could be opened between 23:00–00:00.

## Changes Made

**Files: `TradeApps/breakout/fs/breakout_Rev.py`, `TradeApps/breakout/fs/breakout_R_Rev.py`**

1. Added `from datetime import datetime` import to both files.

2. Added EOD force-close block and EOD entry guard to `process_new_tick` in both files (identical change):

```python
# 2. EOD force-close if past 23:00
if self.open_trade and self.is_eod(current_time):
    print(f"[{datetime.now()}] [EOD-FORCE-CLOSE] Closing {self.trade_product} trade #{self.open_trade['id']} - Past 23:00 cutoff.")
    self.close_trade(current_time, current_price, 'EOD Force Close')
    self.price_history.append(current_price)
    return

# 3. Window full - check entry/reversal; skip new entries after EOD
if window_ready and not self.is_eod(current_time):
    self.check_and_enter(current_time, current_price)
```

3. Both files remain in sync — diff confirms only expected differences (class name, entry direction, description, script_alias).

## Investigation Findings

### breakout_Rev.py vs breakout_R_Rev.py sync check
- Files were already in sync — only expected differences (LONG/SHORT vs SHORT/LONG entry, class name, script_alias)
- Last committed change to both: V20260207_2100

### Apr 23 open trades and Apr 24 behaviour
- ~713 Apr 23 op.json files carried over due to missing EOD close
- These do NOT block new Apr 24 trades for Rev scripts — open trades trigger reversals, not blocks
- `breakout_R.py` and plain `breakout.py` use base `common.py` process_new_tick which already has EOD guard; they were unaffected
- Apr 24 breakout_Rev trades appeared from 00:01 via reversals/TP-SL; breakout_R_Rev trades followed once reversal signals fired

### GBPAUD_C / breakout_R_2_tp10.0_sl50.0 gap investigation
- ~9hr gap (12:34 → 21:29 Apr 23) was script downtime — ALL products stopped simultaneously
- Exit at `2026-04-23T01:38:51` (as seen in _trades_summary.json) was for trade opened at 00:29:11; subsequent virtual cl.json trades (02:12–12:34) had no trade_ids so don't appear in summary view
- Signal audit corrupt files confirm restart at ~21:00 Apr 23

## Plan

- [x] 1. Add EOD force-close block to `breakout_Rev.py` `process_new_tick`
  - Test: diff confirms change applied; logic matches common.py EOD pattern
  - Evidence: see Changes Made above

- [x] 2. Apply identical EOD force-close block to `breakout_R_Rev.py` `process_new_tick`
  - Test: `diff breakout_Rev.py breakout_R_Rev.py` shows only expected differences
  - Evidence: diff output confirmed — 5 expected lines only

- [x] 3. Add EOD entry guard (`not self.is_eod`) to `check_and_enter` call in both scripts
  - Test: entry call now wrapped in `if window_ready and not self.is_eod(current_time)`
  - Evidence: see Changes Made above

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/breakout_Rev.py`, `TradeApps/breakout/fs/breakout_R_Rev.py`
  - Objective-Proved: EOD guard added to both Rev scripts; files remain in sync
  - Status: captured

## Risks/Notes

- Rev scripts' reversal behaviour is intentional — open trades do NOT block new entries, they trigger reversals. `check_and_enter` deliberately has no `if self.open_trade: return` guard.
- EOD fix prevents future carryover; existing Apr 23 open trades resolved naturally via TP/SL/reversal throughout Apr 24 morning.
- Scripts need restart to pick up the change.

## Completion Status

COMPLETE — 2026-04-24
