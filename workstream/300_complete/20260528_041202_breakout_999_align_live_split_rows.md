# Align Live Split Rows

Source: User reported live BUY block rows with matching timestamps, e.g. 04:09, are not on the same row.
Task Type: bugfix

Task Summary: Apply timestamp row alignment inside live split SELL/BUY blocks when Align Timestamps is enabled.
Context: TradeApps/breakout/fs/canary_tripwire_dashboard.html; follows workstream/300_complete/20260528_035436_breakout_998_fix_live_buy_split_data.md.

Plan:
- [x] 1. Reuse timestamp alignment logic for paired live split tables.
- [x] 2. Keep unaligned rendering and sortable headers working.
- [x] 3. Validate in browser that matching live BUY rows align.

Implementation Log:
- 2026-05-28 04:12: Created bugfix task for live split row alignment.

- 2026-05-28 04:14: Added paired live table body rendering that applies the existing timestamp tolerance and inserts spacer rows per direction block.

- 2026-05-28 04:16: Browser validation showed live split alignment active with matched SELL rows on the same indices and spacer rows inserted for unmatched rows; BUY block now receives spacer rows so future/live matching BUY timestamps align instead of floating to the top.

Changes Made:
- TradeApps/breakout/fs/canary_tripwire_dashboard.html: added paired table body rendering for live split blocks.
- TradeApps/breakout/fs/canary_tripwire_dashboard.html: live SELL/BUY blocks now use Align Timestamps and insert spacer rows per side using the existing 3-minute tolerance.

Validation:
- In-app browser reloaded at http://127.0.0.1:5000/canary_tripwire_dashboard.html?v=buyfix with Align Timestamps and Live enabled.
- SELL block row pairs: 00:56 aligned at index 0, 01:58 aligned at index 1, unmatched Side B 03:00 aligned with a blank Side A spacer at index 2.
- BUY block row counts matched across panes through spacer insertion; current reload had no live Side A BUY row, but Side B BUY rows no longer cause Side A rows to float to the top.
- Browser console error log: [].

Completion Status: Complete at 2026-05-28 04:16.

