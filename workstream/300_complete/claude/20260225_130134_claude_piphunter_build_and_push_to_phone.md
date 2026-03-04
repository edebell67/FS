# Task: PipHunter 2.0.2 Build and Push to Phone

## Status
TODO

## Source
- User request: "use skills to push to phone"
- Skill used: `skills/local-apk-build/SKILL.md`

## Task Summary
Build latest PipHunter APK locally and install/push it to connected phone for verification.

## Context
- App path: `TradeApps/breakout/piphunter/app`
- Target version: `2.0.2` from dynamic app config.

## Implementation Log
- INIT: Task created.
- 2026-02-25 13:01: Moved task to `workstream/200_inprogress`.
- 2026-02-25 13:02: Verified local prerequisites: Android SDK exists at `C:\Users\edebe\Android\Sdk`, JDK 17 exists at `C:\Program Files\Java\jdk-17`.
- 2026-02-25 13:03: Attempted `npx expo prebuild --platform android --clean` and `npx expo prebuild --platform android`; both fail with `spawn EPERM` while creating native `android/`.
- 2026-02-25 13:04: Attempted `adb devices -l` via `C:\Users\edebe\Android\Sdk\platform-tools\adb.exe`; fails due sandbox profile permission (`Cannot mkdir 'C:\Users\CodexSandboxOffline\.android': Permission denied`).
- 2026-02-25 13:12: User provided wireless target `192.168.1.115:33205`; direct `adb connect` + install attempted and failed with same sandbox profile permission error.
- 2026-02-25 13:12: Checked APK artifacts in `app/builds`; latest present file is `piphunter-battle.apk` (no `piphunter-2.0.2.apk` filename yet).
- 2026-02-25 13:46: Updated `TradeApps/breakout/piphunter/app/android/app/build.gradle` to `versionCode 3` and `versionName "2.0.2"` directly via shell.
- 2026-02-25 13:47: Attempted `gradlew.bat clean assembleRelease` with `JAVA_HOME` JDK17 and local `GRADLE_USER_HOME`; blocked by sandbox network restriction downloading Gradle wrapper (`gradle-8.3-all.zip`).

## Changes Made
- Updated app code prior to this task already targets fixed signal collapse behavior and app config version `2.0.2`.
- No APK produced in this task due environment restrictions.

## Validation
- Build command attempts:
  - `npx expo prebuild --platform android --clean`
  - `npx expo prebuild --platform android`
  - Result: failed with `spawn EPERM`.
- Install command attempt:
  - `adb devices -l`
  - Result: failed with profile permission error in sandbox.
- Direct user-target attempt:
  - `adb connect 192.168.1.115:33205`
  - `adb -s 192.168.1.115:33205 install -r ...`
  - Result: failed with same `Cannot mkdir 'C:\Users\CodexSandboxOffline\.android': Permission denied`.
- Direct rebuild attempt:
  - `.\gradlew.bat clean assembleRelease`
  - Result: `java.net.SocketException: Permission denied` while fetching `https://services.gradle.org/distributions/gradle-8.3-all.zip`.

## Risks/Notes
- Requires ADB connectivity to phone (USB or wireless).
- Current execution sandbox blocks both Expo native project generation and ADB profile creation, so phone push cannot be completed from this session.

## Completion Status
Awaiting user-side build/install execution path due sandbox restrictions.
