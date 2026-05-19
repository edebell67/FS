Source: User request on 2026-04-01 to create a task for adding a light/dark mode switch to the website rebuild tracked in `20260401_030508_funcuts_full_site_rebuild_loop.md`.
Task Type: standard
Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false
- priority: high
- execution_owner: gemini
**Suggested Agent:** gemini
Task Summary: Implement a user-facing theme switch that allows the rebuilt Funcuts website to toggle between light and dark modes without losing visual quality, accessibility, or functional parity.

Source Task:
- `C:\Users\edebe\eds\workstream\100_backlog\gemini\20260401_030508_funcuts_full_site_rebuild_loop.md`

Context:
- Rebuild output location:
  - `C:\Users\edebe\eds\ep_009_site_rebuild_funcut`
- Parent objective:
  - Rebuild `https://www.funcuts.co.uk/` with no loss of functionality or critical assets.
- Theme-switch objective:
  - Add a polished, reliable light/dark mode control to the rebuilt site.
  - Preserve professional visual quality in both themes.
  - Ensure imagery, typography, buttons, forms, and navigation remain attractive and usable in both modes.

Dependency:
- `C:\Users\edebe\eds\workstream\100_backlog\gemini\20260401_030508_funcuts_full_site_rebuild_loop.md`

## Acceptance Criteria
- The rebuilt Funcuts site includes a visible and intuitive theme switch.
- Users can toggle between light and dark themes without breaking layout, readability, accessibility, or branding.
- Theme choice persists across page navigation and reloads.
- All key public pages in the rebuild support both themes consistently.
- The dark theme remains visually premium rather than a low-effort inversion.

## Plan
- [ ] 1. Inspect the rebuilt Funcuts site structure and identify the right global theme architecture.
  - [ ] Test: Document the theme-switch implementation approach and the files/components that will control global theming.
  - Evidence: Theme architecture notes recorded in this task file.
- [ ] 2. Implement the light/dark switch with consistent theme tokens/styles across the rebuild.
  - [ ] Test: The rebuilt site exposes a working toggle and both themes render correctly across the main public pages.
  - Evidence: File diff and affected files recorded in this task file.
- [ ] 3. Persist the user’s theme preference and verify cross-page consistency.
  - [ ] Test: Reloading the site preserves the selected theme and navigation between pages does not reset it.
  - Evidence: Validation notes and any persistence mechanism recorded in this task file.
- [ ] 4. Review both themes for visual polish and accessibility.
  - [ ] Test: A review pass confirms contrast, readability, navigation clarity, form usability, and overall presentation in both modes.
  - Evidence: Review findings and screenshots recorded in this task file.

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: pending
  - Objective-Proved: Proves the rebuilt site contains the theme-switch implementation files and logic.
  - Status: planned
- Evidence-Type: screenshot
  - Artifact: pending
  - Objective-Proved: Proves the site renders correctly in both light and dark modes.
  - Status: planned
- Evidence-Type: manual_verification
  - Artifact: pending
  - Objective-Proved: Proves the toggle works correctly across pages and reloads.
  - Status: planned
- Evidence-Type: user_feedback
  - Artifact: pending
  - Objective-Proved: Confirms the user accepts the quality and behavior of the theme switch.
  - Status: planned

## Implementation Log
- 2026-04-01 04:13:32 Europe/London: Task created in Gemini backlog for a light/dark mode switch in the Funcuts rebuild.

## Changes Made
- Task definition created and linked to the parent Funcuts rebuild task.

## Validation
- Pending implementation.

## Risks/Notes
- The theme switch should be implemented against the rebuilt Funcuts site, not the legacy live site.
- Both themes must preserve the premium design standard required by the parent rebuild task.

## Completion Status
- State: Backlog
- Timestamp: 2026-04-01 04:13:32 Europe/London
