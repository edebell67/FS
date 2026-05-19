# TASK B5: Implement Reddit Connector

**Workstream:** B - SOCIAL DISTRIBUTION
**Workstream Goal:** Connect to social platforms and manage posting lifecycle.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** C:\Users\edebe\eds\ep_strategy_warehouse_marketing\
**Epic Sequence:** 2.9
**Depends On:** 1.1, 1.2, 1.3
**Blocks:** 2.11, 2.12, 2.13
**Readiness:** ready
**Status:** [x] In Progress (Logic Implemented & Verified)

---

## Source

- **Epic:** workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md
- **Project:** Strategy Warehouse Marketing

## Purpose

Enable posting to Reddit for community engagement in trading/finance subreddits.

## Input

- Z1, Z2, Z3: Infrastructure setup
- Reddit API credentials (BLOCKER - external dependency for LIVE testing)

## Output

- ep_strategy_warehouse_marketing/solution/backend/src/connectors/redditConnector.py
- ep_strategy_warehouse_marketing/solution/backend/src/models/RedditAuth.py

## Plan

- [x] 1. Research existing connectors and define RedditAuth model
  - Test: Check if src/models/RedditAuth.py exists and is valid Pydantic model
  - Evidence: File created and used in connector.
- [x] 2. Implement RedditConnector logic with PRAW
  - Test: Check src/connectors/redditConnector.py for methods: post_text, post_link, post_image, post_comment
  - Evidence: File content verified.
- [x] 3. Create unit tests with mocks to verify connector logic
  - Test: Run python -m unittest tests/test_reddit_connector.py
  - Evidence: Ran 5 tests in 0.044s. OK
- [ ] 4. Verify live authentication (Blocked by credentials)
  - Test: Call erify_auth() with real credentials
  - Evidence: Log showing successful authentication.

## Implementation Log

- 2026-03-17 20:30: Added praw to equirements.txt.
- 2026-03-17 20:35: Created RedditAuth.py model.
- 2026-03-17 20:40: Implemented RedditConnector class in edditConnector.py.
- 2026-03-17 20:45: Created and ran 	est_reddit_connector.py with 100% pass rate.

## Changes Made

- Modified equirements.txt: Added praw==7.7.1.
- Created src/models/RedditAuth.py: Pydantic models for Reddit authentication.
- Created src/connectors/redditConnector.py: Connector class using PRAW.
- Created 	ests/test_reddit_connector.py: Unit tests for the new connector.

## Validation

- Ran unit tests: .\.venv\Scripts\python.exe -m unittest tests/test_reddit_connector.py -> 5/5 passed.

## Evidence

- Objective-Delivery-Coverage: 75% (Logic done, live test blocked)
- Auto-Acceptance: false (Requires credential verification by user)
- - Evidence-Type: test_output
  - Artifact: 	ests/test_reddit_connector.py output
  - Objective-Proved: Reddit connector logic (posting, commenting, karma checks) functions correctly.
  - Status: captured
- - Evidence-Type: file_output
  - Artifact: src/connectors/redditConnector.py
  - Objective-Proved: Connector implementation matches requirements.
  - Status: captured

## Dependency

- Requires: Z1, Z2, Z3 (infrastructure)
- External: Reddit API credentials (needed for final verification)
- Blocks: B7, B8, B9

## Notes

_Reddit has strict self-promotion rules. Logic includes karma checks to avoid posting with low-karma accounts._

## Completion Status
Awaiting user verification (Logic implemented, credentials needed for live test).
