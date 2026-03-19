# TASK D1: Build Autonomous Scheduler

**Workstream:** D - ORCHESTRATION & AUTONOMY
**Workstream Goal:** Make the system self-running with appropriate controls.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 4.1
**Depends On:** 1.4, 2.3, 2.5, 2.11
**Blocks:** 4.2, 4.3
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing

## Purpose

Orchestrate all automated marketing activities to achieve autonomous operation.

## Input

- Z4: Health check endpoint
- A3: Content queue
- B1: Twitter connector
- B7: Posting rules engine

## Output

- `ep_strategy_warehouse_marketing/solution/backend/src/services/autonomousSchedulerService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/config/scheduler_config.yaml`

## Fields

```yaml
scheduler:
  content_generation:
    frequency: "0 */4 * * *"  # Every 4 hours
    data_source: "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex\\{date}\\_*.json"

  posting:
    check_interval_seconds: 60
    platforms:
      twitter: true
      discord: true
      telegram: true
      linkedin: true
      reddit: true
      tiktok: true

  metrics_collection:
    engagement: "*/30 * * * *"  # Every 30 minutes
    followers: "0 0 * * *"  # Daily at midnight

  health_check:
    interval_seconds: 300
```

## Action

1. Implement main scheduling loop using APScheduler or similar
2. Coordinate content generation triggers:
   - Watch Strategy Warehouse data files for changes
   - Generate content on new data
3. Coordinate posting execution:
   - Pull from content queue
   - Route to appropriate connector
   - Respect posting rules
4. Coordinate metric collection:
   - Schedule engagement polling
   - Schedule follower count updates
5. Handle graceful shutdown:
   - SIGTERM handling
   - Drain queue before exit
   - Save state for restart

## Verification

- [ ] Scheduler starts automatically on system boot
- [ ] Scheduler triggers content generation on schedule
- [ ] Scheduler posts content at scheduled times
- [ ] Scheduler respects rate limits across platforms
- [ ] Scheduler stops cleanly on SIGTERM

---

## Evidence

- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: log_output
  - Artifact: Scheduler execution logs
  - Objective-Proved: Scheduler runs autonomously
  - Status: planned
- Evidence-Type: test_output
  - Artifact: Integration test output
  - Objective-Proved: Scheduling logic works correctly
  - Status: planned

## Dependency

- Requires: Z4 (health check), A3 (content queue), B1 (Twitter), B7 (posting rules)
- Blocks: D2 (feedback loop), D3 (kill switch)

## Notes

_Core of autonomous operation. Must be robust and handle failures gracefully._
