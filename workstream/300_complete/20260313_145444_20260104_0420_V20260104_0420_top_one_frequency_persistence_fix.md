# Plan: Finalize top_one_frequency.py Persistence and Strategy Identification

## 1. Objective
- Ensure "UNKNOWN" strategies never appear.
- Prevent file overwriting/data loss (Persistence).
- Implement singleton execution (Lock file).
- Add robust error handling for file I/O.

## 2. Plan of Approach
1.  **Refine Extraction**: Treat "UNKNOWN" string in JSON as missing data and fallback to filename parsing. (Done in code)
2.  **Singleton Check**: Use a `.lock` file to prevent multiple instances from stomping on each other. (Done in code)
3.  **Robust Persistence**: 
    - `load_frequency` will now handle partial/corrupt files and empty strings gracefully.
    - `update_counts` will be strictly additive, appending new pairs and incrementing existing ones.
4.  **Logging**: Add clear logging for every load/save operation.
5.  **Clean Run**: Advise stopping all other Python instances.

## 3. List of Changes
- [x] **top_one_frequency.py**: 
    - [x] Add `LOCK_FILE` logic.
    - [x] Refine `load_frequency` to prevent data loss.
    - [x] Harden `strategy` extraction.
    - [x] Update version to `V20260104_0420`.
- [x] **constants.py**:
    - [x] Update version to `V20260104_0420`.

## 4. Confirmation
- [x] Verified that multiple instances cannot run.
- [x] Verified that strategy names are extracted correctly from filenames.
- [x] Verified that existing records are preserved and new ones appended.
