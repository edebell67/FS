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
Scheduled For: 2026-04-04 21:00:00+01:00
Next Scheduled For: 2026-04-05 01:00:00+01:00
Spawned From: 20260404_170000_breakout_twitter_summary_returns_every_4_hours.md

## Plan

- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-04` completes successfully.
  - Evidence: Command passed and wrote `top2_cross_product_post.json` plus `top2_cross_product_post.md` under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04`.

- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: Validation script confirmed `payload_non_empty=true`, `matches_package=true`, `payload_length=184`, `today_source_date=2026-04-04`, `today_source_last_update=2026-04-04T21:05:09.928669`, and `strategy_product_count=759`.

- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: Health endpoint returned `{"status":"ok","ts":"2026-04-04T20:05:32.456431"}`.

- [x] 4. Post the refreshed payload to X.
  - [x] Test: `POST /api/social/x_api_post` returns a success response with a tweet ID or a concrete blocker such as a rate limit or credential error.
  - Evidence: `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-04` failed closed at the submit step with concrete blocker `HTTP 400 {'error': 'Rate limit: wait 6 more minutes', 'success': False}` after verify/generate/validate all passed; `GET /api/social/status` also reported `can_post=false`, `reason='Rate limit: wait 6 more minutes'`, and a same-trigger successful post already recorded at `2026-04-04T21:01:48.067734`.

## Evidence

Objective-Delivery-Coverage: 85%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json`
  - Objective-Proved: Proves the exact current-date top-2 package output generated for this scheduled run window.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the exact payload prepared for posting and that it matched the generated package.
  - Status: captured

- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the workflow gate results for API verification, content generation, payload validation, and the submit-step rate-limit blocker.
  - Status: captured

- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the exact request body attempted against `POST /api/social/x_api_post` and the HTTP 400 rate-limit response captured for this run.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `GET http://localhost:5000/api/social/status`
  - Objective-Proved: Proves the local publisher reported a same-trigger successful post at `2026-04-04T21:01:48.067734` and rejected the manual rerun because the rate-limit window was still active.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Objective-Proved: Proves the canonical workflow regression coverage still passes after this execution run.
  - Status: captured

- Evidence-Type: user_feedback
  - Artifact: `pending_user_verification`
  - Objective-Proved: Pending operator confirmation on whether the recorded scheduled post state plus the duplicate-run rate-limit blocker is acceptable for this slot.
  - Status: planned

## Implementation Log

- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-04 21:05:17 Europe/London: Ran `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-04` and regenerated the current-date top-2 artifacts.
- 2026-04-04 21:05:24 Europe/London: Ran `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`; result was `Ran 2 tests in 0.050s` and `OK`.
- 2026-04-04 21:05:29 Europe/London: Validated `temp_tweet_top2.txt` against `top2_cross_product_post.json`; the payload matched exactly, was 184 characters, and resolved to source date `2026-04-04` with source last update `2026-04-04T21:05:09.928669`.
- 2026-04-04 21:05:32 Europe/London: Verified local API health at `http://localhost:5000/api/health`; response was `{"status":"ok","ts":"2026-04-04T20:05:32.456431"}`.
- 2026-04-04 21:05:34 Europe/London: Executed `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-04`; verify/generate/validate steps passed and the submit step returned a concrete blocker: `Rate limit: wait 6 more minutes`.
- 2026-04-04 21:05:38 Europe/London: Read `twitter_workflow_status.json` and `twitter_x_api_post_response.json` to confirm the exact attempted payload and the HTTP 400 response body.
- 2026-04-04 21:05:42 Europe/London: Queried `GET http://localhost:5000/api/social/status`; the publisher reported `can_post=false`, `reason='Rate limit: wait 6 more minutes'`, and a same-trigger successful post already logged at `2026-04-04T21:01:48.067734`.

## Changes Made

- Refreshed `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json`.
- Refreshed `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.md`.
- Refreshed `TradeApps\breakout\fs\temp_tweet_top2.txt`.
- Updated `TradeApps\breakout\fs\twitter_workflow_status.json` with the 2026-04-04 21:05 gated run results.
- Updated `TradeApps\breakout\fs\twitter_x_api_post_response.json` with the exact HTTP 400 rate-limit response for the duplicate manual rerun.
- Updated this lifecycle file with executed commands, evidence, and validation results.
- No application code changes were required; the observed failure mode was a runtime rate-limit condition, not a workflow implementation defect.

## Validation

- Command: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-04`
  - Result: passed; wrote `top5_weekly_posting_package.json`, `top5_weekly_posting_package.md`, `top2_cross_product_post.json`, and `top2_cross_product_post.md` under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04`.
- Command: payload/package comparison script against `TradeApps\breakout\fs\temp_tweet_top2.txt` and `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json`
  - Result: passed; `payload_non_empty=true`, `matches_package=true`, `payload_length=184`, `today_source_date=2026-04-04`, `today_source_last_update=2026-04-04T21:05:09.928669`, `strategy_product_count=759`.
- Command: `python -c "from urllib.request import urlopen; print(urlopen('http://localhost:5000/api/health', timeout=30).read().decode('utf-8'))"`
  - Result: passed; returned `{"status":"ok","ts":"2026-04-04T20:05:32.456431"}`.
- Command: `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-04`
  - Result: blocker accepted per task definition; `twitter_workflow_status.json` recorded `final_status=failed` because submit step returned `HTTP 400 {'error': 'Rate limit: wait 6 more minutes', 'success': False}` after prior gates passed.
- Command: `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Result: passed; `Ran 2 tests in 0.050s` and `OK`.
- Command: `GET http://localhost:5000/api/social/status`
  - Result: passed; returned `can_post=false`, `reason='Rate limit: wait 6 more minutes'`, and a same-trigger successful post already present at `2026-04-04T21:01:48.067734`.
- User verification request: Please confirm pass/fail for:
  1. the 2026-04-04 21:00 slot is considered satisfied by the already-recorded same-trigger post at `2026-04-04T21:01:48.067734`,
  2. the regenerated payload in `temp_tweet_top2.txt` is acceptable for this run window,
  3. the duplicate manual rerun blocker `Rate limit: wait 6 more minutes` is acceptable as the recorded live response for this task execution.

## Risks/Notes

- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- If the generated package source date lags the actual run date, record the mismatch explicitly before posting.
- The local API was reachable, but the posting route rejected the manual rerun because the same trigger had already posted at `2026-04-04T21:01:48.067734`.
- Re-running again after the cooldown would create an extra X post for the same 4-hour slot, so no automatic retry was performed.
- After each successful scheduled execution, the scheduler should queue the next run 4 hours later.

## Completion Status

- State: Awaiting user verification
- Timestamp: 2026-04-04 21:05:42 Europe/London
