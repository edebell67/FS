# Task: Add rev_scalper filtering to Profile Match Workflow

## Status
TODO

## Source
- User request: "add rev_scalper checkbox to the profile_match_workflow in C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\workflow_automation.html
when rev scalper selected, do similar to scalper (but for rev scalper).. if both checkboxed ticked then strategies selected can be scalper or rev_scapler only"
- Prerequisite: Task 2 (Define rev_scalper config)

## Task Summary
Add an interactive checkbox to the `profile_match_workflow` section in `workflow_automation.html` to filter for `rev_scalper` strategies. Ensure that if both `scalper` and `rev_scalper` checkboxes are ticked, the workflow selects strategies that are EITHER a `scalper` OR a `rev_scalper`. If only one is ticked, it selects only that specific type.

## Context
- Project: Breakout
- Target File: `C:\Users\edebe\eds\TradeApps\breakout\fs\workflow_automation.html`

## Implementation Log
- 2026-02-25 15:05: Task created.

## Changes Made
- Pending

## Validation
- Verify the checkboxes operate correctly with the logical OR behavior.
- Ensure the `profile_match_workflow` correctly reads `rev_scalper_ratio` from configuration to correctly identify `rev_scalper` strategies.

## Risks/Notes
- Must implement the exact logic correctly so ETHER/OR selection works smoothly if both checkboxes are enabled.

## Completion Status
Pending.
