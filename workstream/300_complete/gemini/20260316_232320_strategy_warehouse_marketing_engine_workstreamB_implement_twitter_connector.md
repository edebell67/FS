# TASK B1: Implement Twitter/X Connector

**Workstream:** B - SOCIAL DISTRIBUTION
**Workstream Goal:** Connect to social platforms and manage posting lifecycle.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 2.5
**Depends On:** 1.1, 1.2, 1.3
**Blocks:** 2.11, 2.12, 2.13, 3.1, 4.1
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing

## Purpose

Enable posting to Twitter/X platform via API for primary social media distribution.

## Input

- Z1, Z2, Z3: Infrastructure setup
- Twitter Developer Account credentials (BLOCKER - external dependency)

## Output

- `ep_strategy_warehouse_marketing/solution/backend/src/connectors/twitterConnector.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/models/TwitterAuth.py`

## Action

1. Implement OAuth 2.0 authentication flow
2. Implement tweet posting:
   - Text-only tweets (max 280 chars)
   - Tweets with media (images up to 4)
   - Thread posting (multiple connected tweets)
3. Implement rate limit handling:
   - Track 15 requests per 15-minute window
   - Queue requests when limit reached
4. Implement error handling and retry logic
5. Log all API interactions for debugging
6. Store posted tweet IDs for engagement tracking

## Verification

- [ ] Successfully authenticate with Twitter API
- [ ] Post text-only tweet
- [ ] Post tweet with image attachment
- [ ] Handle rate limit gracefully (queue, not crash)
- [ ] Log all API interactions for debugging

---

## Evidence

- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: Integration test output (with mock or sandbox)
  - Objective-Proved: Twitter connector functions correctly
  - Status: planned
- Evidence-Type: log_output
  - Artifact: API interaction logs
  - Objective-Proved: Rate limiting and error handling work
  - Status: planned

## Required Skills

- `skills/workstream-task-lifecycle/SKILL.md` - Follow lifecycle format

## Dependency

- Requires: Z1, Z2, Z3 (infrastructure)
- External: Twitter Developer Account credentials
- Blocks: B7, B8, B9, C1, D1

## Notes

_Primary platform connector. Critical path for MVP._
