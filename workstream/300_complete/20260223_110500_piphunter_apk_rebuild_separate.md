# Task: PipHunter APK - Rebuild Both Skins with Separate Packages

## Task Summary
Rebuild both APKs using new local keystores and distinct package names (com.piphunter.battle, com.piphunter.pro).

## Context
- Local credentials configured: `credentials.json` + `credentialsSource: "local"` in eas.json ✅
- Package names: `com.piphunter.battle` / `com.piphunter.pro` ✅

## Implementation Log
- 2026-02-23 11:07: Moved to 200_inprogress
- 2026-02-23 11:08: Battle build attempted — `✔ Using local Android credentials (credentials.json)` ✅
- 2026-02-23 11:08: Upload succeeded but **FREE TIER BUILD QUOTA EXHAUSTED**: "This account has used its Android builds from the Free plan this month"
- 2026-02-23 11:09: Quota resets **Sun Mar 01 2026** (5 days)
- 2026-02-23 11:09: Attempted `--local` build — "Unsupported platform, macOS or Linux is required"

## ⚠️ BLOCKED — Free Tier Quota Exhausted

### Resolution Options:
1. **Wait 5 days** — free tier resets **March 1st 2026**. Then run:
   ```
   cd C:\Users\edebe\eds\TradeApps\breakout\piphunter\app
   npx eas-cli build --platform android --profile preview-battle --non-interactive
   npx eas-cli build --platform android --profile preview-signalpro --non-interactive
   ```
   (Swap `credentials.json` keystore path between builds — see note below)

2. **Upgrade plan** — https://expo.dev/accounts/edebell67/settings/billing

3. **Local build on Linux/Mac** — `--local` requires macOS or Linux, not Windows

### Note: Swapping credentials.json for Pro build
Before running the Pro build, update `credentials.json`:
```json
{
  "android": {
    "keystore": {
      "keystorePath": "./builds/piphunter-pro.jks",
      "keystorePassword": "piphunter2026",
      "keyAlias": "piphunter-pro",
      "keyPassword": "piphunter2026"
    }
  }
}
```

## Completion Status
✅ COMPLETE — Built locally via Gradle on Windows.

## Implementation Details
- Package names: `com.piphunter.battle` and `com.piphunter.pro` confirmed via `app.config.js`.
- Signing: Used separate JKS files in `builds/` directory.
- Environment: JDK 17 + Android SDK local build.
- Result: 
  - `builds/piphunter-battle.apk`
  - `builds/piphunter-pro.apk`

## Sub-tasks
- [x] Trigger Battle build with local credentials ✅
- [x] Battle build completes — Bypassed EAS via local Gradle ✅
- [x] Swap environment for Pro build (Signal Pro) ✅
- [x] Trigger Pro build ✅
- [x] Download/Verify both APKs ✅

## Verification Test
- [x] Two separate APK files generated with different package identifiers. ✅

## Completion Date
2026-02-23 16:20

## Completion Date
(To be filled on completion)
