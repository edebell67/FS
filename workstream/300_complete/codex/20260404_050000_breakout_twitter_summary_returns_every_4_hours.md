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
- Required Skill: `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`
- Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`
- Scheduled For: `2026-04-04 05:00:00+01:00`
- Next Scheduled For: `2026-04-04 09:00:00+01:00`
- Spawned From: `20260404_010000_breakout_twitter_summary_returns_every_4_hours.md`

Dependency: None
Required Skill: `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`
Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`

## Plan

- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-04` completes successfully.
  - Evidence: Command completed successfully at 2026-04-04 05:05 Europe/London and rewrote `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json`, `.md`, and `TradeApps\breakout\fs\temp_tweet_top2.txt`.

- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: `temp_tweet_top2.txt` matched `top2_cross_product_post` exactly at 184 characters after the 05:05 generation run; the JSON payload showed `today_source_date=2026-04-04`, `today_source_last_update=2026-04-04T05:05:09.666813`, leaders `SI +235` and `HG +235`, and `strategy_product_count=759`.

- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: `Invoke-WebRequest -UseBasicParsing 'http://localhost:5000/api/health'` returned `{"status":"ok","ts":"2026-04-04T04:05:13.214248"}`.

- [x] 4. Post the refreshed payload to X.
  - [x] Test: `POST /api/social/x_api_post` returns a success response with a tweet ID or a concrete blocker such as a rate limit or credential error.
  - Evidence: The scheduled canonical workflow run at 2026-04-04 05:01 Europe/London already posted successfully and recorded tweet ID `2040278570635849759` in `TradeApps\breakout\fs\twitter_x_api_post_response.json`. A second manual POST was intentionally not executed after the 05:05 regeneration because the only payload delta was the regenerated `Update at 2026-04-04 05:05` timestamp line, which would have created a duplicate live post.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json`
  - Objective-Proved: Proves which current-date top-2 package output was generated for the 2026-04-04 run.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the refreshed exact post body prepared from the current generated package.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the scheduled canonical workflow completed all gated steps successfully for the live 05:01 run.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the exact live POST request body and X API success response, including tweet ID `2040278570635849759`.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `Invoke-WebRequest -UseBasicParsing 'http://localhost:5000/api/health'`
  - Objective-Proved: Proves the local API was reachable during technical validation.
  - Status: captured

- Evidence-Type: user_feedback
  - Artifact: `Pending user verification request in final response`
  - Objective-Proved: Requests explicit user confirmation before lifecycle completion because this task changes user-visible external posting behavior.
  - Status: planned

## Implementation Log

- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-04 05:01:18 Europe/London: Confirmed the scheduled canonical workflow run for `2026-04-04` succeeded end-to-end; `twitter_workflow_status.json` recorded successful `verify_api`, `generate_content`, `validate_payload`, and `submit_post` steps.
- 2026-04-04 05:01:24 Europe/London: Confirmed `twitter_x_api_post_response.json` captured a successful live X API response with tweet ID `2040278570635849759`.
- 2026-04-04 05:05:11 Europe/London: Re-ran `generate_posting_package.py --date 2026-04-04` to execute the non-posting validation steps requested in this task and refreshed the top-2 package artifacts.
- 2026-04-04 05:05:13 Europe/London: Re-checked `GET /api/health` locally and confirmed the API remained healthy.
- 2026-04-04 05:05:20 Europe/London: Compared the refreshed 05:05 payload against the already-posted 05:01 payload and found the only delta was the regenerated `Update at ...` timestamp line; did not issue a duplicate second live POST.

## Changes Made

- No source-code changes were required in the workspace; the requested top-2 canonical generation and posting workflow was already implemented in:
  - `TradeApps\breakout\fs\run_twitter_canonical_workflow.py`
  - `TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
- Refreshed runtime artifacts for `2026-04-04`:
  - `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json`
  - `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.md`
  - `TradeApps\breakout\fs\temp_tweet_top2.txt`
- Updated this lifecycle file with normalized evidence, execution notes, and validation results.

## Validation

- `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-04`
  - Pass. Wrote the expected `2026-04-04` package files and refreshed `temp_tweet_top2.txt`.
- Manual payload validation against `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json`
  - Pass. `temp_tweet_top2.txt` was non-empty and matched `top2_cross_product_post` exactly.
- `Invoke-WebRequest -UseBasicParsing 'http://localhost:5000/api/health'`
  - Pass. Returned `{"status":"ok","ts":"2026-04-04T04:05:13.214248"}`.
- Scheduled workflow artifact review: `TradeApps\breakout\fs\twitter_workflow_status.json`
  - Pass. `final_status` was `success` for `run_date=2026-04-04`.
- Scheduled workflow artifact review: `TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Pass. Recorded `status_code=200`, `success=true`, and `tweet_id=2040278570635849759`.
- User verification requested on 2026-04-04 in the final response for the externally visible X posting behavior.

## Risks/Notes

- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- If the generated package source date lags the actual run date, record the mismatch explicitly before posting.
- If the local API server is unreachable on `localhost:5000`, stop and record the concrete blocker.
- After each successful execution, the scheduler should queue the next run 4 hours later.
- Re-running the generator after a successful scheduled post will usually change the `Update at ...` line even when the underlying source-derived leader values are unchanged; avoid issuing a second manual POST unless a duplicate X post is explicitly desired.

## Completion Status

- State: Awaiting user verification
- Timestamp: 2026-04-04 05:05:20 Europe/London
Next Scheduled For: 2026-04-04 09:00:00+01:00
