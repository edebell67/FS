# Plan for Modifying Trade Filename Format (2026-01-08)

## 1. Understanding of Requirements
The user wants to insert `{direction}` between `{product}` and `{datetime}` in the trade JSON filename format.
New format: `{strategy name}_{product}_{direction}_{datetime}_{strategy parameters}.json`
This change must be permanent for future files, and existing files in `eds\TradeApps\breakout\json\live` (and simulation folders) must be renamed to match.

## 2. Plan of Approach
1.  **Code Modification**:
    *   Modify `TradeApps/breakout/common.py`:
        *   Update `BaseBreakoutStrategy._generate_trade_filename` to accept `direction` and include it in the returned string.
        *   Update `BaseBreakoutStrategy.enter_trade` to pass `direction` to `_generate_trade_filename`.
    *   Modify `TradeApps/breakout/breakout_Rev.py`:
        *   Update the manual `self.open_trade` initialization to pass `signal` (direction) to `_generate_trade_filename`.
2.  **Migration Tool**:
    *   Create a one-time migration script `TradeApps/breakout/migrate_trade_filenames.py`:
        *   Recurse through `eds/TradeApps/breakout/json/live` and `eds/TradeApps/breakout/json/sim`.
        *   For each `.json` file that doesn't already have a direction badge (LONG/SHORT):
            *   Read the file content to extract `direction`.
            *   Rename the file to the new format.
            *   Update the `json_filename` field *inside* the JSON to match the new filename.
3.  **Version Update**:
    *   Update `constants.py` with version `V20260108_1630`.
4.  **Verification**:
    *   Run the migration script and verify filenames in `2026-01-08`.
    *   Check for orphans or broken references.

## 3. Check List of Changes
*   [ ] Modify `TradeApps/breakout/common.py`:
    *   [ ] Update `_generate_trade_filename` signature and logic.
    *   [ ] Update `enter_trade` call to `_generate_trade_filename`.
*   [ ] Modify `TradeApps/breakout/breakout_Rev.py`:
    *   [ ] Update call to `_generate_trade_filename` with `signal`.
*   [ ] Create and run `TradeApps/breakout/migrate_trade_filenames.py`.
*   [ ] Modify `TradeApps/breakout/constants.py`:
    *   [ ] Update `VERSION` to `V20260108_1630`.

## 4. Confirmation Plan
*   Verify that new trades created by standard strategies (`breakout.py`, `breakout_R.py`, etc.) include `LONG` or `SHORT` in the filename.
*   Verify that `breakout_Rev.py` trades also include the direction badge.
*   Check that `2026-01-08` folder has files like `..._AUD_SHORT_20260108...`.
