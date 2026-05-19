## Objective

Replace the existing every-4-hours recurring Twitter summary task with a single combined recurring workflow that regenerates the latest payload and posts it through the X API route.

## Context

- Existing live recurring backlog task: `C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_010000_breakout_twitter_summary_returns_every_4_hours.md`
- Payload refresh reference: `C:\Users\edebe\eds\workstream\300_complete\20260402_150114_breakout_rerun_twitter_summary_slot_20260402_130000.md`
- X API post reference: `C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md`

## Task Attributes

- project: workstream
- task_type: implementation
- area: recurring_tasks
- priority: high
- status: complete

## Plan

1. Add the requested workflow flag to the payload refresh reference task.
2. Replace the live every-4-hours backlog task definition with the combined payload-generation plus X API posting workflow.
3. Preserve the existing recurrence metadata and next-slot behavior.
4. Record the replacement result and close the lifecycle task.

## Progress Log

- 2026-04-02 23:36:18 Created lifecycle task.
- 2026-04-02 23:36:18 Added `workflow_read: true` to `20260402_150114_breakout_rerun_twitter_summary_slot_20260402_130000.md`.
- 2026-04-02 23:37:09 Replaced `workstream/100_backlog/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md` with a combined recurring definition that regenerates `temp_tweet.txt` and then posts it through `POST /api/social/x_api_post`.
- 2026-04-02 23:37:25 Validation: read back the replacement backlog task and confirmed it preserves 4-hour recurrence metadata while referencing both workflow tasks.

## Outcome

Completed. The live every-4-hours recurring backlog task has been replaced with a combined payload-generation plus X API posting workflow, and the requested workflow flag was added to the payload-refresh reference task.
