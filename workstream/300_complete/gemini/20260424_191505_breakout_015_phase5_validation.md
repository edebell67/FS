# Phase 5: Validation Against Manual Package

## Source
- Epic: `workstream/000_epic/20260424_191435_breakout_015_data_story_engine_implementation.md`
- Implementation Plan: `epics/ep_015_trading_result_video_content/data_story_engine_implementation_plan.md`

## Task Type
standard

## Task Summary
Validate the automated Data Story Engine output against the manually-created 2026-04-24 package. Ensure quality parity and correct any discrepancies.

## Context
- Input: Automated package from Phase 4, Manual package from `2026-04-24/`
- Output: Validation report and any corrections

## Destination Folder
`epics/ep_015_trading_result_video_content/`

## Dependency
`20260424_191504_breakout_015_phase4_video_renderer.md`

## Plan
- [ ] 1. Run `generate_story_package.py --scope forex --date 2026-04-24` to fresh output folder
  - Test: Command completes without error
  - Evidence:

- [ ] 2. Compare generated `summary_net_video_package.json` vs manual version
  - Test: Selected pairs and reasons match or improve upon manual selection
  - Evidence:

- [ ] 3. Compare generated brief vs manual brief
  - Test: Key facts match; automated version is factually correct
  - Evidence:

- [ ] 4. Compare generated script vs manual script
  - Test: Narrative structure followed; claims traceable to source
  - Evidence:

- [ ] 5. Compare generated storyboard vs manual storyboard
  - Test: Scene count and structure match template
  - Evidence:

- [ ] 6. Verify no off-scope products in output
  - Test: All strategies/products are forex-only
  - Evidence:

- [ ] 7. Verify story claims traceable to `_summary_net.json` metrics
  - Test: Each claim can be verified against source data
  - Evidence:

- [ ] 8. Document discrepancies and create fix tasks if needed
  - Test: Discrepancy log created
  - Evidence:

- [ ] 9. Mark engine ready for production use
  - Test: Validation report signed off
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false

- Evidence-Type: manual_verification
  - Artifact: planned
  - Objective-Proved: Automated output matches or exceeds manual quality
  - Status: planned

- Evidence-Type: diff
  - Artifact: planned
  - Objective-Proved: Comparison report shows alignment
  - Status: planned

## Implementation Log


## Changes Made


## Validation


## Risks/Notes
- Manual package is the quality baseline
- Discrepancies may reveal detector or renderer bugs
- User verification required before marking complete

## Completion Status
Not started
