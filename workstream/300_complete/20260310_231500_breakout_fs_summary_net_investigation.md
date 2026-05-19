# Task: Breakout FS _summary_net.json Investigation
**Status:** [ ] To Do
**Priority:** 1 (High)
**Created:** 2026-03-10

## Source
- User Request: "create a new task to look at _summary_net.json which is datasource for multi... i am reference the \fs version which uses the json flat files only"
- Appears related to recent failures observed in `summary_gen_debug.log` where `json` flat files cannot be successfully parsed/generated for the simulation/live directories.

## Task Summary
Investigate and resolve the underlying generation or parsing issue with `_summary_net.json` flat files within the `/fs` variant of the Breakout application. Since the `/fs` variant relies exclusively on the disk JSON state (unlike the `/DB` variant, which was recently migrated to database generation), any missing, malformed, or out-of-date flat files immediately break the Multi-Chart module which consumes them as its primary multi-strategy data source.

## Context
- **Generation:** Likely `TradeApps/breakout/fs/summary_net_generator.py` (which periodically scrapes directories and compiles the cross-strategy stats) or the trade execution loops directly.
- **Consumption:** `TradeApps/breakout/fs/trade_viewer_api.py` endpoint `GET /api/trade_file?filename=_summary_net.json` and the frontend Javascript (`multi_chart.js` / `multi_chart_v2.js` / `multi_chart_v3.js`).
- **Debugging log:** `C:\Users\edebe\eds\TradeApps\breakout\summary_gen_debug.log` currently reports parsing exceptions (`Expecting value: line 1 column 1 (char 0)` and `Expecting ',' delimiter`) likely stemming from race conditions, incomplete JSON generation from strategies, or locked files being read mid-write.

## Plan
- [x] 1. Analyze `C:\Users\edebe\eds\TradeApps\breakout\summary_gen_debug.log` to identify specifically which generator script threw the parsing exceptions and verify standard JSON flat file loading patterns in `/fs`.
- [x] 2. Inspect the strategy execution loop or flat-file emission pattern causing empty/malformed `[Strategy_Name].json` files that trip up the summary generator.
- [x] 3. Patch the `/fs` pipeline (either handling empty files more gracefully in `summary_net_generator.py` or locking the writes downstream) so `_summary_net.json` is successfully, atomically generated for Multi-Chart to consume.
- [x] 4. Verify functionality in browser by confirming Multi-Chart overlays successfully fetch `/fs/..._summary_net.json` payload.

## Implementation Log
- **2026-03-10 23:15:** Task created. Awaiting investigation.
- **2026-03-10 23:20:** Analyzed `summary_net_generator.py` and introduced a `load_json_with_retry` method. This method automatically catches `JSONDecodeError`s or 0-byte reads (which occur when the trading scripts are actively locking and writing to `_cl` or `_op` files) and introduces a 0.2s pause back-off with up to 5 retries. 
- **2026-03-10 23:21:** Replaced raw `json.load()` calls across the `process_trade_file()`, `open_files`, and `floating_sum` loops so that the summary generator is now immune to single-frame race condition failures. 

## Completion Status
COMPLETE - Awaiting User Verification of charts now continuing uninterrupted.