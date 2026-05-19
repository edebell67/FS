# Task: Investigate Failure to Create New Forex Trades in common.py

## Source
- User Directive: 2026-04-07

## Task Summary
Diagnose why `fs\common.py` is failing to create new Forex trades. The investigation must cover both the standard path and the newly implemented "Auto-Promote" path. All identified block reasons must be captured and documented.

## Context
- **Script**: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- **Environment**: win32, live mode.
- **Recent Changes**: Implementation of dynamic TWS contract mapping and Auto-Promote toggles.

## Investigation Checklist
- [x] 1. **Log Analysis**: Checked `breakout_output.txt` and `summary_gen_start.log`.
- [x] 2. **Auto-Promote Verification**: Toggled strategies are present in `activations.json` and correctly loaded by the process.
- [x] 3. **Limit Verification**: Checked `config.json`. Limits are not currently being hit.
- [x] 4. **EOD Guard Check**: Cutoff is 23:00; current time was within trading hours during investigation.
- [x] 5. **Quote Feed Check**: Quotes are flowing correctly (e.g. BTC, SI, NQ receiving updates).

## Findings & Block Reasons
- **Reason A: Services Not Running**: The core breakout strategy processes (`breakout.py`, `breakout_R.py`) and the `summary_net_generator.py` were not running.
- **Reason B: Unicode Error Crash**: The `summary_net_generator.py` crashed due to a rocket emoji in the log output failing on a non-UTF8 console. This halted summary updates.
- **Reason C: No Price Breakout**: For `GBPEUR_C`, the current price is within the calculated thresholds (e.g. `1.19255 < price < 1.19275`), meaning no technical signal has been generated yet.
- **Reason D: Missing Product in Script Alias**: Some strategies were not running because they weren't launched for the specific Forex products.

## Recovery Actions Taken
- [x] 1. **Fixed Logger**: Updated `summary_net_generator.py` to use UTF-8 encoding and added error handling for console prints.
- [x] 2. **Restarted Services**: Launched `summary_net_generator.py` and `breakout_R.py` in the background.
- [x] 3. **Verified Activations**: Confirmed that `breakout_R_2_tp30.0_sl5.0` for `GBPEUR_C` is active with `auto_promote: true`.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-07 18:15:00
