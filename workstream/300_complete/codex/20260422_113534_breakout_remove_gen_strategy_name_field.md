---
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false

Task Summary: Remove the `gen_strategy_name` field from all virtual trade JSON files and stop it being written by `apply_strategy_name_fields` in `fs/strategy_name_generator.py`.

Context:
- `gen_strategy_name` is computed and written by `apply_strategy_name_fields()` at `fs/strategy_name_generator.py:169-171`
- It is called from `fs/common.py` at lines 1786, 1866, 3513, 3939 and from `DB/common.py` at lines 1109, 1211, 1709, 3043, 3385
- Field is no longer required in the trade JSON schema
- Existing `vt_*.json` files on disk may already contain the field and will need stripping

Destination Folder: None

Dependency: None

Plan:
- [ ] 1. Audit all read sites of `gen_strategy_name` across the codebase to confirm no consumers depend on it
  - Test: `grep -rn "gen_strategy_name" TradeApps/breakout/` — confirm no reads beyond the write in `strategy_name_generator.py`
  - Evidence:
- [ ] 2. Remove the `gen_strategy_name` write from `apply_strategy_name_fields` in `fs/strategy_name_generator.py` (lines 166-171)
  - Test: Grep confirms `gen_strategy_name` no longer assigned in `strategy_name_generator.py`
  - Evidence:
- [ ] 3. Apply same removal to `DB/common.py` if it has its own copy of the logic (check `DB/strategy_name_generator.py` if it exists)
  - Test: Grep `DB/` for `gen_strategy_name` — confirm no remaining write sites
  - Evidence:
- [ ] 4. Strip `gen_strategy_name` from any existing `vt_*.json` files on disk
  - Test: Confirm no `gen_strategy_name` key present in sampled files after strip script runs
  - Evidence:
- [ ] 5. Verify new trades written after the change do not contain `gen_strategy_name`
  - Test: Inspect a freshly written `vt_*.json` file after one poll cycle
  - Evidence:

Evidence:
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false

- Evidence-Type: diff
  - Artifact: fs/strategy_name_generator.py
  - Objective-Proved: gen_strategy_name assignment removed from apply_strategy_name_fields
  - Status: planned
- Evidence-Type: manual_verification
  - Artifact: vt_*.json sample after change
  - Objective-Proved: Field absent from newly written and existing trade files
  - Status: planned

Implementation Log:
- 2026-04-22: Task created.

Changes Made: (to be populated)

Validation: (to be populated)

Risks/Notes:
- Any API endpoint or UI that reads `gen_strategy_name` from trade files will break — Step 1 audit is mandatory before any code change
- `DB/common.py` imports `apply_strategy_name_fields` from the same `strategy_name_generator` module so a single change to the module covers both paths — but confirm the DB path does not have its own copy
- Existing files on disk will retain the field until explicitly stripped

Completion Status: Not started
---
