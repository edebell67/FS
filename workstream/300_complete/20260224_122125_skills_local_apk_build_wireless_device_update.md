# Task: Update local-apk-build Skill with Wireless Device Deployment

## Task Summary
Add reusable instructions to the local APK build skill for connecting Android devices wirelessly via ADB and deploying/retesting rebuilt APKs without USB.

## Context
- File: `skills/local-apk-build/SKILL.md`
- Purpose: allow other models/users to reuse a stable wireless deployment workflow.

## Implementation Log
- 2026-02-24 12:21:25: Task created in `workstream/100_todo`.
- 2026-02-24 12:22: Added wireless deployment workflow to `skills/local-apk-build/SKILL.md`.
- 2026-02-24 12:23: Added troubleshooting notes for rotating wireless connect ports and unstable ADB visibility.

## Changes Made
- Updated `skills/local-apk-build/SKILL.md`:
  - Added `Step 6 (Optional): Deploy to Device via Wireless ADB`
  - Added explicit pairing vs connect port guidance
  - Added install + verification commands for wireless target (`adb -s <ip:port> ...`)
  - Added troubleshooting section for intermittent wireless ADB state

## Validation
- `rg -n "Step 6 \\(Optional\\)|Wireless ADB|pairing port|connect port" skills\\local-apk-build\\SKILL.md`
  - Confirmed all new sections exist at expected headings/lines.

## Risks/Notes
- Wireless ADB ports vary by device/session; docs must distinguish pairing port vs connect port.

## Completion Status
Complete - 2026-02-24 12:23
