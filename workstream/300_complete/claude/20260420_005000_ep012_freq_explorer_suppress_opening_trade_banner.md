---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260420_003000_ep012_freq_explorer_immutable_signal_cache]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Frequency Explorer — Opening Trade Banner Alignment Fix

**Source:** Bug report — at 01:47 the 01:00 timeline card was showing a 🟢 OPENING TRADE banner
referencing EURAUD_C, but the card's live leaders list showed NZDAUD_C. The contradiction caused
confusion. User confirmed: the visual representation IS required, at the correct snap time — the
banner content is the immutable cached decision, independent of the live leaders in the card body.

**Destination:** `TradeApps/breakout/fs/frequency_explorer.html`

## Problem
- Opening trade banner showed EURAUD_C (cached, correct)
- Card body leaders showed NZDAUD_C (live data, changed since 01:00)
- Apparent contradiction — both are correct but the visual juxtaposition was confusing
- Intermediate incorrect fix: banner was fully suppressed (wrong — user wants visual at trade time)

## Final Correct Behaviour
- 🟢 OPENING TRADE banner IS shown inline in the timeline card at the snap it fired
- Banner content is **immutable** — always shows the cached product/strategy decision
- Card body leaders are **live** — show current snapshot data at that time (may differ from banner)
- Green card border (`opening-trade-card`) marks the snap visually
- ⚡ SWITCH SIGNAL banners remain yellow, unchanged

## Changes Made

### Timeline card class
```javascript
const cardClass = signal
    ? `timeline-card ${isOpenSignal ? 'opening-trade-card' : 'switch-signal-card'}`
    : 'timeline-card';
```

### Opening trade banner (green, immutable content)
```javascript
const signalBanner = signal ? (isOpenSignal ? `
    <div class="switch-signal-banner" style="border-color:rgba(16,185,129,0.5);background:rgba(16,185,129,0.08);">
        <strong style="color:#10b981;display:block;margin-bottom:3px;">🟢 OPENING TRADE</strong>
        <span style="color:var(--text-main);font-weight:600;">${signal.to.product} / ${signal.to.strategy}</span>
        <span style="display:block;margin-top:3px;color:var(--text-dim);">Net: $${signal.to.net.toFixed(0)}  ·  Count: ${signal.to.count}</span>
    </div>` : `... switch signal banner ...`) : '';
```

## Key Design Decision
The banner and the card body can legitimately show different strategies:
- **Banner** = "what we decided to trade at this time" (immutable, from cache)
- **Card body leaders** = "what the leaderboard looks like at this time NOW" (live, can change)
These are two different things and both are valid to display.

## Completion Status
COMPLETE -- 2026-04-20
