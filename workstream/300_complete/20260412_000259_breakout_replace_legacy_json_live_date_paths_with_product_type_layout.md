# Task: Replace Legacy json/live/{date} Paths With Product-Type Layout

Source: User request on 2026-04-12 to correct all remaining code paths that still use the legacy layout `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\{date}` instead of the current product-type-aware layout `...\fs\json\live\{product_type}\{date}`.

Task Type: refactor

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
Find and correct all remaining runtime and utility code that reads from or writes to the legacy dated live JSON path without `product_type`, and move those call sites to the shared `json_layout` helper flow (`resolve_day_dir`, `ensure_day_dir`, `iter_day_dirs`, or equivalent wrapper functions).

## Problem Statement

Current repository state mixes two layouts:
- legacy: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\{date}`
- current: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\{product_type}\{date}`

The normalized runtime path creation already exists in:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json_layout.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`

But some files still directly construct legacy paths, which can lead to:
- data being written into the wrong folder
- readers missing product-type-scoped data
- inconsistencies between runtime, monitoring, and analysis utilities

Known example:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live_monitor_corrupt.py`

## Objective

Standardize all relevant code on the product-type-aware live JSON folder layout so both creation and lookup consistently resolve to:
- `...\fs\json\{mode}\{product_type}\{date}`

## Requested Changes

- Audit `TradeApps\breakout\fs` for any remaining direct use of:
- `...\fs\json\live\{date}`
- `JSON_TRADES_BASE / date_str`
- hardcoded dated path strings that omit `product_type`

- Replace those with:
- `ensure_day_dir(...)`
- `resolve_day_dir(...)`
- `iter_day_dirs(...)`
- or local wrappers already built on those helpers

- Prioritize runtime-impacting files first, including:
- monitors
- extractors
- summary readers/writers
- automation utilities that may create or mutate day folders

- Preserve backward-safe reading where appropriate if legacy folders still need to be discovered temporarily.
- Do not silently create new legacy day folders as part of the corrected flow.

## Acceptance Criteria

- No remaining runtime-critical writer creates `fs\json\live\{date}` without `product_type`.
- Runtime-critical readers use shared helper-based resolution instead of hardcoded legacy paths.
- Product-type-aware paths are used consistently for the affected files.
- Regression checks confirm corrected code targets `...\live\{product_type}\{date}`.
- Any residual legacy-read-only scripts are explicitly noted if left unchanged.

## Validation

- Search the repo for legacy path construction patterns and review all hits.
- Verify corrected runtime files resolve day folders through shared helpers.
- Run focused tests for changed modules where practical.
- Manually confirm that new output for a sample live date lands under the product-type subfolder and not the legacy root date folder.

## Notes

- This task is about correcting all remaining code paths, not migrating historical data.
- If scope expands materially beyond the breakout `fs` code area, close this task and open a new one.

## Execution Log

### 2026-04-12 00:18
- Moved task from `workstream/100_todo` to `workstream/200_inprogress`.
- Audited `TradeApps\breakout\fs` for direct legacy `json\live\{date}` usage.
- Confirmed the active runtime path helpers already exist in:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json_layout.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`

### 2026-04-12 00:28
- Replaced the legacy flat-date access in `C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live_monitor_corrupt.py`.
- Updated it to iterate product-type day folders using `iter_day_dirs(...)` and `load_layout_config(...)`.
- Corrected `_summary_net.json` reads, open-trade lookups, and closed-trade checks to use the product-type-aware layout.

### 2026-04-12 00:34
- Refactored `C:\Users\edebe\eds\TradeApps\breakout\fs\automated_strategy_selector.py`.
- Changed `_top20.json` discovery to use `resolve_day_dir(...)` across configured product types instead of the legacy `json\live\{date}` root.

### 2026-04-12 00:39
- Refactored `C:\Users\edebe\eds\TradeApps\breakout\fs\bidirectional_analysis.py` and `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_date_analysis.py`.
- Both scripts now load across configured product types through `resolve_day_dir(...)` and aggregate results across the product-type-scoped day folders.

### 2026-04-12 00:43
- Refactored these utility scripts away from hardcoded flat live-date paths:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\analyze_top_strategies.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\check_win_rates.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\compare_buy_vs_sell.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\analyze_buy_patterns.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\day_profile_analyzer.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\debug_pnl_bias.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\simulate_logic.py`
- These now resolve day files through `json_layout` helpers and tolerate missing product-type folders more safely.

### 2026-04-12 00:46
- Tightened `simulate_logic.py` to avoid calling `os.path.exists(None)` when `_top20.json` is absent.

## Validation Results

### Repo Audit
- Searched `TradeApps\breakout\fs` for legacy path patterns using `rg`.
- Fixed the active runtime-critical and top-level analysis/utility scripts that still referenced `fs\json\live\{date}` directly.

### Syntax Validation
- Command:
  - `python -m py_compile "C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live_monitor_corrupt.py" "C:\Users\edebe\eds\TradeApps\breakout\fs\automated_strategy_selector.py" "C:\Users\edebe\eds\TradeApps\breakout\fs\bidirectional_analysis.py" "C:\Users\edebe\eds\TradeApps\breakout\fs\multi_date_analysis.py" "C:\Users\edebe\eds\TradeApps\breakout\fs\analyze_top_strategies.py" "C:\Users\edebe\eds\TradeApps\breakout\fs\check_win_rates.py" "C:\Users\edebe\eds\TradeApps\breakout\fs\compare_buy_vs_sell.py" "C:\Users\edebe\eds\TradeApps\breakout\fs\analyze_buy_patterns.py" "C:\Users\edebe\eds\TradeApps\breakout\fs\day_profile_analyzer.py" "C:\Users\edebe\eds\TradeApps\breakout\fs\debug_pnl_bias.py" "C:\Users\edebe\eds\TradeApps\breakout\fs\simulate_logic.py"`
- Result:
  - Passed

### Focused Runtime Smoke Checks
- Command:
  - `python "C:\Users\edebe\eds\TradeApps\breakout\fs\automated_strategy_selector.py"`
- Result:
  - Passed
  - Output indicated no `_top20.json` data for the current date, which is valid behavior after the path fix.

- Command:
  - `python "C:\Users\edebe\eds\TradeApps\breakout\fs\check_win_rates.py"`
- Result:
  - Passed
  - Output indicated no summary file found for the configured date across product-type folders, which is valid behavior after the path fix.

## Files Changed

- `C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live_monitor_corrupt.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\automated_strategy_selector.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\bidirectional_analysis.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_date_analysis.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\analyze_top_strategies.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\check_win_rates.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\compare_buy_vs_sell.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\analyze_buy_patterns.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\day_profile_analyzer.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\debug_pnl_bias.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\simulate_logic.py`

## Residual Legacy References Left Unchanged

- Documentation, logs, and backups under `C:\Users\edebe\eds\TradeApps\breakout\fs\docs\` and `trade_viewer_api_backup.py`.
- Test fixtures that intentionally create local synthetic day folders inside temp directories.
- Historical one-off scripts outside the current `fs\json` runtime layout, for example:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\calc_net_return.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\check_pnl.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\check_pnl_v2.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\fix_filenames.py`
- These were left untouched because they target older ad hoc directory layouts or maintenance operations rather than the active `fs\json` product-type-aware runtime flow addressed by this task.
