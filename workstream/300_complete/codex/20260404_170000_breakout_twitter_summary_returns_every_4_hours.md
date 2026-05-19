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
Scheduled For: 2026-04-04 17:00:00+01:00
Next Scheduled For: 2026-04-04 21:00:00+01:00
Spawned From: 20260404_130000_breakout_twitter_summary_returns_every_4_hours.md

## Plan
- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-04` completes successfully.
  - Evidence: Generator output in `TradeApps\breakout\fs\twitter_workflow_status.json` shows the package artifacts were rewritten under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\`.

- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: `twitter_workflow_status.json` recorded `Validated payload (184 chars)` and `temp_tweet_top2.txt` matched `top2_cross_product_post.json`.

- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: `Invoke-RestMethod http://localhost:5000/api/health` returned `{"status":"ok","ts":"2026-04-04T16:06:16.262775"}` and the workflow health gate also passed.

- [x] 4. Post the refreshed payload to X.
  - [x] Test: `POST /api/social/x_api_post` returns a success response with a tweet ID or a concrete blocker such as a rate limit or credential error.
  - Evidence: The 17:00 slot already posted successfully at `2026-04-04T17:02:40.807660` according to `GET /api/social/status`; the later duplicate rerun at `2026-04-04T17:06` returned the concrete blocker `Rate limit: wait 6 more minutes` in `twitter_x_api_post_response.json`.

## Evidence
Objective-Delivery-Coverage: 95%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json`
  - Objective-Proved: Proves which current-date package output was generated for the recurring run.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the exact payload prepared for posting and that the refreshed top-2 text exists on disk.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the gated workflow passed health, generation, and payload validation, and that the duplicate rerun failed only on the posting cooldown gate.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `GET http://localhost:5000/api/social/status`
  - Objective-Proved: Proves the scheduled 17:00 recurring slot had already posted successfully at `2026-04-04T17:02:40.807660` with trigger `breakout_top2_cross_product_every_4_hours`.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the live route response for the duplicate rerun, including the concrete rate-limit blocker after the successful 17:02 publish.
  - Status: captured

- Evidence-Type: user_feedback
  - Artifact: `Pending user verification of the live X post for the 2026-04-04 17:02 slot`
  - Objective-Proved: Confirms the user accepts the live posted output as the intended recurring 17:00 publish result.
  - Status: planned

## Implementation Log
- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-04 17:06:16 Europe/London: Confirmed the local API health endpoint was reachable before rerunning the scheduled flow.
- 2026-04-04 17:06:14 Europe/London: Ran `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-04`.
- 2026-04-04 17:06:19 Europe/London: Captured `twitter_workflow_status.json` and `twitter_x_api_post_response.json`; generation and payload validation passed, but the final post step returned a cooldown blocker.
- 2026-04-04 17:06:54 Europe/London: Queried `GET /api/social/status` and confirmed the scheduled 17:00 slot had already posted successfully at `2026-04-04T17:02:40.807660`.
- 2026-04-04 17:07:00 Europe/London: Reconciled this stale in-progress lifecycle file with the already-delivered 17:00 slot outcome and requested user verification.

## Changes Made
- Executed the already-implemented recurring top-2 generate-then-post workflow for the scheduled `2026-04-04 17:00+01:00` slot.
- Refreshed the package and payload artifacts under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\` and `TradeApps\breakout\fs\temp_tweet_top2.txt`.
- Refreshed the workflow/result artifacts `TradeApps\breakout\fs\twitter_workflow_status.json` and `TradeApps\breakout\fs\twitter_x_api_post_response.json`.
- No additional code edits were required after inspection; the task objective had already been delivered by the successful 17:02 scheduled post, and the 17:06 rerun only encountered the expected cooldown.
- Noted the lifecycle duplication: an authoritative completed record already exists at `C:\Users\edebe\eds\workstream\300_complete\codex\20260404_170000_breakout_twitter_summary_returns_every_4_hours.md`.

## Validation
- `Invoke-RestMethod -Uri 'http://localhost:5000/api/health' | ConvertTo-Json -Depth 10`
  - Result: Passed with `{"status":"ok","ts":"2026-04-04T16:06:16.262775"}`.
- `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-04`
  - Result: Partial pass. Generation and payload validation succeeded, and the route call returned the concrete blocker `{"error":"Rate limit: wait 6 more minutes","success":false}` because the 17:00 slot had already posted.
- `Invoke-RestMethod -Uri 'http://localhost:5000/api/social/status' | ConvertTo-Json -Depth 10`
  - Result: Passed and confirmed `can_post=false`, `last_post_time="2026-04-04T17:02:40.807761"`, and a successful recent post for trigger `breakout_top2_cross_product_every_4_hours`.
- 2026-04-04 17:07:00 Europe/London: User verification requested for the live X post associated with the successful 17:02 recurring publish.

## Risks/Notes
- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- If the generated package source date lags the actual run date, record the mismatch explicitly before posting.
- If the local API server is unreachable on `localhost:5000`, stop and record the concrete blocker.
- After each successful execution, the scheduler should queue the next run 4 hours later.
- This lifecycle item is stale relative to the already-completed record in `workstream\300_complete\codex`; both refer to the same 17:00 scheduled slot.

## Completion Status
- State: Awaiting user verification
- Timestamp: 2026-04-04 17:07:00+01:00
