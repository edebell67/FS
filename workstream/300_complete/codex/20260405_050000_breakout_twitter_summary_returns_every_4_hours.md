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
Scheduled For: 2026-04-05 05:00:00+01:00
Next Scheduled For: 2026-04-05 09:00:00+01:00
Spawned From: 20260405_010000_breakout_twitter_summary_returns_every_4_hours.md

## Plan

- [x] 1. Verify the local API is reachable before any posting workflow runs.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response with `{"status":"ok"}`.
  - Evidence: Health endpoint returned HTTP `200` with `{"status":"ok","ts":"2026-04-05T04:04:49.875669"}` at `2026-04-05 05:04:47 Europe/London`.

- [x] 2. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-05` completes successfully.
  - Evidence: Generator exited `0` and wrote `top5_weekly_posting_package.json`, `top5_weekly_posting_package.md`, `top2_cross_product_post.json`, and `top2_cross_product_post.md` under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-05`.

- [x] 3. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: Validation confirmed `payload_non_empty=true`, `matches_package=true`, `payload_length=184`, `today_source_date=2026-04-05`, `today_source_last_update=2026-04-05T05:05:10.223970`, leaders `SI +235` and `HG +235`, and `strategy_product_count=759`.

- [x] 4. Post the refreshed payload to X and capture the live route result.
  - [x] Test: `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-05` returns success with a tweet ID or a concrete blocker such as a rate limit or credential error.
  - Evidence: Canonical workflow exited `1` only because `submit_post` returned the concrete blocker `HTTP 400 {"error":"Rate limit: wait 5 more minutes","success":false}`; `GET /api/social/status` confirmed the same recurring trigger had already posted successfully at `2026-04-05T05:01:09.984589`.

- [x] 5. Run regression coverage for the canonical workflow.
  - [x] Test: `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` passes.
  - Evidence: Unittest run exited `0` with `Ran 2 tests in 0.082s` and `OK`.

## Evidence

Objective-Delivery-Coverage: 90%
Auto-Acceptance: false

- Evidence-Type: test_output
  - Artifact: `GET http://localhost:5000/api/health -> 200 {"status":"ok","ts":"2026-04-05T04:04:49.875669"}`
  - Objective-Proved: Proves the local posting API was reachable before the scheduled workflow executed.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-05\top2_cross_product_post.json`
  - Objective-Proved: Proves which current-date package output was generated for the recurring run.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the exact body prepared for X and confirms it matched the current generated package.
  - Status: captured

- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the gated workflow step results for this scheduled run.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the live route response and exact request body used by the canonical workflow.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Objective-Proved: Proves regression coverage still passes for canonical payload validation behavior.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `GET http://localhost:5000/api/social/status -> can_post=false, last_post_time=2026-04-05T05:01:09.984620, reason='Rate limit: wait 5 more minutes'`
  - Objective-Proved: Proves the scheduler had already completed the 05:00 recurring post window and the manual rerun was rejected only because the active cooldown window was still in effect.
  - Status: captured

- Evidence-Type: user_feedback
  - Artifact: `pending_user_verification`
  - Objective-Proved: Pending operator confirmation that the expected recurring X post for the 2026-04-05 05:00 slot is visible and acceptable on the target account timeline.
  - Status: planned

## Implementation Log

- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-05 05:00:00 Europe/London: Resumed the recurring execution task for the 05:00 slot and normalized the lifecycle file to match the canonical gated workflow and allowed evidence schema before validation.
- 2026-04-05 05:04:47 Europe/London: Verified `GET http://localhost:5000/api/health` returned HTTP `200` with `{"status":"ok","ts":"2026-04-05T04:04:49.875669"}`.
- 2026-04-05 05:05:15 Europe/London: Ran `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-05`; generator exited `0` and refreshed the current-date package artifacts plus `temp_tweet_top2.txt`.
- 2026-04-05 05:05:20 Europe/London: Validated `temp_tweet_top2.txt` against `top2_cross_product_post.json`; the payload matched exactly, remained within the X character limit, and resolved to source date `2026-04-05`.
- 2026-04-05 05:05:56 Europe/London: Ran `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-05`; verify, generate, and validate passed, then `submit_post` returned `HTTP 400 {"error":"Rate limit: wait 5 more minutes","success":false}`.
- 2026-04-05 05:06:04 Europe/London: Queried `GET http://localhost:5000/api/social/status`; endpoint reported `last_post_time=2026-04-05T05:01:09.984620`, `can_post=false`, and a successful same-trigger post already recorded for the 05:00 window.
- 2026-04-05 05:06:12 Europe/London: Ran `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`; result was `Ran 2 tests in 0.082s` and `OK`.

## Changes Made

- Normalized this lifecycle file so the checklist order matches the enforced health -> generate -> validate -> post workflow.
- Replaced non-standard evidence types with allowed evidence types and staged the execution evidence artifacts for this slot.
- Refreshed `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-05\top5_weekly_posting_package.json`.
- Refreshed `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-05\top5_weekly_posting_package.md`.
- Refreshed `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-05\top2_cross_product_post.json`.
- Refreshed `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-05\top2_cross_product_post.md`.
- Refreshed `TradeApps\breakout\fs\temp_tweet_top2.txt`.
- Updated `TradeApps\breakout\fs\twitter_workflow_status.json` with the 2026-04-05 05:05 gated run results.
- Updated `TradeApps\breakout\fs\twitter_x_api_post_response.json` with the concrete duplicate-run rate-limit response for the manual rerun.
- No application code changes were required; the workflow implementation was already correct and the observed failure mode was a runtime cooldown after a successful scheduled post.

## Validation

- `GET http://localhost:5000/api/health`
  - Result: Pass.
  - Summary: Returned HTTP `200` with `{"status":"ok","ts":"2026-04-05T04:04:49.875669"}`.

- `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-05`
  - Result: Pass.
  - Summary: Wrote the 2026-04-05 package and top-2 artifacts successfully.

- Payload parity check between `temp_tweet_top2.txt` and `top2_cross_product_post.json`
  - Result: Pass.
  - Summary: `matches=true`, `char_count=184`, `today_source_date=2026-04-05`, `today_source_last_update=2026-04-05T05:05:10.223970`, leaders `SI +235` and `HG +235`, `strategy_product_count=759`.

- `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-05`
  - Result: Pass for blocker capture, not for duplicate post creation.
  - Summary: Workflow exited `1` after `submit_post` returned `HTTP 400 {"error":"Rate limit: wait 5 more minutes","success":false}`. This was a concrete blocker and occurred because the recurring trigger had already posted successfully at `2026-04-05T05:01:09.984589`.

- `GET http://localhost:5000/api/social/status`
  - Result: Pass.
  - Summary: Returned `can_post=false`, `last_post_time=2026-04-05T05:01:09.984620`, `reason="Rate limit: wait 5 more minutes"`, and `recent_posts[0]` showed the same recurring trigger had already posted successfully at `2026-04-05T05:01:09.984589`.

- `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Result: Pass.
  - Summary: `Ran 2 tests in 0.082s` and `OK`.

- User verification requested:
  - Request: Confirm the expected recurring X post for `2026-04-05 05:01 Europe/London` is visible on the target X account timeline and that treating the manual 05:05 rerun blocker as the recorded live response for this slot is acceptable.
  - Result: Pending user response.

## Risks/Notes

- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- If the generated package source date lags the actual run date, record the mismatch explicitly before posting.
- The local API was reachable. The manual rerun was blocked only because the same trigger had already posted successfully at `2026-04-05T05:01:09.984589`.
- Re-running again after the cooldown would create an extra X post for the same 05:00 slot, so no automatic retry was performed.
- After each successful scheduled execution, the scheduler should queue the next run 4 hours later. The next scheduled run remains `2026-04-05 09:00:00+01:00`.

## Completion Status

- State: Awaiting user verification
- Timestamp: 2026-04-05 05:06:12 Europe/London
