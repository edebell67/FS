# Plan: Update top_one_frequency.py Strategy Identification and Output Path

This plan outlines the changes to `top_one_frequency.py` to support dynamic output paths based on `run_mode` and fix strategy identification logic to prevent "UNKNOWN" entries.

## 1. Understanding of Requirements
- The user wants `top_one_frequency.py` to output its frequency tally to:
    - `C:\Users\edebe\eds\TradeApps\breakout\json\sim\{current date}` if `run_mode` is 'SIM'.
    - `C:\Users\edebe\eds\TradeApps\breakout\json\live\{current date}` if `run_mode` is 'Live'.
- The user reported "UNKNOWN" strategies in the output. This is because some trade files (like SIM trades) do not have the `source_strategy` key in the JSON, so the strategy must be derived from the filename.

## 2. Plan of Approach
1.  **Absolute Paths**: Convert relative paths to absolute paths using the project root.
2.  **Run Mode Logic**: Load `run_mode` from `config.json`, lowercase it, and use it in the directory construction.
3.  **Trade File Lookup**: Adjust search pattern to find `breakout_*.json` files in the daily directory.
4.  **Strategy Identification Fix**: Implement fallback logic to parse the strategy name from the filename if the `source_strategy` key is missing in the JSON data.
5.  **Logging**: Ensure the script logs where it is writing and which files it found.

## 3. List of Changes
- [x] **top_one_frequency.py**: 
    - [x] Update `CONFIG_FILE` path to absolute.
    - [x] Update `run_frequency_update` to use absolute paths for the output directory.
    - [x] Change `base_dir` to the daily folder and pattern to `breakout_*.json`.
    - [x] Implement fallback strategy name extraction from filename.
    - [x] Increment version to `V20260104_0345`.
- [x] **constants.py**:
    - [x] Increment version to `V20260104_0345`.

## 4. Confirmation
- [x] Verified that `json/sim/2026-01-04` contains `breakout_*.json` files.
- [x] Verified that `_top_one_frequency.json` now contains correctly identified strategy names (e.g., `breakout_Rev_2_tp10.0_sl10.0`).
- [x] Confirmed the script uses the correct `sim` or `live` subfolder based on `config.json`.
