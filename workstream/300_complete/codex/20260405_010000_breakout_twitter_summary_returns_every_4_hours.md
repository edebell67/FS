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
Scheduled For: 2026-04-05 01:00:00+01:00
Next Scheduled For: 2026-04-05 05:00:00+01:00
Spawned From: 20260404_210000_breakout_twitter_summary_returns_every_4_hours.md

## Plan

- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-05` completes successfully.
  - Evidence: Command exited `0` and wrote `top2_cross_product_post.json` and `top2_cross_product_post.md` under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-05`.

- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: `temp_tweet_top2.txt` matched `top2_cross_product_post` exactly, payload length was `184`, `today_source_date` was `2026-04-05`, leaders were `SI +235` and `HG +235`, and `strategy_product_count` was `759`.

- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: Health check returned HTTP `200` with `{"status":"ok","ts":"2026-04-05T00:04:18.412783"}`.

- [x] 4. Post the refreshed payload to X.
  - [x] Test: `POST /api/social/x_api_post` returns a success response with a tweet ID or a concrete blocker such as a rate limit or credential error.
  - Evidence: Canonical workflow run at `01:04` returned a concrete blocker `HTTP 400 {"error":"Rate limit: wait 7 more minutes","success":false}` because the same recurring trigger had already posted successfully at `2026-04-05T01:01:13.519136` per `social_posts.json` and `/api/social/status`.

## Evidence

Objective-Delivery-Coverage: 90%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-05\top2_cross_product_post.json`
  - Objective-Proved: Proves which current-date top-2 package was generated for the 2026-04-05 recurring window.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the exact prepared post body matched the generated package before the API call.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-05`
  - Objective-Proved: Proves the generator completed successfully for the scheduled date and refreshed the package artifacts.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `GET http://localhost:5000/api/health -> 200 {"status":"ok","ts":"2026-04-05T00:04:18.412783"}`
  - Objective-Proved: Proves the local posting API was reachable before the posting workflow ran.
  - Status: captured

- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the canonical workflow passed health, generation, and payload validation, then failed only on the duplicate-post rate limiter.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the live route response from the manual 01:04 posting attempt and captures the exact payload used in that attempt.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\social_posts.json`
  - Objective-Proved: Proves the scheduled `breakout_top2_cross_product_every_4_hours` trigger already posted successfully at `2026-04-05T01:01:13.519136`, making the manual rerun a duplicate in the active rate-limit window.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `User to verify the expected 2026-04-05 01:01 recurring X post is visible on the target account/timeline.`
  - Objective-Proved: Confirms the successful scheduled post is externally visible and acceptable from the user perspective.
  - Status: planned

## Implementation Log

- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-05 01:03:41 Europe/London: Ran `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-05`; generator completed successfully and refreshed the current-date package plus `temp_tweet_top2.txt`.
- 2026-04-05 01:03:58 Europe/London: Validated that `temp_tweet_top2.txt` matched `top2_cross_product_post.json` exactly and remained within the X character limit.
- 2026-04-05 01:04:18 Europe/London: Verified `GET http://localhost:5000/api/health` returned `200` with `{"status":"ok"}`.
- 2026-04-05 01:04:29 Europe/London: Ran `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-05`; workflow passed health, generation, and payload validation, then received `HTTP 400` with `Rate limit: wait 7 more minutes`.
- 2026-04-05 01:05:06 Europe/London: Queried `GET http://localhost:5000/api/social/status`; endpoint confirmed the same recurring trigger had already posted successfully at `2026-04-05T01:01:13.519540`.
- 2026-04-05 01:05:33 Europe/London: Ran `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`; payload validation tests passed.

## Changes Made

- No application code changes were required. The existing canonical workflow already generated the top-2 package, validated `temp_tweet_top2.txt`, and posted through `POST /api/social/x_api_post`.
- Refreshed current-date runtime artifacts for the 2026-04-05 window:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-05\top5_weekly_posting_package.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-05\top5_weekly_posting_package.md`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-05\top2_cross_product_post.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-05\top2_cross_product_post.md`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
- Updated this lifecycle file with completed checklist items, validation commands, and captured evidence.

## Validation

- `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-05`
  - Result: Pass.
  - Summary: Wrote the 2026-04-05 package and top-2 artifacts successfully.

- Payload parity check between `temp_tweet_top2.txt` and `top2_cross_product_post.json`
  - Result: Pass.
  - Summary: `matches=true`, `char_count=184`, `today_source_date=2026-04-05`, leaders `SI +235` and `HG +235`, `strategy_product_count=759`.

- `GET http://localhost:5000/api/health`
  - Result: Pass.
  - Summary: Returned HTTP `200` with `{"status":"ok","ts":"2026-04-05T00:04:18.412783"}`.

- `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-05`
  - Result: Pass for blocker capture, not for duplicate post creation.
  - Summary: Workflow exited `1` after `submit_post` returned `HTTP 400 {"error":"Rate limit: wait 7 more minutes","success":false}`. This was a concrete blocker and occurred because the recurring trigger had already posted successfully at `01:01`.

- `GET http://localhost:5000/api/social/status`
  - Result: Pass.
  - Summary: Returned HTTP `200`; `can_post=false`, `reason="Rate limit: wait 6 more minutes"`, and `recent_posts[0]` showed a successful `breakout_top2_cross_product_every_4_hours` post at `2026-04-05T01:01:13.519136`.

- `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Result: Pass.
  - Summary: `Ran 2 tests in 0.109s` and `OK`.

- User verification requested:
  - Request: Confirm the expected recurring X post for `2026-04-05 01:01 Europe/London` is visible on the target X account/timeline and matches the intended top-2 package for that run window.
  - Result: Pending user response.

## Risks/Notes

- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- The manual 01:04 rerun was correctly blocked because the recurring trigger had already posted at 01:01. For this schedule, forcing another retry inside the cooldown window would create an unnecessary duplicate attempt.
- `social_posts.json` stores a truncated preview of successful posts, so the exact full text of the 01:01 success is not preserved there; the exact full text is preserved for the manual 01:04 route attempt in `twitter_x_api_post_response.json`.
- Because the successful scheduled post was observed indirectly via `/api/social/status` and `social_posts.json`, coverage remains below 100% until the user verifies visibility on the account timeline.
- Next scheduled run remains `2026-04-05 05:00:00+01:00`.

## Completion Status

- State: Awaiting user verification
- Timestamp: 2026-04-05 01:05:33 Europe/London
