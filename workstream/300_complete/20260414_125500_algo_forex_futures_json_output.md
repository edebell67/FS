# Task: Output Futures Prices to Separate JSON

## Status
- [x] **100_todo**: Task created
- [x] **200_inprogress**: Work started
- [x] **300_complete**: Task finished

## Metadata
- **Source**: User Request
- **Task Type**: standard
- **Destination Folder**: algo_forex/prices/
- **Dependency**: None

## Task Summary
Modify `tws_fetch_bid_ask5d.py` to output futures products to `futures_prices.json` in the `prices/` folder. The format should be consistent with the existing `forex_prices.json` but focused on futures data.

## Context
- `algo_forex/tws_fetch_bid_ask5d.py`: Main script for fetching and saving prices.
- `algo_forex/prices/`: Output directory for JSON and CSV files.

## Plan
- [x] 1. Define `FUTURES_JSON_FILENAME = 'futures_prices.json'` in `tws_fetch_bid_ask5d.py`.
  - Test: Check if constant is defined correctly.
  - Evidence: File content diff shows `FUTURES_JSON_FILENAME` added to File Settings.
- [x] 2. Update/Add JSON writing logic to produce the separate futures file.
  - Test: Verify `write_prices_to_json` handles the second file.
  - Evidence: `write_prices_to_json` updated to write both `forex_prices.json` and `futures_prices.json`.
- [x] 3. Ensure the output format for `futures_prices.json` matches the `forex_prices.json` structure (timestamp + data keys).
  - Test: Run the script and inspect `futures_prices.json`.
  - Evidence: Standalone test `test_json_output.py` confirmed keys: `['timestamp', 'futures']`.
- [x] 4. Verify both `forex_prices.json` and `futures_prices.json` are updated correctly in the main loop.
  - Test: Run script, check timestamps and data in both files.
  - Evidence: Test script output confirmed both files created with correct data counts.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `algo_forex/prices/futures_prices.json`
  - Objective-Proved: Futures data is saved to the correct separate file.
  - Status: captured

- Evidence-Type: diff
  - Artifact: `algo_forex/tws_fetch_bid_ask5d.py`
  - Objective-Proved: Script logic updated to support dual JSON output.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `algo_forex/test_json_output.py` execution output
  - Objective-Proved: JSON structure and file creation verified.
  - Status: captured

## Implementation Log
- 2026-04-14 12:55: Created task file in `100_todo`.
- 2026-04-14 12:58: Moved to `200_inprogress`.
- 2026-04-14 13:02: Added `FUTURES_JSON_FILENAME` constant.
- 2026-04-14 13:05: Updated `write_prices_to_json` logic.
- 2026-04-14 13:10: Verified with standalone test script.

## Changes Made
- Modified `algo_forex/tws_fetch_bid_ask5d.py`:
  - Added `FUTURES_JSON_FILENAME = 'futures_prices.json'`.
  - Updated `write_prices_to_json` to write `futures_data` to the new separate file in addition to the combined file.

## Validation
- Successfully executed `test_json_output.py` which confirmed:
  - `forex_prices.json` still contains all data (forex, synthetic, futures).
  - `futures_prices.json` is created with `timestamp` and `futures` data.
  - All paths are correctly resolved relative to the script directory.

## Risks/Notes
- None.

## Completion Status
- **Status**: COMPLETE
- **Timestamp**: 2026-04-14 13:15
