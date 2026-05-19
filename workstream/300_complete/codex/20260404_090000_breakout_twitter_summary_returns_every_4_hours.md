Source: User request on 2026-04-03 to mark the current top-2 package generation and X posting workflows as ready, then replace the 4-hour recurring task so it runs both in sequence and continues posting to X every 4 hours.
Task Type: standard

Task Attributes:
- recurring_task: true
- recurrence_type: scheduled
- recurrence_rule: interval
- recurrence_interval_hours: 4
- priority: high
- execution_owner: codex
- workflow_ready: true

**Suggested Agent:** codex

Task Summary: Every 4 hours, generate the current-date top-2 cross-product social package from source data, refresh `temp_tweet_top2.txt`, then post that exact payload through `POST /api/social/x_api_post` and record the live response.

Context:
- Workspace: `C:\Users\edebe\eds`
- Package generator: `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
- Generated package artifacts: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\YYYY-MM-DD\top2_cross_product_post.json` and `.md`
- Live payload file: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
- X API route: `http://localhost:5000/api/social/x_api_post`
- Health route: `http://localhost:5000/api/health`
- Workflow references:
  - `C:\Users\edebe\eds\workstream\300_complete\20260403_114522_breakout_run_top2_cross_product_package_for_current_date.md`
  - `C:\Users\edebe\eds\workstream\300_complete\20260403_114950_breakout_post_current_top2_payload_to_x.md`

Dependency: None
Required Skill: `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`
Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`
Scheduled For: 2026-04-04 09:00:00+01:00
Next Scheduled For: 2026-04-04 13:00:00+01:00
Spawned From: 20260404_050000_breakout_twitter_summary_returns_every_4_hours.md

## Plan
- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-04` completes successfully.
  - Evidence: Generated `top2_cross_product_post.json` and refreshed `temp_tweet_top2.txt` at `2026-04-04T09:04:56+01:00`.

- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: Validation script confirmed `temp_exists=true`, `temp_non_empty=true`, `matches_package=true`, `length=184`, `today_source_date=2026-04-04`, and `today_source_last_update=2026-04-04T09:04:55.220105`.

- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: Health check returned HTTP 200 with `{"status":"ok","ts":"2026-04-04T08:05:25.011120"}`.

- [x] 4. Post the refreshed payload to X.
  - [x] Test: `POST /api/social/x_api_post` returns a success response with a tweet ID or a concrete blocker such as a rate limit or credential error.
  - Evidence: `run_twitter_canonical_workflow.py 2026-04-04` returned a concrete blocker, `HTTP 400 {"error":"Rate limit: wait 6 more minutes","success":false}`, after recording the exact attempted request payload in `twitter_x_api_post_response.json`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json`
  - Objective-Proved: Proves which current-date top-2 package was generated for the 2026-04-04 run.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the exact refreshed payload text prepared for posting and that it matched the generated package.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `GET http://localhost:5000/api/health -> HTTP 200 {"status":"ok","ts":"2026-04-04T08:05:25.011120"}`
  - Objective-Proved: Proves the local API was reachable before the post attempt.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the canonical workflow executed the gates in sequence and failed closed on the submit step with a concrete rate-limit blocker.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the exact `09:05` payload submitted to `POST /api/social/x_api_post` and the live HTTP 400 rate-limit response returned for that attempt.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `User verification requested in Validation section for scheduled-run success at 09:01 and rerun rate-limit outcome at 09:05`
  - Objective-Proved: Proves the required user verification handoff has been requested for the user-visible X posting outcome.
  - Status: captured

## Implementation Log
- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-04 09:04:56 Europe/London: Ran `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-04` and regenerated the current-date package artifacts.
- 2026-04-04 09:05:02 Europe/London: Validated that `temp_tweet_top2.txt` matched `top2_cross_product_post.json` exactly and contained only source-derived values.
- 2026-04-04 09:05:25 Europe/London: Verified `GET http://localhost:5000/api/health` returned HTTP 200 with `status=ok`.
- 2026-04-04 09:05:35 Europe/London: Compared the fresh payload to the existing `09:01` success artifact and confirmed the scheduled run had already posted a different timestamped copy, so an explicit rerun was required to satisfy the exact regenerated payload requirement.
- 2026-04-04 09:05:58 Europe/London: Ran `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-04`; the workflow passed generation/validation gates and failed closed on submit with `Rate limit: wait 6 more minutes`.
- 2026-04-04 09:06:01 Europe/London: Queried `GET http://localhost:5000/api/social/status` and confirmed the latest successful scheduled post occurred at `2026-04-04T09:01:42.786412` under trigger `breakout_top2_cross_product_every_4_hours`.

## Changes Made
- No application code changes were required during this execution.
- Normalized this lifecycle record to the required task format and captured concrete evidence for each sequential validation step.
- Refreshed runtime artifacts for the `2026-04-04` top-2 package and recorded the canonical workflow blocker response for the explicit rerun attempt.

## Validation
- `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-04`
  - Result: exit code 0; wrote `top5_weekly_posting_package.json`, `top5_weekly_posting_package.md`, `top2_cross_product_post.json`, and `top2_cross_product_post.md` under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04`.
- Payload validation script against `top2_cross_product_post.json` and `temp_tweet_top2.txt`
  - Result: `temp_exists=true`, `temp_non_empty=true`, `matches_package=true`, `length=184`, `today_source_date=2026-04-04`, `today_source_last_update=2026-04-04T09:04:55.220105`.
- `GET http://localhost:5000/api/health`
  - Result: HTTP 200 with `{"status":"ok","ts":"2026-04-04T08:05:25.011120"}`.
- `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-04`
  - Result: exit code 1; `verify_api`, `generate_content`, and `validate_payload` passed, and `submit_post` returned `HTTP 400 {"error":"Rate limit: wait 6 more minutes","success":false}`.
- `GET http://localhost:5000/api/social/status`
  - Result: `can_post=false`, `reason="Rate limit: wait 6 more minutes"`, and `last_post_time="2026-04-04T09:01:42.786412"` with a successful scheduled post already recorded for trigger `breakout_top2_cross_product_every_4_hours`.
- User verification requested:
  - Please verify whether the `09:01` scheduled successful X post plus the explicit `09:05` rate-limit blocker is the expected outcome for this `09:00` task instance.

## Risks/Notes
- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- If the generated package source date lags the actual run date, record the mismatch explicitly before posting.
- If the local API server is unreachable on `localhost:5000`, stop and record the concrete blocker.
- After each successful execution, the scheduler should queue the next run 4 hours later.
- The top-2 text embeds the current update timestamp, so a manual rerun after a successful scheduled post will produce a different payload and may legitimately hit the local posting rate limit.

## Completion Status
- State: Awaiting user verification
- Timestamp: 2026-04-04 09:06:01+01:00
