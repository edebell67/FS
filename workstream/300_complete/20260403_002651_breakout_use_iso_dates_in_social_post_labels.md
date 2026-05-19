## Objective

Use explicit ISO dates in the consolidated social post labels so stale-day payloads say `YYYY-MM-DD results` instead of relative labels.

## Task Attributes

- project: breakout
- task_type: bugfix
- area: social_publisher
- priority: high
- status: complete

## Plan

1. Update the consolidated post label logic to use ISO source dates.
2. Regenerate the current payload.
3. Verify `temp_tweet.txt` shows the explicit date labels.

## Progress Log

- 2026-04-03 00:26:51 Created lifecycle task.
- 2026-04-03 00:27:14 Updated the consolidated post label logic to use ISO source dates for stale-day payloads.
- 2026-04-03 00:27:14 Regenerated the package for `2026-04-02`; package JSON now emits `2026-04-02 results` / `Week to 2026-04-02`.
- 2026-04-03 00:27:44 Refreshed `TradeApps/breakout/fs/temp_tweet.txt` from the current package JSON so the live payload file matches the corrected ISO-date labels.

## Outcome

Completed. The consolidated social post now uses explicit ISO dates instead of relative stale-day labels, and the live `temp_tweet.txt` payload has been refreshed to match.
