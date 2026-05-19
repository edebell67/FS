# Task: PipHunter APK - Verify Side-by-Side Device Installation

## Task Summary
Install both rebuilt APKs on the same Android device and verify they coexist as separate apps with distinct identities, themes, and tab sets.

## Context
- APK 1: "PipHunter Battle" (com.piphunter.battle) — dark/gold, Battle tab
- APK 2: "PipHunter Pro" (com.piphunter.pro) — dark/blue, Pro tab
- Both share same API backend

## Sub-tasks
- [ ] Transfer both APKs to device
- [ ] Install "PipHunter Battle" — verify app name on home screen
- [ ] Install "PipHunter Pro" — verify it does NOT overwrite Battle
- [ ] Confirm TWO separate app icons on home screen
- [ ] Open Battle: verify gold theme, Battle tab visible, no Pro tab
- [ ] Open Pro: verify blue theme, Pro tab visible, no Battle tab
- [ ] Verify both apps can be open simultaneously
- [ ] Verify both apps load data from the same API

## Verification Test
1. TWO separate app icons on Android home screen
2. Both apps open independently
3. Each app shows correct skin theme and tabs
4. Uninstalling one does not affect the other

## Completion Date
(To be filled on completion)

## Implementation Log
- 2026-02-24 10:24: Moved from `workstream/100_todo` to `workstream/200_inprogress` as next active PipHunter task.
- 2026-02-24 10:24: Imported latest validation context from prior completed task (`20260223_021100_piphunter_apk_device_testing.md`):
  - Both APKs install and run simultaneously ✅
  - Battle skin differentiation: FAIL
  - Pro skin differentiation/no-change issue: FAIL
  - Pull-to-refresh: PASS
  - Copy-to-clipboard: PASS
  - Runtime stability/no crashes: PASS

## Current Focus
- Diagnose and fix skin differentiation issue so Battle and Pro render distinct UI/tabs as designed.

## Changes Made
- 2026-02-24 10:38: Fixed app entrypoint to use Expo Router route tree instead of legacy `App.tsx`.
  - Updated `TradeApps/breakout/piphunter/app/index.js`:
    - from React Native `AppRegistry` registration of `./App`
    - to `import 'expo-router/entry';`
- 2026-02-24 10:39: Wrapped router root with `SkinProvider` so skin-aware tabs/screens read the build skin consistently.
  - Updated `TradeApps/breakout/piphunter/app/app/_layout.tsx`:
    - Added `SkinProvider` and `BUILD_CONFIG` import
    - Wrapped `<Stack />` with `<SkinProvider defaultSkin={BUILD_CONFIG.APP_SKIN}>`

## Validation
- `npm run -s lint` -> failed (`eslint` command not available in environment).
- `npx tsc --noEmit` -> reports pre-existing type issues centered in legacy `App.tsx` and one router path typing warning in `app/(tabs)/profile.tsx`.
- Impact note: this skin fix bypasses legacy `App.tsx` at runtime by switching entry to Expo Router, which is where the skin-aware tabs/screens live.

## Next Step
- Rebuild both APK variants (Battle + Pro), reinstall on device, and re-run manual skin/tab differentiation checks.

## Implementation Log
- 2026-02-24 11:06: Followed `skills/local-apk-build/SKILL.md` flow to rebuild both variants after entrypoint fix.
- 2026-02-24 11:07: Battle prebuild completed (`APP_SKIN=battle`), release signing set to `builds/piphunter-battle.jks`.
- 2026-02-24 11:14: Battle Gradle build succeeded (`BUILD SUCCESSFUL`, `assembleRelease`), artifact refreshed:
  - `TradeApps/breakout/piphunter/app/builds/piphunter-battle.apk` (updated size ~69.05 MB)
- 2026-02-24 11:41: Signal Pro prebuild completed (`APP_SKIN=signalpro`), release signing set to `builds/piphunter-pro.jks`.
- 2026-02-24 11:49: Signal Pro Gradle build succeeded (`BUILD SUCCESSFUL`, `assembleRelease`), artifact refreshed:
  - `TradeApps/breakout/piphunter/app/builds/piphunter-pro.apk` (updated size ~69.05 MB)
- 2026-02-24 11:50: Verified rebuilt APK metadata via `aapt dump badging`:
  - Battle: package `com.piphunter.battle`, label `PipHunter Battle`
  - Pro: package `com.piphunter.pro`, label `PipHunter Pro`
- 2026-02-24 11:50: Attempted reinstall to device; ADB currently shows no attached devices.

## Validation
- `aapt` verification passed for both rebuilt APKs (package + app label match expected skins).
- Reinstall blocked pending device reconnection:
  - `adb devices -l` -> no connected devices
  - install commands return `device not found`

## Current Blocker
- Awaiting Android device reconnection/authorization to install rebuilt APKs and run the final manual UI differentiation check.

## Implementation Log
- 2026-02-24 12:02: Wireless ADB pairing completed:
  - `adb pair 192.168.1.115:34471 396670` -> success
- 2026-02-24 12:04: Wireless device connected after server refresh:
  - `adb connect 192.168.1.115:39271`
  - `adb devices -l` -> `192.168.1.115:39271 device model:SM_F711B`
- 2026-02-24 12:05: Reinstalled rebuilt APKs over wireless ADB (install wrapper timed out, but post-checks confirm installed/runnable):
  - `com.piphunter.battle` present
  - `com.piphunter.pro` present
- 2026-02-24 12:06: Launched both apps successfully via launcher intents:
  - `monkey -p com.piphunter.battle ...` -> `Events injected: 1`
  - `monkey -p com.piphunter.pro ...` -> `Events injected: 1`

## Validation
- Wireless ADB connection established and stable.
- Both package IDs present on device and both apps launch.
- Pending: manual UI confirmation that Battle/Pro skins are now visually differentiated with correct tab visibility.

## User Test Result
- 2026-02-24 12:09: User confirmed:
  - Battle skin: PASS
  - Pro skin differentiation: FAIL (Pro appears same as Battle)

## Follow-up Fix
- 2026-02-24 12:10: Updated runtime skin resolution in `contexts/SkinProvider.tsx` to avoid defaulting to Battle when `Constants.expoConfig.extra.appSkin` is unavailable in production.
  - Added fallback resolution from installed package ID via `expo-application`:
    - `com.piphunter.pro` -> `signalpro`
    - `com.piphunter.battle` -> `battle`

## Implementation Log
- 2026-02-24 12:12: Rebuilt Signal Pro variant after skin-resolution fallback fix:
  - `APP_SKIN=signalpro` prebuild completed
  - Release build completed (`BUILD SUCCESSFUL`)
- 2026-02-24 12:16: Refreshed `builds/piphunter-pro.apk` and verified:
  - package `com.piphunter.pro`
  - label `PipHunter Pro`
- 2026-02-24 12:16: Installed updated Pro APK over wireless ADB (`192.168.1.115:39271`) and launched successfully via `monkey`.

## Validation
- Technical deployment checks pass for updated Pro build.
- Pending final manual UI check: Pro skin must now display blue/institutional theme and no Battle tab.

## Final User Confirmation
- 2026-02-24 13:02: User confirmed Pro skin now comes through correctly.
- 2026-02-24 13:03: User confirmed skin issue resolved.

## Completion Status
Complete - skin differentiation issue resolved on device (Battle and Pro render correctly as separate skins).
Timestamp: 2026-02-24 13:03
