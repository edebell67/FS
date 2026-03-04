# Task Lifecycle: BreakoutBug list/get global loop error

## Metadata
- task_id: `20260226_144222_breakoutbug_fix_global_loop_list_get_error`
- project: `breakoutbug`
- created_at: `2026-02-26 14:42:22`
- status: `cancelled`
- owner: `codex`

## Objective
Fix recurring runtime error in the global loop:
- `Global Loop Error: 'list' object has no attribute 'get'`

## Context
Observed in runtime logs around live cycle processing and workflow ticks, while APIs continue returning HTTP 200 responses. Activations load successfully, but the global loop repeatedly throws a data-shape mismatch (list used where dict is expected).

## Scope
- Identify the exact global-loop code path where `.get(...)` is called on a list.
- Apply a safe fix that handles expected payload shapes without hiding invalid state.
- Verify no regression for workflow tick execution and live/sim loop paths.

## Implementation Plan
1. Trace global loop execution path and capture offending variable/type at failure point.
2. Patch parsing/normalization logic so dict/list shapes are handled explicitly.
3. Add or update targeted test coverage for the failing shape.
4. Run validation commands and record results.

## Validation Commands
- `python -m pytest tests -k "global loop or workflow or breakout"`
- `python algo_viewer/start.py --sim`
- `python app.py`

## Chronological Updates
- `2026-02-26 14:42:22` Created lifecycle file in `workstream/100_todo` for BreakoutBug fix request.
- `2026-02-26 22:50:50` User confirmed issue appears temporary; task cancelled without code changes and prepared for archive in `workstream/300_complete`.

## Result
Cancelled by user request (temporary issue). No implementation or validation executed.
