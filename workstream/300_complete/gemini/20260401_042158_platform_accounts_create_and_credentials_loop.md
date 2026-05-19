Source: User request on 2026-04-01 to create a looping task for setting up own accounts on Twitter/X, Reddit, Instagram, and YouTube, with orchestration allocated to Gemini.
Task Type: standard
Task Attributes:
- recurring_task: false
- looping_task: true
- loop_until: manual_stop
- loop_interval: on_feedback_cycle
- splittable_task: false
- workflow_task: false
- priority: high
- execution_owner: gemini
**Suggested Agent:** gemini
Task Summary: Orchestrate and complete the setup of owned platform accounts on Twitter/X, Reddit, Instagram, and YouTube, with credentials prepared for future platform communication workflows. Continue iterating until the user explicitly confirms all account setup requirements are complete.

Context:
- Target platforms:
  - Twitter/X
  - Reddit
  - Instagram
  - YouTube
- Orchestration model:
  - Codex acts as orchestrator only.
  - Gemini is the execution owner for completion.
- Credential handling requirement:
  - Credentials or tokens produced by this work must be stored securely.
  - Do not commit secrets or passwords to tracked repository files.
  - Use OS vault, environment variables, or ignored secure local storage.
- Intended use:
  - These credentials will be used to communicate with the platforms in later workflows.

Dependency: None

## Acceptance Criteria
- Each target platform has an owned account created or confirmed available for use.
- Required login credentials, recovery details, and any platform-specific access prerequisites are recorded in a secure non-repo location.
- The task records what was completed for each platform and what remains blocked, if anything.
- The task stays open as a loop until the user explicitly confirms all platform-account requirements are complete.

## Plan
- [ ] 1. Confirm the required account set and define the secure credential-handling approach.
  - [ ] Test: Record the platform checklist and the approved secure storage approach in this task file without storing actual secrets in the repo.
  - Evidence: Platform checklist and secure storage notes appended to this task file.
- [ ] 2. Create or verify ownership of the Twitter/X account and capture any required setup state.
  - [ ] Test: Record whether the account exists, whether login works, and whether credentials/recovery details have been secured outside the repo.
  - Evidence: Platform status notes recorded in this task file.
- [ ] 3. Create or verify ownership of the Reddit account and capture any required setup state.
  - [ ] Test: Record whether the account exists, whether login works, and whether credentials/recovery details have been secured outside the repo.
  - Evidence: Platform status notes recorded in this task file.
- [ ] 4. Create or verify ownership of the Instagram account and capture any required setup state.
  - [ ] Test: Record whether the account exists, whether login works, and whether credentials/recovery details have been secured outside the repo.
  - Evidence: Platform status notes recorded in this task file.
- [ ] 5. Create or verify ownership of the YouTube account and capture any required setup state.
  - [ ] Test: Record whether the account exists, whether login works, and whether credentials/recovery details have been secured outside the repo.
  - Evidence: Platform status notes recorded in this task file.
- [ ] 6. Present status to the user and continue looping until all required platforms are complete and explicitly accepted.
  - [ ] Test: User feedback is requested and recorded; if any platform remains blocked or incomplete, the task remains active.
  - Evidence: User feedback and remaining blocker list recorded in this task file.

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false
- Evidence-Type: manual_verification
  - Artifact: pending
  - Objective-Proved: Proves each platform account has been created or verified and is usable.
  - Status: planned
- Evidence-Type: user_feedback
  - Artifact: pending
  - Objective-Proved: Confirms the user has accepted the completed platform-account setup.
  - Status: planned
- Evidence-Type: not_applicable
  - Artifact: Credentials stored securely outside the repo
  - Objective-Proved: Confirms secrets are intentionally excluded from tracked repository files.
  - Status: planned

## Implementation Log
- 2026-04-01 04:21:58 Europe/London: Looping Gemini task created for owned account setup across Twitter/X, Reddit, Instagram, and YouTube.

## Changes Made
- Task definition created in Gemini backlog with looping behavior and secure credential-handling constraints.
- Task was incorrectly found in `300_complete` without captured evidence or user confirmation; it must remain active backlog work until executed and explicitly accepted.

## Validation
- Pending execution.
- No platform creation or verification evidence captured yet.
- No user confirmation captured yet.

## Risks/Notes
- This task must not place live credentials in tracked repository files.
- Platform sign-up, verification, and anti-abuse flows may require manual checkpoints or user input outside the repo.
- Do not mark complete until the user explicitly confirms all required platform setup work is done.
- This task must remain outside `300_complete` until actual per-platform evidence is recorded and the user explicitly confirms completion.

## Completion Status
- State: Backlog
- Timestamp: 2026-04-01 04:21:58 Europe/London
