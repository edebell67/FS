# TASK A2: Build Content Generation Service

**Workstream:** A - CONTENT PIPELINE
**Workstream Goal:** Transform Strategy Warehouse data into publishable marketing content.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 2.2
**Depends On:** 2.1
**Blocks:** 2.4, 3.1
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing
- **Data Source:** `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\{date}\_*.json`

## Purpose

Generate marketing content from Strategy Warehouse data using templates and punchy, action-oriented language.

## Input

- A1: Content schema definitions
- Strategy Warehouse JSON files (live trading data)

## Output

- `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2`
- `ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2`
- `ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2`

## Action

1. Implement signal-to-content transformer
   - Parse `_summary_net.json` for trading signals
   - Generate punchy headlines (e.g., "BUY surges +2.3% on EURUSD")
2. Implement performance-to-content transformer
   - Parse `_frequency.json` for performance metrics
   - Generate summary posts with key stats
3. Implement strategy ranking content generator
   - Parse `_dna_frequency.json` for strategy rankings
   - Generate leaderboard-style posts
4. Add Jinja2 template engine for content variation
5. Include hashtag generation logic
6. Include call-to-action templates

## Verification

- [ ] Generate valid signal alert content from sample data
- [ ] Generate valid performance summary from sample data
- [ ] All generated content passes schema validation
- [ ] Content includes appropriate hashtags and CTAs
- [ ] Content respects platform character limits

---

## Evidence

- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: Unit test output showing generated content
  - Objective-Proved: Content generation works correctly
  - Status: planned
- Evidence-Type: file_output
  - Artifact: Sample generated content files
  - Objective-Proved: Content matches expected format
  - Status: planned

## Required Skills

- `skills/strategy-battle-punchy-updates/SKILL.md` - Use punchy, action-oriented language
- `skills/workstream-task-lifecycle/SKILL.md` - Follow lifecycle format

## Dependency

- Requires: A1 (content schema)
- Blocks: A4, C1

## Notes

_Use impact verbs: surges, stumbles, holds, rotates, presses. Keep lines short and direct._
