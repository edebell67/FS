# Task: Generate Complete Browser Demo

## Metadata
- **Epic**: 20260403_173500_ep_010_strategy_performance_view.md
- **Deliverable-Type**: UI
- **Deliverable-URL**: http://localhost:3002
- **Priority**: 1
- **Task Type**: verification
- **Task-Type**: Demo Generation

## 1. Understanding of Requirements
Generate a complete browser demo of the `ep_010_strategy_performance_view` epic. This involves running the Next.js application on port 3002 and capturing key user journeys using Playwright screenshots as defined in `demo.mjs`.

## 2. Plan of Approach
1. [ ] Install dependencies (`npm install`) in the project directory: `C:\Users\edebe\eds\epics\ep_010_strategy_performance_view`.
   - Test: Check if `node_modules` exists and contains dependencies.
   - Evidence: planned
2. [ ] Start the development server on port 3002 (`PORT=3002 npm run dev`).
   - Test: `curl http://localhost:3002` returns 200 OK.
   - Evidence: planned
3. [ ] Run the Playwright demo script (`node demo.mjs`).
   - Test: Script completes without error.
   - Evidence: planned
4. [ ] Verify that screenshots are correctly captured in `demo_screenshots/`.
   - Test: Check if 10 `.png` files exist in `demo_screenshots/`.
   - Evidence: planned
5. [ ] Stop the server upon completion.
   - Test: Port 3002 is released.
   - Evidence: planned

## 3. Checklist of Changes
- [ ] Dependencies installed
- [ ] Next.js server running on port 3002
- [ ] `demo.mjs` executed successfully
- [ ] Screenshots verified in `demo_screenshots/`

## 4. Evidence
- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: screenshot
  - Artifact: C:\Users\edebe\eds\epics\ep_010_strategy_performance_view\demo_screenshots\01_landing_dashboard.png
  - Objective-Proved: Landing dashboard view
  - Status: planned
- Evidence-Type: demo
  - Artifact: http://localhost:3002
  - Objective-Proved: Live UI access
  - Status: planned

## Log
- **2026-04-03 17:35**: Task created and added to backlog.
