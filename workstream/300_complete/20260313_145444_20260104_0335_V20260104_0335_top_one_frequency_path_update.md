# Plan: Update top_one_frequency.py Output Path and Data Source

This plan outlines the changes to `top_one_frequency.py` to support dynamic output paths based on `run_mode` and fix the trade file lookup.

## 1. Understanding of Requirements
The user wants `top_one_frequency.py` to output its frequency tally to:
- `C:\Users\edebe\eds\TradeApps\breakout\json\sim\{current date}` if `run_mode` is 'SIM'.
- `C:\Users\edebe\eds\TradeApps\breakout\json\live\{current date}` if `run_mode` is 'Live'.

## 2. Plan of Approach
1.  **Absolute Paths**: Convert relative paths to absolute paths using the project root.
2.  **Run Mode Logic**: Load `run_mode` from `config.json`, lowercase it, and use it in the directory construction.
3.  **Trade File Lookup**: Adjust search pattern to find `breakout_*.json` files in the daily directory, as no `virtual` subfolder exists in the current SIM output.
4.  **Logging**: Ensure the script logs where it is writing and which files it found.

## 3. List of Changes
- [x] **top_one_frequency.py**: 
    - [x] Update `CONFIG_FILE` path.
    - [x] Update `run_frequency_update` to use absolute paths for the output directory.
    - [x] Change `base_dir` to the daily folder and pattern to `breakout_*.json`.
    - [x] Increment version to `V20260104_0335`.

## 4. Confirmation
- Verified that `json/sim/2026-01-04` contains `breakout_*.json` files.
- Verified that `config.json` contains the `run_mode` key.
