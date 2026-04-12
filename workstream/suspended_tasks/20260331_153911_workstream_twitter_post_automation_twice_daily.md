# Every 6 Hours Twitter Post Automation

## Source
User request on 2026-03-31 to post to Twitter using recurring tasks, based on the generated Strategy Warehouse social posting package, with a later cadence update to every 6 hours.

## Task Type
standard

## Task Attributes
- recurring_task: true
- recurrence_type: scheduled
- recurrence_rule: interval
- priority: high
- execution_owner: gemini

## Scope
- Define a recurring automation that posts the current approved Twitter/X draft using the existing browser-based Twitter automation workflow.
- Require the automation to use the latest generated social posting package rather than inventing new copy.
- Keep Codex in an orchestration role and allocate execution to another model where possible.

## Acceptance Criteria
- A recurring automation definition is prepared for user approval.
- The automation references the generated package under `TradeApps/breakout/fs/json/live/social_posting_package/{date}`.
- The automation uses the existing Twitter browser automation workflow and includes dry-run/review guardrails.
- Posting cadence is defined without removing the existing draft automation.
- Automation cadence is every 6 hours in the local timezone.

## Progress Log
- 2026-03-31 15:39:11: Task created in `workstream/100_todo`.
- 2026-03-31 15:40:00: Task moved to `workstream/200_inprogress`.
- 2026-03-31 15:41:30: Initial posting automation proposal prepared with a 12-hour interval.
- 2026-03-31 15:42:30: User changed cadence requirement to every 6 hours; automation proposal updated accordingly.
- 2026-03-31 16:25:00: Proceeding with recurring automation implementation while immediate live posting is being handled separately by another model.
- 2026-03-31 19:50:00: Rendered the app-ready suggested automation definition for user approval, retaining auth/session guardrails in the prompt.

## Proposed Automation
- Name: `Twitter Post Every 6 Hours`
- Cadence: every 6 hours
- Workspace: `C:\Users\edebe\eds`
- Source package:
  - `TradeApps/breakout/fs/json/live/social_posting_package/{today or latest available dated folder}/top5_weekly_posting_package.md`
- Execution model:
  - Orchestrate away from Codex where possible
  - Post the consolidated `Today / Weekly so far / Full details to follow` section only
  - Use the browser-based workflow in `TradeApps/breakout/fs/twitter_browser.py`

## Status
- Automation definition is now ready for user approval in the app UI.
- Live posting remains dependent on a valid Twitter/X session in `TradeApps/breakout/fs/twitter_session`.
