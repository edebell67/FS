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
Scheduled For: 2026-04-03 13:00:00+01:00
Next Scheduled For: 2026-04-03 17:00:00+01:00
Spawned From: `C:\Users\edebe\eds\workstream\300_complete\20260403_114522_breakout_run_top2_cross_product_package_for_current_date.md`

## Plan

- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-03` completes successfully.
  - Evidence: `TradeApps\breakout\fs\twitter_workflow_status.json` recorded generator success and `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\top2_cross_product_post.json` was regenerated at `2026-04-03T13:02:42.884406`.

- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: `twitter_workflow_status.json` recorded `Validated payload (190 chars)` against `top2_cross_product_post.json`; `temp_tweet_top2.txt` matched the exact posted text beginning `2026-04-03 leaders` and the JSON source recorded `today_source_date=2026-04-03`, `today_source_last_update=2026-04-03T13:02:40.333118`, `strategy_product_count=2690`.

- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: `twitter_workflow_status.json` recorded `{'status': 'ok', 'ts': '2026-04-03T12:02:42.642672'}` from `http://localhost:5000/api/health`.

- [x] 4. Post the refreshed payload to X.
  - [x] Test: `POST /api/social/x_api_post` returns a success response with a tweet ID or a concrete blocker such as a rate limit or credential error.
  - Evidence: `twitter_x_api_post_response.json` captured HTTP `200` with `tweet_id=2040037326571683844` for trigger `breakout_top2_cross_product_every_4_hours`.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\top2_cross_product_post.json`
  - Objective-Proved: Proves which current-date package output was generated for the recurring run.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the exact body posted to X and confirms it matches the current generated package.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the gated workflow executed in sequence, including health check, generation, payload validation, and post submission success.
  - Status: captured

- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the posting attempt outcome for the current recurring run.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: User verification requested in chat for workflow behavior, generated payload, and successful X posting outcome.
  - Objective-Proved: Proves manual acceptance has been requested for the user-visible recurring posting behavior.
  - Status: captured

## Implementation Log

- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-03 13:00:00 Europe/London: Read `skills/workstream-task-lifecycle/SKILL.md`, the task file, and the required `skills/twitter-canonical-posting/SKILL.md` before implementation.
- 2026-04-03 13:01:00 Europe/London: Updated `TradeApps\breakout\fs\run_twitter_canonical_workflow.py` to validate and post `temp_tweet_top2.txt` against `top2_cross_product_post.json` and to label the recurring trigger as `breakout_top2_cross_product_every_4_hours`.
- 2026-04-03 13:01:20 Europe/London: Updated `TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` to cover the top-2 payload contract.
- 2026-04-03 13:02:10 Europe/London: Ran `python -m unittest TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow` and confirmed both targeted tests passed.
- 2026-04-03 13:02:40 Europe/London: Ran `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`; the workflow regenerated the current top-2 package, passed health and payload validation, and posted successfully to X with tweet ID `2040037326571683844`.
- 2026-04-03 13:03:30 Europe/London: Requested user verification for the user-visible recurring posting behavior before moving the task to `300_complete`.

## Changes Made

- Combined current-date top-2 package generation with X posting in a single recurring workflow.
- Switched the recurring payload target from `temp_tweet.txt` to `temp_tweet_top2.txt`.
- Anchored the recurring definition to the proven workflow-ready package generation and X posting task records.
- Updated `TradeApps\breakout\fs\run_twitter_canonical_workflow.py` constants and payload validation so the workflow now reads `top2_cross_product_post.json`, checks `top2_cross_product_post`, posts `temp_tweet_top2.txt`, and records the new trigger name `breakout_top2_cross_product_every_4_hours`.
- Updated `TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` fixtures to match the top-2 package filename and payload field.

## Validation

- Recurring definition updated to reflect the current source-derived top-2 social publishing flow.
- `python -m unittest TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow`
  - Result: pass (`Ran 2 tests in 0.088s`, `OK`)
- `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`
  - Result: pass (`final_status=success` in `twitter_workflow_status.json`)
- Workflow health check artifact:
  - `GET http://localhost:5000/api/health` returned `{'status': 'ok', 'ts': '2026-04-03T12:02:42.642672'}`
- Workflow post artifact:
  - `POST http://localhost:5000/api/social/x_api_post` returned HTTP `200` with `{"message":"Tweet posted successfully","success":true,"tweet_id":"2040037326571683844"}`
- User verification requested:
  - Please confirm pass/fail for: 1. the workflow now regenerates the top-2 package every run, 2. the posted payload matches `temp_tweet_top2.txt`, 3. the recorded X response is acceptable.

## Risks/Notes

- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- If the generated package source date lags the actual run date, record the mismatch explicitly before posting.
- If the local API server is unreachable on `localhost:5000`, stop and record the concrete blocker.
- After each successful execution, the scheduler should queue the next run 4 hours later.

## Completion Status

- State: Awaiting user verification
- Timestamp: 2026-04-03 13:03:30 Europe/London
