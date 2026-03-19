# TASK C5: Build Subscriber Growth Dashboard

**Workstream:** C - LANDING PAGE & CONVERSION
**Workstream Goal:** Build the subscriber capture funnel.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 3.5
**Depends On:** 3.3, 3.4
**Blocks:** none
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing

## Purpose

Visualize subscriber metrics and growth trends for internal monitoring.

## Input

- C3: Subscriber database
- C4: Conversion tracking

## Output

- `ep_strategy_warehouse_marketing/solution/frontend/src/pages/Dashboard.tsx`
- `ep_strategy_warehouse_marketing/solution/frontend/src/components/SubscriberChart.tsx`
- `ep_strategy_warehouse_marketing/solution/frontend/src/components/ConversionFunnel.tsx`
- `ep_strategy_warehouse_marketing/solution/frontend/src/components/SourceBreakdown.tsx`
- `ep_strategy_warehouse_marketing/solution/backend/src/routes/dashboardRoutes.py`

## Route

`/dashboard` (protected - requires auth)

## Components

1. **Total Subscribers Card**
   - Current count
   - Change from last period
   - Tier breakdown (free/premium)

2. **Growth Chart**
   - Daily/weekly subscriber growth
   - Interactive date range selector
   - Trend line

3. **Conversion Funnel**
   - Visual funnel: Views → Forms → Submissions → Confirmations
   - Conversion rates at each stage
   - Comparison to previous period

4. **Source Attribution**
   - Bar chart by traffic source
   - Conversion rate by source
   - Best performing sources highlighted

5. **Subscriber Status Breakdown**
   - Pie chart: pending/confirmed/unsubscribed
   - Health indicators

## Verification

- [ ] Navigate to http://localhost:3000/dashboard
- [ ] Dashboard shows real subscriber count
- [ ] Growth chart renders with sample data
- [ ] All charts responsive on mobile
- [ ] Screenshot captured showing dashboard

---

## Evidence

- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: false
- Evidence-Type: url
  - Artifact: http://localhost:3000/dashboard
  - Objective-Proved: Dashboard accessible
  - Status: planned
- Evidence-Type: screenshot
  - Artifact: `ep_strategy_warehouse_marketing/verification/dashboard_screenshot.png`
  - Objective-Proved: Visual design complete
  - Status: planned

## Required Skills

- `skills/skills-main/skills/frontend-design/SKILL.md` - Dashboard aesthetics
- `skills/ui-delivery-viewability/SKILL.md` - Starter script and screenshot evidence

## Dependency

- Requires: C3 (subscriber database), C4 (conversion tracking)
- Blocks: none (end of workstream)

## Notes

_User-visible task - requires manual verification. Dashboard should be visually distinct and informative._
