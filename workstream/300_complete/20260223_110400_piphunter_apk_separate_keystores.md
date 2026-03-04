# Task: PipHunter APK - Generate Keystores for Separate Packages

## Task Summary
Generate Android keystores locally for `com.piphunter.battle` and `com.piphunter.pro`, then configure `credentials.json` so EAS uses them without interactive prompts. This enables both APKs to install side-by-side on the same device.

## Context
- Problem: Both skins used `com.piphunter.app` → Android overwrites one with the other
- Fix: Each skin needs its own unique Android package name + matching keystore
- Tool: Java `keytool` to generate `.jks` keystores locally
- Config: `credentials.json` tells EAS which keystore to use per profile

## Completion Status
Complete — 2026-02-23 11:06 UTC

## Sub-tasks
- [x] Create `builds/` directory for keystores
- [x] Generate keystore for Battle: `piphunter-battle.jks` (alias: piphunter-battle)
- [x] Generate keystore for Pro: `piphunter-pro.jks` (alias: piphunter-pro)
- [x] Create `credentials.json` mapping keystore path/password/alias
- [x] Update `app.config.js` — `com.piphunter.battle` and `com.piphunter.pro`
- [x] Update `eas.json` — `credentialsSource: "local"` on both skin profiles
- [x] Add `credentials.json`, `builds/*.jks`, `builds/*.apk` to `.gitignore`

## Verification Test
1. Both `.jks` files exist in `builds/`
2. `credentials.json` references correct keystore per profile
3. `app.config.js` outputs `com.piphunter.battle` for battle, `com.piphunter.pro` for pro

## Risks/Notes
- Keystores are signing keys — BACK THEM UP
- `credentials.json` contains passwords — never commit to git
- Keystore alias and passwords must match what's in `credentials.json`

## Completion Date
(To be filled on completion)
