## Objective

Create a complete output package that generates a concise social-ready summary for the top 2 products across all product types using actual underlying data only.

## Context

- Target output example:
  - `SI leading +7,050`
  - `NQ +4,035 -> gap: 3,015`
  - `1,000+ strategies. Only the strongest traded.`
  - `Live -- updates on trade close.`
- Ranking scope: top 2 products across all product types combined
- Source policy: no fabricated timestamps, no fabricated returns, no inferred figures beyond arithmetic directly derived from source totals

## Task Attributes

- project: breakout
- task_type: implementation
- area: social_publisher
- priority: high
- status: complete
- workflow_ready: true

## Progress Log

- 2026-04-03 03:18 Europe/London: Traced canonical source inputs for top-2 cross-product ranking and count derivation.
- 2026-04-03 03:18 Europe/London: Confirmed current leader values from live `_top20.json`: `SI 7050`, `NQ 4035`, gap `3015`.
- 2026-04-03 03:18 Europe/London: Confirmed source-derived count from `_summary_net.json` across `forex`, `indices`, `metals`, `energy`: `2801` strategy-product combinations.
- 2026-04-03 03:24 Europe/London: Extended `generate_posting_package.py` to emit a dedicated top-2 cross-product package plus `temp_tweet_top2.txt`.
- 2026-04-03 03:31 Europe/London: Regenerated the package and verified source-derived values: leader `SI +7050`, runner-up `NQ +4035`, gap `3015`, strategy-product count `2713`.
- 2026-04-03 03:32 Europe/London: Refreshed `temp_tweet_top2.txt` from the generated package JSON and confirmed it matches the generated artifact content exactly.

## Changes Made

- Updated `TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py` to generate:
  - `top2_cross_product_post.json`
  - `top2_cross_product_post.md`
  - `temp_tweet_top2.txt`
- Added a dedicated top-2 cross-product short-form output using source-derived values only:
  - leader product and total net
  - runner-up product and total net
  - gap to leader
  - source-derived strategy-product count line
  - live-update closing line

## Validation

- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
  - Result: passed
- `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-02`
  - Result: generated `top2_cross_product_post.json`, `top2_cross_product_post.md`, and refreshed `temp_tweet_top2.txt`
- Direct source verification against live `_top20.json` and `_summary_net.json`
  - Result: `SI 7050`, `NQ 4035`, `gap 3015`, `strategy_product_count 2713`
- `temp_tweet_top2.txt` vs generated JSON payload
  - Result: exact content match after normalized line-ending comparison

## Deliverable

```text
2026-04-02 leaders

Update at 2026-04-03 00:00

SI leading +7,050
NQ +4,035 -> gap: 3,015

2,713 strategy-product combinations tracked. Only the strongest traded.
Live -- updates on trade close.
```

## Required Output

- A generated package that outputs the top 2 products across all product types combined
- The leading product line must show:
  - product name
  - total_net / cumulative pnl
- The second product line must show:
  - product name
  - total_net / cumulative pnl
  - the gap to the leader's total_net
- Supporting closing lines must also be included as part of the package output:
  - strategy-count line derived from actual source data
  - live-update line suitable for publishing

## Acceptance Criteria

1. The package ranks products across all product types, not within a single product type.
2. The leader line shows the top product and its actual source-derived total_net / cumulative pnl.
3. The runner-up line shows the second product, its actual source-derived total_net / cumulative pnl, and the arithmetic gap to the leader.
4. The strategy-count statement is generated from actual underlying source counts or clearly omitted if the count cannot be proven from source data.
5. The final output is publishable as a complete package, not just a partial calculation.
6. `workflow_ready: true` must be added only after the package is tested and confirmed working properly.

## Plan

1. Trace the canonical source files and logic for cross-product ranking across all product types.
2. Define the exact output schema and file/package location for the new top-2 cross-product social output.
3. Implement generation logic using actual source-derived totals and actual source-derived count/gap values.
4. Validate the generated output against underlying source files.
5. Mark the task `workflow_ready: true` only after successful end-to-end validation.

## Validation Expectations

- Verify the generated leader and runner-up values directly against the underlying source files used for ranking.
- Verify the gap calculation equals `leader_total_net - second_total_net`.
- Verify the strategy-count line is backed by actual source data.
- Verify the final output package is complete and ready for publishing.

## Notes

- Do not use relative labels like `Today` if the payload can be viewed historically; use explicit dates where applicable.
- Do not fabricate timestamps, counts, totals, freshness labels, or gap values.
- If the strategy-count phrase `1,000+ strategies` cannot be proven exactly from source data, replace it with a source-derived count or remove/reword it to remain accurate.
