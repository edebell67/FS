# Task: PipHunter APK - Skin-Specific Build Variants

## Task Summary
Configure EAS build to produce two separate APKs — "PipHunter Battle" (com.piphunter.battle) and "PipHunter Pro" (com.piphunter.pro) — using the same codebase with skin-conditional tab rendering.

## Context
- Skill ref: `skills/mobile-app-apk-creation/06-build-apk.md`
- Architecture ref: `contexts/SkinProvider.tsx`
- Build profiles via `eas.json`, dynamic config via `app.config.js`

## Implementation Log
- 2026-02-23 02:13: Moved to 200_inprogress
- 2026-02-23 02:14: Updated `eas.json` — added `preview-battle` and `preview-signalpro` profiles with `APP_SKIN` env
- 2026-02-23 02:15: Created `app.config.js` — reads `APP_SKIN` from process.env, outputs skin-specific name/slug/package/splash
- 2026-02-23 02:16: Updated `SkinProvider.tsx` — `BUILD_CONFIG` now reads `appSkin` from `expo-constants` instead of hardcoding
- 2026-02-23 02:17: Rewrote `_layout.tsx` — uses `href: null` to hide tabs not belonging to current skin
- 2026-02-23 02:17: Tab bar colors now adapt to skin theme (gold for Battle, green for Pro)

## Changes Made
- `eas.json` — OVERWRITTEN: Added `preview-battle` (env APP_SKIN=battle) and `preview-signalpro` (env APP_SKIN=signalpro) profiles
- `app.config.js` — NEW FILE: Dynamic Expo config reads APP_SKIN → outputs name/slug/package per skin
- `contexts/SkinProvider.tsx` — Updated: Added `expo-constants` import, `BUILD_CONFIG` reads from `Constants.expoConfig.extra.appSkin`
- `app/(tabs)/_layout.tsx` — OVERWRITTEN: Tabs conditionally hidden with `href: null`, colors from skin theme

## Validation
- `eas.json` has 4 profiles (preview-battle, preview-signalpro, preview, production)
- `app.config.js` produces correct names: "PipHunter Battle" vs "PipHunter Pro"
- `_layout.tsx` uses `href: skin === 'battle' ? undefined : null` to hide/show tabs
- Different package names allow both APKs on same device

## Risks/Notes
- `app.json` still exists alongside `app.config.js` — Expo uses the dynamic config when both present
- `expo-constants` must already be installed (it's part of Expo SDK)
- EAS may need two separate project registrations if slugs differ

## Completion Status
Complete — 2026-02-23 02:18 UTC

## Sub-tasks
- [x] Update `eas.json` — two preview profiles with APP_SKIN env
- [x] Create `app.config.js` — dynamic config for skin-specific identity
- [x] Battle: name="PipHunter Battle", slug="piphunter-battle", package="com.piphunter.battle"
- [x] Signal Pro: name="PipHunter Pro", slug="piphunter-pro", package="com.piphunter.pro"
- [x] Skin-appropriate splash bg color (Battle #0D0D0D, Pro #111827)
- [x] Update `_layout.tsx` — conditionally show/hide tabs via `href: null`
- [x] Update `SkinProvider.tsx` — read from expo-constants not hardcoded
- [x] Tab bar styling adapts to skin theme colors

## Verification Test
1. `eas.json` has `preview-battle` and `preview-signalpro` profiles
2. `app.config.js` outputs different name/package per skin env
3. Battle build only shows Battle tab, no Pro tab
4. Signal Pro build only shows Pro tab, no Battle tab
5. Each skin uses its correct theme colors

## Risks/Notes
- Two separate EAS project IDs may be needed (one per slug) — or use same project with different profiles
- Package name must be unique per APK to install both on same device
- Assets (icon, splash) could be skin-specific in future but can share for now

## Completion Date
(To be filled on completion)
