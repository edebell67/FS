Source: User request in Codex chat on 2026-05-13 to add auto refresh to `/lead_lag_snapshots.html`.

Task Type: new_feature

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary: Add automatic page refresh to `/lead_lag_snapshots.html` so the snapshot view updates every 5 seconds, with a user-facing toggle to enable or disable the refresh behavior.

Repro URL:
- `/lead_lag_snapshots.html`

Context:
- `TradeApps/breakout/fs/lead_lag_snapshots.html`
- any shared page bootstrap or data-fetch path used by the lead/lag snapshot view

Destination Folder: TradeApps/breakout/fs/

Dependency: None

Plan:
- [ ] 1. Inspect the current lead/lag snapshot load path and identify the safest place to add a 5-second auto-refresh plus an on/off toggle.
  - Test: Confirm whether the page already has any timer-based refresh or shared polling behavior and where a toggle can be wired into the existing UI.
  - Evidence: Notes on the page bootstrap flow, refresh entry point, and control location.
- [ ] 2. Implement the auto-refresh behavior with a toggle that can enable or disable it without breaking manual interactions or in-flight requests.
  - Test: Add a refresh loop that reloads or rehydrates the page every 5 seconds when enabled, and stops cleanly when disabled.
  - Evidence: Code diff summary and file references recorded in Changes Made.
- [ ] 3. Validate that the page continues to render correctly after repeated refresh cycles and that the toggle behaves correctly.
  - Test: Open `/lead_lag_snapshots.html`, switch auto-refresh on/off, wait across multiple 5-second intervals, and confirm data still loads and UI remains stable.
  - Evidence: Validation notes, command output, and user-visible verification.

Evidence:
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: planned
  - Objective-Proved: The auto-refresh change required for the lead/lag snapshot page was implemented.
  - Status: planned
- Evidence-Type: manual_verification
  - Artifact: planned
  - Objective-Proved: The page continues to refresh cleanly every 5 seconds.
  - Status: planned

Implementation Log:
- 2026-05-13 13:49:04: Task created in backlog for adding 5-second auto-refresh to `/lead_lag_snapshots.html`.

Changes Made:
- None yet.

Validation:
- Not run yet.

Risks/Notes:
- A page-wide auto refresh can interfere with active interactions if it is implemented as a hard reload, so the refresh strategy should minimize disruption.
- The toggle should have a clear default state so users can tell whether auto-refresh is currently active.
- If the page already performs expensive fetches, the refresh loop may need to reuse cached data or throttle requests to avoid making the slowdown worse.

Completion Status:
- Backlog created on 2026-05-13 13:49:04.
