# Task: PipHunter APK - Device Testing Both Skins

## Task Summary
Install both APKs (Battle Mode + Signal Pro) on an Android device side-by-side. Verify each skin shows the correct tabs, theme, and features. Confirm they don't interfere with each other.

## Context
- APK 1: "PipHunter Battle" (com.piphunter.battle) — dark/gold, Battle tab
- APK 2: "PipHunter Pro" (com.piphunter.pro) — dark/blue, Pro tab
- Both connect to same API: `https://piphunter-api.onrender.com/api/v1`

## Sub-tasks
- [x] Transfer both APKs to Android device
- [x] Install "PipHunter Battle" APK
- [x] Install "PipHunter Pro" APK (both should install — different package names)
- [ ] Validate PipHunter Battle:
  - [ ] App name on home screen shows "PipHunter Battle"
  - [ ] Dashboard tab loads with market bias, stats, signals
  - [ ] Battle tab: dark/gold theme, strategy cards, VS layout, dominance meter
  - [ ] Battle tab: "BACK THE CHAMPION" CTA, auto-follow toggle
  - [ ] Signals tab: signal list with BUY/SELL filter
  - [ ] Signal detail: trade parameters, copy-to-clipboard, journal modal
  - [ ] NO "Pro" tab visible
- [ ] Validate PipHunter Pro:
  - [ ] App name on home screen shows "PipHunter Pro"
  - [ ] Dashboard tab loads with same data
  - [ ] Pro tab: blue/institutional theme, "Selected Model" card
  - [ ] Pro tab: bucket state indicator (Active Leader / Forming / Silent / Change)
  - [ ] Pro tab: alternative models list (expandable)
  - [ ] Pro tab: stability metrics section
  - [ ] Signals tab: same signal list
  - [ ] Signal detail: same copy-trade functionality
  - [ ] NO "Battle" tab visible
- [x] Verify both apps can be open simultaneously
- [ ] Test pull-to-refresh on each screen in both apps
- [ ] Verify no crashes or white screens in either app

## Verification Test
1. Both APKs install on same device without conflict
2. "PipHunter Battle" shows ONLY Battle-specific tabs/theme
3. "PipHunter Pro" shows ONLY Pro-specific tabs/theme
4. Both apps fetch data from same API successfully
5. Copy-to-clipboard works in both apps
6. No crashes across 5 min of usage per app

## Risks/Notes
- API may need to wake from Render sleep on first load
- If no bucket data available, both skins show their empty/no-leader states
- Both APKs share keystore if built under same EAS project

## Implementation Log
- 2026-02-24 10:04: Refreshed lifecycle context from backlog/in-progress/completed PipHunter docs.
- 2026-02-24 10:05: Confirmed APK artifacts exist:
  - `TradeApps/breakout/piphunter/app/builds/piphunter-battle.apk`
  - `TradeApps/breakout/piphunter/app/builds/piphunter-pro.apk`
- 2026-02-24 10:06: Enabled direct ADB usage via SDK binary: `C:\Users\edebe\Android\Sdk\platform-tools\adb.exe`.
- 2026-02-24 10:06: Checked connected devices with ADB: none attached (`List of devices attached` only).
- 2026-02-24 10:07: Verified APK metadata with `aapt dump badging`:
  - Battle APK package: `com.piphunter.battle`, label: `PipHunter Battle`
  - Pro APK package: `com.piphunter.pro`, label: `PipHunter Pro`

## Current Status
- In progress and ready for live device validation.
- Blocked only on physical device attachment/availability.
- Once a device is connected, run install + behavior checks to complete remaining checklist items.

## Validation
- 2026-02-24 10:17: `adb devices -l` shows authorized device: `R5CR80SE9VM` (`SM_F711B`).
- 2026-02-24 10:17: Installed Battle APK:
  - `adb -s R5CR80SE9VM install -r TradeApps/breakout/piphunter/app/builds/piphunter-battle.apk`
  - Result: `Success`
- 2026-02-24 10:17: Installed Pro APK:
  - `adb -s R5CR80SE9VM install -r TradeApps/breakout/piphunter/app/builds/piphunter-pro.apk`
  - Result: `Success`
- 2026-02-24 10:18: Verified package coexistence:
  - `adb -s R5CR80SE9VM shell pm list packages | findstr com.piphunter`
  - Found both: `com.piphunter.battle`, `com.piphunter.pro`
- 2026-02-24 10:18: Launched both apps via launcher intent:
  - `adb -s R5CR80SE9VM shell monkey -p com.piphunter.battle -c android.intent.category.LAUNCHER 1`
  - `adb -s R5CR80SE9VM shell monkey -p com.piphunter.pro -c android.intent.category.LAUNCHER 1`
  - Result: `Events injected: 1` for each app
- 2026-02-24 10:18: Verified both processes alive simultaneously:
  - `adb -s R5CR80SE9VM shell pidof com.piphunter.battle` -> `10476`
  - `adb -s R5CR80SE9VM shell pidof com.piphunter.pro` -> `10592`

## Remaining Manual Checks
- Visual/tab assertions still require on-device UI walkthrough:
  - Battle tab/theme details and explicit absence of Pro tab
  - Pro tab/theme details and explicit absence of Battle tab
  - Pull-to-refresh, signal-detail copy, and 5-minute stability pass

## User Confirmation
- 2026-02-24 10:21: User confirmed both apps run simultaneously on device without issues.
- 2026-02-24 10:23: Manual validation outcomes from user:
  - Battle skin present: **FAIL** ("no battle skin")
  - Pro skin differentiation/changed UI: **FAIL** ("no change")
  - Pull-to-refresh: PASS
  - Signal-detail copy-to-clipboard: PASS (at time of test)
  - Crash/white-screen over runtime check: PASS (no crashes)

## Completion Status
Completed (testing cycle executed) with failed acceptance criteria for skin/tab differentiation.
Timestamp: 2026-02-24 10:23

## Completion Date
(To be filled on completion)
