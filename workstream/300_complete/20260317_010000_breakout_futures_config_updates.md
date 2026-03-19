# Task: Configure Futures Multipliers and Min Values

`Source`: `C:\Users\edebe\eds\plans\20260317_0100_V20260317_0100_Futures_Config_Updates.md`
`Task Summary`: Update config.json with accurate multipliers and min values for futures products (CL, ES, NQ, YM, SI, HG, NG) to ensure correct P&L calculations and price tracking.
`Context`: `TradeApps\breakout\fs\config.json`, `TradeApps\breakout\fs\constants.py`
`Dependency`: None

## Plan
- [x] 1. Update `config.json` with new multipliers, min values, and product types.
  - [x] Test: Check `config.json` for new keys and correct values.
  - [x] Evidence: `config.json` updated with individual multipliers for CL, ES, NQ, YM, SI, HG, NG.
- [x] 2. Update version in `constants.py`.
  - [x] Test: Check `VERSION` is `V20260317_0100`.
  - [x] Evidence: `constants.py` updated.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `TradeApps\breakout\fs\config.json`
  - Objective-Proved: Per-product multipliers and min values configured.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `TradeApps\breakout\fs\constants.py`
  - Objective-Proved: Version bumped to V20260317_0100.
  - Status: captured

## Implementation Log
- 2026-03-17 00:52: Updated `config.json` with `min_value_by_product`, `pip_multiplier_by_product`, `product_type_by_product`, and `trade_products` for futures.
- 2026-03-17 01:00: Updated `constants.py` to `V20260317_0100`.

## Changes Made
- `TradeApps\breakout\fs\config.json`: Added/Updated futures configurations (CL, ES, NQ, YM, SI, HG, NG).
- `TradeApps\breakout\fs\constants.py`: Updated `VERSION` to `V20260317_0100`.

## Validation
- Verified `config.json` has `SI` in `trade_products`.
- Verified `HG` and `SI` are under `metals` in `product_type_by_product`.
- Verified multipliers: CL=100, ES=5, NQ=2, YM=0.5, SI=500, HG=2500, NG=1000.
- Verified min_values match tick sizes.

## Risks/Notes
- None

## Completion Status
**COMPLETE** - 2026-03-17 01:05
