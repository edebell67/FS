# Phase 1: Loader / Normalization

## Source
- Epic: `workstream/000_epic/20260424_191435_breakout_015_data_story_engine_implementation.md`
- Implementation Plan: `epics/ep_015_trading_result_video_content/data_story_engine_implementation_plan.md`

## Task Type
standard

## Task Summary
Build the loader and normalization layer that reads breakout source JSON files and converts them into a stable row-based internal structure for the story engine.

## Context
- Primary input: `_summary_net.json`
- Initial scope: `forex`
- Output: normalized row list for downstream feature calculation

## Destination Folder
`TradeApps/breakout/fs/tools/data_story_engine/`

## Dependency
None

## Plan
- [ ] 1. Create `loader.py` and `normalizers.py`
  - Test: Both modules import without error
  - Evidence:

- [ ] 2. Implement `_summary_net.json` loader
  - Test: Loads the file and returns parsed top-level object
  - Evidence:

- [ ] 3. Implement normalization to flatten `strategies -> product -> snapshots` into row records
  - Test: Returns one normalized row per strategy/product pair
  - Evidence:

- [ ] 4. Populate MVP normalized fields
  - Test: Each row includes `date`, `scope`, `strategy`, `product`, `points`, `first_net`, `last_net`, `max_net`, `min_net`, `reversal`
  - Evidence:

- [ ] 5. Add defensive handling for empty/malformed buckets
  - Test: Bad or empty buckets do not crash the run
  - Evidence:

- [ ] 6. Add module docstrings explaining the normalized schema
  - Test: Docstrings describe input shape and output row shape
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: planned
  - Objective-Proved: Loader and normalizer convert source JSON into stable rows for downstream phases
  - Status: planned

## Implementation Log


## Changes Made


## Validation


## Risks/Notes
- Phase 1 should stay minimal and support `_summary_net.json` first.
- Additional inputs such as trade files and `_top20.json` can be added after the MVP row model is stable.
- Phase 2 depends on this exact task file.

## Completion Status
Not started
