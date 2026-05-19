# Source
- User request in Codex thread on 2026-03-26 to fix breakout P&L so product-specific valuation uses `min_move` and `min_value`, with front-loaded cost preserved.

# Task Summary
Replace the invalid global `pip_value` assumption for mixed product types with product-specific move valuation based on the user's stated formula:
`(price2 - price1) / min_move * min_value`, while keeping adhoc cost front-loaded.

# Context
- `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`

# Dependency
Dependency: None

# Plan
- [x] 1. Inspect current breakout config and code paths for `min_value_by_product`, `pip_multiplier_by_product`, and P&L calculation.
  - [x] Test: Search and read the current resolver and P&L code blocks.
  - [x] Evidence: Confirmed `min_value_by_product` exists and is resolved by `_min_value_for_product()`, but current P&L still uses global `PIP_VALUE`.
- [ ] 2. Confirm the intended source of `min_move` and the correct BTC values before editing.
  - [x] Test: Resolve the missing `min_move` definition and reconcile the repo values with the user's example.
  - [x] Evidence: User confirmed `min_move_by_product` is required; BTC config updated to `min_move_by_product["BTC"]=0.01` and `min_value_by_product["BTC"]=0.0025`.
- [x] 3. Implement the product-specific P&L formula in both strategy and virtual-trade paths, keeping front-loaded cost behavior intact.
  - [x] Test: Update `common.py` and config so product-specific USD conversion uses `min_move_by_product` + `min_value_by_product`, with fallback to the prior global path when product-specific values are absent.
  - [x] Evidence: Added `_min_move_for_product()` and `_pip_value_for_product()`; both strategy and virtual-trade P&L paths now use product-specific `pip_value`.
- [x] 4. Validate the revised arithmetic against a BTC example and record the exact calculations.
  - [x] Test: Run a deterministic check showing the BTC example computes the expected move value and that front-loaded cost remains applied.
  - [x] Evidence: For BTC with `min_move=0.01`, `min_value=0.0025`, and `pip_multiplier=0.25`, USD per internal pip is `1.0`; for `71259.62 -> 71459.62` SHORT, `gross_pnl_pips=-50`, `gross_usd=-50`, `net_return=-155`, `alt_net=-57`.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - Objective-Proved: Confirms the current P&L implementation still uses global `PIP_VALUE` and requires change.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
  - Objective-Proved: Confirms the current repo has `min_value_by_product` and `pip_multiplier_by_product`, but no explicit `min_move` field.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: User confirmed `min_move_by_product` should be added and front-loaded cost should remain.
  - Objective-Proved: Confirms the intended design basis for the P&L model update.
  - Status: captured
- Evidence-Type: user_feedback
  - Artifact: User confirmed on 2026-03-26 that the updated quantity separation is correct and requested moving the task to `300_complete` if completed.
  - Objective-Proved: Confirms the user accepted the separation of order sizing from `min_value_by_product` and approved completion.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - Objective-Proved: Confirms P&L now derives product-specific USD-per-pip from `min_move_by_product` and `min_value_by_product`.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
  - Objective-Proved: Confirms BTC config now includes `min_move_by_product["BTC"]=0.01` and `min_value_by_product["BTC"]=0.0025`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Deterministic PowerShell arithmetic check recorded in Validation.
  - Objective-Proved: Confirms the BTC example computes the expected USD-per-pip and preserves front-loaded cost.
  - Status: captured

# Implementation Log
- 2026-03-26 00:26:51 Created lifecycle file for fixing product-specific P&L valuation.
- 2026-03-26 00:26:51 Verified that `_min_value_for_product()` already exists, but `calculate_pnl()` and `_calculate_v_trade_pnl()` still convert using global `PIP_VALUE`.
- 2026-03-26 00:26:51 Verified the current repo has no `min_move` / tick-size field, so the exact formula cannot be implemented safely without clarifying the intended source of `min_move`.
- 2026-03-26 00:26:51 User confirmed `min_move_by_product` is required and cost remains front-loaded.
- 2026-03-26 00:26:51 Updated BTC config to use `min_value_by_product["BTC"]=0.0025` and added `min_move_by_product["BTC"]=0.01`.
- 2026-03-26 00:26:51 Added `_min_move_for_product()` and `_pip_value_for_product()` in `common.py`.
- 2026-03-26 00:26:51 Updated both strategy and virtual-trade P&L paths to use product-specific USD-per-pip while retaining fallback to the prior global `pip_value` path for products without `min_move_by_product`.
- 2026-03-26 00:26:51 Validated the BTC example numerically and preserved `2x` front-loaded adhoc cost behavior.
- 2026-03-26 00:26:51 Added crypto `min_move_by_product` entries for `ETH`, `SOL`, and `XRP` per user-provided values.
- 2026-03-26 00:26:51 Decoupled order sizing from `min_value_by_product` so exchange-derived tick values can be stored without altering quantity behavior.
- 2026-03-26 00:26:51 Populated non-crypto futures `min_move_by_product` and `min_value_by_product` values while leaving the user-provided crypto values intact.

# Changes Made
- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`:
  - `min_value_by_product["BTC"]`: `2.5e-05` -> `0.0025`
  - added `min_move_by_product["BTC"] = 0.01`
  - added `min_move_by_product["ETH"] = 0.01`
  - added `min_move_by_product["SOL"] = 0.01`
  - added `min_move_by_product["XRP"] = 0.0001`
  - updated futures tick-value config:
    - `CL`: `min_move=0.01`, `min_value=10.0`
    - `ES`: `min_move=0.25`, `min_value=12.5`
    - `HG`: `min_move=0.0005`, `min_value=12.5`
    - `NG`: `min_move=0.001`, `min_value=10.0`
    - `NQ`: `min_move=0.25`, `min_value=5.0`
    - `SI`: `min_move=0.005`, `min_value=25.0`
    - `YM`: `min_move=1.0`, `min_value=5.0`
- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`:
  - added `_min_move_for_product()`
  - added `_pip_value_for_product()`
  - changed `BaseBreakoutStrategy.calculate_pnl()` to use product-specific USD-per-pip
  - changed `_calculate_v_trade_pnl()` to use product-specific USD-per-pip
  - changed `_trade_quantity_for_product()` to stop deriving order size from `min_value_by_product`

# Validation
- Ran repository search for `min_value_by_product`, `pip_multiplier_by_product`, `min_move`, and current P&L conversion logic.
- Confirmed:
  - `config.json` contains `min_value_by_product` and `pip_multiplier_by_product`
  - `common.py` resolves `min_value_by_product` but does not use it for P&L conversion
  - `common.py` has no existing `min_move` resolver
- Post-change validation:
  - `config.json` now contains:
    - `min_value_by_product["BTC"] = 0.0025`
    - `min_move_by_product["BTC"] = 0.01`
    - `min_move_by_product["CL"] = 0.01`, `min_value_by_product["CL"] = 10.0`
    - `min_move_by_product["ES"] = 0.25`, `min_value_by_product["ES"] = 12.5`
    - `min_move_by_product["ETH"] = 0.01`
    - `min_move_by_product["HG"] = 0.0005`, `min_value_by_product["HG"] = 12.5`
    - `min_move_by_product["NG"] = 0.001`, `min_value_by_product["NG"] = 10.0`
    - `min_move_by_product["NQ"] = 0.25`, `min_value_by_product["NQ"] = 5.0`
    - `min_move_by_product["SI"] = 0.005`, `min_value_by_product["SI"] = 25.0`
    - `min_move_by_product["SOL"] = 0.01`
    - `min_move_by_product["XRP"] = 0.0001`
    - `min_move_by_product["YM"] = 1.0`, `min_value_by_product["YM"] = 5.0`
  - `common.py` now contains:
    - `_min_move_for_product()`
    - `_pip_value_for_product()`
    - product-specific USD conversion in both P&L paths
    - quantity calculation no longer depends on `min_value_by_product`
- Deterministic BTC check:
  - `btc_min_move=0.01`
  - `btc_min_value=0.0025`
  - `btc_multiplier=0.25`
  - `btc_usd_per_internal_pip=1`
  - For `entry=71259.62`, `exit=71459.62`, `SHORT`:
    - `gross_pnl_pips=-50`
    - `gross_usd=-50`
    - `net_return=-155`
    - `alt_net=-57`
- User verification requested:
  - Please verify that for BTC the new outcome is intended, especially the updated `alt_net=-57` for the sample trade under the corrected product-specific valuation model.
- User verification received:
  - User confirmed the updated quantity separation is correct.
  - User confirmed the task should move to `300_complete` as-is if completed.

# Risks/Notes
- The user's formula requires both `min_move` and `min_value`.
- Product-specific valuation now depends on `min_move_by_product` being configured correctly for each non-forex product that should not use the legacy global `pip_value`.
- Products without `min_move_by_product` continue to fall back to the prior global `pip_value` behavior.
- Order sizing is now separated from `min_value_by_product`, so future tick-value maintenance will not implicitly change `quantity`.

# Completion Status
Completed - 2026-03-26 00:26:51
