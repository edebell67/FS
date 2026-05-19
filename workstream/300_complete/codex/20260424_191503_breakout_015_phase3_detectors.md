# Phase 3: After-the-Fact Detectors

## Source
- Epic: `workstream/000_epic/20260424_191435_breakout_015_data_story_engine_implementation.md`
- Implementation Plan: `epics/ep_015_trading_result_video_content/data_story_engine_implementation_plan.md`

## Task Type
standard

## Task Summary
Build story detectors that create confirmed story objects from completed daily data. Implement top winner, worst loser, biggest reversal, market courtroom, and autopsy detectors.

## Context
- Input: Feature-enriched rows from Phase 2
- Output: List of StoryObject instances

## Destination Folder
`TradeApps/breakout/fs/tools/data_story_engine/`

## Dependency
`20260424_191502_breakout_015_phase2_feature_builder.md`

## Plan
- [ ] 1. Create `detectors.py` module with detector base pattern
  - Test: Module imports without error
  - Evidence:

- [ ] 2. Implement `detect_top_winner(rows)` - sort by last_net desc, select highest
  - Test: Returns StoryObject with correct strategy/product for known data
  - Evidence:

- [ ] 3. Implement `detect_worst_loser(rows)` - sort by last_net asc, select lowest
  - Test: Returns StoryObject with correct strategy/product for known data
  - Evidence:

- [ ] 4. Implement `detect_biggest_reversal(rows)` - sort by reversal desc
  - Test: Returns StoryObject with largest reversal pair
  - Evidence:

- [ ] 5. Implement `detect_market_courtroom(rows)` - strongest positive/negative divergence
  - Test: Returns hero/villain pair with reason
  - Evidence:

- [ ] 6. Implement `detect_autopsy(rows)` - determine session driver (cluster, side, group)
  - Test: Returns StoryObject explaining session outcome
  - Evidence:

- [ ] 7. Create `confidence.py` with confidence scoring logic
  - Test: Each story object has confidence field set
  - Evidence:

- [ ] 8. Implement `run_all_detectors(rows, date, scope)` orchestration function
  - Test: Returns list of all detected story objects
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: planned
  - Objective-Proved: Detectors produce valid story objects from sample data
  - Status: planned

## Implementation Log


## Changes Made


## Validation


## Risks/Notes
- Detectors should fail gracefully if no qualifying candidate exists
- Market courtroom requires at least two divergent pairs
- Autopsy may produce weak output on flat days

## Completion Status
Not started
