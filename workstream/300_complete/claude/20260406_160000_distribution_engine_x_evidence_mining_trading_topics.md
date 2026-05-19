Source: User request on 2026-04-06 to create X/Twitter evidence mining task, mirroring the Reddit evidence mining workflow.

Task Type: standard

Task Attributes:
- looping_task: true
- loop_until: manual_stop
- loop_interval: weekly
- recurring_task: true
- recurrence_type: scheduled
- recurrence_rule: interval
- recurrence_interval_days: 7
- priority: high
- execution_owner: claude
- workflow_ready: false

**Suggested Agent:** claude

Task Summary: Extract high-engagement posts (ranked by replies/comments, not likes) from X/Twitter trading-related topics and accounts, storing results in distribution engine evidence format.

Context:
- Workspace: `C:\Users\edebe\eds`
- Distribution Engine: `C:\Users\edebe\eds\skills\distribution_engine`
- Evidence Mining Skill: `C:\Users\edebe\eds\skills\distribution_engine\core\evidence_mining.md`
- Target Topics/Hashtags:
  - #trading
  - #daytrading
  - #forex
  - #algotrading
  - #stockmarket
  - #futures
- Target Accounts (high-engagement trading accounts):
  - Search for accounts with high reply rates
- Output Path: `C:\Users\edebe\eds\epics\ep_011_distribution_engine\evidence\x\`
- Engagement Metric: replies/comments (NOT likes/retweets)
- Reference: Reddit evidence mining at `platforms/reddit/skills/reddit_evidence_mining_public.py`

Dependency: None

Execution Workflow:
1. Connect to X API (or use public scraping method)
2. For each topic/hashtag, fetch top posts sorted by reply count
3. Filter posts meeting engagement threshold
4. Extract and store evidence
5. Feed into pattern extraction

Scheduled For: 2026-04-06 16:00:00+01:00
Next Scheduled For: 2026-04-13 16:00:00+01:00

## Objective
Extract high-engagement posts from X/Twitter trading topics for the distribution engine evidence mining workflow, prioritizing reply count over likes.

## Plan
- [ ] 1. Determine X API access method
  - [ ] Test: Identify if X API credentials exist or if public scraping is needed
  - Evidence:

- [ ] 2. Create X evidence mining script
  - [ ] Test: Script can fetch posts from trading hashtags
  - Evidence:

- [ ] 3. Implement engagement sorting (replies, not likes)
  - [ ] Test: Results sorted by reply_count DESC
  - Evidence:

- [ ] 4. Mine evidence from #trading
  - [ ] Test: Returns top 10 posts sorted by reply count
  - Evidence:

- [ ] 5. Mine evidence from #daytrading
  - [ ] Test: Returns top 10 posts sorted by reply count
  - Evidence:

- [ ] 6. Mine evidence from #forex
  - [ ] Test: Returns top 10 posts sorted by reply count
  - Evidence:

- [ ] 7. Mine evidence from #algotrading
  - [ ] Test: Returns top 10 posts sorted by reply count
  - Evidence:

- [ ] 8. Store evidence in distribution engine format
  - [ ] Test: Evidence JSON file created at ep_011_distribution_engine/evidence/x/YYYY-MM-DD_x_evidence.json
  - Evidence:

- [ ] 9. Validate evidence output matches distribution engine schema
  - [ ] Test: JSON structure matches Reddit evidence format
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: X evidence mining script
  - Objective-Proved: Proves X connection is established
  - Status: planned

- Evidence-Type: file_output
  - Artifact: ep_011_distribution_engine/evidence/x/YYYY-MM-DD_x_evidence.json
  - Objective-Proved: Proves evidence mining executed successfully
  - Status: planned

- Evidence-Type: log_output
  - Artifact: API response showing posts retrieved with reply counts
  - Objective-Proved: Proves engagement-based sorting (replies not likes)
  - Status: planned

## Validation Rules
- Do not count likes/retweets as primary engagement metric
- Prioritize replies/comments as engagement signal
- Minimum 10 replies per post to qualify
- Maximum 30 days age for posts
- Store all evidence in distribution engine format
- Do not fabricate engagement numbers

## Risks/Notes
- X API access may require paid tier for search functionality
- Rate limits are stricter than Reddit
- May need to use existing twitter-automation skills from workspace
- Consider using firecrawl or similar for public data if API unavailable
- Existing X posting workflow at `C:\Users\edebe\eds\skills\twitter-automation\`

## Output Schema
```json
{
  "run_id": "YYYY-MM-DD_x_trading",
  "domain": "trading",
  "source": {
    "platform": "x",
    "topics": ["trading", "daytrading", "forex", "algotrading"],
    "scan_date": "YYYY-MM-DD",
    "criteria": {
      "min_replies": 10,
      "max_age_days": 30,
      "sort_by": "replies"
    }
  },
  "titles": [
    {
      "topic": "#trading",
      "text": "...",
      "url": "https://x.com/...",
      "replies": 0,
      "retweets": 0,
      "likes": 0,
      "age_days": 0,
      "author": "..."
    }
  ]
}
```

## Completion Status
- State: TODO
- Timestamp:
