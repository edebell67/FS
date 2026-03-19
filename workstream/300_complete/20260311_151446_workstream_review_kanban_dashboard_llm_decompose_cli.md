Source: Direct review request for workstream kanban and decomposition scripts.
Task Summary: Perform a code review of kanban_dashboard.py and llm_decompose_cli.py, document findings with file/line references, and capture validation evidence.
Context: workstream/kanban_dashboard.py; workstream/llm_decompose_cli.py
Plan:
- [x] 1. Read lifecycle instructions and create the in-progress task record.
  - [x] Test: Confirm a single lifecycle file exists in workstream/200_inprogress for this review task.
  - [x] Evidence: Creating workstream/200_inprogress/20260311_151446_workstream_review_kanban_dashboard_llm_decompose_cli.md.
- [x] 2. Inspect both target files and identify concrete review findings with exact references.
  - [x] Test: Capture line-numbered references for each finding from both Python files.
  - [x] Evidence: Collected line-numbered excerpts for kanban_dashboard.py lines 2861-2889 and 3170-3377, and llm_decompose_cli.py lines 18-29.
- [x] 3. Summarize the review outcome and record validation results in this lifecycle file.
  - [x] Test: Final response includes prioritized findings and the lifecycle file records commands/results.
  - [x] Evidence: Review findings documented below; final response prepared from this record.
Implementation Log:
- 2026-03-11 15:14:46 Created review task and moved directly into in-progress for active verification work.
- 2026-03-11 15:15:00 Read skills/workstream-task-lifecycle/SKILL.md and confirmed lifecycle naming/content requirements.
- 2026-03-11 15:16:30 Inspected worker, review gate, and decomposition parser paths with line-numbered file dumps.
- 2026-03-11 15:17:20 Reproduced _extract_summary fallback behavior and _mark_all_checkboxes_complete behavior with local Python snippets.
Changes Made:
- Created lifecycle task file for this review.
- No source code changes made; review-only task.
Validation:
- [x] Lifecycle file path reserved and task started.
- [x] `Get-Content C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
  - Result: Confirmed required lifecycle workflow and task-file template requirements.
- [x] Line-numbered inspection of `workstream/kanban_dashboard.py`
  - Result: Captured exact references for review gate file moves/deletes, agent command fallback, checkbox auto-completion, and completion gate flow.
- [x] Line-numbered inspection of `workstream/llm_decompose_cli.py`
  - Result: Captured exact references for summary extraction fallback and task generation behavior.
- [x] `python -` snippet importing `workstream.llm_decompose_cli._extract_summary`
  - Result: Markdown sample with `## Task Summary` returned `## Task Summary Build the dashboard and validate the pipeline.` instead of the section body alone.
- [x] `python -` snippet importing `workstream.kanban_dashboard._mark_all_checkboxes_complete`
  - Result: Function converted prerequisite, plan, test, evidence, and validation checkboxes to checked, including `Evidence: pending`.
Risks/Notes:
- Review-only task; no code changes planned unless separately requested.
- Findings:
  - High: `workstream/kanban_dashboard.py` lines 3173-3186 route `gemini` and `claude` fallback execution through the `codex exec` binary/prompt path, so non-Codex lanes run the wrong agent whenever no env override is configured.
  - High: `workstream/kanban_dashboard.py` lines 3134-3139 and 3365-3377 mark every unchecked checkbox in the task file as complete before gating completion, which can falsely satisfy tests/evidence/validation and preserve `Evidence: pending` as if it passed.
  - Medium: `workstream/kanban_dashboard.py` lines 2863-2889 identify review artifacts with `core_name in f`, which can move/delete unrelated files when one backlog id is a substring of another.
  - Medium: `workstream/llm_decompose_cli.py` lines 18-29 fail to parse standard section-style `## Task Summary` markdown; the fallback returns the heading text plus body, degrading the generated decomposition prompt content.
Completion Status: Complete as of 2026-03-11 15:18:00
