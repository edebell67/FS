# Plan - V20260123_0630 - Correct Master Summary Format & Track fs/ Library

## 1. Understanding of Requirements
- The user requested the `_summary_net.json` format to match 2026-01-22 exactly (removing the `meta` section).
- The user pointed out that GitHub does not have previous versions of the generator, indicating the `fs/` library should have been committed.

## 2. Plan of Approach
1.  **Format Fix**: Modify `fs/summary_net_generator.py` to remove the `meta` section from the output JSON.
2.  **Process Management**: Kill all stale background processes of `summary_net_generator.py` to ensure only the fixed code runs.
3.  **Git Tracking**:
    - Check git status of `breakout/fs/`.
    - Add logic files (Python, HTML, JS, CSS, MD) to the repository.
    - Exclude large data directories (like `json/`) to prevent repository bloat.
4.  **Verification**:
    - Trigger the generator manually.
    - Verify `_summary_net.json` format for today matches yesterday's structure.
    - Verify file tracking in Git.

## 3. List of Changes
- `fs/summary_net_generator.py`:
    - [x] Remove `meta` section from `output` dictionary. (2026-01-23 04:55)
- `fs/constants.py`:
    - [x] Update version to `V20260123_0630`. (2026-01-23 06:30)
- `Git Repository`:
    - [x] Track `breakout/fs/` core library files. (2026-01-23 07:15)

## 4. Verification Results
- [x] `_summary_net.json` for 2026-01-23 contains `last_update` and `strategies` only.
- [x] Multiple stale processes (PIDs 10388, 37560, 34728, 8424) killed.
- [x] `git ls-files` confirms `breakout/fs/summary_net_generator.py` is now tracked.
- [x] Today's Master Summary successfully generated with full strategy depth.
