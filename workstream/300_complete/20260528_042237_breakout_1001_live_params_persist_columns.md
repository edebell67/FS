# Live Params Persist Columns

Source: User reported parameters are hidden in Live mode, live-open rows are lost on reload, and requested ability to hide columns.
Task Type: bugfix/feature

Task Summary: Keep parameter controls visible during Live mode, preserve active live rows across reloads where possible, and add column visibility controls for the canary/tripwire dashboard.
Context: TradeApps/breakout/fs/canary_tripwire_dashboard.html; follows workstream/300_complete/20260528_041855_breakout_1000_restore_live_open_rows_after_alignment.md.

Plan:
- [x] 1. Refactor Live layout so side parameters remain visible while split live tables are shown.
- [x] 2. Persist live directional rows/states and restore live-open rows after reload.
- [x] 3. Add column visibility controls that apply to normal and live tables.
- [x] 4. Validate Live mode, reload recovery, alignment, and column hiding in the browser.

Implementation Log:
- 2026-05-28 04:22: Created combined follow-up task for visible parameters, live-open reload recovery, and hideable columns.

- 2026-05-28 04:29: Patched Live layout to keep parameter headers visible, added column visibility menu, and added localStorage-backed live snapshot restore for directional live rows/states.

- 2026-05-28 04:31: Browser validation showed Live active after reload, parameter inputs visible, live board displayed, Alt Net hidden and still hidden after reload, and no console errors.

Changes Made:
- TradeApps/breakout/fs/canary_tripwire_dashboard.html: Live mode now keeps the Side A/Side B parameter headers visible and hides only the normal historical table bodies.
- TradeApps/breakout/fs/canary_tripwire_dashboard.html: added localStorage-backed live snapshot save/restore for liveDirectionalTrades and liveStates keyed by date/product/side parameters.
- TradeApps/breakout/fs/canary_tripwire_dashboard.html: Live startup now merges persisted live_open rows back onto freshly loaded closed history for the same context.
- TradeApps/breakout/fs/canary_tripwire_dashboard.html: added Columns menu and column visibility rendering for normal and live tables.

Validation:
- In-app browser at http://127.0.0.1:5000/canary_tripwire_dashboard.html?v=params-persist-cols.
- Live mode active: true; live board display: flex.
- Parameter controls visible in Live: left TP visible true, right TP visible true.
- Reload recovery: after reload, Live checked true and Live active true for the saved same date/product/params context.
- Column hiding: Alt Net removed from visible headers while USD Alt Net remained; hidden setting persisted after reload.
- Browser console error log: [].

Risks/Notes:
- Live-open row recovery is scoped to the same date, product, and side parameter signature. Changing parameters intentionally starts a different live context.
- A row that already closed and appears in API history will be loaded from history; only live_open rows are merged from the saved browser snapshot.

Completion Status: Complete at 2026-05-28 04:31.

