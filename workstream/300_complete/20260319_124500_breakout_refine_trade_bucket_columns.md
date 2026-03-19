# Task: Refine Trade Bucket Columns & Start Time Standardization

## Status: IN PROGRESS
**Timestamp**: 2026-03-19 12:45:00
**Project**: breakout

### 1. Objective
Refine TB P&L columns and standardize chart start times to allow for precise "since creation" P&L tracking.

### 2. Work Log
#### [2026-03-19 12:45]
- Initialized Task. Standardized chart start to 00:00:00.
- Implemented 6-column strategy grid in `trade_bucket.html`.

#### [2026-03-19 13:55]
- Hotfix: Resolved issue where "Create Net" was always 0.00 for manual buckets.
- Implemented dynamic baseline resolution in `trade_viewer_api.py`.

#### [2026-03-19 15:00]
- Hotfix: Standardized chart start time for automated workflows (`top_x`, `profile_match`).
- Automated buckets now also use 00:00:00 as the chart baseline.
- Bumped version to `V20260319_1500`.

### 3. Validation Results
- [x] Version Updated: `V20260319_1245`.
- [x] Code Logic: `current_net` relative to 00:00, `creation_delta` relative to 00:00.
- [x] UI Headers: Start Net (0.00), Create Net, Latest Net, Net Δ.
- [x] UI Logic: Sub-strategies now display specific Live Net (promoted trades sum).
