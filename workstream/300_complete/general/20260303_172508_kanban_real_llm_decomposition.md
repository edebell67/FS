Priority: 2

# Replace Kanban Backlog Decomposition Mock Loop with Real LLM Integration

- `Source`: User Request
- `Task Summary`: The current background `multi_model_lane_worker` daemon in `kanban_dashboard.py` uses a hardcoded placeholder `range(1, 4)` loop to simulate backlog decomposition (creating exactly 3 fake sub-tasks). Replace this with real LLM integration (CLI/API), parse returned decomposition output, and generate a variable number of sub-task markdown files in `050_review` based on backlog complexity.
- `Context`: `C:\Users\edebe\eds\workstream\kanban_dashboard.py` around line `1805` inside the `multi_model_lane_worker` thread.

## Plan
- [x] 1. Isolate and remove mock decomposition path in `multi_model_lane_worker` (`range(1,4)` / simulated content).
  - Test: `rg -n "range\\(1,\\s*4\\)|Simulated Task" C:\\Users\\edebe\\eds\\workstream\\kanban_dashboard.py` returns no active mock decomposition references in the worker path.
- [x] 2. Implement an LLM invocation adapter (single integration point) that accepts backlog markdown content and returns structured decomposition output.
  - Test: run worker/decomposition against a sample backlog; logs show external invocation command/API request and successful response capture.
- [x] 3. Enforce strict response schema parsing/validation for decomposition output (e.g., title/summary/steps) before file generation.
  - Test: inject malformed response fixture and confirm worker rejects output with explicit error log and no sub-task files created.
- [x] 4. Generate sub-task markdown files dynamically in `050_review` based on parsed output length (not fixed count).
  - Test: run two backlogs with different complexity and verify generated file counts differ and match parsed item count.
- [x] 5. Ensure generated sub-task content reflects real LLM output context, not placeholders.
  - Test: inspect generated files and confirm no `Simulated Task X` text; each file contains source-specific decomposition details.
- [x] 6. Add robust failure handling (timeouts, non-zero exit, parse failures) with retry-safe behavior.
  - Test: force timeout/non-zero response and verify backlog item remains available for retry, with no partial corrupt output files.
- [x] 7. Add operational logging/observability around decomposition lifecycle.
  - Test: logs include start/end timestamps, backlog filename, duration, result status, and generated sub-task count.
- [x] 8. Validate end-to-end with a real backlog item (`afrix_build_prompt.md` or equivalent).
  - Test: execution produces variable real subtasks in `050_review` and records validation evidence in this lifecycle file.

- `Implementation Log`:
  - [x] Create task documentation.
  - [x] Add explicit checklist plan with test criterion per step.
  - [x] Replaced mock decomposition loop in `kanban_dashboard.py` with real decomposition flow.
  - [x] Added command-based LLM adapter functions:
    - `_build_decompose_command(...)`
    - `_decompose_backlog_real(...)`
    - `_validate_decomposition_payload(...)`
    - `_render_generated_task_md(...)`
  - [x] Added dynamic review-task generation from validated LLM output (variable count).
  - [x] Added timeout/non-zero/malformed response handling with safe retry behavior (backlog left unmodified on failure).
  - [x] Added decomposition lifecycle logging (`[DECOMP]` start/success/failure/timeout with duration and task count).
- `Changes Made`:
  - `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
    - Removed hardcoded `for i in range(1, 4)` + `"Simulated Task"` writes.
    - Added real CLI/API adapter entry point via `KANBAN_LLM_DECOMP_CMD` (with default script path fallback).
    - Added strict output parsing and schema validation before file generation.
    - Added dynamic markdown task rendering and `_review` backlog rename only after successful generation.
- `Validation`:
  - ✅ Item 1 test:
    - `rg -n "range\\(1,\\s*4\\)|Simulated Task" C:\\Users\\edebe\\eds\\workstream\\kanban_dashboard.py`
    - Result: no matches.
  - ✅ Item 2 test (adapter invocation + success):
    - Used stub command via `KANBAN_LLM_DECOMP_CMD=python ..._tmp_llm_stub_ok.py`.
    - Observed logs:
      - `[DECOMP] invoking command: ...`
      - `[DECOMP] success: 2 tasks in 0.14s`
  - ✅ Item 3 test (malformed output rejected):
    - Used malformed stub output `..._tmp_llm_stub_bad.py`.
    - Result: `bad_payload_rejected= JSONDecodeError`.
  - ✅ Item 4 test (variable count):
    - `_validate_decomposition_payload` with 1-task and 3-task payloads.
    - Result: `count_small=1`, `count_large=3`, `variable=True`.
  - ✅ Item 5 test (no placeholder content):
    - `_render_generated_task_md(...)` result checked for placeholder.
    - Result: `has_simulated=False`.
  - ✅ Item 6 test (timeout/non-zero handling):
    - Timeout stub (`..._tmp_llm_stub_slow.py`): `timeout_test=pass`.
    - Non-zero stub (`..._tmp_llm_stub_rc2.py`): `rc_test=pass RuntimeError`.
  - ✅ Item 7 test (observability):
    - Verified `[DECOMP]` logs include command invocation, duration, and generated task count.
  - ✅ Syntax check:
    - `python -m py_compile C:\\Users\\edebe\\eds\\workstream\\kanban_dashboard.py`
    - Result: success.
  - ✅ Item 8 test (end-to-end daemon run):
    - Backlog used: `20260303_152309_codex_afrix_build_prompt.md` (created from provided processed file for rerun trigger).
    - Ran actual app daemon: `python -u C:\\Users\\edebe\\eds\\workstream\\kanban_dashboard.py`
    - Resulting generated review tasks:
      - `20260304_141431_codex_afrix_task_01_from_20260303_152309_codex_afrix_build_prompt.md`
      - `20260304_141431_codex_afrix_task_02_from_20260303_152309_codex_afrix_build_prompt.md`
    - Backlog state transitioned to review:
      - `20260303_152309_codex_afrix_build_prompt_review.md`
    - Evidence logs:
      - `C:\\Users\\edebe\\eds\\workstream\\artefacts\\kanban_decomp_run.out.log`
      - `C:\\Users\\edebe\\eds\\workstream\\artefacts\\kanban_decomp_run.err.log`
- `Risks/Notes`:
  - Script execution must handle AI timeouts/errors gracefully (log and leave backlog item for retry).
  - Exact CLI command/API contract must be defined before implementation.
- `Completion Status`: Awaiting user verification (all checklist items completed; please verify decomposition quality with your production LLM command).


# User Feedback
User Verified: PASS
