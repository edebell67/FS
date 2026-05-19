## Objective

Remove fabricated timestamping from the social posting package and ensure the combined posting workflow always uses a freshly regenerated `temp_tweet.txt` derived from the current package output.

## Context

- Current bug: `generate_posting_package.py --date YYYY-MM-DD` stamps `generated_at` as `YYYY-MM-DDT23:59:59`, which produces a fake `Update at ... 23:59` label.
- Current workflow risk: the combined recurring path can read a stale `temp_tweet.txt` because the generator does not guarantee rewriting that file.
- Publishing target: X/Twitter posts must use only actual source-derived values and actual source timestamps.

## Task Attributes

- project: breakout
- task_type: bugfix
- area: social_publisher
- priority: high
- status: complete

## Plan

1. Patch the posting package generator to use actual source update timestamps in the consolidated post.
2. Make the generator rewrite `temp_tweet.txt` from the current consolidated post every run.
3. Update the combined recurring task definition so it explicitly verifies the refreshed payload came from the new package.
4. Validate by regenerating the package and comparing `temp_tweet.txt` to the current package JSON/Markdown.

## Progress Log

- 2026-04-03 00:16:05 Created lifecycle task.
- 2026-04-03 00:16:41 Updated `TradeApps/breakout/fs/tools/social_posting_package/generate_posting_package.py` so the consolidated post label uses actual source update timestamps instead of a synthetic `23:59:59` timestamp for `--date` runs.
- 2026-04-03 00:16:41 Updated the generator to rewrite `TradeApps/breakout/fs/temp_tweet.txt` from the current `consolidated_twitter_post` output on every run.
- 2026-04-03 00:16:41 Updated the live recurring backlog task so validation requires `temp_tweet.txt` to match the current generated package output.
- 2026-04-03 00:17:06 Validation: regenerated the `2026-04-02` posting package and confirmed the current package JSON now reports `today_source_last_update=04/03/2026 00:00:12`.
- 2026-04-03 00:17:18 Validation: verified `TradeApps/breakout/fs/temp_tweet.txt` now reflects the regenerated package output rather than the stale `(Ref: 18:31:22)` payload path.
- 2026-04-03 00:17:33 Validation: directly compared the package `today_product_leaders` against the underlying live `_top20.json` sources; the current top-5 list (`SI 7050`, `NQ 4035`, `CL 3635`, `ES 2675`, `HG 1780`) matched the source-derived best-per-product data.

## Outcome

Completed. The fabricated end-of-day timestamp path has been removed from the social posting package workflow, `temp_tweet.txt` is now regenerated from the current package output each run, and the current published returns were verified against the underlying live `_top20.json` source data.
