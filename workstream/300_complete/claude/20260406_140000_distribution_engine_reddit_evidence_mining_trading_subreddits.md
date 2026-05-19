Source: User request on 2026-04-06 to create Reddit connection via Google OAuth and use distribution engine to extract high-engagement titles from trading subreddits.

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

Task Summary: Establish Reddit API connection using Google OAuth, then execute the distribution engine evidence mining skill to extract top-engagement titles (ranked by comments, not upvotes) from trading-related subreddits: r/trading, r/daytrading, r/forex, r/algotrading.

Context:
- Workspace: `C:\Users\edebe\eds`
- Distribution Engine: `C:\Users\edebe\eds\skills\distribution_engine`
- Evidence Mining Skill: `C:\Users\edebe\eds\skills\distribution_engine\core\evidence_mining.md`
- Pattern Extraction Skill: `C:\Users\edebe\eds\skills\distribution_engine\core\pattern_extraction.md`
- Target Subreddits:
  - r/trading
  - r/daytrading
  - r/forex
  - r/algotrading
- Output Path: `C:\Users\edebe\eds\skills\distribution_engine\domains\trading\evidence\`
- Engagement Metric: comments (NOT upvotes/likes)
- Min Comments Threshold: 20 (per config/thresholds.json)

Dependency: None

Execution Workflow:
1. Authenticate with Reddit API via Google OAuth
2. For each subreddit, fetch top posts sorted by comment count
3. Filter posts meeting engagement threshold
4. Extract and store evidence
5. Feed into pattern extraction

Scheduled For: 2026-04-06 14:00:00+01:00
Next Scheduled For: 2026-04-13 14:00:00+01:00

## Objective
Connect to Reddit API using Google OAuth and extract high-engagement titles from trading subreddits for the distribution engine evidence mining workflow.

## Plan
- [ ] 1. Set up Reddit API application credentials
  - [ ] Test: Reddit app created at reddit.com/prefs/apps with valid client_id and client_secret
  - Evidence:

- [ ] 2. Configure Google OAuth for Reddit authentication
  - [ ] Test: OAuth flow completes and returns valid access_token
  - Evidence:

- [ ] 3. Create Reddit API client script
  - [ ] Test: Script can authenticate and fetch posts from r/trading
  - Evidence:

- [ ] 4. Implement evidence mining for r/trading
  - [ ] Test: Returns top 10 posts sorted by comment count (min 20 comments)
  - Evidence:

- [ ] 5. Implement evidence mining for r/daytrading
  - [ ] Test: Returns top 10 posts sorted by comment count (min 20 comments)
  - Evidence:

- [ ] 6. Implement evidence mining for r/forex
  - [ ] Test: Returns top 10 posts sorted by comment count (min 20 comments)
  - Evidence:

- [ ] 7. Implement evidence mining for r/algotrading
  - [ ] Test: Returns top 10 posts sorted by comment count (min 20 comments)
  - Evidence:

- [ ] 8. Store evidence in distribution engine format
  - [ ] Test: Evidence JSON file created at domains/trading/evidence/YYYY-MM-DD_reddit_evidence.json
  - Evidence:

- [ ] 9. Validate evidence output matches distribution engine schema
  - [ ] Test: JSON validates against runs/_template_run/evidence.json schema
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: Reddit API client script
  - Objective-Proved: Proves Reddit connection is established
  - Status: planned

- Evidence-Type: file_output
  - Artifact: domains/trading/evidence/YYYY-MM-DD_reddit_evidence.json
  - Objective-Proved: Proves evidence mining executed successfully
  - Status: planned

- Evidence-Type: log_output
  - Artifact: API response showing posts retrieved with comment counts
  - Objective-Proved: Proves engagement-based sorting (comments not upvotes)
  - Status: planned

## Validation Rules
- Do not count upvotes/likes as engagement metric
- Only count comments and unique commenters
- Minimum 20 comments per post to qualify
- Maximum 30 days age for posts
- Store all evidence in distribution engine format
- Do not fabricate engagement numbers

## Risks/Notes
- Reddit API rate limits: 60 requests/minute for OAuth apps
- Google OAuth may require additional setup if not already configured
- Some subreddits may have posting restrictions that affect comment counts
- Evidence mining should capture post URL, title, comment count, age, and subreddit

## Output Schema
```json
{
  "run_id": "YYYY-MM-DD_reddit_trading",
  "domain": "trading",
  "source": {
    "platform": "reddit",
    "subreddits": ["trading", "daytrading", "forex", "algotrading"],
    "scan_date": "YYYY-MM-DD",
    "criteria": {
      "min_comments": 20,
      "max_age_days": 30,
      "sort_by": "comments"
    }
  },
  "titles": [
    {
      "subreddit": "r/trading",
      "title": "...",
      "url": "https://reddit.com/r/...",
      "comments": 0,
      "upvotes": 0,
      "age_days": 0
    }
  ]
}
```

## Completion Status
- State: TODO
- Timestamp:
