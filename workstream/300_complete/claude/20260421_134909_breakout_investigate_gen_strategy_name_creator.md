---
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false

Task Summary: Identify which function sets the `gen_strategy_name` field on virtual trade JSON files.

Context:
- Sample vt_ file contains: `"gen_strategy_name": "tango-matrix_2_z17a_def3"`
- `_create_new_v_trade` calls `apply_strategy_name_fields(trade_data)` at `fs/common.py:3939`

Destination Folder: None

Dependency: None

Plan:
- [x] 1. Inspect `apply_strategy_name_fields` to confirm whether it sets `gen_strategy_name`
  - Test: Grep for definition — found in `fs/strategy_name_generator.py:146`
  - Evidence: Function sets `record["gen_strategy_name"]` at line 170
- [x] 2. Grep full codebase for `gen_strategy_name` assignments
  - Test: Grep confirmed only written inside `apply_strategy_name_fields`
  - Evidence: `fs/strategy_name_generator.py:169-171`
- [x] 3. Trace how the value `tango-matrix_2_z17a_def3` is derived
  - Test: Read full `strategy_name_generator.py`
  - Evidence: See Changes Made section
- [x] 4. Document findings
  - Test: Findings recorded below
  - Evidence: See Changes Made section

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: manual_verification
  - Artifact: TradeApps/breakout/fs/strategy_name_generator.py lines 135–173
  - Objective-Proved: `gen_strategy_name` is set exclusively by `apply_strategy_name_fields` via `gen_strategy_name()`
  - Status: captured

Implementation Log:
- 2026-04-21: Task created and investigated in same session.

Changes Made: None — investigation only.

**Findings:**

- **Field set by**: `apply_strategy_name_fields(record)` in `fs/strategy_name_generator.py:146`
  - Called from `_create_new_v_trade` at `fs/common.py:3939` (plus 3 other call sites in `fs/common.py`: lines 1786, 1866, 3513)
- **Field computed by**: `gen_strategy_name(strategy_name, product)` at `strategy_name_generator.py:135`
- **How the value is derived** (e.g. `tango-matrix_2_z17a_def3`):
  1. Parses `strategy_name` → extracts `strategy`, `window`, `tp`, `sl`
  2. MD5-hashes `"{PRODUCT}_{strategy}"` → picks two words from a 70-word WORDS list → alias e.g. `tango-matrix`
  3. Appends `window` → `_2_`
  4. MD5-hashes `"{PRODUCT}_tp_{tp}"` → first 3 hex chars, prefixed `z` → `z17a`
  5. MD5-hashes `"{PRODUCT}_sl_{sl}"` → first 3 hex chars, prefixed `d` → `def3`
  6. Final format: `{alias}_{window}_z{tp_code}_d{sl_code}`
- **Module imported at**: `fs/common.py:29`

Validation:
- Confirmed `gen_strategy_name` has no other write sites in `fs/` outside `strategy_name_generator.py`

Risks/Notes:
- Alias is deterministic and stable for a given product+strategy combination
- `apply_strategy_name_fields` is also called on load/repair paths so the field can be backfilled on existing files

Completion Status: Complete — 2026-04-21
---
