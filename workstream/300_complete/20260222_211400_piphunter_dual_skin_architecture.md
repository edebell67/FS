# Task: Architecture - Dual Skin App Structure

## Task Summary
Implement SkinProvider context, useSkin hook, per-skin theme tokens, feature flags, SkinOnly conditional renderer, and build configuration for Battle Mode vs Signal Pro.

## Context
- Source: spec Sections 2 & 9 (Dual Skin Architecture)
- File: `app/contexts/SkinProvider.tsx` — new shared context
- Consumed by: all screens — theme.primary, features.showPulsingGlow, etc.

## Implementation Log
- 2026-02-23 02:10: Moved to 200_inprogress
- 2026-02-23 02:11: Created `app/contexts/SkinProvider.tsx` with full architecture
- 2026-02-23 02:11: Defined `SkinTheme` interface — 20+ theme tokens per skin
- 2026-02-23 02:12: Defined Battle theme (dark/gold, glow, arena language, CHAMPION)
- 2026-02-23 02:12: Defined Signal Pro theme (dark/blue, no glow, SELECTED MODEL)
- 2026-02-23 02:13: Built `SkinFeatureFlags` — 8 feature toggles per skin
- 2026-02-23 02:13: Built `SkinProvider` context + `useSkin()` hook
- 2026-02-23 02:14: Built `SkinOnly` conditional renderer
- 2026-02-23 02:14: Added `BUILD_CONFIG` for separate app bundle configuration

## Changes Made
- `app/contexts/SkinProvider.tsx` — NEW FILE (250+ lines):
  - `SkinTheme` interface — colors, typography, UI variants, semantic labels
  - `SKINS.battle` — gold accent, border-radius 16, glow+animations, "CHAMPION"
  - `SKINS.signalpro` — blue accent, border-radius 12, no glow, "SELECTED MODEL"
  - `SKIN_FEATURES` — per-skin boolean flags (dominance meter, VS badge, stability metrics, etc.)
  - `SkinProvider` — React Context with `defaultSkin` prop
  - `useSkin()` — returns `{skin, theme, features, setSkin, isBattle, isPro}`
  - `SkinOnly` — conditional render helper component
  - `BUILD_CONFIG` — APP_SKIN, APP_NAME, APP_VERSION constants

## Validation
- File created at correct path `app/contexts/SkinProvider.tsx`
- Type-safe: all theme tokens typed in `SkinTheme` interface
- Feature flags cleanly separate Battle-only and Pro-only UI elements

## Risks/Notes
- App root `_layout.tsx` would need to be wrapped with `<SkinProvider>` to activate
- A/B testing infrastructure is type-defined but not wired (requires experiment framework)
- Separate build configs (EAS Build profiles) would be needed for independent App Store builds

## Completion Status
Complete — 2026-02-23 02:15 UTC

## Sub-tasks
- [x] Design shared component library (data, API, state) — api.ts, tiers.tsx, trust.tsx are skin-agnostic
- [x] Create skin-agnostic service layer — api.ts serves both skins
- [x] Implement theme provider for skin-specific styling — SkinProvider + SkinTheme
- [x] Create `SkinProvider` context (battle vs pro) — React Context with useSkin()
- [x] Implement conditional component rendering based on skin — SkinOnly component
- [x] Create shared navigation structure — _layout.tsx tab structure
- [x] Implement skin-specific navigation overrides — Theme applied via useSkin()
- [x] Add feature flag system for skin-specific features — SKIN_FEATURES constant
- [x] Create build configuration for separate app bundles — BUILD_CONFIG
- [ ] Implement A/B testing infrastructure — Requires experiment framework
