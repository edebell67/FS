Source: User request on 2026-04-07 to create a task that posts the "Today + Weekly So Far" consolidated leaderboard to Twitter, including gen_strategy_name.
Task Type: standard
Task Attributes:
- recurring_task: true
- recurrence_type: scheduled
- recurrence_rule: interval
- recurrence_interval_hours: 4
- priority: high
- execution_owner: codex
- workflow_ready: false
**Suggested Agent:** codex
Task Summary: Generate and post a consolidated cross-product leaderboard showing Today top 5 and Weekly-so-far top 5 with gen_strategy_name, product, and net return.
Context:
- Workspace: `C:\Users\edebe\eds`
- Source data (weekly stats with gen_strategy_name):
  - Forex: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\YYYY-MM-DD.json`
  - Indices: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\indices\stats\weekly\YYYY-MM-DD.json`
  - Metals: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\stats\weekly\YYYY-MM-DD.json`
  - Energy: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\energy\stats\weekly\YYYY-MM-DD.json`
- Posting path: `Twitter/X`
Destination Folder: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\YYYY-MM-DD\`
Dependency: None

## Objective

Produce and publish a single consolidated cross-product leaderboard Twitter post showing:
1. Today's top 5 performers (across all product types) with gen_strategy_name
2. Weekly-so-far top 5 performers (across all product types) with gen_strategy_name

## Output Format

### Twitter Post (Single Post)

```text
Update at YYYY-MM-DD HH:MM

Today
1. {gen_strategy_name} ({product}) {today_net}
2. {gen_strategy_name} ({product}) {today_net}
3. {gen_strategy_name} ({product}) {today_net}
4. {gen_strategy_name} ({product}) {today_net}
5. {gen_strategy_name} ({product}) {today_net}

Weekly so far
1. {gen_strategy_name} ({product}) {weekly_net}
2. {gen_strategy_name} ({product}) {weekly_net}
3. {gen_strategy_name} ({product}) {weekly_net}
4. {gen_strategy_name} ({product}) {weekly_net}
5. {gen_strategy_name} ({product}) {weekly_net}

Full details to follow.
#StrategyWarehouse #FuturesTrading #AlgoTrading
```

### Example Output

```text
Update at 2026-04-07 12:00

Today
1. cipher-lattice_2_z840_d22b (NQ) 3085
2. cipher-lattice_2_z840_d4bc (NQ) 2885
3. prism-vertex_2_z838_d4a1 (SI) 2650
4. cipher-lattice_2_z840_d94c (NQ) 2485
5. meridian-sigma_2_z317_d1a8 (CL) 1600

Weekly so far
1. cipher-lattice_2_z840_d22b (NQ) 6900
2. prism-vertex_2_z838_d4a1 (SI) 5800
3. cipher-lattice_2_z840_d4bc (NQ) 5205
4. cipher-lattice_2_z840_d94c (NQ) 4805
5. meridian-sigma_2_z317_d1a8 (CL) 4200

Full details to follow.
#StrategyWarehouse #FuturesTrading #AlgoTrading
```

### Output Artifacts
- `consolidated_leaderboard_posting_package.json` - structured data for automation
- `consolidated_leaderboard_posting_package.md` - human-readable package with post draft

## Data Extraction Logic

1. Read weekly stats JSON from each product type (forex, indices, metals, energy)
2. Extract `gen_strategy_name`, `product`, `total_net`, and `daily[current_date]` from top_strategies
3. Aggregate all strategies across product types
4. Sort by today's net for "Today" leaderboard (top 5)
5. Sort by total_net for "Weekly so far" leaderboard (top 5)
6. Format into single Twitter post

## Plan
- [x] 1. Read weekly stats JSON for each product type for the current week.
  - [x] Test: `python - <<verification script>>` confirms `2026-04-06.json` exists for forex, indices, metals, and energy, and each file contains `top_strategies[0].gen_strategy_name`.
  - Evidence: Verification output showed source files present with counts `forex=1000`, `indices=559`, `metals=436`, `energy=431`, all with `has_gen_strategy_name=true`.
- [x] 2. Extract and aggregate strategies across all product types.
  - [x] Test: `python - <<verification script>>` reports the combined list contains cross-product rows with `gen_strategy_name`, `product`, `today_net`, and `weekly_net`.
  - Evidence: Verification output reported `combined_strategy_count=2426` from the four weekly stats files.
- [x] 3. Generate Today top 5 (sorted by current date's net).
  - [x] Test: `python - <<verification script>>` checks `today_sorted_desc == true` in `consolidated_leaderboard_posting_package.json`.
  - Evidence: Generated Today top 5 ranks were `helix-lotus_2_zbc1_dc81`, `lumen-vertex_2_zbc1_d2aa`, `helix-lotus_2_zbc1_d2aa`, `helix-lotus_2_zbc1_d713`, `helix-lotus_3_zbc1_d2aa`.
- [x] 4. Generate Weekly-so-far top 5 (sorted by total_net).
  - [x] Test: `python - <<verification script>>` checks `weekly_sorted_desc == true` in `consolidated_leaderboard_posting_package.json`.
  - Evidence: Generated Weekly top 5 ranks were `lumen-vertex_2_zbc1_d2aa`, `helix-lotus_2_zbc1_d2aa`, `cipher-lattice_2_z840_d22b`, `helix-lotus_3_zbc1_d2aa`, `cipher-lattice_2_z840_d4bc`.
- [x] 5. Generate the posting package in both JSON and Markdown formats.
  - [x] Test: `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08` writes `consolidated_leaderboard_posting_package.json` and `.md` to the destination folder.
  - Evidence: Generator wrote `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\consolidated_leaderboard_posting_package.json` and `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\consolidated_leaderboard_posting_package.md`.
- [x] 6. Validate Twitter post is within 280 character limit.
  - [x] Test: `python - <<verification script>>` confirms `twitter_post.char_count <= 280` and workflow validation accepts the payload.
  - Evidence: `char_count=274`; workflow status recorded `Validated payload (274 chars)`.
- [x] 7. Post to Twitter/X.
  - [x] Test: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_consolidated_leaderboard_workflow.py 2026-04-08` returns success from `POST http://localhost:5000/api/social/x_api_post`.
  - Evidence: Workflow status recorded HTTP 200 with `tweet_id=2041863085883851251`.
- [x] 8. Record the live outcome with tweet ID or failure reason.
  - [x] Test: Evidence section updated with captured tweet ID and response artifact path.
  - Evidence: Response artifact `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_consolidated_leaderboard_post_response.json` captured tweet ID `2041863085883851251`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\consolidated_leaderboard_posting_package.json`
  - Objective-Proved: Proves the consolidated leaderboard was generated with source-derived data including gen_strategy_name.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\consolidated_leaderboard_posting_package.md`
  - Objective-Proved: Proves the post draft was prepared in the validated format.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m unittest TradeApps.breakout.fs.tests.test_run_twitter_consolidated_leaderboard_workflow`
  - Objective-Proved: Proves the dedicated workflow validates nested payload shape, temp tweet parity, and successful post recording behavior.
  - Status: captured
- Evidence-Type: url
  - Artifact: `https://x.com/i/web/status/2041863085883851251`
  - Objective-Proved: Proves the consolidated leaderboard was successfully published to X.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_consolidated_leaderboard_post_response.json`
  - Objective-Proved: Proves the exact request payload and the returned tweet ID from the local X API workflow.
  - Status: captured

## Implementation Log
- 2026-04-07 12:19:26 Europe/London: Task created to deliver consolidated leaderboard Twitter post with gen_strategy_name.
- 2026-04-08 13:56 Europe/London: Updated `generate_posting_package.py` to read weekly stats JSON directly, build `consolidated_leaderboard_posting_package.{json,md}`, preserve full `gen_strategy_name` in artifacts, and emit a compact single-post tweet draft.
- 2026-04-08 13:57 Europe/London: Added `run_twitter_consolidated_leaderboard_workflow.py` and unit coverage for payload validation and X post recording.
- 2026-04-08 13:57 Europe/London: Generated the live `2026-04-08` consolidated package, validated the 274-character tweet, and posted it successfully to X as tweet `2041863085883851251`.

## Changes Made
- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py` to:
  - read weekly stats files from `fs\json\live\<product_type>\stats\weekly\<week_start>.json`
  - aggregate cross-product strategy rows using `gen_strategy_name`, `product`, `daily[current_date]`, and `total_net`
  - create `consolidated_leaderboard_posting_package.json` and `.md`
  - write `temp_tweet_consolidated_leaderboard.txt`
  - retain legacy package outputs for existing workflows
- Added `C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_consolidated_leaderboard_workflow.py` for single-post local API execution against `x_api_post`
- Added `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_consolidated_leaderboard_workflow.py` for workflow validation coverage

## Validation
- `python -m unittest TradeApps.breakout.fs.tests.test_run_twitter_consolidated_leaderboard_workflow`
  - Result: `Ran 3 tests in 0.286s` / `OK`
- `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08`
  - Result: wrote legacy outputs plus `consolidated_leaderboard_posting_package.json` and `.md` under `...\social_posting_package\2026-04-08\`
- `python - <<verification script>>`
  - Result: source files existed, `combined_strategy_count=2426`, `today_sorted_desc=true`, `weekly_sorted_desc=true`, `tweet_char_count=274`
- `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_consolidated_leaderboard_workflow.py 2026-04-08`
  - Result: health check OK, payload validation OK, `POST http://localhost:5000/api/social/x_api_post` returned HTTP 200 with tweet ID `2041863085883851251`

## Validation Rules
- Do not fabricate gen_strategy_name, net returns, or tweet IDs.
- Use only source data from weekly stats JSON files.
- If source data is missing or stale, record the exact blocker.
- If X posting fails, record the exact error response.
- Post must fit within 280 character limit (may need to truncate gen_strategy_name if too long).

## Risks/Notes
- gen_strategy_name values like "cipher-lattice_2_z840_d22b" may be too long for Twitter character limits.
- Implemented deterministic truncation in the live tweet body only; full `gen_strategy_name` values remain intact in the JSON and Markdown artifacts.
- Cross-product aggregation requires reading all 4 product type weekly stats files.
- Today's net may be 0 for strategies that haven't traded yet today.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-08 13:57:36 Europe/London
Next Scheduled For: 2026-04-08 18:00:36+01:00
