Source: User request to implement generic epic decomposition for any selected markdown file in /epic-decomposition, using skills/epic-decomposition and skills/ui-delivery-viewability where relevant, with LLM-backed intelligence and /epic-review-compatible output.
Task Summary: Replace the shallow epic decomposition flow with a skill-driven, LLM-backed decomposition engine that generates many deliverable task markdown files linked to the source epic and ready for review/allocation.
Context: workstream/kanban_dashboard.py; workstream/epic/bizPA.md; skills/epic-decomposition/SKILL.md; skills/ui-delivery-viewability/SKILL.md
Plan:
- [x] 1. Read the relevant skill files and inspect the target epic plus current decomposition flow.
  - [x] Test: Confirm the required decomposition and UI-viewability rules plus the current backend/UI path are captured.
  - [x] Evidence: Read skills/epic-decomposition/SKILL.md, skills/ui-delivery-viewability/SKILL.md, workstream/epic/bizPA.md, and traced /epic-decomposition in workstream/kanban_dashboard.py.
- [x] 2. Design and implement a reusable decomposition engine that uses skill-guided prompting plus LLM-backed task generation for arbitrary markdown epics.
  - [x] Test: The backend accepts a selected epic path and returns a validated multi-task payload with source-epic traceability and review-compatible metadata.
  - [x] Evidence: Added workstream/epic_decompose_cli.py plus validated payload handling in workstream/kanban_dashboard.py; live bizPA decomposition returned a 31-task JSON payload with epic/workstream/priority/source metadata.
- [x] 3. Wire /api/decompose-epic to the new engine and persist generated task markdown files for /epic-review.
  - [x] Test: Running the decomposition path against workstream/epic/bizPA.md creates multiple task files with epic/workstream metadata and source links.
  - [x] Evidence: Local replay of the validated bizPA payload created 31 files under workstream/100_todo, each with `Epic`, `Workstream`, `Priority`, and `Source Epic Path` metadata.
- [x] 4. Validate the implementation with at least one real decomposition run and record results.
  - [x] Test: Execute a local decomposition run, inspect generated output shape, and confirm /epic-review compatibility assumptions.
  - [x] Evidence: Live LLM-backed decomposition run for bizPA completed after schema fix; `_list_epics()` reports `bizpa_mvp_product_requirements_document` with 31 tasks across workstreams A-K.
Implementation Log:
- 2026-03-11 15:51:36 Started implementation task and opened the relevant skills and bizPA PRD.
- 2026-03-11 15:54:00 Added `workstream/epic_decompose_cli.py` to drive skill-guided LLM decomposition with JSON schema validation and artifact capture.
- 2026-03-11 15:56:00 Replaced the shallow regex-only epic decomposition path in `workstream/kanban_dashboard.py` with an LLM-backed decomposition runner, payload validation, source-epic traceability, and review-compatible task rendering.
- 2026-03-11 15:58:00 Fixed Windows temp/artifact handling and switched the Codex prompt transport to stdin to avoid command-line length issues.
- 2026-03-11 16:00:52 Ran a live network-backed decomposition validation against `workstream/epic/bizPA.md`, hit a response schema error, and updated the schema to require all declared task fields.
- 2026-03-11 16:16:08 Completed a successful live bizPA decomposition run producing a 31-task payload with warnings and suggested model affinities.
- 2026-03-11 16:19:43 Replayed the validated bizPA payload through the local write path, creating 31 task markdown files in `workstream/100_todo` and confirming Epic Review discovery.
Changes Made:
- Lifecycle task created for the decomposition implementation.
- Added `C:\Users\edebe\eds\workstream\epic_decompose_cli.py`
- Updated `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- Generated bizPA decomposition task files under `C:\Users\edebe\eds\workstream\100_todo\`
Validation:
- [x] Read and summarized the applicable skills and source epic.
- [x] `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\epic_decompose_cli.py`
  - Result: Both Python files compiled successfully after the implementation changes.
- [x] Live network-backed run: `python C:\Users\edebe\eds\workstream\epic_decompose_cli.py --input C:\Users\edebe\eds\workstream\epic\bizPA.md`
  - Result: After one schema correction and a longer timeout, the LLM returned a valid 31-task decomposition for bizPA with warnings and suggested agent affinities.
- [x] Local write-path replay using saved bizPA decomposition output
  - Result: `decompose_epic('workstream/epic/bizPA.md', {})` created 31 task files in `workstream/100_todo`.
- [x] Epic Review discovery check via `_list_epics()`
  - Result: Epic slug `bizpa_mvp_product_requirements_document` is listed with 31 tasks across workstreams `A` through `K`.
- [x] Generated file inspection
  - Result: Sample files contain `Epic`, `Workstream`, `Priority`, `Source Epic Path`, verification checklists, and UI-viewability-expanded notes where relevant.
Risks/Notes:
- LLM-backed decomposition depends on a locally available executable or environment override; implementation should provide deterministic fallback/error reporting if the configured model path is unavailable.
- Current default path uses local `codex exec`; alternatively `KANBAN_EPIC_DECOMP_CMD` can be set to another compatible command.
- UI-visible workflow changed: user verification is still required for `/epic-decomposition` and `/epic-review` interaction in the browser.
Completion Status: Awaiting user verification as of 2026-03-11 16:22:00


# User Feedback
User Verified: PASS
