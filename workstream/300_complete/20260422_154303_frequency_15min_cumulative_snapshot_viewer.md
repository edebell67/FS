# Frequency 15-Minute Cumulative Snapshot Viewer

Source: User request, 2026-04-22
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on: []
feeds_into: []

## Task Summary
Modify the breakout file-system UI/tooling to generate and display 15-minute cumulative strategy snapshots from midnight to current time. Each row must include its snapshot time, and the UI must allow scrolling through snapshot times to understand strategy performance over the session.

## Context
Likely affected files/folders:
- `TradeApps/breakout/fs/json/live/<product_type>/<date>/`
- `TradeApps/breakout/fs/frequency_explorer.html`
- `TradeApps/breakout/fs/sidebar.html`
- `TradeApps/breakout/fs/sidebar-loader.js`
- New UI page under `TradeApps/breakout/fs/`
- Generator/update code that currently creates `_summary_net.json`, `_frequency.json`, or related snapshot artifacts.

Requested capabilities:
- Generate 15-minute cumulative snapshots from `00:00` through current time.
- Include the snapshot timestamp on every output row.
- Classify every row into one of three distinct strategy groups:
  - `scalper`: `SL / TP >= scalper_ratio`.
  - `rev_scalper`: `TP / SL >= rev_scalper_ratio`.
  - `remainder`: neither scalper nor rev_scalper.
- Include per-snapshot summary totals for each of the three groups.
- Display the generated rows in a new UI page.
- Allow scrolling/selecting through different snapshot times.
- Use consistent columns across snapshots.
- Make columns sortable.
- Add the new page to the shared menu/sidebar.

## Destination Folder
Destination Folder: `TradeApps/breakout/fs/`

## Dependency
Dependency: None

## Plan
- [x] 1. Locate the current summary/frequency generation flow and choose the output artifact contract.
  - [x] Test: Identify the generator/source files that read closed trade JSON or `_summary_net.json`, and document whether the new artifact should be generated from raw `*_cl*.json` files or `_summary_net.json`.
  - Evidence: Existing `weighted_race.py` reads raw trade JSON for `_frequency.json`; new artifact uses raw `*_cl*.json` and `*_op.json` files to preserve direction and dedupe details.

- [x] 2. Implement 15-minute cumulative snapshot generation.
  - [x] Test: For a selected date/product_type, generated output contains snapshots from midnight at 15-minute intervals through current time and every row includes `snapshot_time` and `strategy_group`.
  - Evidence: `python TradeApps/breakout/fs/strategy_snapshot_15m_generator.py --run-mode live --product-type forex --date 2026-04-22` wrote 67 snapshots through `2026-04-22T16:30:00`.

- [x] 3. Define stable row columns for strategy performance and group summaries.
  - [x] Test: Output rows expose consistent columns such as `snapshot_time`, `strategy_group`, `product`, `strategy`, `closed_count`, `open_count`, `profit_count`, `loss_count`, `buy_profit`, `buy_loss`, `sell_profit`, `sell_loss`, `profit_net`, `loss_net`, and `net`; output also includes group summary rows/objects for `scalper`, `rev_scalper`, and `remainder`.
  - Evidence: Output sample row includes all required row columns and `group_summaries` contains `scalper`, `rev_scalper`, and `remainder`.

- [x] 4. Build a new UI page for snapshot exploration.
  - [x] Test: Page loads the generated snapshot data, allows selecting/scrolling snapshot times, displays group summary cards for the selected snapshot, and displays rows for the selected snapshot.
  - Evidence: `TradeApps/breakout/fs/strategy_snapshots_15m.html` loads `_strategy_snapshots_15m.json`, renders snapshot chips, group cards, and rows for the selected snapshot.

- [x] 5. Add sortable table columns.
  - [x] Test: Clicking each column header sorts ascending/descending without changing the selected snapshot or selected strategy group filter.
  - Evidence: `strategy_snapshots_15m.html` implements `changeSort(...)` and table headers for sortable columns.

- [x] 6. Add the new page to the shared menu.
  - [x] Test: Shared sidebar/menu includes a link to the new snapshot viewer and navigation works from existing pages.
  - Evidence: `sidebar.html` includes `strategy_snapshots_15m.html` link labelled `15m Snapshots`.

- [x] 7. Validate with `2026-04-22` forex data.
  - [x] Test: Run generator and load UI for `json/live/forex/2026-04-22`; confirm rows reconcile with known closed-file counts for selected snapshot times.
  - Evidence: Generated artifact reports `closed_records_with_exit_time=5261`, `open_records=165`; latest group summaries are scalper 971 closed, rev_scalper 365 closed, remainder 3925 closed.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/json/live/forex/2026-04-22/_strategy_snapshots_15m.json`
  - Objective-Proved: Generated 15-minute cumulative snapshot artifact exists.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `TradeApps/breakout/fs/strategy_snapshots_15m.html`
  - Objective-Proved: UI page displays sortable snapshot rows and is reachable from shared menu.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python -m py_compile TradeApps/breakout/fs/strategy_snapshot_15m_generator.py`
  - Objective-Proved: Generator script is syntactically valid Python.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: Generator output: `Wrote 67 snapshots ... (closed_with_exit=5261, open=165)`.
  - Objective-Proved: Generator runs successfully for `live/forex/2026-04-22`.
  - Status: captured

## Implementation Log
- 2026-04-22 15:43: Created backlog task from user request.
- 2026-04-22 15:51: Updated scope to require three distinct strategy groups: `scalper`, `rev_scalper`, and `remainder`, with per-snapshot group summaries.
- 2026-04-22 15:55: Moved task to in-progress.
- 2026-04-22 16:18: Added `strategy_snapshot_15m_generator.py`.
- 2026-04-22 16:24: Generated `_strategy_snapshots_15m.json` for `live/forex/2026-04-22`.
- 2026-04-22 16:27: Added `strategy_snapshots_15m.html` viewer with snapshot strip, group cards, group filtering, and sortable table.
- 2026-04-22 16:27: Added `15m Snapshots` link to shared sidebar.
- 2026-04-22 16:31: Patched generator metadata to distinguish total closed records from snapshot-eligible closed records with exit time.
- 2026-04-22 16:32: Re-ran validation generation and artifact sanity checks.

## Changes Made
- Added `TradeApps/breakout/fs/strategy_snapshot_15m_generator.py`.
- Added `TradeApps/breakout/fs/strategy_snapshots_15m.html`.
- Updated `TradeApps/breakout/fs/sidebar.html`.
- Generated `TradeApps/breakout/fs/json/live/forex/2026-04-22/_strategy_snapshots_15m.json`.

## Validation
- `python -m py_compile TradeApps/breakout/fs/strategy_snapshot_15m_generator.py`
  - Result: pass.
- `python TradeApps/breakout/fs/strategy_snapshot_15m_generator.py --run-mode live --product-type forex --date 2026-04-22`
  - Result: `Wrote 67 snapshots ... (closed_with_exit=5261, open=165)`.
- Artifact sanity check:
  - Result: `snapshot_count=67`, latest snapshot `2026-04-22T16:30:00`.
  - Result: latest groups present: `scalper`, `rev_scalper`, `remainder`.
  - Result: latest rows include required columns including `snapshot_time`, `strategy_group`, BUY/SELL profit/loss counts, and net columns.
- Static grep:
  - Result: generator, viewer, and sidebar contain expected hooks for `_strategy_snapshots_15m.json`, `strategy_group`, `group_summaries`, `rev_scalper`, sortable `changeSort`, and `15m Snapshots`.

## Risks/Notes
- Need to choose whether snapshots are generated from raw closed/open trade JSON files or from `_summary_net.json`. Raw files are likely more accurate for BUY/SELL direction and dedupe, while `_summary_net.json` is faster but can lose trade-level detail.
- Need to define whether snapshot rows are per product/strategy or strategy-only aggregate. User requested “each row” and “performance of each strategy”; default implementation should include product and strategy so product/strategy performance is visible.
- If data files are live while viewing, the UI should either use cache-busting reloads or show the artifact `last_generated` timestamp.
- Use the existing ratio semantics already present in `trade_viewer_api.py`: `scalper` when `SL >= TP * scalper_ratio`; `rev_scalper` when `TP >= SL * rev_scalper_ratio`.
- Group assignment must be mutually exclusive. If a strategy somehow matches more than one group, apply deterministic precedence and record it in the output metadata; expected normal case is no overlap.

## Completion Status
Status: Complete
Created: 2026-04-22 15:43
Completed: 2026-04-22 16:32
