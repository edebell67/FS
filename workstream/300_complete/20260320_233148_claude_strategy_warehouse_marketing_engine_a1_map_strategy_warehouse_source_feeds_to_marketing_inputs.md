Source: `C:\Users\edebe\eds\workstream\000_epic\20260316_135233_strategy_warehouse_autonomous_marketing_engine_processed.md`

Task Summary: Establish a canonical mapping from the live JSON feed files to the internal marketing content inputs used across generation, scheduling, and analytics.

Context:
- Workstream A: Content Pipeline
- Epic: Strategy Warehouse Autonomous Marketing Engine
- Expected Output: Source feed field map, parser contract, and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/source_feed_map.py` or equivalent mapping artifact.

Dependency: Z1, Z2, Z3

Priority: 1

# Map Strategy Warehouse source feeds to marketing inputs

## Input
Local Strategy Warehouse JSON path and the clarified source files `_summary_net.json`, `_frequency.json`, `_dna_frequency.json`, `_dna_alt_frequency.json`.

## Output
Source feed field map, parser contract, and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/source_feed_map.py` or equivalent mapping artifact.

## Plan
- [x] 1. Inspect and normalize the source JSON structures, define required and optional fields, and document fallback behavior when expected feed files are missing or partially populated.
  - [x] Test: Each source JSON file is mapped to a normalized internal structure consumed by downstream services.
  - [x] Evidence: `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\source_feed_map.py` created and validated against live JSON files.
- [x] 2. The field map identifies required, optional, and derived values explicitly.
  - [x] Test: The field map identifies required, optional, and derived values explicitly.
  - [x] Evidence: `source_feed_map.py` contains typed Pydantic models with default values and field aliases.
- [x] 3. Fallback behavior is documented for missing or stale feed inputs.
  - [x] Test: Fallback behavior is documented for missing or stale feed inputs.
  - [x] Evidence: Comments and custom validators in `source_feed_map.py` implement and document fallback logic.

## Validation
- [x] Each source JSON file is mapped to a normalized internal structure consumed by downstream services.
- [x] The field map identifies required, optional, and derived values explicitly.
- [x] Fallback behavior is documented for missing or stale feed inputs.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `python verify_mapping.py` output showing successful parsing of all 4 JSON files.
  - Objective-Proved: Delivery of `A1` for the consolidated Strategy Warehouse epic.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\source_feed_map.py`
  - Objective-Proved: Canonical mapping artifact exists.
  - Status: captured

## Implementation Log
- Created from fresh decomposition of the consolidated epic on 2026-03-20 23:31:48.
- 2026-03-21 01:40:00: Identified source JSON files in `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-20`.
- 2026-03-21 01:45:00: Inspected JSON structures for `_summary_net.json`, `_frequency.json`, `_dna_frequency.json`, and `_dna_alt_frequency.json`.
- 2026-03-21 01:50:00: Implemented Pydantic models in `ep_strategy_warehouse_marketing/solution/backend/src/schemas/source_feed_map.py` to act as the canonical map and parser contract.
- 2026-03-21 02:00:00: Validated the mapping using a script that parses actual live data from March 20, 2026.
- 2026-03-21 02:05:00: Updated task file and documented completion.

## Changes Made
- Created `ep_strategy_warehouse_marketing/solution/backend/src/schemas/source_feed_map.py`.
- Added Pydantic models: `NetPoint`, `SummaryNetFeed`, `Leader`, `FrequencySnapshot`, `FrequencyFeed`, `WarehouseSnapshot`.
- Implemented field aliases and custom validators for robust parsing and fallback behavior.

## Risks/Notes
- Task created from fresh decomposition after active-lane reset.
- Pydantic models provide automated validation and normalization.

Completion Status: Complete
