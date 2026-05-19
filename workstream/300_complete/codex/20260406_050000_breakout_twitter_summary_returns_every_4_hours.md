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
Suggested Agent: codex
Task Summary: Every 4 hours, generate the current-date top-2 cross-product social package from source data, refresh `temp_tweet_top2.txt`, then post that exact payload through `POST /api/social/x_api_post` and record the live response.
Destination Folder: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\`
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
Scheduled For: 2026-04-06 05:00:00+01:00
Next Scheduled For: 2026-04-06 09:00:00+01:00
Spawned From: 20260406_010000_breakout_twitter_summary_returns_every_4_hours.md

## Plan
- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08` completes successfully and writes `top2_cross_product_post.json`, `top2_cross_product_post.md`, and `temp_tweet_top2.txt`.
  - Evidence: Generator completed at 2026-04-08 14:19 Europe/London and wrote the expected package files under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\`.
- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json[top2_cross_product_post]`, and remains within X length limits.
  - Evidence: Validation script returned `{"match": true, "char_count": 194, "non_empty": true, "within_limit": true}` against the refreshed 2026-04-08 artifacts.
- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: Health route returned `{"status":"ok","ts":"2026-04-08T13:19:27.060678"}` before the gated workflow run.
- [x] 4. Post the refreshed payload to X.
  - [x] Test: `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-08` returns success and records the live route response in `twitter_x_api_post_response.json`, or records a concrete blocker.
  - Evidence: Workflow returned exit code `0`; `twitter_workflow_status.json` recorded `final_status: success`; `twitter_x_api_post_response.json` recorded HTTP 200 with tweet ID `2041868680724685054`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\top2_cross_product_post.json`
  - Objective-Proved: Proves which current-date package output was generated for the recurring run.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the exact body prepared for X and confirms it matches the current generated package.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `GET http://localhost:5000/api/health` and `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the local posting workflow prerequisites passed and the gated workflow recorded per-step status.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the posting attempt outcome for the current recurring run.
  - Status: captured
- Evidence-Type: user_feedback
  - Artifact: Verification requested from user after successful live post with tweet ID `2041868680724685054`.
  - Objective-Proved: Records that user verification is still required before this task can be closed and moved to `300_complete`.
  - Status: captured

## Implementation Log
- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-08 15:00:00 Europe/London: Normalized this lifecycle file to the required workstream schema before executing the live workflow steps.
- 2026-04-08 15:19:11 Europe/London: Ran `generate_posting_package.py --date 2026-04-08`; generator wrote the 2026-04-08 top-2, top-5, and consolidated leaderboard artifacts and refreshed `temp_tweet_top2.txt`.
- 2026-04-08 15:19:27 Europe/London: Confirmed `GET http://localhost:5000/api/health` returned `status=ok`.
- 2026-04-08 15:19:31 Europe/London: Verified `temp_tweet_top2.txt` matched `top2_cross_product_post.json[top2_cross_product_post]` and measured 194 characters.
- 2026-04-08 15:19:50 Europe/London: Ran `run_twitter_canonical_workflow.py 2026-04-08`; gated workflow posted successfully and recorded tweet ID `2041868680724685054`.
- 2026-04-08 15:20:00 Europe/London: Requested user verification for the successful live-posting outcome before final archival.

## Changes Made
- Combined current-date top-2 package generation with X posting in a single recurring workflow.
- Switched the recurring payload target from `temp_tweet.txt` to `temp_tweet_top2.txt`.
- Anchored the recurring definition to the proven workflow-ready package generation and X posting task records.
- Normalized the lifecycle document so execution evidence can be recorded step-by-step against the mandated checklist format.
- Executed the live recurring workflow for 2026-04-08 and captured the generated package, payload validation, workflow status, and X API response artifacts.

## Validation
- Recurring definition updated to reflect the current source-derived top-2 social publishing flow.
- `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08`
  - Pass: expected package files written under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\`.
- Payload validation script against `top2_cross_product_post.json` and `temp_tweet_top2.txt`
  - Pass: `match=true`, `char_count=194`, `non_empty=true`, `within_limit=true`.
- `GET http://localhost:5000/api/health`
  - Pass: returned `{"status":"ok","ts":"2026-04-08T13:19:27.060678"}`.
- `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-08`
  - Pass: exit code `0`; `twitter_workflow_status.json` shows `final_status: success`; `twitter_x_api_post_response.json` shows HTTP 200 and tweet ID `2041868680724685054`.
- User verification requested on 2026-04-08 for the live-posting outcome and scheduler behavior.

## Risks/Notes
- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- If the generated package source date lags the actual run date, record the mismatch explicitly before posting.
- If the local API server is unreachable on `localhost:5000`, stop and record the concrete blocker.
- After each successful execution, the scheduler should queue the next run 4 hours later.

## Completion Status
- State: AWAITING_USER_VERIFICATION
- Timestamp: 2026-04-08 15:20:00 Europe/London
