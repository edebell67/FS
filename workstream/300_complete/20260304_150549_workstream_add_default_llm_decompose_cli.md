# Workstream Task Lifecycle

- Task: Add default decomposition CLI at `workstream/llm_decompose_cli.py`
- Owner: codex
- Started: 2026-03-04 15:04:00
- Status: Completed

## Plan
- [x] Create `llm_decompose_cli.py` with `--agent` and `--input` interface expected by worker.  
Test: Running script with valid input returns JSON object containing `tasks` list.
- [x] Ensure generated payload matches worker validation schema (title/summary/steps/tests).  
Test: Output tasks include required fields and parse as valid JSON.
- [x] Run syntax and execution validation.  
Test: `python -m py_compile ...` passes and direct script execution succeeds for codex backlog input.

## Validation Log
- `python -m py_compile C:\Users\edebe\eds\workstream\llm_decompose_cli.py` passed.
- `python C:\Users\edebe\eds\workstream\llm_decompose_cli.py --agent codex --input C:\Users\edebe\eds\workstream\000_backlog\codex\20260303_152309_codex_afrix_build_prompt.md` returned valid JSON with 2 tasks.

## Files Changed
- `C:\Users\edebe\eds\workstream\llm_decompose_cli.py`
