# Source
- User request in Codex thread on 2026-03-25 to verify whether `product_type_cost` was applied correctly in breakout code and in a BTC `*_cld.json` output.

# Task Summary
Verify the current breakout implementation of `product_type_cost` against the completed workstream note from 2026-03-23 and inspect a BTC cloud JSON file to confirm whether the cost deduction is reflected in output data.

# Context
- `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py`
- `C:\Users\edebe\eds\tests\_tmp_regen_probe\json\sim\crypto\2026-03-15\breakout_2_tp10.0_sl30.0_2771ab55_BTC_20260315_040537_2_0.00015_10.0_30.0_cld.json`
- `C:\Users\edebe\eds\workstream\300_complete\20260323_191500_breakout_add_product_type_cost_config.md`

# Dependency
Dependency: None

# Plan
- [x] 1. Read the completed workstream note and inspect the current breakout code/config for `product_type_cost` usage.
  - [x] Test: `rg -n "product_type_cost|calculate_pnl|_calculate_v_trade_pnl|product_type_for_product" C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\config.json C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py` returns the relevant code references.
  - [x] Evidence: Located config entry in `config.json` and deduction logic in both `calculate_pnl` and `_calculate_v_trade_pnl`; current code also shows a later `V20260325_0500` change doubling the adhoc cost.
- [x] 2. Locate a BTC `*_cld.json` file and compare its P&L fields to expected cost behavior.
  - [x] Test: Open a BTC `*_cld.json` file and compare `gross_pnl_pips`, `net_return`, and `alt_net` with the active config assumptions.
  - [x] Evidence: Sample file dated `2026-03-15` shows `gross_pnl_pips=10.0000000384`, `net_return=95.0000003842`, `alt_net=-125.0000003842`, which matches commission/spread-only behavior and not the current crypto `product_type_cost=50`.
- [x] 3. Record the verification result and conclusion.
  - [x] Test: Summarize whether the current code and available BTC output data are aligned.
  - [x] Evidence: Conclusion recorded below: code wiring exists, but the sampled BTC `*_cld.json` predates the feature and therefore does not prove current cost application in generated outputs.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - Objective-Proved: Confirms `product_type_cost` lookup is implemented for both standard and virtual trade P&L paths.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
  - Objective-Proved: Confirms active config currently defines `product_type_cost` values including `crypto: 50` and `forex: 5`.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\tests\_tmp_regen_probe\json\sim\crypto\2026-03-15\breakout_2_tp10.0_sl30.0_2771ab55_BTC_20260315_040537_2_0.00015_10.0_30.0_cld.json`
  - Objective-Proved: Confirms the sampled BTC cloud JSON does not include the later product-type cost deduction in its stored P&L output.
  - Status: captured

# Implementation Log
- 2026-03-25 23:37:21 Created verification task file and gathered references from the completed 2026-03-23 workstream note.
- 2026-03-25 23:37:21 Verified current code paths in `common.py` and current config values in `config.json`.
- 2026-03-25 23:37:21 Located BTC `*_cld.json` samples under `tests\_tmp_regen_probe\json\sim\crypto\2026-03-15`.
- 2026-03-25 23:37:21 Compared one BTC sample file against current config expectations and recorded the mismatch in timeline and behavior.
- 2026-03-25 23:38:00 Opened live BTC cloud JSON `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\crypto\2026-03-25\breakout_2_tp3.0_sl5.0_0d241493_BTC_20260325_093358_2_0.00015_3.0_5.0_cld.json` and confirmed current adhoc cost behavior is present in stored output.

# Changes Made
- No product code changes.
- Added this lifecycle verification document.

# Validation
- Ran `rg -n "product_type_cost|calculate_pnl|_calculate_v_trade_pnl|product_type_for_product" C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\config.json C:\Users\edebe\eds\TradeApps\breakout\fs\constants.py`.
- Opened relevant sections of `common.py`, `config.json`, and `constants.py`.
- Located BTC `*_cld.json` files with `rg --files C:\Users\edebe\eds | rg -i "btc.*cld|cld.*btc|btccld|xbt.*cld|cld.*xbt|btc.*cloud|cloud.*btc"`.
- Opened `C:\Users\edebe\eds\tests\_tmp_regen_probe\json\sim\crypto\2026-03-15\breakout_2_tp10.0_sl30.0_2771ab55_BTC_20260315_040537_2_0.00015_10.0_30.0_cld.json`.
- Result:
  - Current code does apply `product_type_cost`.
  - Current code returns `total_adhoc_cost = adhoc_cost_usd * 2`, which is a later behavior than the 2026-03-23 workstream summary described.
  - The sampled BTC cloud JSON is dated 2026-03-15, before the feature was added, so it does not show the cost deduction.
  - No newer post-2026-03-23 BTC `*_cld.json` sample was found in `tests\_tmp_regen_probe\json`.
  - User supplied live BTC sample `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\crypto\2026-03-25\breakout_2_tp3.0_sl5.0_0d241493_BTC_20260325_093358_2_0.00015_3.0_5.0_cld.json`.
  - That file contains `"adhoc_cost_usd": 100.0`, which matches current config `crypto: 50` multiplied by the current code path's `2x` rule.
  - Its stored P&L values are internally consistent with the live code:
    - `gross_pnl_pips = -5.0` -> gross USD `-50`
    - `net_return = -155.0` -> `-50 - 5 commission - 100 adhoc`
    - `alt_net = -75.0` -> `+50 - 5 commission - 20 spread - 100 adhoc`

# Risks/Notes
- The current repo state has diverged from the 2026-03-23 completed workstream note: config values are no longer all zero, version is now `V20260325_1300`, and both P&L functions now deduct double the configured adhoc cost.
- The BTC sample used for validation predates the feature, so it cannot confirm the current runtime output end-to-end.
- A fresh BTC `*_cld.json` generated after 2026-03-23 would be needed to fully confirm output behavior against the live code.
- The user-provided live BTC JSON now provides that post-change confirmation and shows the repo is operating with the current `2x` adhoc-cost behavior rather than the original `1x` interpretation from the 2026-03-23 note.

# Completion Status
Completed - 2026-03-25 23:37:21
