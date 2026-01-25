# Plan: Update `top_one_frequency.py` Output Path

This plan outlines the changes to move the `top_one_frequency.json` output file to a dynamic directory based on the run mode and current date.

## 1. Understanding of Requirements
The user wants `top_one_frequency.json` to be saved in `C:\Users\edebe\eds\TradeApps\breakout\json\{run mode}\{current date}` instead of the current working directory.

## 2. Plan of Approach
1.  **Update Version**: Change the version number in `constants.py` and `top_one_frequency.py` to `V20260104_0045`.
2.  **Modify `top_one_frequency.py`**:
    *   Update `load_frequency` to accept a `filepath` parameter.
    *   Update `save_frequency` to accept a `filepath` parameter.
    *   In `run_frequency_update`, calculate the target directory path using `run_mode` and `today_str`.
    *   Ensure the target directory exists using `os.makedirs` or `Path.mkdir`.
    *   Construct the full path to `top_one_frequency.json` in the target directory.
    *   Pass this path to `load_frequency` and `save_frequency`.
3.  **Verification**: Confirm that the file is created in the correct subfolder.

## 3. Checklist of Changes
- [x] Update `VERSION` in `C:\Users\edebe\eds\TradeApps\breakout\constants.py` to `V20260104_0045`.
- [x] Update `VERSION` in `C:\Users\edebe\eds\TradeApps\breakout\top_one_frequency.py` to `V20260104_0045`.
- [x] Modify `load_frequency` in `top_one_frequency.py` to accept `filepath`.
- [x] Modify `save_frequency` in `top_one_frequency.py` to accept `filepath`.
- [x] Update `run_frequency_update` in `top_one_frequency.py` to:
    - [x] Calculate `output_dir = Path("json") / run_mode / today_str`.
    - [x] Create `output_dir` if it doesn't exist.
    - [x] Use `output_dir / "top_one_frequency.json"` for loading and saving.
- [x] Verify that all changes have been implemented correctly.

## 4. Confirmation Plan
I will apply the changes and then check if the script runs and produces the file in the new location.
Note: I won't be able to easily "run" it and verify it's working without external data, but I will double-check the logic.

Date: 2026-01-04
Version: V20260104_0045
