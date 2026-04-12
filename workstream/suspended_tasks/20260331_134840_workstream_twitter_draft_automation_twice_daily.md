# Twice Daily Twitter Draft Automation

## Source
User request on 2026-03-31 to create a new 2x-daily recurring task that drafts Twitter/X data output, uses the latest local Twitter workflow/assets, and allocates execution to another model so Codex can stay focused on outcomes.

## Task Type
standard

## Task Attributes
- recurring_task: true
- recurrence_type: scheduled
- recurrence_rule: interval
- looping_task: false
- splittable_task: false
- workflow_task: false
- depends_on: []
- feeds_into: []

## Task Summary
Create a new recurring automation that runs twice daily and prepares draft Twitter/X output from the latest available Strategy Warehouse trading data without posting it. The automation prompt should instruct the agent to use the current local Twitter drafting workflow, create/update a lifecycle file, and allocate execution to a non-Codex worker lane where possible.

## Context
- Automation goal: draft-only Twitter/X content, not posting.
- Under the lifecycle schema, `Task Type` remains explicitly `standard`; the recurring behavior is expressed in `Task Attributes`.
- Latest local drafting implementation:
  - `TradeApps/breakout/fs/tools/social_posting_package/generate_posting_package.py`
  - `TradeApps/breakout/fs/tools/social_posting_package/README.md`
- Relevant prior workstream references:
  - `workstream/300_complete/20260323_040702_strategy_warehouse_twitter_tiktok_content_generator_mvp.md`
  - `workstream/300_complete/20260326_174209_breakout_twitter_post_preparation_top5_multi_product_types.md`
  - `workstream/300_complete/20260323_130435_breakout_social_content_browser_twitter_posting.md`
- Relevant local skills now identified:
  - `skills/strategy-warehouse-social-posting/SKILL.md`
  - `skills/twitter-automation/SKILL.md`
- App scheduling constraints support hourly interval schedules cleanly, so a 12-hour interval is the safest approximation of “2x daily” in the current UI.

## Dependency
Dependency: None

## Plan

- [x] 1. Identify the latest local Twitter/X drafting workflow and confirm the best source artifact for recurring draft generation.
  - [x] Test: Review the local Twitter/X drafting implementation and supporting workstream records to confirm the recommended drafting path.
  - Evidence: `TradeApps/breakout/fs/social_content_generator.py` and the completed Twitter drafting workstream files confirm a current draft-generation path that is separate from posting.

- [x] 2. Draft a recurring automation prompt that tells the agent to generate Twitter/X draft output only, keep a lifecycle record, and allocate execution away from Codex.
  - [x] Test: Review the proposed automation prompt and confirm it specifies draft-only behavior, output expectations, delegation/orchestration intent, and no-posting safeguards.
  - Evidence: Prepared automation prompt includes draft-only output, references the local generator/workflow, requires lifecycle usage, and instructs delegation to Gemini or Claude where possible.

- [x] 3. Present the new automation definition for user approval in the app.
  - [x] Test: Render a `suggested create` automation directive with a 12-hour recurrence and the selected workspace.
  - Evidence: Assistant response includes a `suggested create` automation directive for `Twitter Draft Twice Daily` targeting `C:\Users\edebe\eds`.

## Evidence
Objective-Delivery-Coverage: 85%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/social_content_generator.py`
  - Objective-Proved: Confirms there is an existing local implementation for Twitter/X draft generation based on live data.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `workstream/300_complete/20260323_040702_strategy_warehouse_twitter_tiktok_content_generator_mvp.md`
  - Objective-Proved: Confirms the established Twitter/X draft-generation workflow and CLI usage.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `workstream/300_complete/20260326_174209_breakout_twitter_post_preparation_top5_multi_product_types.md`
  - Objective-Proved: Confirms recent drafting/formatting guidance for Twitter/X-ready post output and character-limit validation.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: Pending automation creation directive in the app UI.
  - Objective-Proved: Will prove the new recurring automation has been defined for user review/acceptance.
  - Status: planned

- Evidence-Type: user_feedback
  - Artifact: Pending user acceptance or adjustment of the proposed automation.
  - Objective-Proved: Final confirmation that the cadence and drafting prompt are acceptable.
  - Status: planned

## Implementation Log
- 2026-03-31 13:48:40 +01:00 — Task created from user request to establish a twice-daily Twitter/X draft automation.
- 2026-03-31 13:49:00 +01:00 — Moved task to `workstream/200_inprogress` when automation design work began.
- 2026-03-31 13:50:00 +01:00 — Reviewed the current local Twitter/X draft generator and recent workstream records for drafting and posting-package preparation.
- 2026-03-31 13:52:00 +01:00 — Chose a 12-hour recurring interval as the supported approximation of “2x daily” in the app scheduling model.
- 2026-03-31 13:53:00 +01:00 — Prepared an automation prompt that keeps the work draft-only, uses the lifecycle process, and asks the agent to delegate execution away from Codex where possible.
- 2026-03-31 13:57:00 +01:00 — Corrected the lifecycle metadata so the task is explicitly modeled as recurring through `Task Attributes` instead of being marked as non-recurring.
- 2026-03-31 19:50:00 +01:00 — Rendered the app-ready suggested automation definition so the draft recurring task can be approved and created from the UI.

## Changes Made
- `workstream/200_inprogress/20260331_134840_workstream_twitter_draft_automation_twice_daily.md`
  - Created and updated lifecycle documentation for the recurring Twitter/X draft automation request.
  - Recorded the automation design assumptions: draft-only output, 12-hour cadence, workspace `C:\Users\edebe\eds`, and delegation preference to a non-Codex worker.
  - Updated `Task Attributes` to `recurring_task: true`, `recurrence_type: scheduled`, and `recurrence_rule: interval`.

## Validation
- Reviewed `TradeApps/breakout/fs/social_content_generator.py`
  - Result: Confirms a current Twitter draft-generation CLI exists.
- Reviewed `workstream/300_complete/20260323_040702_strategy_warehouse_twitter_tiktok_content_generator_mvp.md`
  - Result: Confirms established Twitter draft-generation workflow and expected outputs.
- Reviewed `workstream/300_complete/20260326_174209_breakout_twitter_post_preparation_top5_multi_product_types.md`
  - Result: Confirms recent Twitter/X-ready formatting and character-limit validation workflow.
- Automation creation directive rendered in assistant response for final user acceptance in the app UI.

## Risks/Notes
- The automation system’s supported RRULE model does not cleanly express two fixed daily times in a single rule, so this proposal uses a 12-hour interval assumption.
- No dedicated Twitter skill is available in the current session registry, so the automation prompt relies on the latest local workflow artifacts and script instead.
- Because the automation has not yet been accepted in the UI, this task should remain in progress until the user confirms or adjusts the proposed setup.

## Proposed Automation Definition
- Name: `Twitter Draft Twice Daily`
- Schedule assumption: every 12 hours in the user’s local timezone (`Europe/London`)
- Workspace: `C:\Users\edebe\eds`
- Prompt summary: use the workstream lifecycle process plus the local social-posting and Twitter automation skills, orchestrate the work by allocating execution to Gemini or Claude rather than Codex when possible, run the social posting package generator, draft the consolidated `Today / Weekly so far / Full details to follow` update with hashtags, include character counts and concise rationale, do not publish to X, and report the drafted output in the inbox item with any blocker if fresh data is unavailable.

## Completion Status
Awaiting user approval of the proposed automation as of 2026-03-31 19:50:00 +01:00.
