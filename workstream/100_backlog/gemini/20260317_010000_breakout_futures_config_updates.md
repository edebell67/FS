# Task: Configure Futures Multipliers and Min Values

`Source`: `C:\Users\edebe\eds\plans\20260317_0100_V20260317_0100_Futures_Config_Updates.md`
`Task Summary`: Update config.json with accurate multipliers and min values for futures products (CL, ES, NQ, YM, SI, HG, NG) to ensure correct P&L calculations and price tracking.
`Context`: `TradeApps\breakout\fs\config.json`, `TradeApps\breakout\fs\constants.py`
`Dependency`: None

## Plan
- [ ] 1. Update `config.json` with new multipliers, min values, and product types.
  - Test: Check `config.json` for new keys and correct values.
  - Evidence: `config.json` updated with individual multipliers for CL, ES, NQ, YM, SI, HG, NG.
- [ ] 2. Update version in `constants.py`.
  - Test: Check `VERSION` is `V20260317_0100`.
  - Evidence: `constants.py` updated.

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `TradeApps\breakout\fs\config.json`
  - Objective-Proved: Per-product multipliers and min values configured.
  - Status: planned
- Evidence-Type: file_output
  - Artifact: `TradeApps\breakout\fs\constants.py`
  - Objective-Proved: Version bumped to V20260317_0100.
  - Status: planned

## Implementation Log
- (Awaiting start)

## Changes Made
- (Awaiting start)

## Validation
- (Awaiting start)

## Risks/Notes
- None

## Completion Status
**PENDING**


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
