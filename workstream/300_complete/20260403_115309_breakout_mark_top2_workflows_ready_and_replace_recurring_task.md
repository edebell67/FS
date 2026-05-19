## Objective

Mark the current-date top-2 package generation and X posting task records as `workflow_ready: true`, then rewrite the 4-hour recurring task definition so it combines those two workflows and continues posting to X every 4 hours.

## Task Attributes

- project: breakout
- task_type: maintenance
- area: social_publisher
- priority: high
- status: todo

## Plan

1. Update the two completed lifecycle files with `workflow_ready: true`.
2. Rewrite the recurring 4-hour task definition at `20260403_130000_breakout_twitter_summary_returns_every_4_hours.md`.
3. Ensure the new recurrence references current-date top-2 package generation followed by X posting.
4. Record the changes and close the task.

## Progress Log

- 2026-04-03 11:53:09 Created lifecycle task.
- 2026-04-03 11:54:20 Added `workflow_ready: true` to the current-date top-2 package generation and X posting task records.
- 2026-04-03 11:54:32 Rewrote `workstream/100_backlog/codex/20260403_130000_breakout_twitter_summary_returns_every_4_hours.md` to combine generation and posting every 4 hours.
- 2026-04-03 11:55:04 Read back all three files to verify the updated workflow markers and recurring definition.

## Outcome

Completed successfully.

Changes made:
- Updated `C:\Users\edebe\eds\workstream\300_complete\20260403_114522_breakout_run_top2_cross_product_package_for_current_date.md` with `- workflow_ready: true`
- Updated `C:\Users\edebe\eds\workstream\300_complete\20260403_114950_breakout_post_current_top2_payload_to_x.md` with `- workflow_ready: true`
- Replaced `C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_130000_breakout_twitter_summary_returns_every_4_hours.md` so it now runs:
  1. current-date top-2 package generation
  2. payload validation against `top2_cross_product_post.json`
  3. local API health check
  4. X post through `/api/social/x_api_post`

Validation:
- Both completed workflow files contain `workflow_ready: true`
- The recurring task definition references the two workflow-ready task records
- The recurring task explicitly uses `temp_tweet_top2.txt` and continues on a 4-hour interval
