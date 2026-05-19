# Plan: Fix Strategy Performance Data Display (V20260120_0430)

This plan addresses the issue where the Strategy Performance screen displays no data.

## 1. Understanding of Requirements
The Strategy Performance screen is empty for the current date (2026-01-20). The `DATA_SOURCE` is set to `"database"`, but the PostgreSQL `trades` table is empty for today. Investigation revealed that `backfill_trades.py`, which synchronizes JSON trade files to the database, has hardcoded dates that exclude today.

## 2. Plan of Approach
1.  **Modify `backfill_trades.py`**: Remove the hardcoded dates from the default configuration to allow processing of the current date and all other available date folders.
2.  **Update Versioning**: Increment the version number in `constants.py` to `V20260120_0430`.
3.  **Execute Sync**: Run the `backfill_trades.py` script to populate the database with today's trade data.
4.  **Verification**: 
    *   Confirm rows are present in the `trades` table for `2026-01-20`.
    *   Open the Strategy Performance screen in the browser to ensure data is displayed correctly.

## 3. List of Changes

### `backfill_trades.py`
- [ ] Modify line 20: Change default `BACKFILL_DATES` to an empty string to allow processing all dates by default.
- [ ] Add comments with timestamp and version tag.

### `constants.py`
- [ ] Update `VERSION` to `"V20260120_0430"`.

## 4. Execution Steps
1.  Apply code changes to `backfill_trades.py`.
2.  Update version in `constants.py`.
3.  Run `python backfill_trades.py` (one-off execution to sync, then let it run or suggest user keeps it running).
4.  Check DB count for today.
5.  Open browser and navigate to `strategy_performance.html`.
