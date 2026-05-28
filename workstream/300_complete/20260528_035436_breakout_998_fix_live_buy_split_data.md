# Fix Live BUY Split Data

Source: User reported BUY trades are not appearing in live split mode on /canary_tripwire_dashboard.html.
Task Type: bugfix

Task Summary: Ensure live split mode loads and tracks BUY trades independently from SELL trades for both Side A and Side B.
Context: TradeApps/breakout/fs/canary_tripwire_dashboard.html; follows workstream/300_complete/20260528_034003_breakout_997_canary_live_split_sortable_tables.md.

Plan:
- [x] 1. Reproduce/inspect why BUY block is empty.
- [x] 2. Add independent directional datasets and live states for SELL and BUY.
- [x] 3. Validate that BUY rows appear and sorting/split order still work.

Implementation Log:
- 2026-05-28 03:54: Created follow-up bugfix task for missing BUY rows in live split mode.

- 2026-05-28 03:57: Added independent live directional trade stores/states and changed live split rendering to read SELL/BUY-specific datasets.

- 2026-05-28 04:08: Browser validation showed live split active with SELL counts Side A=2/Side B=3 and BUY counts Side A=0/Side B=8 for current date/parameters; Show First BUY reordered blocks; sortable headers remained active; browser console errors were empty.

Changes Made:
- TradeApps/breakout/fs/canary_tripwire_dashboard.html: live mode now loads SELL and BUY history independently for Side A and Side B on startup.
- TradeApps/breakout/fs/canary_tripwire_dashboard.html: live quote polling now advances four independent live states: left SELL, left BUY, right SELL, right BUY.
- TradeApps/breakout/fs/canary_tripwire_dashboard.html: live split rendering now reads direction-specific datasets instead of filtering the main selected-direction tables.

Validation:
- In-app browser at http://127.0.0.1:5000/canary_tripwire_dashboard.html?v=buyfix with Live enabled.
- BUY block visible and populated where strategy data exists: Side B (Canary) 8 BUY rows; Side A (Macro) 0 BUY rows for current macro parameters.
- Show First BUY produced block order [BUY, SELL].
- Sortable live header count remained 48 and BUY Side B Net Pips sort toggled active.
- Browser console error log: [].

Completion Status: Complete at 2026-05-28 04:08.

