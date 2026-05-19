# Review Single Slot Worker Refill Behavior

## Metadata
- Project: workstream
- Task: review_single_slot_worker_refill_behavior
- Started: 2026-03-22 00:05:00
- Status: complete

## Source
- User request in Codex thread on 2026-03-22 to review why Gemini ends up with most tasks in progress despite the single-slot refill change.

## Task Summary
Review the current kanban/controller implementation to determine whether the "load one task at a time and refill a free model with one item" behavior was implemented correctly, and identify the reasons Gemini still accumulates most active tasks.

## Context
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- `C:\Users\edebe\eds\workstream\run_agent.py`

## Dependency
Dependency: None

## Plan
- [x] 1. Inspect both active controller paths and the single-slot configuration.
  - Test: Locate the worker claim loops and concurrency gates in both `kanban_dashboard.py` and `run_agent.py`.
  - Evidence: Confirmed the active paths are `multi_model_lane_worker()` in `kanban_dashboard.py` and `TaskGate`/`AgentController` in `run_agent.py`, with concurrency constants set to `1`.
- [x] 2. Verify whether the implementation matches the intended behavior.
  - Test: Compare actual claim/retry/fill logic to the requested "refill any free model with one item" behavior.
  - Evidence: Documented mismatches: duplicated schedulers, no fair free-model dispatcher, and retry pinning that biases tasks into model-specific lanes.
- [x] 3. Summarize findings and risks for the user.
  - Test: Produce a concise review with root cause and likely fix direction.
  - Evidence: Findings and likely fix direction recorded below.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: review
  - Artifact: `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Objective-Proved: The dashboard still runs its own worker threads while also launching `run_agent.py`, so task claiming is not centralized.
  - Status: verified
- Evidence-Type: review
  - Artifact: `C:\Users\edebe\eds\workstream\run_agent.py`
  - Objective-Proved: The controller uses task preference sorting, not fair round-robin refill across free models.
  - Status: verified

## Findings
- [P1] Two schedulers are active at the same time. `kanban_dashboard.py` both launches `run_agent.py` and starts its own `multi_model_lane_worker()` threads, so task claiming is not centralized. Relevant refs: `kanban_dashboard.py:3807`, `kanban_dashboard.py:7568`, `kanban_dashboard.py:7577`.
- [P1] The dashboard worker path does not implement "refill any free model with one item" fairness. Each worker independently scans `100_backlog/general`, sorts the same ready list, and claims `ready_tasks[0]`. There is no shared round-robin or least-loaded assignment step. Relevant refs: `kanban_dashboard.py:7492`, `kanban_dashboard.py:7524`, `kanban_dashboard.py:7525`.
- [P1] Retry behavior still pins failed work into a specific next-agent lane, which can accumulate in Gemini regardless of the new slot limits. Relevant refs: `kanban_dashboard.py:362`, `kanban_dashboard.py:398`, `kanban_dashboard.py:404`, `kanban_dashboard.py:406`.
- [P2] The change to `MAX_CONCURRENT_INPROGRESS_TASKS = 1` in the dashboard path is a global in-progress cap, not "one task for each free model." That means it does not implement per-free-worker refill logic. Relevant refs: `kanban_dashboard.py:8`, `kanban_dashboard.py:7486`.
- [P2] `run_agent.py` prefers worker-matching tasks but still uses sorted preference selection rather than balanced distribution. A faster or more frequently polling worker can keep reclaiming suitable work when the slot frees. Relevant refs: `run_agent.py:391`, `run_agent.py:412`, `run_agent.py:435`, `run_agent.py:485`.

## Recommended Fix Direction
- Pick one orchestrator. Either use `run_agent.py` as the sole scheduler, or use the internal `multi_model_lane_worker()` path, but not both.
- Put all decomposition output and retries back into `100_backlog/general` unless there is an explicit user override.
- Replace per-worker polling of `general` with one shared dispatcher that assigns the next ready task to the least-loaded available worker.
- Define the intended concurrency explicitly:
  - global single task total, or
  - one task per free worker
  - The current code implements neither cleanly across the full system.

## Validation
- [x] Locate claim loops and concurrency gates.
- [x] Compare actual logic to requested behavior.
- [x] Record findings with file references.
