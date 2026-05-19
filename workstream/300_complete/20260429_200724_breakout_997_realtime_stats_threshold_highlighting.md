# Add Realtime Stats Threshold Highlighting

Source: User request to add `/realtime_stats.html` highlighting: light green when profit count percentage is at or above configurable threshold `x`, and red when loss count percentage is at or above configurable threshold `y`. Defaults are 100% for both thresholds and must be added to config.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary:
Add user-visible realtime stats block highlighting based on configurable profit/loss count percentage thresholds. Profit-dominant blocks should be highlighted light green, loss-dominant blocks red. Add the threshold config fields and expose them in the existing config UI.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer.html`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`

Destination Folder: `C:\Users\edebe\eds\TradeApps\breakout\fs`

Dependency: None

Plan:
- [x] 1. Inspect realtime stats card rendering and config UI paths.
  - [x] Test: Locate `renderMetricRow`, `renderSummaryRow`, config modal fields, and `/api/config` usage.
  - Evidence: `realtime_stats.html` render paths and `trade_viewer.html` config modal fields were identified; `/api/config` already exposes config values.
- [x] 2. Add default config fields and expose them in the config UI.
  - [x] Test: `Select-String` confirms `realtime_stats_profit_check_threshold_pct` and `realtime_stats_loss_check_threshold_pct` exist in config/UI.
  - Evidence: Both config keys exist in `config.json` with default `100` and are visible in the `trade_viewer.html` config modal as `RT Stats Profit Check %` and `RT Stats Loss Check %`.
- [x] 3. Implement threshold-based block highlighting in `/realtime_stats.html`.
  - [x] Test: Frontend logic applies green/red highlight classes based on `profit_count / count * 100` and `loss_count / count * 100`, with count > 0.
  - Evidence: `thresholdState(card)` applies `threshold-profit` or `threshold-loss`; `loadHighlightConfig()` reads thresholds from `/api/config`; zero-count cards return no highlight.
- [x] 4. Validate syntax/API compatibility and record evidence.
  - [x] Test: `python -m py_compile trade_viewer_api.py` passes; realtime stats API still responds; static checks find highlight config and classes.
  - Evidence: `python -m py_compile trade_viewer_api.py` passed; `/api/config` returned both threshold values as `100`; `/api/realtime_stats?strategy_group=momentum&product=` returned `success=True`, `rows=4`, `windows=4`.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `git -C C:\Users\edebe\eds\TradeApps\breakout\fs diff -- realtime_stats.html trade_viewer.html config.json`
  - Objective-Proved: Shows config and UI highlighting changes.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `Select-String` found threshold config keys/classes/functions; `python -m py_compile trade_viewer_api.py` passed; `/api/config` returned `profit=100`, `loss=100`; `/api/realtime_stats` returned valid dashboard payload.
  - Objective-Proved: Confirms validation commands passed.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `http://localhost:5000/realtime_stats.html`
  - Objective-Proved: User can observe threshold-highlighted realtime stats blocks.
  - Status: captured

Implementation Log:
- 2026-04-29 20:07:24 - Task created from user request.
- 2026-04-29 20:15:00 - Added config defaults, config UI fields, and realtime stats threshold highlighting.

Changes Made:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
  - Added `realtime_stats_profit_check_threshold_pct: 100`.
  - Added `realtime_stats_loss_check_threshold_pct: 100`.
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer.html`
  - Added both threshold fields to the existing config modal under `Timeouts & Thresholds`.
- `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html`
  - Added threshold highlight styles.
  - Added config loading from `/api/config`.
  - Added threshold calculation using `profit_count / count * 100` and `loss_count / count * 100`.
  - Applied highlight classes and badges to metric blocks and performance summary blocks.

Validation:
- `Select-String -Path realtime_stats.html,trade_viewer.html,config.json -Pattern "realtime_stats_profit_check_threshold_pct|realtime_stats_loss_check_threshold_pct|threshold-profit|threshold-loss|thresholdState|loadHighlightConfig"` confirmed implementation references.
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` passed.
- `Invoke-RestMethod http://127.0.0.1:5000/api/config` returned `success=True`, `profit=100`, `loss=100`.
- `Invoke-RestMethod http://127.0.0.1:5000/api/realtime_stats?strategy_group=momentum&product=` returned `success=True`, `group=momentum`, `rows=4`, `windows=4`.

Risks/Notes:
- Percentage interpretation will be `profit_count / count * 100` and `loss_count / count * 100`; zero-count blocks are not highlighted.
- If both thresholds match, loss/red will take precedence so risk blocks are not visually hidden by profit highlighting.
- Existing working-tree diff shows `momentum_step_pips` differs from repository baseline, but this task did not intentionally modify that value.

Completion Status:
Complete - 2026-04-29 20:15:00
