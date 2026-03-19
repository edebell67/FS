# Plan: Optimized Summary Net Generator UI Sync [V20260123_0415]

This plan outlines the replacement of the existing `summary_net_generator.py` with a highly optimized version that leverages file-state flags (`_cld.json`) and memory caching to ensure fast UI updates regardless of trade volume.

## 1. Understanding of Requirements
- **Format Parity**: Must produce `_summary_net.json` with the exact keys (`strategies`, `last_update`, `t`, `net`, `buyPercent`, etc.) required by the dashboard.
- **Performance**: Must avoid re-processing closed trades. Once a trade is closed and accounted for, it should be "marked as done."
- **Real-time**: Open trades (`_op.json`) must be integrated into the timeline dynamically on every cycle.

## 2. Plan of Approach
1.  **State Management**:
    - Build a memory cache that stores the "Closed-Only" cumulative P&L for each Strategy/Product pair.
    - On startup, scan for any existing `_cld.json` files to bootstrap the cache.
2.  **The Loop (Every 30s)**:
    - **Step A (Process New Closures)**: Look for any `_cl.json` files. Add their P&L to the cache and rename them to `_cld.json`.
    - **Step B (Snapshot Open Trades)**: Look for all `_op.json` files. 
    - **Step C (Merge)**: Deep-copy the "Closed Cache," append the "Open Snapshot" to the ends of the relevant timelines, and sort by timestamp.
    - **Step D (Atomic Write)**: Write the result to `_summary_net.json`.
3.  **Robustness**:
    - Handle `live` and `sim` modes concurrently.
    - Clean up orphaned `.tmp` files.
    - Robust timestamp parsing to prevent sorting errors.

## 3. List of Changes
- [x] **`fs/summary_net_generator.py`**: 
    - [ ] Implement `SummaryGenerator` class with internal caching.
    - [ ] Add `_cld.json` renaming logic.
    - [ ] Add Win Rate (`buyPercent`/`sellPercent`) logic.
    - [ ] Ensure atomic JSON writes.
- [x] **`fs/Constants.py`**: 
    - [ ] Update VERSION to `V20260123_0415`.

## 4. Verification Plan
- Run the script and check `summary_gen_debug.log`.
- Verify `_cl.json` files are being renamed to `_cld.json`.
- Verify `_summary_net.json` contains cumulative data for both closed and open trades.
- Verify dashboard graph updates correctly.
