# TASK D3: Build Manual Override and Kill-Switch

**Workstream:** D - ORCHESTRATION & AUTONOMY
**Workstream Goal:** Make the system self-running with appropriate controls.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 4.3
**Depends On:** 4.1
**Blocks:** 4.4
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing

## Purpose

Enable human control over autonomous system with emergency stop capability.

## Input

- D1: Autonomous scheduler

## Output

- `ep_strategy_warehouse_marketing/solution/backend/src/services/killSwitchService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/routes/adminRoutes.py`
- `ep_strategy_warehouse_marketing/solution/frontend/src/pages/AdminPanel.tsx`
- `ep_strategy_warehouse_marketing/solution/frontend/src/components/KillSwitch.tsx`
- `ep_strategy_warehouse_marketing/solution/frontend/src/components/PlatformControls.tsx`

## Route

`/admin` (protected - requires auth)

## Components

1. **Global Kill Switch**
   - Big red button to stop all posting immediately
   - Confirmation dialog
   - Status indicator (active/paused)

2. **Platform-Specific Controls**
   - Pause/resume per platform
   - Status indicators per platform
   - Queue depth per platform

3. **Content Approval Queue**
   - Pending posts awaiting approval
   - Approve/reject buttons
   - Edit before posting

4. **Activity Log**
   - Recent actions taken
   - Manual interventions logged
   - Timestamp and actor

## Action

1. Implement global pause/resume control:
   - Immediately stop all posting
   - Hold queue but don't clear
   - Resume continues from queue
2. Implement per-platform pause control
3. Implement content approval queue:
   - Posts requiring human review
   - Approve/reject/edit workflow
4. Implement emergency stop (kill all pending):
   - Clear all queues
   - Stop all scheduled jobs
5. Log all manual interventions with timestamp and actor

## Verification

- [ ] Pause button stops all posting immediately
- [ ] Resume button continues from queue
- [ ] Kill switch clears pending queue
- [ ] All actions logged with timestamp and user
- [ ] Screenshot of admin panel captured

---

## Evidence

- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: false
- Evidence-Type: demo
  - Artifact: Admin panel walkthrough
  - Objective-Proved: Kill switch and controls work
  - Status: planned
- Evidence-Type: screenshot
  - Artifact: `ep_strategy_warehouse_marketing/verification/admin_panel_screenshot.png`
  - Objective-Proved: UI complete
  - Status: planned
- Evidence-Type: test_output
  - Artifact: Integration test for pause/resume
  - Objective-Proved: Control logic works
  - Status: planned

## Required Skills

- `skills/ui-delivery-viewability/SKILL.md` - Screenshot evidence

## Dependency

- Requires: D1 (autonomous scheduler)
- Blocks: D4 (weekly reports)

## Notes

_User-visible task - requires manual verification. Critical safety feature for autonomous operation._
