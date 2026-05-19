Source: User request on 2026-04-08 to run a Reddit engagement campaign using distribution_engine skills with trading strategy data.
Task Type: standard
Task Attributes:
- workflow_task: true
- workflow_name: distribution_engine
- workflow_stage: backlog
- splittable_task: true
- split_output_type: files
- priority: high
- execution_owner: claude
**Suggested Agent:** claude
Task Summary: Execute a Reddit engagement campaign using the distribution_engine skill framework, mining evidence from trading subreddits, generating variants from strategy performance data, and deploying test posts.
Context:
- Workspace: `C:\Users\edebe\eds`
- Distribution Engine: `C:\Users\edebe\eds\skills\distribution_engine`
- Growth Engine: `C:\Users\edebe\eds\skills\growth_engine_integrated`
- Source data: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-07\`
- Available source packages:
  - `top5_weekly_posting_package.json` - Weekly top 5 per product type
  - `top3_daily_posting_package.json` - Daily top 3 per product type
  - `top2_cross_product_post.json` - Cross-product leaders
- Reddit skills: `C:\Users\edebe\eds\skills\distribution_engine\platforms\reddit\skills\`
- Core skills: `C:\Users\edebe\eds\skills\distribution_engine\core\`
Destination Folder: `C:\Users\edebe\eds\epics\ep_011_distribution_engine\reddit`
Dependency: None

## Objective

Execute the distribution_engine loop for Reddit:
```
Mine → Extract → Map → Generate → Adapt → Deploy → Measure → Score → Create/Mutate/Prune
```

Target subreddits: r/algotrading, r/Daytrading, r/Forex, r/futurestrading, r/options

## Distribution Engine Loop Steps

### Phase 1: Evidence Mining
- Scan target subreddits for high-comment posts about trading strategies/performance
- Extract top 10 title patterns with high engagement
- Record source metadata (subreddit, upvotes, comments, age)

### Phase 2: Pattern Extraction
- Identify common hooks from successful posts
- Extract title mechanics (questions, numbers, outcomes, timeframes)
- Document patterns for variant generation

### Phase 3: Data Mapping
- Map strategy performance data to extracted patterns
- Bind: gen_strategy_name, product, net returns, weekly/daily metrics
- Create content hooks from real performance data

### Phase 4: Variant Generation
- Generate 3-5 title/post variants per pattern
- Use different hooks: question, outcome, comparison, insight
- Ensure authenticity (real data, not hype)

### Phase 5: Platform Adaptation
- Format for Reddit (title length, flair requirements)
- Add appropriate subreddit context
- Include required disclosures (algo trading, simulated/paper)

### Phase 6: Deployment
- Stage posts for controlled test deployment
- Track: subreddit, post time, title variant
- Capture post URLs/IDs

### Phase 7: Measurement & Scoring
- Track: comments, unique commenters, upvote ratio
- Apply scoring formula: `(Comments × 3) + (Unique Commenters × 5) + (Repeat Commenters × 10)`
- Rank variant effectiveness

## Output Structure

```
epics/ep_011_distribution_engine/reddit/
├── evidence/
│   └── 2026-04-08_evidence.json          # Mined patterns from subreddits
├── patterns/
│   └── 2026-04-08_patterns.json          # Extracted title mechanics
├── mapped_data/
│   └── 2026-04-08_mapped.json            # Strategy data bound to patterns
├── variants/
│   └── 2026-04-08_variants.json          # Generated post variants
├── adapted/
│   └── 2026-04-08_reddit_posts.json      # Reddit-formatted posts
├── deployed/
│   └── 2026-04-08_deployment_log.json    # Post URLs, timestamps
├── measurements/
│   └── 2026-04-08_metrics.json           # Engagement tracking
└── scores/
    └── 2026-04-08_scores.json            # Ranked variants
```

## Plan
- [ ] 1. Mine evidence from target subreddits (r/algotrading, r/Daytrading, r/Forex).
  - [ ] Test: `evidence/2026-04-08_evidence.json` contains 10+ high-engagement posts with comment counts.
  - Evidence:
- [ ] 2. Extract patterns from mined evidence.
  - [ ] Test: `patterns/2026-04-08_patterns.json` contains identified hooks and title mechanics.
  - Evidence:
- [ ] 3. Map strategy performance data to patterns.
  - [ ] Test: `mapped_data/2026-04-08_mapped.json` binds real gen_strategy_name and net values to hooks.
  - Evidence:
- [ ] 4. Generate 3-5 post variants per pattern.
  - [ ] Test: `variants/2026-04-08_variants.json` contains multiple variant posts.
  - Evidence:
- [ ] 5. Adapt variants for Reddit format and rules.
  - [ ] Test: `adapted/2026-04-08_reddit_posts.json` contains Reddit-ready posts with appropriate titles.
  - Evidence:
- [ ] 6. Stage deployment plan (do not post without approval).
  - [ ] Test: `deployed/2026-04-08_deployment_log.json` contains staged posts with target subreddits.
  - Evidence:
- [ ] 7. Document measurement criteria and scoring formula.
  - [ ] Test: Scoring formula documented in output folder.
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: `evidence/2026-04-08_evidence.json`
  - Objective-Proved: Proves evidence mining executed on target subreddits.
  - Status: planned
- Evidence-Type: file_output
  - Artifact: `variants/2026-04-08_variants.json`
  - Objective-Proved: Proves variants generated from real strategy data.
  - Status: planned
- Evidence-Type: file_output
  - Artifact: `adapted/2026-04-08_reddit_posts.json`
  - Objective-Proved: Proves Reddit-ready posts prepared for deployment.
  - Status: planned
- Evidence-Type: manual_verification
  - Artifact: User approval of deployment plan
  - Objective-Proved: Proves campaign ready for controlled test.
  - Status: planned

## Implementation Log
- 2026-04-08 01:02:14 Europe/London: Task created for Reddit engagement campaign using distribution_engine.

## Changes Made
- None yet.

## Validation Rules
- Do not fabricate engagement metrics or post URLs.
- Use only source-derived strategy performance data.
- Do not deploy posts without explicit user approval.
- Follow Reddit rules: no spam, appropriate subreddit selection, required disclosures.
- Comments > Likes - prioritize engagement depth over reach.

## Risks/Notes
- Reddit has strict self-promotion rules - posts must provide value, not just advertise.
- Some subreddits require minimum karma/account age to post.
- Strategy performance posts should include appropriate disclaimers.
- Start with r/algotrading as most relevant; test before expanding.
- Consider posting as discussion/question rather than announcement.

## Reddit Content Guidelines
- Lead with insight, not promotion
- Include real data points (gen_strategy_name, actual returns)
- Ask genuine questions to drive engagement
- Disclose: algorithmic, simulated/paper trading if applicable
- Avoid: hype language, unrealistic claims, excessive self-promotion

## Completion Status
- State: TODO
- Timestamp:
