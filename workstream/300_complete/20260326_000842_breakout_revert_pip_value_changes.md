# Source
- User request in Codex thread on 2026-03-26 to revert any change relating to `pip_value`.

# Task Summary
Revert the unapproved `common.py` changes that made pip value resolve from `min_value_by_product`.

# Context
- `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`

# Dependency
Dependency: None

# Plan
- [x] 1. Identify the unapproved `pip_value`-related code changes in `common.py`.
  - [x] Test: Read the modified helper and the P&L calculation blocks to confirm the added `_get_pip_value()` path and substitutions.
  - [x] Evidence: Confirmed `common.py` contained a new `_get_pip_value()` helper and both strategy/v-trade P&L paths had been switched to it.
- [x] 2. Revert only the `pip_value`-related changes.
  - [x] Test: Remove `_get_pip_value()` and restore the original `PIP_VALUE` / `config.get('pip_value', 10.0)` references.
  - [x] Evidence: `common.py` now uses `gross_pnl_usd = gross_pnl * PIP_VALUE` and `_calculate_v_trade_pnl()` now uses `float(config.get('pip_value', 10.0))`.
- [x] 3. Verify the revert is complete.
  - [x] Test: Search `common.py` for `_get_pip_value` and inspect the restored code snippets.
  - [x] Evidence: No `_get_pip_value` symbol remains; the restored P&L code paths are present on disk.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - Objective-Proved: Confirms the unapproved `pip_value`-related edits were removed.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - Objective-Proved: Confirms the repo is back to the original global `PIP_VALUE` behavior for the affected code paths.
  - Status: captured

# Implementation Log
- 2026-03-26 00:08:42 Created lifecycle file for reverting the unapproved `pip_value` changes.
- 2026-03-26 00:08:42 Inspected `common.py` and confirmed the added `_get_pip_value()` helper and the substituted P&L references.
- 2026-03-26 00:08:42 Reverted the helper and restored the original `PIP_VALUE` / `config.get('pip_value', 10.0)` behavior.
- 2026-03-26 00:08:42 Verified the helper is gone and the restored code is present.

# Changes Made
- Reverted the added `_get_pip_value()` helper in `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`.
- Restored `BaseBreakoutStrategy.calculate_pnl()` to use `PIP_VALUE`.
- Restored `_calculate_v_trade_pnl()` to use `float(config.get('pip_value', 10.0))`.

# Validation
- Searched `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py` for `_get_pip_value` and confirmed it no longer exists.
- Re-read the strategy P&L block and confirmed:
  - `gross_pnl_usd = gross_pnl * PIP_VALUE`
  - `alt_gross_pnl_usd = alt_gross_pnl * PIP_VALUE`
  - `spread_cost_usd = spread_pips * PIP_VALUE`
- Re-read the virtual-trade P&L block and confirmed:
  - `pip_value = float(config.get('pip_value', 10.0))`

# Risks/Notes
- This revert only removed the unapproved `pip_value` changes in `common.py`.
- The separate BTC multiplier config change to `0.25` in `config.json` was not reverted because it is not a `pip_value` change.

# Completion Status
Completed - 2026-03-26 00:08:42
