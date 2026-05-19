# Phase 2: Feature Builder

## Source
- Epic: `workstream/000_epic/20260424_191435_breakout_015_data_story_engine_implementation.md`
- Implementation Plan: `epics/ep_015_trading_result_video_content/data_story_engine_implementation_plan.md`

## Task Type
standard

## Task Summary
Build feature calculator that computes reusable features for story detectors from normalized rows.

## Context
- Input: Normalized row list from Phase 1
- Output: Rows enriched with detector-ready feature fields

## Destination Folder
`TradeApps/breakout/fs/tools/data_story_engine/`

## Dependency
`20260424_191501_breakout_015_phase1_loader_normalization.md`

## Plan
- [ ] 1. Create `feature_builder.py` module
  - Test: Module imports without error
  - Evidence:

- [ ] 2. Implement `compute_features(normalized_rows)` function
  - Test: Returns rows with all feature fields populated
  - Evidence:

- [ ] 3. MVP features: final_net, session_high, session_low, reversal_size, net_gain, slope_proxy
  - Test: Each feature calculates correctly for known sample
  - Evidence:

- [ ] 4. Add optional point_density/update_count feature
  - Test: Feature present when data supports it
  - Evidence:

- [ ] 5. Document feature definitions in module docstring
  - Test: Docstring explains each feature
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: planned
  - Objective-Proved: Feature builder produces detector-ready rows
  - Status: planned

## Implementation Log


## Changes Made


## Validation


## Risks/Notes
- Keep feature set minimal for MVP
- Future features: rank_velocity, rolling_window_return, side_dominance

## Completion Status
Not started
