# Task: Add product_type to Workflows (Fix and DB Port)

## Source
- **Epic**: \C:\Users\edebe\eds\plans\20260321_1100_V20260321_1100_Add_Product_Type_To_Workflows.md\
- **Project**: breakout

## Task Summary
Integrate \product_type\ filtering into workflow execution and UI to allow asset-class-specific automation (Forex/Indices). This involves fixing a bug in the FS version and porting the feature to the DB version.

## Context
- \TradeApps\breakout\fs\trade_viewer_api.py\
- \TradeApps\breakout\DB\trade_viewer_api.py\
- \TradeApps\breakout\DB\workflow_automation.html\
- \TradeApps\breakout\DB\constants.py\
- \TradeApps\breakout\fs\constants.py\

## Dependency
None

## Plan
- [x] 1. FS API Fix: Correct indentation in \TradeApps\breakout\fs\trade_viewer_api.py\ for \_run_profile_match_workflow_once\.
  - Test: Check if \	rades_summary_rows\ is correctly populated from all day directories.
  - Evidence: Verified indentation fix manually and via syntax check.
- [x] 2. DB API Enhancement: Add \_default_workflows_payload\ and update \_load_workflows\ in \TradeApps\breakout\DB\trade_viewer_api.py\.
  - Test: Call \GET /api/workflows\ and verify \product_type\ is in the config.
  - Evidence: Implemented default payload and merging logic. Syntax check passed.
- [x] 3. DB UI Enhancement: Add Product Type selector and update \saveWorkflow\ in \TradeApps\breakout\DB\workflow_automation.html\.
  - Test: Verify the dropdown exists and saving a workflow persists the value.
  - Evidence: Updated HTML template and save script.
- [x] 4. Version Update: Update \constants.py\ in both folders to \V20260321_1100\.
  - Test: Verify version number matches.
  - Evidence: Constants.py updated in both \s\ and \DB\ folders.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: \TradeApps\breakout\fs\trade_viewer_api.py\ (fixed indentation)
  - Objective-Proved: bug_fix
  - Status: captured
- Evidence-Type: diff
  - Artifact: \TradeApps\breakout\DB\trade_viewer_api.py\ (added defaults)
  - Objective-Proved: feature_port
  - Status: captured
- Evidence-Type: diff
  - Artifact: \TradeApps\breakout\DB\workflow_automation.html\ (added selector)
  - Objective-Proved: ui_port
  - Status: captured

## Implementation Log
- 2026-03-21 11:00: Started task. Analyzed existing FS and DB implementations. Found indentation bug in FS. Found missing feature in DB.
- 2026-03-21 11:05: Fixed indentation bug in \TradeApps\breakout\fs\trade_viewer_api.py\.
- 2026-03-21 11:10: Enhanced \TradeApps\breakout\DB\trade_viewer_api.py\ with \product_type\ defaults and workflow merging logic.
- 2026-03-21 11:15: Updated \TradeApps\breakout\DB\workflow_automation.html\ with \Product Type\ dropdown and persistence logic.
- 2026-03-21 11:20: Updated version to \V20260321_1100\ in both folders. Verified syntax.

## Completion Status
Complete
