# Task: Fix Simulation Summary Generation

## Status
- **Objective**: Ensure simulation data is visible in strategy_performance.html.
- **Delivery**: summary_net_generator.py respects config run_mode and processes sim trades.
- **Coverage**: summary_net_generator.py

## Plan
1. [x] Modify summary_net_generator.py to respect run_mode from config.json.
2. [x] Add logging to verify which mode is being processed.
3. [x] Start the generator and verify output.

## Log
- Detected that summary_net_generator.py is not running.
- Detected that _cl.json files exist but are not processed.
- Identified that summary_net_generator.py is hardcoded to iterate over both modes but user requested it to follow config.
- Fixed TabError and indentation issues in summary_net_generator.py.
- Successfully verified that _summary_net.json is now populated for sim mode.
- Generator is now running in the background (PID 5936).
