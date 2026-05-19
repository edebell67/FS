Source: User request on 2026-04-02 to replace the existing every-4-hours Twitter summary recurrence with a combined workflow that prepares the latest payload and posts it through the X API route.

Task Type: standard

Task Attributes:
- recurring_task: true
- recurrence_type: scheduled
- recurrence_rule: interval
- recurrence_interval_hours: 4
- priority: high
- execution_owner: codex

**Suggested Agent:** codex

Task Summary: Every 4 hours, regenerate the latest Strategy Warehouse summary payload into `temp_tweet.txt`, then submit that prepared text through `POST /api/social/x_api_post`, recording the exact live response.

Context:
- Workspace: `C:\Users\edebe\eds`
- Payload generator: `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
- Prepared payload file: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet.txt`
- X API route: `http://localhost:5000/api/social/x_api_post`
- Summary returns inputs: latest Strategy Warehouse social posting package and related return summary artefacts under `TradeApps\breakout\fs\json\live\social_posting_package`
- Workflow references:
  - `C:\Users\edebe\eds\workstream\300_complete\20260402_150114_breakout_rerun_twitter_summary_slot_20260402_130000.md`
  - `C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md`

Dependency: None
Required Skill: `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`
Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`
Scheduled For: 2026-04-03 09:00:00+01:00
Next Scheduled For: 2026-04-03 13:00:00+01:00
Spawned From: 20260403_050000_breakout_twitter_summary_returns_every_4_hours.md

## Plan

- [x] 1. Regenerate the latest summary returns payload for the current run window.
  - [x] Test: `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-03` completes successfully and refreshes `temp_tweet.txt`.
  - Evidence: `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\top5_weekly_posting_package.json` and `.md` were regenerated; `TradeApps\breakout\fs\twitter_workflow_status.json` recorded the generator step as successful.

- [x] 2. Validate the prepared post body without inventing unsupported figures.
  - [x] Test: Confirm `temp_tweet.txt` is non-empty, was rewritten by the current generator run, matches the current `consolidated_twitter_post`, and remains within X posting constraints.
  - Evidence: `TradeApps\breakout\fs\temp_tweet.txt` contained the regenerated 229-character consolidated post for the 2026-04-03 run and matched `consolidated_twitter_post` in `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\top5_weekly_posting_package.json`.

- [x] 3. Submit the prepared payload through the X API route.
  - [x] Test: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03` returns success and `POST /api/social/x_api_post` yields either a tweet ID or a concrete blocker.
  - Evidence: `TradeApps\breakout\fs\twitter_x_api_post_response.json` captured HTTP 200 with `tweet_id` `2039976545347850662` for the 2026-04-03 recurring run.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\top5_weekly_posting_package.json`; `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet.txt`
  - Objective-Proved: Proves the exact regenerated payload package and prepared tweet text used for the recurring X post run.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`; `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the gated workflow steps passed and the X API route returned HTTP 200 with tweet ID `2039976545347850662`.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Pending operator verification of live post `2039976545347850662` on X against the regenerated `temp_tweet.txt` body.
  - Objective-Proved: Allows operator confirmation that the regenerated summary payload was posted live with the expected text.
  - Status: planned

## Implementation Log

- 2026-04-02 23:36:18 Europe/London: Recurring task definition replaced to combine payload generation with X API route posting every 4 hours.
- 2026-04-03 09:01:10 Europe/London: Ran `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`; workflow verified API health, regenerated the social posting package, validated `temp_tweet.txt`, and submitted the X API post.
- 2026-04-03 09:01:16 Europe/London: Captured `TradeApps\breakout\fs\twitter_x_api_post_response.json` with HTTP 200 success and tweet ID `2039976545347850662`; awaiting operator verification of the live X post before closing the recurring run.

## Changes Made

- Replaced the prior browser-based recurring posting definition with a combined payload-generation plus X API posting workflow.
- Regenerated `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\top5_weekly_posting_package.json` and `.md`, refreshed `TradeApps\breakout\fs\temp_tweet.txt`, and updated `TradeApps\breakout\fs\twitter_workflow_status.json` plus `TradeApps\breakout\fs\twitter_x_api_post_response.json` for the 09:00 recurring run.
- Updated this lifecycle file with completed checklist items, captured evidence, and a pending operator-verification state.

## Validation

- `Invoke-WebRequest -UseBasicParsing http://localhost:5000/api/health` returned `{"status":"ok","ts":"2026-04-03T08:01:12.084569"}`.
- `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03` completed with exit code `0`.
- `TradeApps\breakout\fs\twitter_workflow_status.json` recorded success for `verify_api`, `generate_content`, `validate_payload`, and `submit_post`.
- Prepared payload validation passed: `temp_tweet.txt` contained the same 229-character consolidated text stored in `top5_weekly_posting_package.json`.
- X route validation passed: `TradeApps\breakout\fs\twitter_x_api_post_response.json` captured HTTP `200` with payload `{"message":"Tweet posted successfully","success":true,"tweet_id":"2039976545347850662"}`.
- 2026-04-03 09:02 Europe/London: Requested operator verification of the live X post for tweet ID `2039976545347850662` against the regenerated payload text before moving this task to `300_complete`.

## Risks/Notes

- If the local API server is not reachable on `localhost:5000`, stop and record the concrete connectivity blocker.
- Use local data only; do not invent returns or write new market figures without a source artifact.
- After successful completion, the Kanban scheduler should spawn the next occurrence 4 hours later.
- Technical execution succeeded, but this run cannot move to complete until operator verification is received because `Auto-Acceptance` is `false` and the task produced a user-visible post.

## Completion Status

- State: Awaiting user verification
- Timestamp: 2026-04-03 09:01:16 Europe/London
