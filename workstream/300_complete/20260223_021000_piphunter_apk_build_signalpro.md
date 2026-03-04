# Task: PipHunter APK - Build Signal Pro APK (Skin B)

## Task Summary
Execute the EAS cloud build for the Signal Pro skin — producing a standalone `.apk` with the professional blue/institutional theme, Pro tab, and Selected Model ranking UI.

## Context
- Skill ref: `skills/mobile-app-apk-creation/06-build-apk.md`
- App dir: `TradeApps/breakout/piphunter/app/`
- Build profile: `preview-signalpro`
- Output: APK named "PipHunter Pro", package `com.piphunter.pro`
- Prerequisite: Tasks 1-3 must be complete

## Sub-tasks
- [ ] Navigate to app dir: `cd TradeApps/breakout/piphunter/app`
- [ ] Trigger Pro build: `eas build --platform android --profile preview-signalpro`
- [ ] Monitor build progress (terminal or expo.dev)
- [ ] Wait for build completion (10-20 min)
- [ ] Download Pro APK from build output URL
- [ ] Save APK: `TradeApps/breakout/piphunter/builds/piphunter-pro.apk`

## Verification Test
1. `eas build` starts without errors on `preview-signalpro` profile
2. Build status reaches "Finished" on expo.dev
3. APK downloads successfully
4. APK installs as "PipHunter Pro" on device
5. App shows Pro tab (not Battle tab)

## Risks/Notes
- Can run this build while Battle build is still in progress (separate profile)
- Different package name allows both APKs to be installed side-by-side on same device
- Uses same EAS project but different slug if needed

## Completion Date
(To be filled on completion)
