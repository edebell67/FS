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
Scheduled For: 2026-04-03 17:00:00+01:00
Next Scheduled For: 2026-04-03 21:00:00+01:00
Spawned From: 20260403_130000_breakout_twitter_summary_returns_every_4_hours.md

## Plan

- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-03` completes successfully.
  - Evidence: 2026-04-03 17:02 Europe/London run wrote `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\top2_cross_product_post.json` and `.md`; unit regression `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` passed (`Ran 2 tests ... OK`).

- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: Validation script confirmed `payload_non_empty=true`, `matches_package=true`, `payload_length=190`, `today_source_date=2026-04-03`, `today_source_last_update=2026-04-03T17:02:06.670448`, and payload text `2026-04-03 leaders ... NQ leading +1,740 ... ES +885 -> gap: 855 ... 2,733 strategy-product combinations tracked. Only the strongest traded.` before the live post.

- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: Health check returned HTTP 200 with `{"status":"ok","ts":"2026-04-03T16:02:32.161353"}` before the posting run; canonical workflow health gate also passed and recorded a second successful API reachability check in `twitter_workflow_status.json`.

- [x] 4. Post the refreshed payload to X.
  - [x] Test: `POST /api/social/x_api_post` returns a success response with a tweet ID or a concrete blocker such as a rate limit or credential error.
  - Evidence: `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03` completed with `final_status=success`; `TradeApps\breakout\fs\twitter_x_api_post_response.json` recorded HTTP 200 and `tweet_id=2040037326571683844` for trigger `breakout_top2_cross_product_every_4_hours`.

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
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the posting attempt outcome for the current recurring run.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Objective-Proved: Proves the canonical workflow payload validation logic still passes regression coverage after the live run.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `User verification requested in assistant final response for posted X update and task outcome`
  - Objective-Proved: Records the required user-visible verification request before lifecycle completion.
  - Status: captured

## Implementation Log

- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-03 17:02 Europe/London: Ran `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-03` and refreshed the current-date top-2 package artifacts plus `temp_tweet_top2.txt`.
- 2026-04-03 17:02 Europe/London: Verified `temp_tweet_top2.txt` was non-empty, matched `top2_cross_product_post.json`, and resolved to source date `2026-04-03` with source last update `2026-04-03T17:02:06.670448`.
- 2026-04-03 17:02 Europe/London: Confirmed `GET http://localhost:5000/api/health` returned HTTP 200 with `status=ok`.
- 2026-04-03 17:02 Europe/London: Executed `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`, which regenerated the payload, posted it via `/api/social/x_api_post`, and captured the live response artifact with tweet ID `2040037326571683844`.
- 2026-04-03 17:02 Europe/London: Ran `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` to confirm the canonical workflow validation tests still pass.

## Changes Made

- Combined current-date top-2 package generation with X posting in a single recurring workflow.
- Switched the recurring payload target from `temp_tweet.txt` to `temp_tweet_top2.txt`.
- Anchored the recurring definition to the proven workflow-ready package generation and X posting task records.
- Executed the live recurring run for `2026-04-03`, producing updated package artifacts, refreshed payload text, `twitter_workflow_status.json`, and `twitter_x_api_post_response.json`.

## Validation

- `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-03`
  - Result: success; wrote `top5_weekly_posting_package.json`, `top5_weekly_posting_package.md`, `top2_cross_product_post.json`, and `top2_cross_product_post.md` under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03`.
- Payload verification script against `temp_tweet_top2.txt` and `top2_cross_product_post.json`
  - Result: `payload_non_empty=true`, `matches_package=true`, `payload_length=190`, `today_source_date=2026-04-03`, `today_source_last_update=2026-04-03T17:02:06.670448`.
- `GET http://localhost:5000/api/health`
  - Result: HTTP 200 with `{"status":"ok","ts":"2026-04-03T16:02:32.161353"}`.
- `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`
  - Result: success; `twitter_workflow_status.json` recorded all four gates as `ok=true`, and `twitter_x_api_post_response.json` captured HTTP 200 with `tweet_id=2040037326571683844`.
- `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Result: passed (`Ran 2 tests in 0.141s`, `OK`).
- User verification requested in assistant final response
  - Result: pending user pass/fail confirmation for the posted X update and lifecycle closure.

## Risks/Notes

- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- If the generated package source date lags the actual run date, record the mismatch explicitly before posting.
- If the local API server is unreachable on `localhost:5000`, stop and record the concrete blocker.
- After each successful execution, the scheduler should queue the next run 4 hours later.
- Pre-post payload verification and the canonical posting workflow observed different snapshots as live source data updated during the run window. The actual posted payload is the later canonical workflow payload recorded in `twitter_x_api_post_response.json`, and that artifact is the authoritative live-post record for this execution.

## Completion Status

- State: Awaiting user verification
- Timestamp: 2026-04-03 17:02:47 Europe/London
