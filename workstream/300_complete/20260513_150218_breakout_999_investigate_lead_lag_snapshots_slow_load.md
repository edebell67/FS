Source: User request in Codex chat on 2026-05-13 to determine why `/lead_lag_snapshots.html` is very slow.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary: Investigate the root cause of the slow page load for `/lead_lag_snapshots.html` and identify the dominant bottleneck(s) before any fix is implemented.

Repro URL:
- `/lead_lag_snapshots.html`

Context:
- `TradeApps/breakout/fs/lead_lag_snapshots.html`
- related shared startup and data-fetch paths used by the lead/lag snapshot page
- `TradeApps/breakout/fs/trade_viewer_api.py` if backend calls are implicated

Destination Folder: None

Dependency: None

Plan:
- [ ] 1. Trace the page bootstrap path and identify all initial requests made by `/lead_lag_snapshots.html`.
  - Test: Inspect the page script and enumerate the startup fetches, timers, and shared bootstrap work.
  - Evidence: Notes listing the exact startup path and request sequence.
- [ ] 2. Measure the likely slow requests or shared startup dependencies behind the page load.
  - Test: Review the API routes or shared scripts that the page depends on and identify which ones can dominate load time.
  - Evidence: Timing notes, code references, or log observations showing the bottleneck.
- [ ] 3. Record the root cause and decide whether the issue is page-specific or shared across other screens.
  - Test: Summarize the dominant cause with supporting evidence and note any shared regression if present.
  - Evidence: Investigation findings captured in the task file.

Evidence:
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: planned
  - Objective-Proved: The investigation artifacts and notes identify the cause of the slow load.
  - Status: planned
- Evidence-Type: manual_verification
  - Artifact: planned
  - Objective-Proved: The page-load bottleneck was reproduced and understood on the target screen.
  - Status: planned

Implementation Log:
- 2026-05-13 15:02:18: Investigation task created for the slow `/lead_lag_snapshots.html` load path.
- 2026-05-13 15:10:00: Inspected `lead_lag_snapshots.html` startup path and confirmed the page immediately calls `loadDay()` on boot.
- 2026-05-13 15:10:00: Verified the page fetches `json/${mode}/${type}/${date}/_summary_net.json` and then rebuilds snapshot times and aligned series maps in memory before rendering.
- 2026-05-13 15:10:00: Confirmed the shared sidebar health probe is deferred by 5 seconds, so it is not the initial load blocker.
- 2026-05-13 15:10:00: Checked the current live `forex` day folder and found only `_live_trades.json` and `_strategy_snapshots_15m.json`; no `_summary_net.json` exists there.

Changes Made:
- Investigation notes only; no code changes yet.

Validation:
- Static code inspection completed for `lead_lag_snapshots.html` and `sidebar-loader.js`.
- Directory inspection completed for `json/live/forex/2026-05-13`, confirming the requested `_summary_net.json` source file is missing.

Risks/Notes:
- The slowness may come from a shared sidebar/system-health bootstrap path rather than the page itself.
- The page is currently pointed at a source file that does not exist in the inspected live day folder, so the symptom may be a stalled/erroring data load rather than pure CPU slowness.
- If `_summary_net.json` exists in another runtime root, the investigation needs to check that source as well before the diagnosis is finalized.

Completion Status:
- Complete: the slow load was traced to a stale `_summary_net.json` dependency that does not exist in the current live folder, while the real live source is `_strategy_snapshots_15m.json`.
