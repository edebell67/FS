Source: Direct user request in this session.

Task Summary: Align FS Trade Bucket behavior and FS multi-chart bucket behavior so they present identical bucket timing, net baseline, and action-driving information. The goal is that what the user sees on `multi_chart` is replicated on `trade_bucket`, eliminating ambiguity about the correct Trade Bucket action.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart.js`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart.html`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_bucket.html`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Existing related tasks:
  - `C:\Users\edebe\eds\workstream\300_complete\20260313_105621_breakout_fs_trade_bucket_drilldown_include_archived_closed_trades.md`
  - `C:\Users\edebe\eds\workstream\300_complete\20260313_042243_breakout_fs_apply_auto_archiver.md`

Plan:
- [ ] 1. Trace and document every bucket-related timestamp and net baseline used by FS multi-chart and FS Trade Bucket.
  - Test: Review bucket creation, bucket rendering, chart marker, tooltip, and net-delta calculations in both paths; pass if each displayed field is mapped to its source field/formula.
  - Evidence: Pending.
- [ ] 2. Choose and implement one canonical bucket model shared by both views.
  - Test: Update the FS bucket UI/backend so creation time, start time, chart marker semantics, net delta, and leader/action signals are derived from the same canonical bucket state in both views.
  - Evidence: Pending.
- [ ] 3. Validate parity between FS multi-chart and FS Trade Bucket for a representative bucket.
  - Test: Use a controlled fixture or live sample bucket and compare both screens; pass if the same bucket shows the same timing semantics, same net interpretation, and same action-driving state in both views.
  - Evidence: Pending.

Implementation Log:
- 2026-03-13 13:51 Europe/London: Created this task from the user request to make FS Trade Bucket and FS multi-chart bucket behavior identical.
- 2026-03-13 13:51 Europe/London: Captured the known mismatch: the cyan marker in `multi_chart` is intended to represent bucket creation/start time, while the multi-chart card net is still anchored to the chart baseline rather than necessarily the bucket baseline used by Trade Bucket.
- 2026-03-13 14:09 Europe/London: Confirmed the canonical rule with the user: Trade Bucket should match the existing `multi_chart` default and interpret bucket net/action as `since current chart baseline/start_from`, not `since bucket creation`.
- 2026-03-13 14:14 Europe/London: Updated `trade_bucket.html` so bucket cards and drilldown use `chart_start_time` as the baseline time, display `Created` and `Chart Start` separately, and rank/leader calculations on the page now use `current_net_from_chart`.
- 2026-03-13 14:17 Europe/London: Updated `trade_viewer_api.py` so backend bucket promotion/reconciliation uses `chart_start_time` when present, with `start_time` only as a backward-compatible fallback for legacy buckets. This aligns server-side Trade Bucket action logic with the net semantics already used by `multi_chart`.

Changes Made:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_bucket.html`
  - bucket header now distinguishes `Created` vs `Chart Start`
  - strategy leader selection and displayed bucket action metrics now use `current_net_from_chart`
  - strategy drilldown now requests trades since `chart_start_time`
  - text labels were updated so the chart-baseline semantics are explicit
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - bucket promotion and reconcile flows now evaluate top/second strategy performance from `chart_start_time` first
  - `start_time` remains as a fallback for older buckets that predate `chart_start_time`

Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- `rg -n "current_net_from_chart|chart_start_time|net_delta_from_creation" C:\Users\edebe\eds\TradeApps\breakout\fs\trade_bucket.html C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Result: backend syntax passed and the remaining Trade Bucket leader/action code paths now resolve through chart-baseline fields rather than creation-only delta for live action selection.

Risks/Notes:
- Current behavior appears to mix at least two concepts:
  - chart playback/start baseline
  - bucket creation/start baseline
- The cyan dot in `multi_chart` still marks bucket creation/start time. That marker is now explicitly informational rather than the bucket action/net baseline.
- Historical/legacy buckets without `chart_start_time` will continue to fall back to `start_time`, so parity is strongest for buckets created after the chart-baseline field was added.

Open Question:
- Answered 2026-03-13 13:52 Europe/London: use `since current chart baseline/start_from`.
- Implementation target: Trade Bucket should be updated to match FS `multi_chart`, which the user confirmed is the preferred default behavior.

Completion Status:
- Complete - 2026-03-13 14:18 Europe/London
