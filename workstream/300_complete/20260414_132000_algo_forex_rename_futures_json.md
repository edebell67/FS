# Task: Rename Futures JSON Output to Index Prices

## Status
- [x] **100_todo**: Task created
- [x] **200_inprogress**: Work started
- [x] **300_complete**: Task finished

## Metadata
- **Source**: User Request
- **Task Type**: standard
- **Destination Folder**: algo_forex/prices/
- **Dependency**: 20260414_125500_algo_forex_futures_json_output.md

## Task Summary
Change the constant `FUTURES_JSON_FILENAME` to `INDEX_JSON_FILENAME` and update the filename from `futures_prices.json` to `index_prices.json` in `tws_fetch_bid_ask5d.py`.

## Context
- `algo_forex/tws_fetch_bid_ask5d.py`: Main script for fetching and saving prices.

## Plan
- [x] 1. Update `FUTURES_JSON_FILENAME` to `INDEX_JSON_FILENAME = 'index_prices.json'` in `tws_fetch_bid_ask5d.py`.
  - Test: Check if constant is renamed correctly.
  - Evidence: Constant is now `INDEX_JSON_FILENAME`.
- [x] 2. Update all references in `write_prices_to_json` to use the new constant.
  - Test: Verify the JSON output function uses the new name.
  - Evidence: `write_prices_to_json` updated and verified.
- [x] 3. Verify the script generates `index_prices.json` instead of `futures_prices.json`.
  - Test: Run standalone test script.
  - Evidence: `index_prices.json` created successfully; `futures_prices.json` removed.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `algo_forex/prices/index_prices.json`
  - Objective-Proved: File name changed correctly.
  - Status: captured

- Evidence-Type: diff
  - Artifact: `algo_forex/tws_fetch_bid_ask5d.py`
  - Objective-Proved: Constant and logic updated.
  - Status: captured

## Implementation Log
- 2026-04-14 13:20: Created task file in `100_todo`.
- 2026-04-14 13:22: Moved to `200_inprogress`.
- 2026-04-14 13:25: Renamed constant and updated references in `tws_fetch_bid_ask5d.py`.
- 2026-04-14 13:28: Deleted old `futures_prices.json` and verified `index_prices.json` generation.

## Changes Made
- Modified `algo_forex/tws_fetch_bid_ask5d.py`:
  - `FUTURES_JSON_FILENAME` -> `INDEX_JSON_FILENAME = 'index_prices.json'`.
  - Updated `write_prices_to_json` function and log messages.

## Validation
- Ran `test_rename_output.py` which confirmed creation of `index_prices.json`.
- Manually deleted `futures_prices.json`.

## Risks/Notes
- None.

## Completion Status
- **Status**: COMPLETE
- **Timestamp**: 2026-04-14 13:30
