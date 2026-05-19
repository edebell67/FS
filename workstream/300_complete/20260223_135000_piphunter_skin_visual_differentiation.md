# Task: PipHunter - Skin Visual Differentiation

## Task Summary
Wire the existing `useSkin()` hook into all screen components so Battle Mode renders with dark/gold gaming theme and Signal Pro renders with dark/blue institutional theme. Rebuild both APKs after.

## Context
- Both APKs install as separate apps ✅ (com.piphunter.battle / com.piphunter.pro)
- `SkinProvider.tsx` and `BUILD_CONFIG` correctly detect skin from build env ✅
- Problem: No screen component calls `useSkin()` — all use hardcoded colors
- Reference image provided for Battle Mode: dark/gold, glowing borders, "VS" badge, "CHAMPION" labels, "BACK THE CHAMPION" CTA

## Sub-tasks

### 1. Theme Integration — Shared Screens
- [ ] `app/(tabs)/index.tsx` (Dashboard): Replace hardcoded colors with `useSkin()` theme tokens
- [ ] `app/(tabs)/signals.tsx`: Apply skin-aware colors (primary, surface, text)
- [ ] `app/(tabs)/streaks.tsx`: Apply skin-aware colors
- [ ] `app/(tabs)/profile.tsx`: Apply skin-aware colors
- [ ] Tab bar already themed via `_layout.tsx` ✅

### 2. Battle Mode UI — `battle.tsx`
Inspired by reference image aesthetic (dark/gold, premium gaming energy, glowing effects):
- [ ] Dark background (#0D0D0D) with gold (#F59E0B) accents throughout
- [ ] Glowing card borders, subtle animated effects
- [ ] Competitive/gaming language: "Champion", "VS", "Battle", "Arena"
- [ ] Bold typography, high contrast
- [ ] Premium feel — not a basic list view
- [ ] Wire to real API data (signals, buckets) where available
- [ ] Fallback to mock/placeholder data for elements not yet served by API

### 3. Signal Pro UI — `signalpro.tsx`
Style with institutional professional look:
- [ ] Clean blue (#3B82F6) accent headers
- [ ] Ranked list with numbered positions
- [ ] Expandable sections for strategy details
- [ ] Stability metrics display
- [ ] Dark background (#111827), muted tones, no glow effects

### 4. Rebuild Both APKs
- [ ] `expo prebuild --clean` with APP_SKIN=battle → Gradle build → piphunter-battle.apk
- [ ] `expo prebuild --clean` with APP_SKIN=signalpro → Gradle build → piphunter-pro.apk
- [ ] Verify with `aapt dump badging` — correct names and packages
- [ ] Install on device — confirm visually distinct

## Verification Test
1. Battle APK: dark/gold theme, glowing effects, gaming language ("Champion", "VS", "Battle")
2. Pro APK: dark/blue theme, clean lines, professional language ("Selected Model", "Ranking")
3. Dashboard colors differ between the two apps
4. Both apps load data from the same API

## Risks/Notes
- Battle UI is the largest sub-task — many visual elements from reference
- Data binding to real API signals needed for Champion/Challenger cards
- Animations (glow, lightning) may need `react-native-reanimated`
- `expo prebuild --clean` wipes signing config — must re-apply per skill

## Completion Date
(To be filled on completion)
