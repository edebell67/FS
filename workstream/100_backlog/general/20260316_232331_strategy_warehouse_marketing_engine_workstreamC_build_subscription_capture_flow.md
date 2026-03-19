# TASK C2: Build Subscription Capture Flow

**Workstream:** C - LANDING PAGE & CONVERSION
**Workstream Goal:** Build the subscriber capture funnel.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 3.2
**Depends On:** 3.1
**Blocks:** 3.3
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing

## Purpose

Capture subscriber email and preferences with a smooth UX flow including double opt-in.

## Input

- C1: Landing page

## Output

- `ep_strategy_warehouse_marketing/solution/frontend/src/components/SubscriptionForm.tsx`
- `ep_strategy_warehouse_marketing/solution/frontend/src/components/PricingTiers.tsx`
- `ep_strategy_warehouse_marketing/solution/backend/src/routes/subscriptionRoutes.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/services/emailService.py`

## Components

1. **Subscription Form**
   - Email input with validation
   - Tier selection (Free / Premium)
   - Preference checkboxes (signal types, frequency)
   - Submit button with loading state

2. **Pricing Tiers Display**
   - Free tier features
   - Premium tier features and pricing
   - Visual differentiation

3. **Confirmation Flow**
   - Success message after submission
   - Email confirmation (double opt-in)
   - Welcome email on confirmation

## Action

1. Implement email capture form with client-side validation
2. Implement server-side validation and storage
3. Implement double opt-in flow:
   - Generate confirmation token
   - Send confirmation email
   - Handle confirmation link click
4. Implement preference selection (signal types, frequency)
5. Integrate Stripe for premium tier checkout (if selected)
6. Handle form states: idle, loading, success, error

## Verification

- [ ] Submit email via form
- [ ] Receive confirmation email (mock in test)
- [ ] Form validates email format
- [ ] Form shows success message after submission
- [ ] Screenshot of subscription flow captured

---

## Evidence

- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: false
- Evidence-Type: demo
  - Artifact: Subscription flow walkthrough
  - Objective-Proved: Full flow works end-to-end
  - Status: planned
- Evidence-Type: screenshot
  - Artifact: `ep_strategy_warehouse_marketing/verification/subscription_flow_screenshot.png`
  - Objective-Proved: UI complete
  - Status: planned
- Evidence-Type: test_output
  - Artifact: Integration test output
  - Objective-Proved: Form submission works correctly
  - Status: planned

## Required Skills

- `skills/ui-delivery-viewability/SKILL.md` - Screenshot evidence

## Dependency

- Requires: C1 (landing page)
- Blocks: C3 (subscriber database)
- External: SMTP service, Stripe (for premium)

## Notes

_User-visible task - requires manual verification. Smooth UX is critical for conversion._
