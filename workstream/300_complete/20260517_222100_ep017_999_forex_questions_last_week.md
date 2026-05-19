# EP017 Forex Questions Last Week Research

Source: Telegram request, 2026-05-17: "ok find top 5 questions being asked with regards to trading forex in the last week"

Task Type: standard
Destination Folder: workstream/300_complete
Dependency: Available recent X/Twitter API search data via configured bearer token.

## Plan
- Use authenticated X recent search for last-week forex/trading question posts.
- Cluster recurring question themes.
- Rank themes by frequency/engagement and provide examples.

## Evidence
- Objective: Identify top 5 recurring forex-trading questions from the last week.
- Delivery: Concise ranked list with practical implications.
- Coverage: X recent-search posts containing forex-related terms and question language.
- Auto-Acceptance: Each theme includes question wording and evidence basis.

## Implementation Log
- Created task file and moved to in-progress.
- Queried X recent-search API for forex-related English posts; gathered an initial sample of 248 candidate posts before account credits depleted on later queries.
- Queried Reddit public JSON for r/Forex, r/Daytrading, r/Forexstrategy, and r/algotrading `/new` posts from the last 7 days; filtered 314 question-style posts.
- Clustered questions by recurring theme: strategy/setup, beginner/education, risk/position/costs, bots/backtesting/automation, broker/prop firm trust, psychology/balance.

## Changes Made
- No product/code changes.

## Validation
- Current date basis confirmed: 2026-05-17 Sunday BST.
- Reddit source count: 314 recent question-style posts across relevant trading subreddits.
- X source count: 248 candidate posts before later queries returned X API `CreditsDepleted`.
- Ranked by theme frequency first, then comments/score/visible X engagement as supporting signal.

## Risks/Notes
- X API credits depleted mid-run, so X coverage is partial.
- Reddit/X data is directional market-research evidence, not a complete census of all forex questions.
- Spam/promotional posts were downweighted/ignored where obvious.

## Completion Status
- Complete.
