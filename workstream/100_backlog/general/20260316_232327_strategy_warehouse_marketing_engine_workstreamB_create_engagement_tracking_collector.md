# TASK B8: Create Engagement Tracking Collector

**Workstream:** B - SOCIAL DISTRIBUTION
**Workstream Goal:** Connect to social platforms and manage posting lifecycle.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 2.12
**Depends On:** 2.5, 2.6, 2.7, 2.8, 2.9, 2.10
**Blocks:** 4.2
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing

## Purpose

Collect engagement metrics from posted content across all platforms for performance analysis.

## Input

- B1-B6: All platform connectors

## Output

- `ep_strategy_warehouse_marketing/solution/backend/src/services/engagementTrackerService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/models/EngagementMetric.py`

## Fields

```python
class EngagementMetric:
    metric_id: UUID
    post_id: UUID
    platform: Platform
    collected_at: datetime
    impressions: int
    likes: int
    comments: int
    shares: int  # retweets, reposts, etc.
    clicks: int
    engagement_rate: float
    platform_specific: Dict  # platform-specific metrics
```

## Action

1. Poll Twitter API for tweet metrics (likes, retweets, replies, impressions)
2. Poll Discord for message reactions
3. Poll Telegram for message views
4. Poll LinkedIn for post impressions and engagement
5. Poll Reddit for upvotes, comments, karma impact
6. Poll TikTok for views, likes, shares, comments
7. Store metrics with content_id foreign key
8. Schedule collection at 1hr, 6hr, 24hr, 7d post-publish

## Verification

- [ ] Collect metrics for posted content after 1hr, 24hr
- [ ] Store metrics in persistent database
- [ ] Handle API errors gracefully (don't lose data)
- [ ] Metrics correctly attributed to source content

---

## Evidence

- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: Unit test output for metric collection
  - Objective-Proved: Engagement tracking works correctly
  - Status: planned
- Evidence-Type: log_output
  - Artifact: Metric collection logs
  - Objective-Proved: Collection scheduled and executed
  - Status: planned

## Dependency

- Requires: B1-B6 (all platform connectors)
- Blocks: D2 (performance feedback loop)

## Notes

_Critical for A-B testing and content optimization. Collect at multiple time points for decay analysis._
