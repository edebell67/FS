# Task: Tier System - Feature Gating Infrastructure

## Task Summary
Implement the three-axis tier system (Bucket Visibility, Data Depth, Control) with Core/Advanced/Portfolio tiers, TierGate component, TierProvider context, and upgrade prompts.

## Context
- Source: spec Sections 6 & 7 (Pricing Axes, Tier Structure)
- File: `app/services/tiers.tsx` — new shared service/component
- Wrappable: any screen component can use `<TierGate>` or `useTier()` hook

## Implementation Log
- 2026-02-23 01:56: Moved to 200_inprogress
- 2026-02-23 01:57: Created `app/services/tiers.tsx` with full tier infrastructure
- 2026-02-23 01:57: Defined 3 tiers with complete config per axis
- 2026-02-23 01:58: Built TierProvider (React Context) with hasFeature() and canAccessBuckets()
- 2026-02-23 01:58: Built TierGate component with locked card + upgrade modal
- 2026-02-23 01:59: Built tier comparison UI inside upgrade modal (side-by-side columns)

## Changes Made
- `app/services/tiers.tsx` — NEW FILE (250+ lines):
  - `TierConfig` interface — all 3 axes defined as boolean/number fields
  - `TIERS` constant — Core (1 bucket, intraday, manual), Advanced (5 buckets, rolling+alerts, limited auto), Portfolio (all, full history+duration, full auto)
  - `TierProvider` — React Context wrapping app, provides `useTier()` hook
  - `useTier()` — returns `{currentTier, config, hasFeature, canAccessBuckets, setTier}`
  - `TierGate` — renders children if permitted, otherwise shows locked card + upgrade modal
  - Upgrade modal shows 3-column tier comparison + "Upgrade Now" CTA

## Validation
- File created at correct path
- Type-safe: `FeatureKey` type derives from `TierConfig` interface
- `TierGate` correctly compares tier order when `requiredTier` is specified

## Risks/Notes
- `user_tiers` Supabase table not created (backend task)
- Payment flow / in-app purchases not wired (requires Stripe/RevenueCat)
- Currently defaults to 'core' tier — production would load from API

## Completion Status
Complete — 2026-02-23 02:00 UTC

## Sub-tasks
- [x] Design tier data model (Core, Advanced, Portfolio) — `TIERS` constant
- [ ] Create `user_tiers` table in Supabase — Backend task
- [x] Implement Axis 1 - Bucket Visibility — maxBuckets: 1/5/-1
- [x] Implement Axis 2 - Data Depth — intradayData/rollingData/historicalData/leaderDurationMetrics
- [x] Implement Axis 3 - Control — manualMode/limitedAutomation/fullAutomation/allocationControls
- [x] Create `TierGate` component for UI gating — Locked card + upgrade modal
- [x] Implement upgrade prompts for locked features — Modal with CTA
- [x] Add tier status to user profile — useTier() hook
- [x] Create tier comparison screen — Side-by-side columns in modal
