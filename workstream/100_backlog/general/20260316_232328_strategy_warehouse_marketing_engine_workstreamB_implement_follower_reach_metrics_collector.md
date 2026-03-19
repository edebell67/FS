# TASK B9: Implement Follower/Reach Metrics Collector

**Workstream:** B - SOCIAL DISTRIBUTION
**Workstream Goal:** Connect to social platforms and manage posting lifecycle.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 2.13
**Depends On:** 2.5, 2.6, 2.7, 2.8, 2.9, 2.10
**Blocks:** 4.2
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing

## Purpose

Track account-level growth metrics across all platforms to measure overall reach and follower growth.

## Input

- B1-B6: All platform connectors

## Output

- `ep_strategy_warehouse_marketing/solution/backend/src/services/accountMetricsService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/models/AccountMetric.py`

## Fields

```python
class AccountMetric:
    metric_id: UUID
    platform: Platform
    collected_at: datetime
    followers: int
    following: int
    total_posts: int
    total_impressions: int  # if available
    engagement_rate: float  # if available
    growth_rate_7d: float
    growth_rate_30d: float
```

## Action

1. Poll follower/subscriber counts daily per platform:
   - Twitter: followers
   - Discord: server members
   - Telegram: channel subscribers
   - LinkedIn: followers/connections
   - Reddit: karma, subscriber count
   - TikTok: followers
2. Poll impressions/reach weekly per platform
3. Calculate growth rates:
   - Daily change
   - Week-over-week percentage
   - Month-over-month percentage
4. Store historical data for trending (90 days minimum)
5. Generate aggregate cross-platform metrics

## Verification

- [ ] Record daily follower count per platform
- [ ] Calculate week-over-week growth percentage
- [ ] Store 90 days of historical data
- [ ] Generate aggregate cross-platform metrics

---

## Evidence

- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: Unit test output for metric collection
  - Objective-Proved: Account metrics tracking works
  - Status: planned
- Evidence-Type: log_output
  - Artifact: Daily metric collection logs
  - Objective-Proved: Collection scheduled and historical data stored
  - Status: planned

## Dependency

- Requires: B1-B6 (all platform connectors)
- Blocks: D2 (performance feedback loop)

## Notes

_Key objective metric: week-over-week follower growth. This directly measures "aggressive reach" goal._
