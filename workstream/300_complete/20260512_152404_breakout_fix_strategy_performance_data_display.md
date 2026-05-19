Source: User request in Codex chat on 2026-05-12 to fix the lack of data display in `/strategy_performance.html`.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary: Investigate and fix the missing data display on the live breakout strategy performance page so `/strategy_performance.html` renders its expected data on the current FS-backed application path.

Context:
- `TradeApps/breakout/fs/strategy_performance.html`
- `TradeApps/breakout/fs/trade_viewer_api.py`
- `TradeApps/breakout/fs/sidebar.html`
- related page links from `TradeApps/breakout/fs/live_trades.html`

Destination Folder: TradeApps/breakout/fs/

Dependency: None

Plan:
- [x] 1. Reproduce the missing-data behavior and identify the failing data path.
  - Test: Load `/strategy_performance.html` against the current breakout app and confirm which request, data source, or render path is failing.
  - Evidence: Browser/API observations and implementation log notes naming the failing path.
- [x] 2. Implement the fix in the relevant frontend and/or backend files.
  - Test: Update the page so its data fetch and render path succeeds for the intended live configuration.
  - Evidence: File diff summary and code references recorded in Changes Made.
- [ ] 3. Validate that data displays correctly after the fix.
  - Test: Reload `/strategy_performance.html` and confirm the expected strategy-performance data renders without the prior blank state.
  - Evidence: Validation notes, command output, and user-visible verification artifact.

Evidence:
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: planned
  - Objective-Proved: The code changes required for the strategy performance data-display fix were implemented.
  - Status: planned
- Evidence-Type: manual_verification
  - Artifact: planned
  - Objective-Proved: The page visibly displays the expected data after the fix.
  - Status: planned

Implementation Log:
- 2026-05-12 15:24:04: Task created in backlog for `/strategy_performance.html` missing-data fix.
- 2026-05-12 15:31:00: Reproduced the blank-data condition through `/api/stats_summary`, which returned an empty `data` array for `mode=live`, `date=2026-05-12`, and `product_type=forex` even though the expected live JSON files existed under `X:\eds\TradeApps\breakout\fs\json\live\forex\2026-05-12`.
- 2026-05-12 15:39:00: Confirmed the browser-facing traffic on `127.0.0.1:5000` was served by a WSL-hosted `trade_viewer_api.py` instance, not just the Windows Python process, which explained why an initial Windows-only restart did not change the page behavior.
- 2026-05-12 15:46:00: Patched `_iter_day_dirs_for()` in `TradeApps/breakout/fs/trade_viewer_api.py` so product-type requests explicitly prefer product-type day directories such as `live/forex/YYYY-MM-DD` before falling back to legacy root-level day folders.
- 2026-05-12 15:49:00: Restarted the WSL-hosted API instance and re-ran the stats endpoint against `127.0.0.1:5000`; the endpoint returned populated strategy rows and snapshot payloads for the same live `forex` request.

Changes Made:
- Updated `TradeApps/breakout/fs/trade_viewer_api.py` in `_iter_day_dirs_for()` to prefer explicit product-type day directories for requests like `product_type=forex`, preventing `/api/stats_summary` from resolving against the wrong legacy day folder and returning empty results.
- Confirmed the active browser-facing API process was the WSL-hosted `python3 trade_viewer_api.py` instance and restarted that instance after the backend patch so the live page would pick up the fix.

Validation:
- Before fix: `Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:5000/api/stats_summary?mode=live&date=2026-05-12&product_type=forex&limit=5&view=top&sort_key=total_net&sort_dir=desc&include_dist=false'` returned an empty `data` array, matching the blank page state.
- Data source confirmed present: `X:\eds\TradeApps\breakout\fs\json\live\forex\2026-05-12\_summary_net.json` and related live files existed for the requested date.
- After fix and WSL API restart: the same endpoint returned populated rows including `GBP / breakout / 2_tp20.0_sl50.0 / total_net 840.0`, plus a non-empty `snapshot` object.
- User-visible verification: on 2026-05-12 the user confirmed `/strategy_performance.html` is visible again and the data is rendering.

Risks/Notes:
- Root cause was server-side path resolution for product-type day folders, combined with the fact that the page was being served by a WSL-hosted API process that needed its own restart after the backend change.
- An unrelated pre-existing worktree diff for `/api/debug_paths` exists in `TradeApps/breakout/fs/trade_viewer_api.py`; it was not part of this task's fix.

Completion Status:
- Complete on 2026-05-12 after API-level validation and user confirmation that `/strategy_performance.html` is visible again.
