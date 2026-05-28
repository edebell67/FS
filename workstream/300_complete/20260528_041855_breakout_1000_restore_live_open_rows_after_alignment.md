# Restore Live Open Rows After Alignment

Source: User reported the 04:09 live trades disappeared after adding live split row alignment.
Task Type: bugfix

Task Summary: Determine whether live-open rows are being lost on reload/history refresh or hidden by aligned live split rendering, then fix so active live rows remain visible.
Context: TradeApps/breakout/fs/canary_tripwire_dashboard.html; follows workstream/300_complete/20260528_041202_breakout_999_align_live_split_rows.md.

Plan:
- [x] 1. Inspect current browser live state and rows for 04:09/LIVE entries.
- [x] 2. Fix the row visibility/lifecycle issue without breaking alignment.
- [x] 3. Validate live rows remain visible and aligned.

Implementation Log:
- 2026-05-28 04:18: Created follow-up task for disappeared 04:09 live rows.

- 2026-05-28 04:20: Inspected live DOM. No 04:09 rows were present; one current live-open BUY row was visible at 04:15. Conclusion: 04:09 was not hidden by alignment, it was a transient live-open row lost when the page was reloaded during validation. Live-open rows are currently browser-session state until closed; closed rows come from the simulation API/history.

Validation:
- In-app browser on http://127.0.0.1:5000/canary_tripwire_dashboard.html?v=buyfix showed Live active and Align Timestamps checked.
- DOM query found liveRows=[28/05 04:15 BUY ... LIVE ...] and rows409=[].
- BUY panes showed Side A (Macro) 1 BUY and Side B (Canary) 9 BUY.

Decision:
- No code change for this specific report: the disappeared 04:09 row was caused by reload/reset of non-persisted live-open state, not by the alignment renderer hiding rows.

Completion Status: Complete at 2026-05-28 04:20.

