# Plan: Fix Tie-Breaking in Auto-Activation (V20251223_1330)

## 1. Understanding of Requirements
The auto-activation logic currently activates multiple strategies when they share the exact same top P&L, despite `top_n_strategies` being set to `1` in `config.json`. The goal is to ensure that only `top_n` strategies are activated, even in cases of ties, by introducing a deterministic tie-breaking mechanism.

## 2. Plan of Approach
1.  **Update Configuration**: Increment the version number in `constants.py`.
2.  **Modify `common.py`**:
    *   Adjust the sorting of `net_candidates_raw` and `alt_candidates_raw` to include a secondary sort key (strategy name) for deterministic tie-breaking.
    *   Ensure that exactly `slots_to_fill` strategies are selected after sorting.
3.  **Update Documentation**: Document the change in `CHANGELOG.md`.
4.  **Verify**: Confirm that only one strategy is active in `activations.json` after the change.

## 3. List of Changes

*   [x] **`TradeApps/breakout/constants.py`**:
    *   Update `VERSION` to `"V20251223_1330"`.

*   [x] **`TradeApps/breakout/common.py`**:
    *   In `_perform_auto_activation_check`, locate the `net_candidates_raw.sort` line.
    *   Change `net_candidates_raw.sort(key=lambda x: x['pnl'], reverse=True)` to `net_candidates_raw.sort(key=lambda x: (x['pnl'], x['key']), reverse=True)`.
    *   Locate the `alt_candidates_raw.sort` line.
    *   Change `alt_candidates_raw.sort(key=lambda x: x['pnl'], reverse=True)` to `alt_candidates_raw.sort(key=lambda x: (x['pnl'], x['key']), reverse=True)`.
    *   Add versioned comments with the new version number and timestamp.

*   [x] **`TradeApps/breakout/CHANGELOG.md`**:
    *   Add a new section `[V20251223_1330] - 2025-12-23`.
    *   Add item for "Fixed auto-activation tie-breaking to ensure only `top_n` strategies are activated, even with identical P&L values."

## 4. Verification Plan
- Run the Trade Viewer application (if not already running).
- Check `activations.json` to confirm that only one strategy is marked as `active: true` for auto-activated slots.