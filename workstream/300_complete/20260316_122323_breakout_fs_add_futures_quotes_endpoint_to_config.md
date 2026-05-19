# Task: Add futures quotes endpoint to live and sim config

## Source
- User request on 2026-03-16 to add futures endpoint to config for live and sim: `http://127.0.0.1:8002/api/vw_000_futures_quotes`

## Task Summary
- Update the FS runtime config so both `live` and `sim` endpoint lists include the futures quotes endpoint.

## Context
- `TradeApps/breakout/fs/config.json`

## Plan
- [x] 1. Add the futures endpoint to both `live` and `sim` endpoint arrays.
  - [x] Test: patch `TradeApps/breakout/fs/config.json` to include the requested futures URL under both run modes.
  - [x] Evidence: `TradeApps/breakout/fs/config.json` now contains `http://127.0.0.1:8002/api/vw_000_futures_quotes` once in `live` and once in `sim`.
- [x] 2. Validate the config file and confirm the inserted entries.
  - [x] Test: run JSON parse validation and a targeted search for the futures endpoint.
  - [x] Evidence: JSON parse validation passed and `rg` returned two matches in `config.json`.

## Implementation Log
- 2026-03-16 12:23:23 Created task from user request.
- 2026-03-16 12:26:00 Added the futures quotes endpoint to both `live` and `sim` endpoint arrays in `TradeApps/breakout/fs/config.json`.
- 2026-03-16 12:27:00 Validated the JSON file and confirmed both inserted entries with `rg`.

## Changes Made
- Updated `TradeApps/breakout/fs/config.json`:
  - Added `http://127.0.0.1:8002/api/vw_000_futures_quotes` to `endpoints.live`
  - Added `http://127.0.0.1:8002/api/vw_000_futures_quotes` to `endpoints.sim`

## Validation
- `python -c "import json, pathlib; json.load(open(r'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\config.json', 'r', encoding='utf-8')); print('config_json_valid=true')"`
  - Result: `config_json_valid=true`
- `rg -n "vw_000_futures_quotes" TradeApps\breakout\fs\config.json`
  - Result:
    - `31:            "http://127.0.0.1:8002/api/vw_000_futures_quotes"`
    - `36:            "http://127.0.0.1:8002/api/vw_000_futures_quotes"`

## Evidence
- Objective-Delivery-Coverage: 100%
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
  - Objective-Proved: Both `live` and `sim` config arrays contain the requested futures endpoint.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `config_json_valid=true`
  - Objective-Proved: The edited config remains valid JSON.
  - Status: captured

## Risks/Notes
- This repository stores both `live` and `sim` quote endpoint arrays in `config.json`; there is no separate `config.sim.json` file present in `TradeApps/breakout/fs`.

## Completion Status
- Complete - 2026-03-16 12:27 GMT
