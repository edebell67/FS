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

Scheduled For: 2026-04-08 21:49:04+01:00
Next Scheduled For: 2026-04-09 01:49:04+01:00
Spawned From: 20260408_174904_breakout_consolidated_leaderboard_twitter_post.md

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
  - [x] Test: All four product type weekly stats files exist and contain `top_strategies` with `gen_strategy_name`.
  - Evidence: `forex`, `indices`, `metals`, and `energy` weekly files for `2026-04-06` were read successfully; each sampled `top_strategies[0]` record included `gen_strategy_name` and `daily["2026-04-08"]`.
- [x] 2. Extract and aggregate strategies across all product types.
  - [x] Test: Combined list contains strategies from all product types with gen_strategy_name, product, today_net, and weekly_net.
  - Evidence: `consolidated_leaderboard_posting_package.json` contains merged rows with `product_type`, `product`, `gen_strategy_name`, `today_net`, and `weekly_net` sourced from all four weekly stats files.
- [x] 3. Generate Today top 5 (sorted by current date's net).
  - [x] Test: Top 5 sorted correctly by today's net return.
  - Evidence: `today_top_5` values were `3760, 3690, 3475, 2705, 2615`, which confirms descending sort by `today_net`.
- [x] 4. Generate Weekly-so-far top 5 (sorted by total_net).
  - [x] Test: Top 5 sorted correctly by weekly cumulative net.
  - Evidence: `weekly_top_5` values were `15450, 8700, 7265, 7000, 6050`, which confirms descending sort by `weekly_net`.
- [x] 5. Generate the posting package in both JSON and Markdown formats.
  - [x] Test: `consolidated_leaderboard_posting_package.json` and `.md` exist in destination folder.
  - Evidence: Both files were regenerated under `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\`.
- [x] 6. Validate Twitter post is within 280 character limit.
  - [x] Test: Post text length <= 280 characters.
  - Evidence: The generated single-post draft measured `274` characters in both the package JSON and workflow status artifact.
- [x] 7. Post to Twitter/X.
  - [x] Test: POST returns success with tweet ID or concrete blocker.
  - Evidence: `POST http://localhost:5000/api/social/x_api_post` returned HTTP `200` with `tweet_id` `2041982221611917502`.
- [x] 8. Record the live outcome with tweet ID or failure reason.
  - [x] Test: Evidence section updated with captured tweet ID or exact error.
  - Evidence: `twitter_consolidated_leaderboard_post_response.json` captured the exact request text, HTTP response, and tweet ID; this lifecycle file now records the final tweet URL.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\consolidated_leaderboard_posting_package.json`
  - Objective-Proved: Proves the consolidated leaderboard was generated from the weekly stats source files with full `gen_strategy_name`, `today_net`, and `weekly_net` data.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\consolidated_leaderboard_posting_package.md`
  - Objective-Proved: Proves the human-review posting package and draft were rendered for the same generated leaderboard.
  - Status: captured
- Evidence-Type: url
  - Artifact: `https://x.com/i/web/status/2041982221611917502`
  - Objective-Proved: Proves the consolidated leaderboard update was published to X.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_consolidated_leaderboard_workflow_status.json`
  - Objective-Proved: Proves the ordered workflow steps passed: API health, content generation, payload validation, X POST, and outcome recording.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_consolidated_leaderboard_post_response.json`
  - Objective-Proved: Proves the exact 274-character submitted tweet text, HTTP 200 response, and returned tweet ID `2041982221611917502`.
  - Status: captured

## Implementation Log

- 2026-04-07 12:19:26 Europe/London: Task created to deliver consolidated leaderboard Twitter post with gen_strategy_name.
- 2026-04-08 21:50:54 Europe/London: Reviewed the lifecycle skill and task file, confirmed the repo already contained `generate_posting_package.py` and `run_twitter_consolidated_leaderboard_workflow.py`, and verified the live weekly stats inputs for `forex`, `indices`, `metals`, and `energy`.
- 2026-04-08 21:50:56 Europe/London: Executed `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_consolidated_leaderboard_workflow.py 2026-04-08`.
- 2026-04-08 21:51:00 Europe/London: Workflow completed successfully, regenerated the consolidated posting package, validated the tweet at 274 characters, and posted successfully to X with tweet ID `2041982221611917502`.

## Changes Made

- Updated this lifecycle file with completed checklist items, normalized evidence entries, validation outputs, and final completion state.
- Regenerated `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\consolidated_leaderboard_posting_package.json`.
- Regenerated `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\consolidated_leaderboard_posting_package.md`.
- Refreshed `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_consolidated_leaderboard.txt`, `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_consolidated_leaderboard_workflow_status.json`, and `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_consolidated_leaderboard_post_response.json`.

## Validation

- `python -` inspection of the four weekly stats files for `2026-04-06`: passed. Confirmed each file exists and that sampled `top_strategies[0]` records contain `product`, `gen_strategy_name`, `total_net`, and `daily["2026-04-08"]`.
- `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_consolidated_leaderboard_workflow.py 2026-04-08`: passed. Recorded API health OK, package generation OK, payload validation OK, POST OK, and tweet ID `2041982221611917502`.
- `Get-Content -Raw C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\consolidated_leaderboard_posting_package.json`: passed. Verified `today_top_5`, `weekly_top_5`, source weekly file paths, and `twitter_post.char_count = 274`.

## Risks/Notes

- gen_strategy_name values like `cipher-lattice_2_z840_d22b` are too long for a full 10-entry single tweet, so the published post uses the existing compact single-post formatter while preserving full names in the JSON and Markdown artifacts.
- Cross-product aggregation depends on all four weekly stats files being present for the current week start.
- Today's net may be `0` for strategies that have not traded yet on the live date.

## Completion Status

- State: COMPLETE
- Timestamp: 2026-04-08 21:51:00 Europe/London
