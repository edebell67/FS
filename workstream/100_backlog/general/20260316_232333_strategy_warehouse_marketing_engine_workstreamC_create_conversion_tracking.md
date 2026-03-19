# TASK C4: Create Conversion Tracking

**Workstream:** C - LANDING PAGE & CONVERSION
**Workstream Goal:** Build the subscriber capture funnel.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 3.4
**Depends On:** 3.1, 3.2
**Blocks:** 3.5, 4.2
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing

## Purpose

Track visitor-to-subscriber conversion funnel to measure marketing effectiveness.

## Input

- C1: Landing page
- C2: Subscription flow

## Output

- `ep_strategy_warehouse_marketing/solution/backend/src/services/conversionTrackingService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/models/ConversionEvent.py`
- `ep_strategy_warehouse_marketing/solution/frontend/src/hooks/useTracking.ts`

## Fields

```python
class ConversionEvent:
    event_id: UUID
    session_id: str
    event_type: Enum[page_view, form_view, form_submit, confirmation_click, subscription_complete]
    timestamp: datetime
    source: str  # utm_source
    medium: str  # utm_medium
    campaign: str  # utm_campaign
    referrer: str
    user_agent: str
    metadata: Dict  # additional event data
```

## Action

1. Implement frontend tracking hook:
   - Track page views with UTM params
   - Track form impressions
   - Track form interactions
2. Implement backend tracking endpoints:
   - POST /api/track for event recording
   - GET /api/conversions for reporting
3. Track conversion funnel stages:
   - Page view → Form view → Form submit → Confirmation → Complete
4. Calculate conversion rates:
   - Form views / Page views
   - Submissions / Form views
   - Completions / Submissions
5. Attribute conversions to traffic source

## Verification

- [ ] Record page view with utm_source
- [ ] Record form submission event
- [ ] Calculate conversion rate (submissions / views)
- [ ] Attribute conversions to traffic source

---

## Evidence

- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: Unit test output for tracking
  - Objective-Proved: Event tracking works correctly
  - Status: planned
- Evidence-Type: log_output
  - Artifact: Tracking event logs
  - Objective-Proved: Events recorded and attributed
  - Status: planned

## Dependency

- Requires: C1 (landing page), C2 (subscription flow)
- Blocks: C5 (subscriber dashboard), D2 (feedback loop)

## Notes

_Critical for understanding which traffic sources convert best. Used to optimize marketing spend._
