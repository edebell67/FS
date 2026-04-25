# Task: Refine Grid History Update Rules

## Status
- **Status:** COMPLETED
- **Created:** 2026-04-24 23:05:00
- **Completed:** 2026-04-24 23:25:00
- **Project:** Breakout
- **Priority:** High

## Objective
Refine the conditions under which `grid_live_history` is updated to ensure only meaningful state changes are recorded.

## Implementation (2026-04-24)
- **Change Detection**: Upgraded `_archive_grid_live` to compare the `old_state` with `new_data`. (V20260424_2310)
- **Filtered Archiving**: The system now only records history if:
    - A strategy/model changes its **Product**.
    - A strategy/model changes its **Metric**.
    - A strategy is **Added** or **Removed** from the grid.
    - A trade bucket is **Deleted** (forced archive).
- **Suppressed Updates**: History updates are now suppressed for:
    - Adding new trade buckets (unless they immediately trigger a leadership promotion).
    - Changes to non-critical fields like `current_total_net`.
    - Redundant periodic sweeps where the product/metric mapping remains identical.

## Impact
This change, combined with the previous 60s throttling, will reduce the frequency of history file generation by an estimated 90% while still preserving a perfect record of all material strategy shifts.

## Timeline/Log
- **2026-04-24 23:05:00:** Task created.
- **2026-04-24 23:15:00:** Implemented change-detection logic in `trade_viewer_api.py`.
- **2026-04-24 23:20:00:** Updated API call sites to differentiate between material and non-material changes.
- **2026-04-24 23:25:00:** Verified and completed.
