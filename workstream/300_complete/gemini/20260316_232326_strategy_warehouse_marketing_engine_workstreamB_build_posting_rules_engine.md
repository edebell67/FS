# TASK B7: Build Posting Rules Engine

**Workstream:** B - SOCIAL DISTRIBUTION
**Workstream Goal:** Connect to social platforms and manage posting lifecycle.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 2.11
**Depends On:** 2.5, 2.6, 2.7, 2.8, 2.9, 2.10
**Blocks:** 4.1
**Readiness:** ready
**Status:** [x] Complete

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing

## Purpose

Define and enforce posting rules across all 6 platforms to optimize engagement and respect guardrails.

## Input

- B1-B6: All platform connectors (Twitter, Discord, Telegram, LinkedIn, Reddit, TikTok)

## Output

- `ep_strategy_warehouse_marketing/solution/backend/src/services/postingRulesService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/config/posting_rules.yaml`

## Fields

```yaml
platforms:
  twitter:
    posting_windows:
      - start: "09:00"
        end: "12:00"
        timezone: "UTC"
      - start: "17:00"
        end: "20:00"
        timezone: "UTC"
    max_posts_per_day: 10
    min_interval_minutes: 60
    required_hashtags: ["#trading", "#forex", "#strategywarehouse"]

  discord:
    max_posts_per_day: 20
    channels:
      signals: "channel_id_1"
      performance: "channel_id_2"

guardrails:
  blocked_actions:
    - spend_money
    - respond_to_dms
  requires_approval:
    - posts_with_predictions
```

## Action

1. [x] Implement timing rules (best times to post per platform)
2. [x] Implement frequency rules (max posts per day per platform)
3. [x] Implement content rules (hashtag limits, mention limits)
4. [x] Implement guardrail rules:
   - Block spending money (ads) - MANDATORY
   - Block responding to DMs - MANDATORY
5. [x] Add rule validation before posting
6. [x] Log rule violations for review
7. [x] Fix module path conflicts (added `__init__.py` and fixed `sys.path.insert(0, ...)` in tests)

## Verification

- [x] Rules prevent posting outside configured windows
- [x] Rules enforce daily post limits
- [x] Rules add required hashtags/mentions
- [x] Guardrails block posts that need human approval
- [x] Rule configuration is hot-reloadable
- [x] Verified imports work even with environment path conflicts

---

## Evidence

- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: Unit test output for rule validation
  - Objective-Proved: Rules enforce correctly
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `posting_rules.yaml` configuration file
  - Objective-Proved: Rules are configurable
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `solution/backend/src/__init__.py` and `services/__init__.py`
  - Objective-Proved: Package structure is correct
  - Status: captured

## Implementation Log
- 2026-03-17 21:00: Created `posting_rules.yaml` with platform-specific timing, frequency, and content rules.
- 2026-03-17 21:05: Implemented `PostingRulesService.py` with YAML loading, hot-reload, and stateful tracking.
- 2026-03-17 21:10: Added `pyyaml` to `requirements.txt`.
- 2026-03-17 21:15: Created and ran `tests/test_posting_rules.py` verifying all rules and guardrails.
- 2026-03-17 21:30: Fixed `ModuleNotFoundError` by adding `__init__.py` files and using `sys.path.insert(0, ...)` in tests to avoid conflicts with `DataInsights` package.

## Dependency

- Requires: B1-B6 (all platform connectors) - VERIFIED COMPLETE
- Blocks: D1 (autonomous scheduler)

## Notes

_Guardrails are mandatory: no spending, no DM responses. These cannot be overridden by configuration. The package structure now uses `__init__.py` to ensure proper import resolution across different workspaces._
