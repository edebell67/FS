# Source
- User request in Codex thread on 2026-03-25 to correct BTC multiplier from `0.025` to `0.25`.

# Task Summary
Update breakout configuration so `pip_multiplier_by_product["BTC"]` is `0.25` instead of `0.025`.

# Context
- `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`

# Dependency
Dependency: None

# Plan
- [x] 1. Confirm the current BTC multiplier value in breakout config.
  - [x] Test: Read the `pip_multiplier_by_product` block in `config.json` and verify the existing BTC value.
  - [x] Evidence: Confirmed the pre-change BTC value was `0.025`.
- [x] 2. Update the BTC multiplier to the intended value.
  - [x] Test: Edit `config.json` so `pip_multiplier_by_product["BTC"]` equals `0.25`.
  - [x] Evidence: `config.json` now stores `"BTC": 0.25`.
- [x] 3. Verify the updated config value is present on disk.
  - [x] Test: Re-read the `pip_multiplier_by_product` block and confirm BTC now shows `0.25`.
  - [x] Evidence: Post-edit re-read confirmed `"BTC": 0.25`.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
  - Objective-Proved: Confirms the BTC multiplier was corrected from `0.025` to `0.25`.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
  - Objective-Proved: Confirms the active config currently stores `"BTC": 0.25`.
  - Status: captured

# Implementation Log
- 2026-03-25 23:59:41 Created lifecycle file for BTC multiplier correction.
- 2026-03-25 23:59:41 Confirmed the config block and updated BTC multiplier to `0.25`.
- 2026-03-26 00:00:00 Re-read the config block and verified the persisted value is `0.25`.

# Changes Made
- Updated `pip_multiplier_by_product["BTC"]` in `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json` from `0.025` to `0.25`.

# Validation
- Read the `pip_multiplier_by_product` block in `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`.
- Verified the current stored value is:
  - `"BTC": 0.25`

# Risks/Notes
- This changes BTC P&L scaling by 10x relative to the prior config value.
- Existing historical JSON outputs will remain as originally written; only future calculations that load this config will use `0.25`.

# Completion Status
Completed - 2026-03-26 00:00:00
