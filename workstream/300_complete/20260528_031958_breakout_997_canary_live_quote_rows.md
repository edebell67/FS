# Canary Live Quote Rows

Source: Direct user request to add a live toggle to `/canary_tripwire_dashboard.html` using `http://127.0.0.1:8002/api/vw_000_fx_quotes`.
Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary: Add a live mode to the canary tripwire dashboard that, when viewing the current date, polls live FX quotes every 5 seconds and appends/updates live rows using the same entry/exit rules on both sides.
Context: `TradeApps/breakout/fs/canary_tripwire_dashboard.html`, `TradeApps/breakout/fs/trade_viewer_api.py`, `03_execution_experiments.py`, `03_execution_experiments_X.py`.
Destination Folder: None
Dependency: None

Plan:
- [x] 1. Inspect live quote API shape and existing dashboard/script logic.
  - [x] Test: Request `http://127.0.0.1:8002/api/vw_000_fx_quotes` and inspect dashboard/script entry/exit code.
  - Evidence: Quote API returns `data` rows with `timestamp`, `code`, `bid`, `ask`, and `stale`; scripts use trailing `open_bid/open_ask`, EP threshold, TP/SL pips, direction filters, and X-inverted signal mapping.
- [x] 2. Add backend quote proxy.
  - [x] Test: `/api/live_fx_quotes` returns selected product quote without CORS issues.
  - Evidence: `/api/live_fx_quotes?product=GBP` returned `success=True code=gbp bid=1.34045 ask=1.34055 stale=False` after server restart.
- [x] 3. Add dashboard live toggle and client-side live execution engine.
  - [x] Test: HTML contains live toggle, status, 5-second polling, and live row update logic for both sides.
  - Evidence: Served HTML contains `id="live-toggle"`, `id="live-status"`, and `/api/live_fx_quotes`; JavaScript includes live state, quote polling, entry/exit processing, live open-row updates, and stats refresh.
- [x] 4. Validate live behavior.
  - [x] Test: Browser automation enables live on the current date and verifies live status updates without breaking historical simulation.
  - Evidence: Browser automation returned `liveChecked=True`, `status='Live GBP 28/05 03:24 1.34045/1.34055'`, left/right historical rows still rendered.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `/api/live_fx_quotes?product=GBP` -> `success=True code=gbp bid=1.34045 ask=1.34055 stale=False`
  - Objective-Proved: Dashboard server can fetch current live GBP quotes from port 8002.
  - Status: captured
- Evidence-Type: demo
  - Artifact: Browser automation against `http://127.0.0.1:5000/canary_tripwire_dashboard.html?v=live`
  - Objective-Proved: Live toggle can be enabled on the current date and updates live status from the quote feed.
  - Status: captured

Implementation Log:
- 2026-05-28 03:19: Created task, fetched quote API sample, and inspected dashboard/script logic.
- 2026-05-28 03:22: Added `/api/live_fx_quotes` Flask proxy for `http://127.0.0.1:8002/api/vw_000_fx_quotes`.
- 2026-05-28 03:23: Added dashboard Live toggle, live status text, 5-second polling, and per-side live execution state machine.
- 2026-05-28 03:24: Restarted port 5000 server and validated live quote proxy plus browser live toggle flow.

Changes Made:
- `TradeApps/breakout/fs/trade_viewer_api.py`: added `GET /api/live_fx_quotes?product=<code>` proxy endpoint.
- `TradeApps/breakout/fs/canary_tripwire_dashboard.html`: added Live toggle and live status display.
- `TradeApps/breakout/fs/canary_tripwire_dashboard.html`: added live quote polling every 5 seconds on current date only.
- `TradeApps/breakout/fs/canary_tripwire_dashboard.html`: added client-side live execution logic for standard and X-inverted signal mapping, direction filters, EP entry threshold, TP/SL exit thresholds, live open-row updates, closed live rows, cumulative totals, and win-rate refresh.

Validation:
- `python -m py_compile trade_viewer_api.py` passed.
- `/api/live_fx_quotes?product=GBP` returned `success=True` with a non-stale GBP quote.
- Served dashboard HTML contains live toggle/status and live quote API code.
- Browser automation set the current date, ran simulation, enabled Live, and observed `Live GBP 28/05 03:24 1.34045/1.34055`.

Risks/Notes:
- Live entry/exit starts from the latest quote observed after live mode is enabled; it does not reconstruct hidden script state from historical JSONL beyond using existing displayed historical trades for cumulative totals and recent win percentage.
- A live row is appended only after the same entry rules trigger. If price does not move by EP from the live anchor quote, live mode remains armed with status updates but no new row.

Completion Status: Complete at 2026-05-28 03:24.
