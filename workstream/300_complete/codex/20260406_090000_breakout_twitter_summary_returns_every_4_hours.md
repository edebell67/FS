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
Destination Folder: `C:\Users\edebe\eds\TradeApps\breakout\fs\`
Dependency: None
Required Skill: `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`
Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`
Scheduled For: 2026-04-06 09:00:00+01:00
Next Scheduled For: 2026-04-06 13:00:00+01:00
Spawned From: 20260406_050000_breakout_twitter_summary_returns_every_4_hours.md

## Plan
- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08` completes successfully.
  - Evidence: 2026-04-08 14:27 Europe/London run wrote `top2_cross_product_post.json` and `top2_cross_product_post.md` under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08`; regression `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` passed with `Ran 2 tests ... OK`.
- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: Validation script confirmed `payload_non_empty=true`, `matches_package=true`, `generated_date=2026-04-08`, `today_source_date=2026-04-08`, `today_source_last_update=2026-04-08T14:27:10.703606`, `strategy_product_count=2945`, and payload length `194`.
- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: Health check returned `{"status":"ok","ts":"2026-04-08T13:27:40.138611"}` before the posting workflow run.
- [x] 4. Post the refreshed payload to X.
  - [x] Test: `POST /api/social/x_api_post` returns a success response with a tweet ID or a concrete blocker such as a rate limit or credential error.
  - Evidence: Initial 2026-04-08 14:27 Europe/London workflow attempt recorded transient rate limiting (`wait 2 more minutes`), then retry at 14:30 succeeded; `twitter_x_api_post_response.json` captured HTTP 200 with `tweet_id=2041871401896841447` for trigger `breakout_top2_cross_product_every_4_hours`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\top2_cross_product_post.json`
  - Objective-Proved: Proves which current-date package output was generated for the recurring run.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the exact body prepared for posting and that it matched the generated package.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Objective-Proved: Proves the canonical workflow payload validation regression still passes after the live run.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the gated workflow finished with `final_status=success` and all four steps recorded `ok=true` for the successful retry.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the posting attempt outcome and the exact live X API response for the recurring run, including `tweet_id=2041871401896841447`.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `User verification requested in final response for tweet_id=2041871401896841447`
  - Objective-Proved: Requests explicit pass/fail confirmation on the live recurring post before final completion.
  - Status: planned

## Implementation Log
- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-08 14:25 Europe/London: Read `skills\workstream-task-lifecycle\SKILL.md`, then loaded `skills\twitter-canonical-posting\SKILL.md` and the current task file before inspecting the recurring workflow entrypoint plus generator dependencies.
- 2026-04-08 14:27 Europe/London: Ran `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08` and refreshed the current-date social package artifacts plus `temp_tweet_top2.txt`.
- 2026-04-08 14:27 Europe/London: Verified `temp_tweet_top2.txt` was non-empty, matched `top2_cross_product_post.json`, and resolved to source date `2026-04-08` with source last update `2026-04-08T14:27:10.703606`.
- 2026-04-08 14:27 Europe/London: Confirmed the local API health endpoint returned `status=ok` before running the canonical posting workflow.
- 2026-04-08 14:27 Europe/London: Executed `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-08`; the first attempt failed only at the post gate with transient X rate limiting (`wait 2 more minutes`) while still writing `twitter_workflow_status.json` and `twitter_x_api_post_response.json`.
- 2026-04-08 14:30 Europe/London: Retried `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-08` after the rate-limit window elapsed; the retry completed successfully and captured live tweet ID `2041871401896841447`.
- 2026-04-08 14:30 Europe/London: Ran `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` to confirm the canonical workflow validation tests still pass.
- 2026-04-08 14:30 Europe/London: Updated this lifecycle file with captured evidence, checklist completion, and a pending user-verification gate.

## Changes Made
- Combined current-date top-2 package generation with X posting in a single recurring workflow.
- Switched the recurring payload target from `temp_tweet.txt` to `temp_tweet_top2.txt`.
- Anchored the recurring definition to the proven workflow-ready package generation and X posting task records.
- Executed the live recurring run for `2026-04-08`, producing updated package artifacts, refreshed payload text, `twitter_workflow_status.json`, and `twitter_x_api_post_response.json`.
- Normalized this lifecycle file to the required workstream template by adding `Destination Folder`, compliant evidence types, captured validation evidence, and an explicit completion state.

## Validation
- `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08`
  - Result: success; wrote `top5_weekly_posting_package.json`, `top5_weekly_posting_package.md`, `top2_cross_product_post.json`, `top2_cross_product_post.md`, `consolidated_leaderboard_posting_package.json`, and `consolidated_leaderboard_posting_package.md` under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08`.
- Payload validation script against `temp_tweet_top2.txt` and `top2_cross_product_post.json`
  - Result: success; payload existed, was non-empty, matched the generated package exactly, and resolved to source date `2026-04-08` with source last update `2026-04-08T14:27:10.703606`.
- `GET http://localhost:5000/api/health`
  - Result: success; returned `{"status":"ok","ts":"2026-04-08T13:27:40.138611"}`.
- `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-08`
  - Result: first attempt hit transient rate limiting (`HTTP 400`, `wait 2 more minutes`) and captured the blocker artifact.
- `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-08`
  - Result: retry success; `twitter_workflow_status.json` recorded all four gates as `ok=true`, and `twitter_x_api_post_response.json` captured HTTP 200 with `tweet_id=2041871401896841447`.
- `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Result: success; `Ran 2 tests in 0.080s` and `OK`.
- User verification request
  - Result: pending; final response asks for pass/fail confirmation on package generation, payload contents, and the live X post represented by `tweet_id=2041871401896841447`.

## Risks/Notes
- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- If the generated package source date lags the actual run date, record the mismatch explicitly before posting.
- If the local API server is unreachable on `localhost:5000`, stop and record the concrete blocker.
- X API posting can temporarily rate-limit the recurring task even when the generator and local route are healthy; retry only after the reported wait window expires.
- After each successful execution, the scheduler should queue the next run 4 hours later.

## Completion Status
- State: Awaiting user verification
- Timestamp: 2026-04-08T14:30:52.4741808+01:00
