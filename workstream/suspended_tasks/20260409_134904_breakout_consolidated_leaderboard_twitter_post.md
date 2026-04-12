# SUSPENDED: 2026-04-09 13:35

This recurring task has been suspended by user request. 
Future runs of this chain are paused until further notice.

Source: User request on 2026-04-09 to "suspend both tasks".

---
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
Scheduled For: 2026-04-09 13:49:04+01:00
Spawned From: 20260409_094904_breakout_consolidated_leaderboard_twitter_post.md

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
- [ ] 1. Read weekly stats JSON for each product type for the current week.
  - [ ] Test: All four product type weekly stats files exist and contain `top_strategies` with `gen_strategy_name`.
  - Evidence:
- [ ] 2. Extract and aggregate strategies across all product types.
  - [ ] Test: Combined list contains strategies from all product types with gen_strategy_name, product, today_net, and weekly_net.
  - Evidence:
- [ ] 3. Generate Today top 5 (sorted by current date's net).
  - [ ] Test: Top 5 sorted correctly by today's net return.
  - Evidence:
- [ ] 4. Generate Weekly-so-far top 5 (sorted by total_net).
  - [ ] Test: Top 5 sorted correctly by weekly cumulative net.
  - Evidence:
- [ ] 5. Generate the posting package in both JSON and Markdown formats.
  - [ ] Test: `consolidated_leaderboard_posting_package.json` and `.md` exist in destination folder.
  - Evidence:
- [ ] 6. Validate Twitter post is within 280 character limit.
  - [ ] Test: Post text length <= 280 characters.
  - Evidence:
- [ ] 7. Post to Twitter/X.
  - [ ] Test: POST returns success with tweet ID or concrete blocker.
  - Evidence:
- [ ] 8. Record the live outcome with tweet ID or failure reason.
  - [ ] Test: Evidence section updated with captured tweet ID or exact error.
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `consolidated_leaderboard_posting_package.json`
  - Objective-Proved: Proves the consolidated leaderboard was generated with source-derived data including gen_strategy_name.
  - Status: planned
- Evidence-Type: file_output
  - Artifact: `consolidated_leaderboard_posting_package.md`
  - Objective-Proved: Proves the post draft was prepared in the validated format.
  - Status: planned
- Evidence-Type: live_post_result
  - Artifact: Tweet ID from POST response
  - Objective-Proved: Proves the consolidated leaderboard was successfully published to X.
  - Status: planned

## Implementation Log
- 2026-04-07 12:19:26 Europe/London: Task created to deliver consolidated leaderboard Twitter post with gen_strategy_name.

## Changes Made
- None yet.

## Validation Rules
- Do not fabricate gen_strategy_name, net returns, or tweet IDs.
- Use only source data from weekly stats JSON files.
- If source data is missing or stale, record the exact blocker.
- If X posting fails, record the exact error response.
- Post must fit within 280 character limit (may need to truncate gen_strategy_name if too long).

## Risks/Notes
- gen_strategy_name values like "cipher-lattice_2_z840_d22b" may be too long for Twitter character limits.
- May need to use abbreviated format if character limit exceeded.
- Cross-product aggregation requires reading all 4 product type weekly stats files.
- Today's net may be 0 for strategies that haven't traded yet today.

## Completion Status
- State: TODO
- Timestamp:
