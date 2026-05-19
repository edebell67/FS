# Restore _top20.json Generation in Summary Generator [2026-03-12]

## 1. Understanding of Requirements
Recent optimizations to `summary_net_generator.py` (V20260311_1730) accidentally omitted the logic to generate `_top20.json`. This file is critical for the "Top X Multi-Chart Loader" workflow and other dashboard features. The file exists on disk but is stale (updated only at midnight by potentially residual processes or a one-off run).

## 2. Plan of Approach
1. **Analyze existing data in `SummaryGenerator`**: All necessary metrics (net, buy/sell totals, counts, percentages) are already tracked in `self.totals`.
2. **Implement Top 20 Logic**:
    * Extract all `(strategy, product)` combinations from `self.totals` for the current mode/date.
    * Map them to the `_top20.json` format.
    * Sort by `total_net` (descending).
    * Take the top 20 entries.
3. **Write File**: Add a third `atomic_write_json` call to `process_date` to save `_top20.json`.
4. **Update Version**: Bump version to `V20260312_2315` in `constants.py` and `summary_net_generator.py`.
5. **Verify**: Run the generator and check that `_top20.json` is updated with current timestamps and data.

## 3. List of Changes
* **`TradeApps/breakout/fs/summary_net_generator.py`**:
    * [x] Implement `_top20.json` construction in `process_date` (lines 415-442).
    * [x] Add `atomic_write_json` call for `_top20.json` (line 448).
    * [x] Update `VERSION` to `V20260312_2315` (line 15).
* **`TradeApps/breakout/fs/constants.py`**:
    * [x] Update `VERSION` to `V20260312_2315`.

## 4. Progress Tracking
- [x] Create Task File (Done)
- [x] Implement Code Changes
- [x] Verify Updates

## 5. Post-Implementation Modification [2026-03-13]
- [x] Increased output from 20 to 200 items (line 441: `top_20_candidates[:200]`)
- [x] Kept key name as `"top20"` for backward compatibility
- [x] Added comment explaining the 200 item output

## Completion Status
- Complete - 2026-03-13 15:20 Europe/London
