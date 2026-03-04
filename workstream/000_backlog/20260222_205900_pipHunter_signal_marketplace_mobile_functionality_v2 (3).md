# Signal Marketplace -- Mobile Platform Specification

*Last updated: 2026-02-22 16:38 UTC*

------------------------------------------------------------------------

# 1. Core Engine (Shared Across Both Apps)

## 1.1 Strategy Universe

-   Hundreds of internal strategies running continuously.
-   Each strategy acts only when its own logic triggers.
-   Strategies trade internally regardless of external promotion status.

## 1.2 Buckets (Independent Silos)

-   Strategies grouped into buckets (2--3 per bucket).
-   Bucket members are structurally opposed (diametrically opposite
    logic).
-   Bucket composition is locked intraday.
-   Buckets operate independently (risk silos).

## 1.3 Competitive Ranking

-   Continuous ranking based on **daily PnL (intraday only)**.
-   Daily reset of ranking.
-   Leadership determined strictly by profitability.
-   Minimum leadership gap required to prevent noise flips.

## 1.4 Formulation Gate

-   Strategy must meet minimum daily trade count before eligibility.
-   Rules uniform across all buckets.
-   Until formulated → not eligible for promotion.

## 1.5 Promotion Logic

-   Only Rank 1 (leader) is eligible for live recommendation.
-   Leader must be:
    -   Formulated
    -   Positive PnL
    -   Above leadership gap
-   If no positive leader → no trade promoted.

## 1.6 Switch Timing

-   Leadership recalculated continuously.
-   Promotion switch occurs at next signal cycle.

------------------------------------------------------------------------

# 2. External Product Structure

Two separate mobile apps (skins), same backend engine.

------------------------------------------------------------------------

# 3. Skin A -- Battle Mode (Gamified Identity)

## Purpose

High engagement, visual competition, emotional participation.

## Core UI Concept

-   Bucket displayed as live head‑to‑head battle.
-   Visual "Champion" leader.
-   Dominance meter (selection margin).
-   Smooth animated leader transitions.
-   Clear "No Leader / No Trade" state.

## Key Elements

-   Strategy A vs Strategy B (optionally C).
-   Leader highlighting.
-   Live tick movement.
-   "Back the Champion" CTA.
-   Optional Auto‑Follow toggle.

## Emotional Positioning

-   Competitive.
-   Energetic.
-   Entertaining but disciplined.

------------------------------------------------------------------------

# 4. Skin B -- Signal Pro (Professional Mode)

## Purpose

Institutional credibility, capital allocation mindset.

## Core UI Concept

-   Ranked list presentation (no arena language).
-   Rank 1 labeled "Selected Model".
-   Ranked alternatives visible but subdued.
-   Selection margin shown clearly.
-   Stability metrics (tier dependent).

## Design Rules

-   Flat, minimal, structured layout.
-   No glow, no heavy animation.
-   Smooth number transitions only.
-   Expandable data (reduce visual clutter).

## Core States

-   Active leader
-   Forming (awaiting formulation)
-   No leader (silent bucket)
-   Leader change (timestamped)

------------------------------------------------------------------------

# 5. User Modes

## 5.1 Manual Mode

-   View recommended signal.
-   Copy trade manually.

## 5.2 Auto-Follow Mode

-   Allocate capital per bucket.
-   Automated execution (tier gated).
-   Risk controls configurable.

------------------------------------------------------------------------

# 6. Pricing Axes

Pricing determined by functionality, not skin.

## Axis 1 -- Bucket Visibility

-   1 bucket
-   3--5 buckets
-   All buckets

## Axis 2 -- Data Depth

-   Intraday only
-   Rolling (e.g., 5‑day)
-   Historical analytics
-   Leader duration metrics

## Axis 3 -- Control

-   Manual only
-   Limited automation
-   Full automation
-   Allocation controls
-   Portfolio aggregation

------------------------------------------------------------------------

# 7. Example Tier Structure

## Core

-   1 bucket
-   Intraday data
-   Manual follow

## Advanced

-   3--5 buckets
-   Intraday + rolling metrics
-   Alerts
-   Limited automation

## Portfolio

-   All buckets
-   Full data depth
-   Allocation tools
-   Risk caps
-   Full automation

------------------------------------------------------------------------

# 8. Critical Trust Features

-   No promotion on negative PnL.
-   Minimum trade formulation required.
-   Leadership gap prevents noise switching.
-   Silent bucket when no qualified leader.

------------------------------------------------------------------------

# 9. Product Positioning

Battle Mode → Engagement & identity.\
Signal Pro → Allocation & discipline.

Both powered by the same competitive signal engine.

------------------------------------------------------------------------
