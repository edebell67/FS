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
Scheduled For: 2026-04-04 01:00:00+01:00
Next Scheduled For: 2026-04-04 05:00:00+01:00
Spawned From: 20260403_210000_breakout_twitter_summary_returns_every_4_hours.md

## Plan

- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-04` completes successfully.
  - Evidence: 2026-04-04 01:12 Europe/London run wrote `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json` and `.md` with `generated_date=2026-04-04` and source last update `2026-04-04T01:12:25.057008`.

- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: `TradeApps\breakout\fs\temp_tweet_top2.txt` matched `top2_cross_product_post.json[top2_cross_product_post]` exactly; payload length `184`; text resolved to `2026-04-04 leaders`, update stamp `2026-04-04 01:12`, leaders `SI +235` and `HG +235`, gap `0`, strategy-product count `759`.

- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: Direct health check returned HTTP `200` with `{"status":"ok","ts":"2026-04-04T00:12:44.672548"}`; the canonical workflow also recorded `verify_api.ok=true` with API timestamp `2026-04-04T00:13:00.263083`.

- [x] 4. Post the refreshed payload to X.
  - [x] Test: `POST /api/social/x_api_post` returns a success response with a tweet ID or a concrete blocker such as a rate limit or credential error.
  - Evidence: `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-04` completed with `final_status=success`; `twitter_x_api_post_response.json` recorded HTTP `200`, trigger `breakout_top2_cross_product_every_4_hours`, and `tweet_id=2040221111992922151`.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json`
  - Objective-Proved: Proves which current-date package output was generated for the recurring run.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the exact body posted to X and confirms it matches the current generated package.
  - Status: captured

- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the posting attempt outcome for the current recurring run.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Objective-Proved: Proves the canonical workflow payload validation contract still passes after the scheduled run.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: User verification requested for the 2026-04-04 01:00 Europe/London recurring run outcome and posted payload.
  - Objective-Proved: Proves the user has been asked to confirm the delivered behavior and live X post are acceptable.
  - Status: captured

## Implementation Log

- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-04 01:12 Europe/London: Ran `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-04` and refreshed the current-date top-2 package artifacts.
- 2026-04-04 01:12 Europe/London: Verified `temp_tweet_top2.txt` matched `top2_cross_product_post.json[top2_cross_product_post]` exactly and confirmed the payload remained source-derived and within X length limits.
- 2026-04-04 01:12 Europe/London: Verified `GET http://localhost:5000/api/health` returned HTTP `200` and `{"status":"ok"}` before posting.
- 2026-04-04 01:13 Europe/London: Executed `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-04`; the workflow regenerated the payload, revalidated it, posted successfully through `/api/social/x_api_post`, and captured `tweet_id=2040221111992922151`.
- 2026-04-04 01:13 Europe/London: Ran `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` and confirmed `Ran 2 tests ... OK`.

## Changes Made

- No source-code changes were required for this run; the existing recurring workflow, generator, and scheduler references were already aligned to the top-2 canonical posting flow.
- Refreshed the runtime artifacts for the 2026-04-04 01:00 recurring run in `TradeApps\breakout\fs`, including the generated package JSON/Markdown, `temp_tweet_top2.txt`, `twitter_workflow_status.json`, and `twitter_x_api_post_response.json`.
- Updated this lifecycle record with the captured validation and evidence for the 2026-04-04 execution.

## Validation

- `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-04`
  - Result: passed; generated `top2_cross_product_post.json` and `.md` for `2026-04-04`.
- Manual payload comparison of `TradeApps\breakout\fs\temp_tweet_top2.txt` vs `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json`
  - Result: passed; exact string match, `184` chars, source date `2026-04-04`, source last update `2026-04-04T01:12:25.057008`.
- Direct `GET http://localhost:5000/api/health`
  - Result: passed; HTTP `200` with `{"status":"ok","ts":"2026-04-04T00:12:44.672548"}`.
- `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-04`
  - Result: passed; `twitter_workflow_status.json` recorded `final_status=success` and `twitter_x_api_post_response.json` captured HTTP `200` with `tweet_id=2040221111992922151`.
- `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Result: passed; `Ran 2 tests in 0.059s` and `OK`.
- User verification request
  - Result: pending; requested pass/fail confirmation for: 1. the recurring run regenerated the current-date top-2 package, 2. the payload posted to X matches `temp_tweet_top2.txt`, 3. the live post outcome `tweet_id=2040221111992922151` is acceptable.

## Risks/Notes

- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- If the generated package source date lags the actual run date, record the mismatch explicitly before posting.
- If the local API server is unreachable on `localhost:5000`, stop and record the concrete blocker.
- After each successful execution, the scheduler should queue the next run 4 hours later.

## Completion Status

- State: Awaiting user verification
- Timestamp: 2026-04-04 01:13:30 Europe/London
