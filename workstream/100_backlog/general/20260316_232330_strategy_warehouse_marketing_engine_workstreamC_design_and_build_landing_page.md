# TASK C1: Design and Build Landing Page

**Workstream:** C - LANDING PAGE & CONVERSION
**Workstream Goal:** Build the subscriber capture funnel.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 3.1
**Depends On:** 1.1, 1.2, 1.3, 2.1, 2.5
**Blocks:** 3.2
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing

## Purpose

Create a high-converting landing page for Strategy Warehouse that captures subscribers and drives conversions.

## Input

- A1: Content schema (for value prop messaging)
- B1: Twitter connector (for social proof embed)
- Z1, Z2, Z3: Infrastructure

## Output

- `ep_strategy_warehouse_marketing/solution/frontend/` - React + Vite project
- `ep_strategy_warehouse_marketing/solution/frontend/src/pages/LandingPage.tsx`
- `ep_strategy_warehouse_marketing/solution/frontend/src/components/Hero.tsx`
- `ep_strategy_warehouse_marketing/solution/frontend/src/components/SocialProof.tsx`
- `ep_strategy_warehouse_marketing/solution/frontend/src/components/Features.tsx`
- `ep_strategy_warehouse_marketing/solution/frontend/src/components/CTA.tsx`
- `ep_strategy_warehouse_marketing/start_landing_page.bat`

## Route

`/` (root)

## Components

1. **Hero Section**
   - Bold headline with value proposition
   - Subheadline explaining the product
   - Primary CTA button
   - Background with atmospheric design (not generic gradient)

2. **Social Proof Section**
   - Live performance metrics from Strategy Warehouse
   - Testimonials (if available)
   - Platform follower counts

3. **Feature Highlights**
   - Key features with icons
   - Benefit-focused copy

4. **Call-to-Action**
   - Email subscription form
   - Free vs. Premium tier options

5. **Footer**
   - Legal/compliance disclaimers
   - Social links
   - Contact info

## Verification

- [ ] Navigate to http://localhost:3000/
- [ ] Page loads in under 2 seconds
- [ ] Mobile responsive (375px viewport)
- [ ] CTA button prominent and clickable
- [ ] Screenshot captured showing full page

---

## Evidence

- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: false
- Evidence-Type: url
  - Artifact: http://localhost:3000/
  - Objective-Proved: Landing page accessible and functional
  - Status: planned
- Evidence-Type: screenshot
  - Artifact: `ep_strategy_warehouse_marketing/verification/landing_page_screenshot.png`
  - Objective-Proved: Visual design complete
  - Status: planned
- Evidence-Type: demo
  - Artifact: `ep_strategy_warehouse_marketing/start_landing_page.bat`
  - Objective-Proved: One-click startup works
  - Status: planned

## Required Skills

- `skills/skills-main/skills/frontend-design/SKILL.md` - Distinctive design, avoid generic aesthetics
- `skills/skills-main/skills/web-artifacts-builder/SKILL.md` - React + Vite + Tailwind setup
- `skills/ui-delivery-viewability/SKILL.md` - Starter script and screenshot evidence

## Design Requirements (from frontend-design skill)

MUST AVOID:
- Generic fonts (Inter, Roboto, Arial)
- Purple gradients on white backgrounds
- Cookie-cutter centered layouts
- Excessive rounded corners

SHOULD INCLUDE:
- Distinctive typography (display + body font pairing)
- Cohesive color palette with CSS variables
- Motion and micro-interactions
- Atmospheric backgrounds (textures, patterns)

## Dependency

- Requires: Z1, Z2, Z3 (infrastructure), A1 (content schema), B1 (Twitter for social proof)
- Blocks: C2 (subscription flow)

## Notes

_User-visible task - requires manual verification. Design must be distinctive, not generic "AI slop"._
