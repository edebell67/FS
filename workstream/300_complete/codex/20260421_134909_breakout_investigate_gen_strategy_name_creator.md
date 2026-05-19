---
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false

Task Summary: Identify which function sets the `gen_strategy_name` field on virtual trade JSON files in `TradeApps/breakout/fs/json/live/forex/<date>/virtual/`.

Context:
- Sample vt_ file contains: `"gen_strategy_name": "tango-matrix_2_z17a_def3"`
- Field is present alongside `source_strategy` and `strategy_name`
- `_create_new_v_trade` in `fs/common.py:3858` builds the initial trade payload but does not explicitly set `gen_strategy_name` in the visible schema (lines 3910–3935)
- `apply_strategy_name_fields(trade_data)` is called at line 3936 — this is a candidate

Destination Folder: None

Dependency: None

Plan:
- [ ] 1. Inspect `apply_strategy_name_fields` to confirm whether it sets `gen_strategy_name`
  - Test: Grep for `apply_strategy_name_fields` definition in `fs/common.py`; read function body
  - Evidence:
- [ ] 2. If not there, grep full codebase for `gen_strategy_name` assignments
  - Test: `grep -rn "gen_strategy_name" TradeApps/breakout/fs/` — identify all write sites
  - Evidence:
- [ ] 3. Trace how the value `tango-matrix_2_z17a_def3` is derived from `source_strategy`
  - Test: Confirm the mapping/transformation logic and the data source feeding it
  - Evidence:
- [ ] 4. Document findings in this task file
  - Test: Function name, file, line number recorded below
  - Evidence:

Evidence:
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true

- Evidence-Type: manual_verification
  - Artifact: not_applicable
  - Objective-Proved: Function and line that sets gen_strategy_name identified
  - Status: planned

Implementation Log:
- 2026-04-21: Task created.

Changes Made: (to be populated — investigation only, no code changes expected)

Validation: (to be populated)

Risks/Notes:
- `gen_strategy_name` may be set via a normalisation/repair function called after initial file write
- Value format `tango-matrix_2_z17a_def3` suggests a human-readable alias mapped from a strategy hash or key

Completion Status: Not started
---
