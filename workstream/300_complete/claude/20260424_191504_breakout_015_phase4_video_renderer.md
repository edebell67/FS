# Phase 4: Video Package Renderer

## Source
- Epic: `workstream/000_epic/20260424_191435_breakout_015_data_story_engine_implementation.md`
- Implementation Plan: `epics/ep_015_trading_result_video_content/data_story_engine_implementation_plan.md`

## Task Type
standard

## Task Summary
Build video package renderer that replaces manual package drafting. Takes story objects as input and outputs the complete video content package.

## Context
- Input: List of StoryObject instances from Phase 3
- Output: Complete video package in `ep_015_trading_result_video_content/YYYY-MM-DD/`

## Destination Folder
`TradeApps/breakout/fs/tools/data_story_engine/renderers/`

## Dependency
`20260424_191503_breakout_015_phase3_detectors.md`

## Plan
- [ ] 1. Create `renderers/` directory and `video_package_renderer.py`
  - Test: Module imports without error
  - Evidence:

- [ ] 2. Implement `render_video_package(story_objects, date, scope)` main function
  - Test: Function creates output directory
  - Evidence:

- [ ] 3. Generate `summary_net_video_package.json` from story objects
  - Test: JSON file matches schema with selected pairs
  - Evidence:

- [ ] 4. Generate `summary_net_video_brief.md` - operator-facing summary
  - Test: Brief describes selected stories
  - Evidence:

- [ ] 5. Generate `summary_net_video_script.txt` - narration script
  - Test: Script follows narrative framework (hook, context, result, comparison, interpretation, close)
  - Evidence:

- [ ] 6. Generate `summary_net_video_storyboard.md` - scene breakdown
  - Test: 5 scenes with hook, curve reveal, comparison, interpretation, closing
  - Evidence:

- [ ] 7. Generate `summary_net_video_hook_options.txt` - 3-5 hook variants
  - Test: File contains multiple hook options
  - Evidence:

- [ ] 8. Generate `summary_net_video_overlay_copy.txt` - on-screen text
  - Test: Short lines readable in under 2 seconds
  - Evidence:

- [ ] 9. Generate `summary_net_video_asset_manifest.json` - visual asset refs
  - Test: JSON lists required charts, backgrounds, logos
  - Evidence:

- [ ] 10. Generate `summary_net_video_render_notes.md` - export settings
  - Test: Notes include aspect ratio, pacing, QA checklist
  - Evidence:

- [ ] 11. Generate optional `summary_net_video_prompt.txt` and `summary_net_video_thumbnail_brief.txt`
  - Test: Files created if story objects warrant them
  - Evidence:

- [ ] 12. Create `generate_story_package.py` CLI entry point
  - Test: `python generate_story_package.py --scope forex --date 2026-04-24` produces package
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: planned
  - Objective-Proved: Complete video package generated from story objects
  - Status: planned

- Evidence-Type: demo
  - Artifact: planned
  - Objective-Proved: CLI command produces dated package
  - Status: planned

## Implementation Log


## Changes Made


## Validation


## Risks/Notes
- Templates from `template_package/` should guide output format
- Hook and script quality depends on story object richness
- Fallback to restrained recap if stories are weak

## Completion Status
Not started
