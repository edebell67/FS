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
Destination Folder: `C:\Users\edebe\eds\TradeApps\breakout\fs\`
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
Scheduled For: 2026-04-05 21:00:00+01:00
Next Scheduled For: 2026-04-06 01:00:00+01:00
Spawned From: 20260405_170000_breakout_twitter_summary_returns_every_4_hours.md

## Plan
- [x] 1. Verify the local API is reachable before allowing the gated workflow to post.
  - [x] Test: `Invoke-RestMethod -Uri 'http://localhost:5000/api/health' -Method Get | ConvertTo-Json -Depth 10` returns a concrete health response with `"status": "ok"`.
  - Evidence: `{"status":"ok","ts":"2026-04-08T12:45:56.592831"}`
- [x] 2. Confirm the current-date top-2 cross-product package was generated for `2026-04-08`.
  - [x] Test: `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\top2_cross_product_post.json'` shows `generated_date=2026-04-08`, `today_source_date=2026-04-08`, leaders `SI` and `CL`, and the package text written at `2026-04-08T13:41:29`.
  - Evidence: `top2_cross_product_post.json` contains the generated `top2_cross_product_post` body and source metadata for the `2026-04-08` run.
- [x] 3. Validate the refreshed payload before posting.
  - [x] Test: `@' ... '@ | python -` comparison script returns `"tweet_matches_package": true`, `"tweet_length": 194`, and reads `response_success=true` from the current workflow artifacts.
  - Evidence: `temp_tweet_top2.txt` matches `top2_cross_product_post.json`, remains non-empty, and reflects only the source-derived values recorded in the package artifact.
- [x] 4. Confirm the live X posting outcome for the current recurring run.
  - [x] Test: `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json'` and `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json'` show `run_date=2026-04-08`, HTTP `200`, `success=true`, and `tweet_id=2041859050053234770`.
  - Evidence: The current 4-hour slot completed successfully at `2026-04-08T13:41` and produced tweet ID `2041859050053234770`; a duplicate manual POST was intentionally not forced after the successful live run.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\top2_cross_product_post.json`
  - Objective-Proved: Proves the exact current-date package output, source date, source last update, and generated text for the recurring run.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the exact body prepared for posting and confirms the live payload file is populated.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `Invoke-RestMethod -Uri 'http://localhost:5000/api/health' -Method Get | ConvertTo-Json -Depth 10` -> `{"status":"ok","ts":"2026-04-08T12:45:56.592831"}`
  - Objective-Proved: Proves the local posting API was reachable for the current run.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python payload comparison summary` -> `{"tweet_matches_package": true, "tweet_length": 194, "response_success": true, "tweet_id": "2041859050053234770"}`
  - Objective-Proved: Proves the prepared payload matches the generated package and the current workflow artifacts are internally consistent.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the exact live route request and the successful `POST /api/social/x_api_post` response for the current recurring run.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the gated workflow completed all four steps successfully for `2026-04-08`.
  - Status: captured
- Evidence-Type: url
  - Artifact: `https://x.com/i/web/status/2041859050053234770`
  - Objective-Proved: Provides the live tweet access path derived from the returned tweet ID for user verification.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `Pending user confirmation for package generation, payload match, and live tweet visibility/content using tweet ID 2041859050053234770`
  - Objective-Proved: Tracks the required user-visible verification gate before moving the task to complete.
  - Status: planned

## Implementation Log
- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-08 13:45:56+01:00 Europe/London: Verified `GET http://localhost:5000/api/health` returned `{"status":"ok","ts":"2026-04-08T12:45:56.592831"}`.
- 2026-04-08 13:46:00+01:00 Europe/London: Read the current generated package artifact `json/live/social_posting_package/2026-04-08/top2_cross_product_post.json` and confirmed the run resolved to source date `2026-04-08` with leaders `SI` and `CL`.
- 2026-04-08 13:46:05+01:00 Europe/London: Verified `temp_tweet_top2.txt` matches `top2_cross_product_post.json` and remains within X length limits.
- 2026-04-08 13:46:10+01:00 Europe/London: Confirmed the gated workflow artifacts already captured a successful current-slot live post at `2026-04-08T13:41`, including HTTP `200` and tweet ID `2041859050053234770`.
- 2026-04-08 13:47:33+01:00 Europe/London: Updated the lifecycle record to align with the required API-first gated workflow and left the task awaiting user verification instead of forcing a duplicate post.

## Changes Made
- Combined current-date top-2 package generation with X posting in a single recurring workflow.
- Switched the recurring payload target from `temp_tweet.txt` to `temp_tweet_top2.txt`.
- Anchored the recurring definition to the proven workflow-ready package generation and X posting task records.
- Updated this lifecycle file to match the enforced API-first gating in `skills\twitter-canonical-posting\SKILL.md` and the existing `run_twitter_canonical_workflow.py` implementation.
- No additional product code edits were required during this execution pass; the existing workflow code and artifacts already satisfied the requested behavior for the current `2026-04-08` run.

## Validation
- `Invoke-RestMethod -Uri 'http://localhost:5000/api/health' -Method Get | ConvertTo-Json -Depth 10`
  - Pass: returned `{"status":"ok","ts":"2026-04-08T12:45:56.592831"}`
- `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\top2_cross_product_post.json'`
  - Pass: package shows `generated_date=2026-04-08`, `today_source_date=2026-04-08`, leaders `SI` and `CL`, and post text `2026-04-08 leaders ...`
- `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt'`
  - Pass: payload is non-empty and matches the package text exactly
- `@' ... '@ | python -`
  - Pass: returned `tweet_matches_package=true`, `tweet_length=194`, `response_success=true`, `tweet_id=2041859050053234770`
- `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json'`
  - Pass: all steps `verify_api`, `generate_content`, `validate_payload`, and `submit_post` are `ok=true` for `run_date=2026-04-08`
- `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json'`
  - Pass: route artifact records HTTP `200`, `success=true`, and `tweet_id=2041859050053234770`
- User verification requested on 2026-04-08 for:
  - package generation for `2026-04-08`
  - payload match between the package and `temp_tweet_top2.txt`
  - live tweet visibility/content for tweet ID `2041859050053234770`

## Risks/Notes
- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- If the generated package source date lags the actual run date, record the mismatch explicitly before posting.
- If the local API server is unreachable on `localhost:5000`, stop and record the concrete blocker.
- After each successful execution, the scheduler should queue the next run 4 hours later.
- A second manual `POST /api/social/x_api_post` was not triggered during this update because the current slot had already posted successfully at `2026-04-08T13:41`; rerunning it would have created a duplicate live tweet outside the scheduler cadence.

## Completion Status
- State: Awaiting user verification
- Timestamp: 2026-04-08T13:47:33.5996281+01:00
