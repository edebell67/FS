# TASK A1: Define Publishable Content Schema

**Workstream:** A - CONTENT PIPELINE
**Workstream Goal:** Transform Strategy Warehouse data into publishable marketing content.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 2.1
**Depends On:** 1.1, 1.2, 1.3
**Blocks:** 2.2, 2.3, 2.4, 3.1
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing
- **Data Source:** `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\{date}\_*.json`

## Purpose

Define the data structures for all marketing content types that will be published across social platforms.

## Input

- Strategy Warehouse JSON files:
  - `_summary_net.json` - Performance summaries
  - `_frequency.json` - Trading frequency data
  - `_dna_frequency.json` - Strategy DNA metrics
  - `_dna_alt_frequency.json` - Alternative DNA metrics
- Infrastructure setup (Z1, Z2, Z3)

## Output

- `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`

## Fields

```python
content_id: UUID
content_type: Enum[signal_alert, performance_summary, strategy_ranking, educational]
headline: str  # max 100 chars for Twitter
body: str  # max 280 chars for Twitter, longer for other platforms
media_urls: List[str]  # optional images/charts
hashtags: List[str]
call_to_action: str
landing_page_url: str
created_at: datetime
scheduled_for: datetime
platform_variants: Dict[Platform, VariantContent]
source_data: Dict  # Reference to source JSON data
```

## Action

1. Analyze Strategy Warehouse JSON file structures
2. Define Pydantic models for each content type
3. Create platform-specific constraints (char limits, media formats)
4. Generate JSON schema from Pydantic models
5. Add validation rules for each field
6. Document schema with examples

## Verification

- [ ] Schema validates all required content types
- [ ] Schema enforces platform-specific constraints (char limits)
- [ ] Schema documented with examples
- [ ] Schema can parse sample Strategy Warehouse data

---

## Evidence

- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `content_schema.py` and `publishable_content_schema.json`
  - Objective-Proved: Schema definitions complete
  - Status: planned
- Evidence-Type: test_output
  - Artifact: Unit test output validating schema against sample data
  - Objective-Proved: Schema validates correctly
  - Status: planned

## Required Skills

- `skills/workstream-task-lifecycle/SKILL.md` - Follow lifecycle format

## Dependency

- Requires: Z1, Z2, Z3 (infrastructure)
- Blocks: A2, A3, A4, C1

## Notes

_Foundation task for content pipeline. All content generation depends on this schema._
