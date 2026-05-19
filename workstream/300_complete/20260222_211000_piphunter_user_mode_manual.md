# Task: User Mode - Manual Trading Interface

## Task Summary
Implement the Manual Mode interface: signal detail view with trade parameters, one-tap copy-to-clipboard, lot size presets, confidence indicator, and trade journal prompt.

## Context
- Source: spec Section 5.1 (Manual Mode)
- File: `app/app/signal/[id].tsx` — replaced placeholder with full implementation
- Dependencies: `expo-clipboard` for copy functionality

## Implementation Log
- 2026-02-23 01:44: Moved to 200_inprogress
- 2026-02-23 01:45: Rebuilt `signal/[id].tsx` from placeholder to full manual trading screen
- 2026-02-23 01:46: Built `ConfidenceRing` component — circular ring with HIGH/MEDIUM/LOW labels
- 2026-02-23 01:46: Built trade parameters card — Entry, TP, SL, Strategy, P&L rows
- 2026-02-23 01:47: Built lot size selector — 0.01, 0.05, 0.1, 0.5, 1.0 quick presets
- 2026-02-23 01:47: Built copy-to-clipboard — formats all params, uses expo-clipboard
- 2026-02-23 01:48: Built trade journal modal — slide-up sheet after copy with text input + save

## Changes Made
- `app/app/signal/[id].tsx` — OVERWRITTEN (250+ lines). Full signal detail screen with:
  - `ConfidenceRing` — color-coded ring (green/amber/red by confidence %)
  - Trade parameters card — entry_price, target_price, stop_loss, strategy, net_pnl
  - Lot size selector — 5 presets with active state
  - "COPY TRADE PARAMETERS" button — copies formatted text to clipboard, shows ✓ feedback
  - Trade journal modal — bottom sheet with reasoning text input, skip/save
  - Loading and error states with navigation

## Validation
- File created successfully, overwrites the placeholder
- Uses `expo-clipboard` for clipboard (standard Expo SDK)
- Signal loaded via `api.getSignal(id)` from services/api.ts

## Risks/Notes
- `expo-clipboard` must be installed in the project (`npx expo install expo-clipboard`)
- Deep link to broker app not implemented (would require broker-specific URL schemes)
- Signal notifications require push notification setup (separate task)

## Completion Status
Complete — 2026-02-23 01:49 UTC

## Sub-tasks
- [x] Create `SignalView` component (current recommended signal) — Full detail screen
- [x] Display signal details: direction, entry, target, stop loss — Trade parameters card
- [x] Implement `CopyTradeButton` with one-tap copy — Clipboard + success feedback
- [x] Add clipboard copy for trade parameters — Formatted multi-line string
- [ ] Create deep link to broker app — Requires broker URL schemes
- [x] Implement signal history view — Available via Signals tab
- [ ] Add signal notification preferences — Requires push setup
- [x] Create quick-copy presets (lot size) — 5 lot presets
- [x] Implement trade journal entry prompt — Bottom sheet modal
- [x] Add signal confidence/strength indicator — ConfidenceRing component
