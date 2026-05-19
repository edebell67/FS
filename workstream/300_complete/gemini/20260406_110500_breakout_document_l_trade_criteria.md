# Document L-Trade Generation Criteria in common.py

Source: [User request](C:\Users\edebe\eds\TradeApps\breakout\fs\common.py)
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
  workflow_name: ""
  workflow_stage: backlog
  depends_on: []
  feeds_into: []

## Task Summary
Document the full criteria required to generate an L-trade (Live/Limit Trade) based on the logic in `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`.

## Context
The generation of L-trades is governed by multiple layers of guards and configurations in the `breakout` system. The core logic resides in `_handle_live_orders` and `_create_l_trade_order`.

### Full Criteria Details (Identified from common.py)

1.  **L-Trade Generation Mode**:
    - `l_trade_generation_mode` in `config.json` must be set to `'normal'` or `'both'`.
    - If set to `'trade_bucket'`, the standard direct L-trade path is disabled.

2.  **Market Bias Entry Alignment**:
    - If `enforce_market_bias` is `true` in `config.json`, the trade direction (`LONG`/`SHORT`) must align with the current market bias.
    - Uses `_is_market_bias_entry_allowed` helper.

3.  **Activation Status**:
    - The specific direction (`buy` or `sell`) and mode (`net` or `alt`) must be enabled for the product in the system's activation map.
    - Verified via `self._is_active(dir_key, mode)`.

4.  **Profitability Guard**:
    - If configured, the `profitability_guard` checks if the strategy's recent performance (all-time or daily) meets the minimum P&L threshold.
    - Verified via `self._is_profitability_guard_passed(dir_key, mode)`.

5.  **Global Bypass (Grid Mode)**:
    - If `bypass_criteria_check` is `'immediately'` or `'ultra'`, activation and profitability guards are bypassed.
    - Requirement: Strategy/Product must exist in `grid_live.json`.
    - If `'immediately'`, the summary net P&L for that strategy/mode must be positive (`> 0`).

6.  **Archive Process Guard**:
    - New L-trades are blocked if `config.json` has `archive: true`.
    - Prevents race conditions during end-of-day archiving.

7.  **Group Daily Target Guard**:
    - Each `source_group` (e.g., `breakout`, `grid_live`) can have a `daily_target` (default `$400.00`).
    - If the closed P&L for the group today has reached this target, new L-trades are blocked.

8.  **Max Live Trades (Global/Group Cap)**:
    - `max_live_trades` (default `1`) limits the number of concurrent open live trades per `source_group`.
    - Includes a 30-second "memory cache" for trades sent but not yet persisted to disk.

9.  **TWS Routing Cap (NET Mode Only)**:
    - If mode is `'net'`, the number of open NET orders cannot exceed `max_trades_to_tws`.
    - This is a global cap across all products for TWS routing.

## Dependency
None

## Plan
- [ ] 1. Finalize the documentation of L-trade criteria into a formal reference (this task file serves as the primary record).
- [ ] 2. Update any related README or internal wiki if applicable (optional, pending user confirmation).
- [ ] 3. Verify that all listed criteria match the current version of `common.py`.

## Evidence
Objective-Delivery-Coverage: 100% (Criteria documented in task file)
Auto-Acceptance: true

- Evidence-Type: documentation
  - Artifact: `workstream\100_backlog\20260406_110500_breakout_document_l_trade_criteria.md`
  - Objective-Proved: Full criteria for L-trade generation captured and documented.
  - Status: captured

## Implementation Log
- 2026-04-06 11:05: Researched `common.py` and extracted full criteria details. Created backlog task.

## Changes Made
- Documented 9 specific criteria required for L-trade generation.

## Validation
- Criteria were extracted directly from `common.py` lines 980, 1156, 1175, 1272, 3010-3110.

## Risks/Notes
- These criteria are subject to change with future updates to `common.py`.
- Some guards (like Daily Target) are group-specific.

## Completion Status
Backlog
