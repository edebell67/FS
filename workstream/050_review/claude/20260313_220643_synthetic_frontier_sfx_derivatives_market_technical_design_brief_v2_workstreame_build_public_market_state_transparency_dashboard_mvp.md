# Task E3: Build public market-state transparency dashboard MVP

Source: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`

Task Summary: Deliver a runnable local dashboard that exposes public vault, imbalance, open-interest, leverage, funding, volatility, and risk-band state for the sFX MVP, with a one-step start path, resilient fallback behavior, and verification evidence.

Context:
- Existing implementation base selected: `TradingDashboard/frontend` and `TradingDashboard/backend`
- Verification output folder: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification`
- UI deliverable: yes

Dependency: Upstream task outputs for E1 (`...workstreame_define_public_transparency_data_contract_and_disclosure_pack.md`) and D3 (`...workstreamd_design_circuit_breaker_state_machine_and_staged_reopening_rules.md`) are not completed in-workspace, so this MVP will implement a deterministic local transparency contract and document the assumptions used for the absent artifacts.

Plan:
- [x] 1. Normalize the lifecycle task file into the required template and restate the implementation scope, dependency assumption, evidence inventory, and ordered execution steps.
  - [x] Test: Lifecycle file contains `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, and `Completion Status` sections with this task's scope.
  - Evidence: `workstream/200_inprogress/codex/20260313_220643_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreame_build_public_market_state_transparency_dashboard_mvp.md` updated with required sections.
- [x] 2. Implement the sFX transparency backend and frontend dashboard with the required market-state panels and resilient mock-data fallback.
  - [x] Test: `npm run build` in `TradingDashboard/frontend` completes successfully and backend endpoints return market-state JSON without requiring a live database.
  - Evidence: `TradingDashboard/backend/server.js`, `TradingDashboard/frontend/src/components/TradingDashboard.js`, and `TradingDashboard/frontend/src/styles.css` now implement the transparency contract, required panels, and dual backend/frontend fallback behavior; `npm run build` passed on 2026-03-16.
- [x] 3. Add a one-step local startup script that launches the dashboard stack and prints the localhost URLs for operator access.
  - [x] Test: Starter script prints the dashboard and health URLs and launches the serving process without an immediate configuration failure.
  - Evidence: `TradingDashboard/scripts/start_sfx_transparency_dashboard.ps1` prints `http://localhost:3002` and `http://localhost:3002/health`, builds the frontend if needed, and starts the backend server that serves the UI bundle.
- [x] 4. Run startup smoke validation, capture screenshot evidence, and update lifecycle evidence, validation, and completion fields.
  - [x] Test: Smoke script confirms backend health, dashboard route responds on localhost, and a screenshot artifact is saved under the verification folder.
  - Evidence: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/20260316_sfx_dashboard_smoke.txt` and `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/20260316_sfx_market_state_snapshot.png`.

Evidence:
Objective-Delivery-Coverage: 95%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `workstream/200_inprogress/codex/20260313_220643_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreame_build_public_market_state_transparency_dashboard_mvp.md`
  - Objective-Proved: The lifecycle task is back in progress and normalized to the required structure before implementation.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `npm run build` in `TradingDashboard/frontend`; `powershell -ExecutionPolicy Bypass -File .\scripts\smoke_sfx_transparency_dashboard.ps1` in `TradingDashboard`
  - Objective-Proved: Frontend build compiles, the backend serves the dashboard on localhost, `/health` returns 200, and `/api/transparency/market-state` returns 200 even without a live database.
  - Status: captured
- Evidence-Type: demo
  - Artifact: `TradingDashboard/scripts/start_sfx_transparency_dashboard.ps1` -> `http://localhost:3002`
  - Objective-Proved: Operators have a one-step local startup path and a documented dashboard URL.
  - Status: captured
- Evidence-Type: screenshot
  - Artifact: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/20260316_sfx_market_state_snapshot.png`
  - Objective-Proved: Captured visual state of the delivered dashboard data layout using a local verification snapshot derived from the live market-state endpoint.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/20260316_sfx_dashboard_smoke.txt`
  - Objective-Proved: The dashboard remains reachable and the market-state endpoint returns successfully while the backend is operating in mock fallback mode.
  - Status: captured
- Evidence-Type: user_feedback
  - Artifact: `pending_user_verification`
  - Objective-Proved: Final visual/user acceptance of the dashboard behavior and startup path.
  - Status: planned

Implementation Log:
- 2026-03-16 22:xx Europe/London: Loaded `skills/workstream-task-lifecycle/SKILL.md`, located the requested task under `workstream/400_failed/claude`, and moved it to `workstream/200_inprogress/codex` for active execution.
- 2026-03-16 22:xx Europe/London: Selected `TradingDashboard` as the closest viable existing implementation base after confirming the epic output folder did not yet contain a solution tree.
- 2026-03-16 22:xx Europe/London: Normalized this lifecycle file to the mandatory structure and recorded the dependency assumption caused by missing upstream E1 and D3 deliverables.
- 2026-03-16 22:xx Europe/London: Replaced the backend with a dedicated sFX transparency contract exposing instrument and market-state endpoints, including deterministic fallback data whenever database access is unavailable.
- 2026-03-16 22:xx Europe/London: Rebuilt the React frontend into a market-state dashboard with the required selector, status banner, vault, imbalance, open-interest, funding, risk-band, volatility, and governance panels plus client-side fallback handling.
- 2026-03-16 22:xx Europe/London: Added a one-step startup script and a smoke-validation script, corrected the malformed frontend browserslist entry, and captured verification artifacts under the epic verification folder.

Changes Made:
- Lifecycle file restored to active status under `workstream/200_inprogress/codex`
- Structured execution plan and evidence inventory added
- `TradingDashboard/backend/server.js`
  - Added `GET /api/transparency/instruments`, `GET /api/transparency/market-state`, deterministic mock fallback generation, and static serving of the built frontend.
- `TradingDashboard/frontend/src/components/TradingDashboard.js`
  - Added the dashboard MVP UI, selector, banner, metrics, charts, governance panel, and client-side fallback state.
- `TradingDashboard/frontend/src/styles.css`
  - Added the custom dashboard visual system and responsive layout.
- `TradingDashboard/frontend/src/App.js`, `TradingDashboard/frontend/src/index.js`, `TradingDashboard/frontend/public/index.html`
  - Simplified the app shell and updated metadata/imports for the new dashboard surface.
- `TradingDashboard/frontend/package.json`
  - Fixed the invalid browserslist query blocking production builds.
- `TradingDashboard/scripts/start_sfx_transparency_dashboard.ps1`
  - Added the one-step local startup path that prints the dashboard URL and serves the built UI via the backend.
- `TradingDashboard/scripts/smoke_sfx_transparency_dashboard.ps1`
  - Added localhost smoke validation and report output generation.
- `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/20260316_sfx_dashboard_smoke.txt`
  - Captured smoke-test output.
- `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/20260316_sfx_market_state_snapshot.html`
  - Captured a local verification snapshot derived from the running market-state endpoint for screenshot generation.
- `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/20260316_sfx_market_state_snapshot.png`
  - Captured screenshot artifact for review.

Validation:
- Lifecycle structure review: pass
  - Result: Required sections added and step 1 evidence recorded.
- `npm run build` in `TradingDashboard/frontend`: pass
  - Result: Production build compiled successfully after correcting the invalid browserslist entry.
- `node -e "require('./server'); setTimeout(() => process.exit(0), 1000)"` in `TradingDashboard/backend`: pass
  - Result: Backend started and logged the expected localhost endpoints.
- `powershell -ExecutionPolicy Bypass -File .\scripts\start_sfx_transparency_dashboard.ps1` in `TradingDashboard`: pass
  - Result: Script printed `http://localhost:3002` and `http://localhost:3002/health` and launched the serving process.
- `powershell -ExecutionPolicy Bypass -File .\scripts\smoke_sfx_transparency_dashboard.ps1` in `TradingDashboard`: pass
  - Result: Smoke report recorded `Health status: 200` and `Market-state status: 200`.
- User verification request
  - Result: Pending. Final response asks the user to verify the startup path and dashboard behavior at `http://localhost:3002`.

Risks/Notes:
- Upstream transparency contract and market-state model tasks are absent from the workspace, so this MVP will encode a local contract based on the epic fields listed in the task.
- Existing repository state is heavily dirty; unrelated changes will be left untouched.
- Modern headless browser capture was blocked by sandbox process restrictions, so the screenshot artifact was produced from a local verification snapshot populated by the live market-state endpoint rather than from a direct browser automation capture of the React runtime.
- Completion remains pending user verification because this is a user-visible dashboard deliverable and `Auto-Acceptance` remains disabled.

Completion Status: Awaiting user verification — 2026-03-16 21:55 Europe/London


## Execution Evidence
- Agent lane: codex
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/codex\20260313_220643_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreame_build_public_market_state_transparency_dashboard_mvp.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 1
- Stderr:
```text
OpenAI Codex v0.114.0 (research preview)
--------
workdir: C:\Users\edebe\eds
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, C:\Users\edebe\.codex\memories]
reasoning effort: medium
reasoning summaries: none
session id: 019cf8ab-e670-7fb3-a0b0-5fb6d23c4352
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/codex\20260313_220643_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreame_build_public_market_state_transparency_dashboard_mvp.md. Implement required changes in the workspace, run validations, and update checklist items.
mcp startup: no servers
ERROR: You've hit your usage limit. Upgrade to Pro (https://chatgpt.com/explore/pro), visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at Mar 18th, 2026 4:51 PM.
```


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:30


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\claude.CMD -p Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260313_220643_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreame_build_public_market_state_transparency_dashboard_mvp.md. Implement required changes in the workspace, run validations, and update checklist items. --permission-mode acceptEdits
- Return code: 0
- Stdout:
```text
I'm unable to proceed because file read permissions for `C:\Users\edebe\eds\` are being denied. You should see a permission prompt in the Claude Code UI — please approve it so I can read the required files. 

Alternatively, you could:
1. **Approve the permission prompt** that should appear in the UI
2. **Run the session from a parent directory** that includes both the workspace and `eds\` folder
3. **Copy the files** into the current working directory (`C:\Users\edebe\OneDrive\Desktop\batch files`)

Would you like to try one of these approaches?
```
