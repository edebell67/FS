# Canary Live Split Sortable Tables

Source: Direct user request to show live mode as two row blocks, one for SELL trades and one for BUY trades, and make column headings sortable.
Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary: Extend `/canary_tripwire_dashboard.html` live mode with a two-block split view by trade direction and sortable column headers.
Context: `TradeApps/breakout/fs/canary_tripwire_dashboard.html`, existing live quote integration from `20260528_031958_breakout_997_canary_live_quote_rows.md`.
Destination Folder: None
Dependency: `workstream/300_complete/20260528_031958_breakout_997_canary_live_quote_rows.md`

Plan:
- [x] 1. Add live split view controls and containers.
  - [x] Test: HTML contains a Show First control and live split containers for SELL and BUY blocks.
  - Evidence: Added `#live-show-first` and `#live-split-board`; live board renders `.live-direction-block` sections for `SELL` and `BUY`.
- [x] 2. Render live mode as two directional blocks.
  - [x] Test: Live toggle shows split view, first block follows Show First selection, and historical two-panel view remains available when Live is off.
  - Evidence: Browser automation showed body live mode active with blocks `['SELL', 'BUY']`, then Show First `BUY` changed blocks to `['BUY', 'SELL']`.
- [x] 3. Add sortable headers.
  - [x] Test: Clicking table headers sorts by the selected column and toggles direction.
  - Evidence: Browser automation found 48 live sortable headers; clicking Entry Time toggled `sort-asc=True` then `sort-desc=True`.
- [x] 4. Validate browser behavior.
  - [x] Test: Browser automation checks split view visibility, block order, and sorting.
  - Evidence: Browser run on `http://127.0.0.1:5000/canary_tripwire_dashboard.html?v=split-sort` passed split-order and sort-toggle checks.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `first={'bodyLive': True, 'blocks': ['SELL', 'BUY'], 'sortableCount': 48, 'status': 'Live GBP 28/05 03:43 1.34015/1.34025'}; second={'blocks': ['BUY', 'SELL']}; sort1={'asc': True, 'desc': False}; sort2={'asc': False, 'desc': True}`
  - Objective-Proved: Live split view, Show First ordering, and sortable header toggles work in browser.
  - Status: captured

Implementation Log:
- 2026-05-28 03:40: Created feature task from user request.
- 2026-05-28 03:41: Added Show First control and live split board markup/CSS.
- 2026-05-28 03:42: Added shared table column metadata, sort state, sortable headers, and live split rendering by direction.
- 2026-05-28 03:43: Validated live split and sorting with browser automation.

Changes Made:
- `TradeApps/breakout/fs/canary_tripwire_dashboard.html`: added `Show First` select with `SELL`/`BUY` options.
- `TradeApps/breakout/fs/canary_tripwire_dashboard.html`: added live split board that replaces the standard two-panel table layout while Live is enabled.
- `TradeApps/breakout/fs/canary_tripwire_dashboard.html`: added SELL and BUY direction blocks; each block contains Side A and Side B tables filtered to that direction.
- `TradeApps/breakout/fs/canary_tripwire_dashboard.html`: added sortable column metadata and click handlers for standard and live split table headers.

Validation:
- Browser automation with current date, Run Simulation, and Live enabled:
  - Live body class active: `True`
  - Default block order: `['SELL', 'BUY']`
  - After Show First set to `BUY`: `['BUY', 'SELL']`
  - Sortable header count in live split: `48`
  - Header click toggled `sort-asc` then `sort-desc`.

Risks/Notes:
- Interpret "depending on show first selection" as a new Show First control that can put SELL or BUY block first in live split mode.

Completion Status: Complete at 2026-05-28 03:43.
