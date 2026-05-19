Source: `C:\Users\edebe\eds\workstream\000_epic\20260316_135233_strategy_warehouse_autonomous_marketing_engine_processed.md`

Task Summary: Monitor scheduler health, connector failures, and queue backlog and raise operational alerts when autonomous execution is degraded.

Context:
- Workstream D: Orchestration and Autonomy
- Epic: Strategy Warehouse Autonomous Marketing Engine
- Expected Output: `ep_strategy_warehouse_marketing/solution/backend/src/services/healthMonitorService.py` and `ep_strategy_warehouse_marketing/solution/backend/src/config/alerting_config.yaml`.

Dependency: Z6, D1

Priority: 1

# Implement health monitoring and alerting service

## Input
Health endpoint from Z6 and scheduler service from D1.

## Output
`ep_strategy_warehouse_marketing/solution/backend/src/services/healthMonitorService.py` and `ep_strategy_warehouse_marketing/solution/backend/src/config/alerting_config.yaml`.

## Plan
- [x] 1. Implement periodic health checks and threshold-based alerting for critical runtime conditions, with support for email or other notification channels when configured.
  - [x] Test: `python -m pytest ep_strategy_warehouse_marketing/solution/backend/tests/test_health_monitor_service.py -q -k scheduler_heartbeat_alert_triggers_when_heartbeat_stops`; pass if the scheduler-down alert is emitted when the heartbeat age exceeds the configured missed-heartbeat window.
  - [x] Evidence: `healthMonitorService.py` now evaluates heartbeat staleness and dispatches deduped alerts through logging, email, and optional webhook channels; the targeted pytest case passed.
- [x] 2. Connector-auth failure and backlog-threshold conditions are detectable by the monitor.
  - [x] Test: `python -m pytest ep_strategy_warehouse_marketing/solution/backend/tests/test_health_monitor_service.py -q -k connector_failure_and_backlog_thresholds_are_detected`; pass if a failing connector and warning backlog depth both produce alerts in one evaluation pass.
  - [x] Evidence: Connector `verify_auth()` checks and queue-depth threshold evaluation are implemented and the targeted pytest case passed with both alert classes detected.
- [x] 3. Normal operation does not generate repeated false-positive alerts.
  - [x] Test: `python -m pytest ep_strategy_warehouse_marketing/solution/backend/tests/test_health_monitor_service.py -q -k normal_operation_does_not_emit_repeated_false_positives`; pass if healthy runtime inputs produce no alerts across repeated checks.
  - [x] Evidence: Healthy heartbeat, connector, and queue state produced zero alerts across repeated monitor runs; alert history remained empty in the targeted pytest case.
- [x] 4. Health-monitor configuration supports alert thresholds and channel toggles.
  - [x] Test: `python -m pytest ep_strategy_warehouse_marketing/solution/backend/tests/test_health_monitor_service.py -q -k configuration_supports_thresholds_and_channel_toggles`; pass if the monitor loads threshold overrides and channel enablement flags from config.
  - [x] Evidence: `alerting_config.yaml` defines scheduler, connector, queue, and channel settings and the targeted pytest case passed against an override config.

## Validation
- [x] An alert condition is produced when the scheduler heartbeat stops unexpectedly.
  - Command: `python -m pytest ep_strategy_warehouse_marketing/solution/backend/tests/test_health_monitor_service.py -q -k scheduler_heartbeat_alert_triggers_when_heartbeat_stops`
  - Result: `1 passed, 3 deselected` (with one existing SQLAlchemy deprecation warning from `src/models/database.py`).
- [x] Connector-auth failure and backlog-threshold conditions are detectable by the monitor.
  - Command: `python -m pytest ep_strategy_warehouse_marketing/solution/backend/tests/test_health_monitor_service.py -q -k connector_failure_and_backlog_thresholds_are_detected`
  - Result: `1 passed, 3 deselected` (with one existing SQLAlchemy deprecation warning from `src/models/database.py`).
- [x] Normal operation does not generate repeated false-positive alerts.
  - Command: `python -m pytest ep_strategy_warehouse_marketing/solution/backend/tests/test_health_monitor_service.py -q -k normal_operation_does_not_emit_repeated_false_positives`
  - Result: `1 passed, 3 deselected` (with one existing SQLAlchemy deprecation warning from `src/models/database.py`).
- [x] Health-monitor configuration supports alert thresholds and channel toggles.
  - Command: `python -m pytest ep_strategy_warehouse_marketing/solution/backend/tests/test_health_monitor_service.py -q -k configuration_supports_thresholds_and_channel_toggles`
  - Result: `1 passed, 3 deselected` (with one existing SQLAlchemy deprecation warning from `src/models/database.py`).
- [x] Consolidated regression of the new monitor suite.
  - Command: `python -m pytest ep_strategy_warehouse_marketing/solution/backend/tests/test_health_monitor_service.py -q`
  - Result: `4 passed` (with one existing SQLAlchemy deprecation warning from `src/models/database.py`).

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `python -m pytest ep_strategy_warehouse_marketing/solution/backend/tests/test_health_monitor_service.py -q`
  - Objective-Proved: Heartbeat-loss, connector-auth failure, backlog-threshold, alert-deduping, and config-toggle behavior all pass under automated validation.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/services/healthMonitorService.py`, `ep_strategy_warehouse_marketing/solution/backend/src/config/alerting_config.yaml`, `ep_strategy_warehouse_marketing/solution/backend/tests/test_health_monitor_service.py`
  - Objective-Proved: The monitor service, runtime alert configuration, scheduler wiring, and automated test coverage were added to the backend workspace.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/services/autonomousSchedulerService.py`, `ep_strategy_warehouse_marketing/solution/backend/src/services/contentQueueService.py`, `ep_strategy_warehouse_marketing/solution/backend/src/services/__init__.py`
  - Objective-Proved: Existing scheduler and queue components were integrated with the new health monitoring flow instead of leaving the service unused.
  - Status: captured

## Implementation Log
- Created from fresh decomposition of the consolidated epic on 2026-03-20 23:31:48.
- 2026-03-21 21:03: Read `skills/workstream-task-lifecycle/README` equivalent instructions from `SKILL.md`, reviewed the D7 lifecycle file, and inspected the scheduler, queue, connector, and config surfaces in the backend workspace.
- 2026-03-21 21:10: Implemented `HealthMonitorService` with scheduler heartbeat monitoring, connector auth checks, queue backlog threshold checks, deduped alert activation, and configurable logging/email/webhook channels.
- 2026-03-21 21:12: Added `src/config/alerting_config.yaml`, exposed the service through `src/services/__init__.py`, added `get_backlog_depth()` to `ContentQueueService`, and wired the scheduler health-monitoring job to invoke the new service.
- 2026-03-21 21:18: Added focused backend tests covering heartbeat loss, connector plus backlog alerting, healthy-state no-alert behavior, and config overrides/channel toggles.
- 2026-03-21 21:23: Initial pytest runs failed because this environment denied access to pytest temp directories created via the `tmp_path` fixture; removed the fixture dependency from the new test file and re-ran validations successfully.

## Changes Made
- Added `ep_strategy_warehouse_marketing/solution/backend/src/services/healthMonitorService.py`.
  - Introduced `AlertEvent` plus logging, email, and webhook notification channels.
  - Added config-driven checks for scheduler missed heartbeats, connector authentication failures, and queue backlog thresholds.
  - Added alert deduplication so persistent failures do not spam repeated notifications during the cooldown window.
- Added `ep_strategy_warehouse_marketing/solution/backend/src/config/alerting_config.yaml`.
  - Declared heartbeat, connector, backlog, and alert-channel defaults used by the monitor.
- Updated `ep_strategy_warehouse_marketing/solution/backend/src/services/autonomousSchedulerService.py`.
  - Instantiates the new health monitor, records scheduler heartbeat timestamps, and runs the health monitor job on the configured cadence.
- Updated `ep_strategy_warehouse_marketing/solution/backend/src/services/contentQueueService.py`.
  - Added `get_backlog_depth()` so the monitor can measure outstanding queue pressure against configured thresholds.
- Updated `ep_strategy_warehouse_marketing/solution/backend/src/services/__init__.py`.
  - Exported `HealthMonitorService` through the service package.
- Added `ep_strategy_warehouse_marketing/solution/backend/tests/test_health_monitor_service.py`.
  - Added automated regression coverage for the four D7 acceptance conditions and a full suite pass.

## Risks/Notes
- Task created from fresh decomposition after active-lane reset.
- `src/models/database.py` still emits an existing SQLAlchemy `declarative_base()` deprecation warning during test runs. It does not block D7 delivery, but it remains cleanup debt outside this task.

Completion Status: Complete - 2026-03-21 21:23:00


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\claude.CMD -p Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260320_233148_gemini_strategy_warehouse_marketing_engine_d7_implement_health_monitoring_and_alerting_service.md. Implement required changes in the workspace, run validations, and update checklist items. --permission-mode acceptEdits
- Return code: 0
- Stdout:
```text
It seems the permission prompt isn't appearing for you. This might be a permission mode issue. Could you try one of these options:

1. **Approve the permission** when the prompt appears (it may be in a different part of your terminal)
2. **Run Claude Code with broader permissions** - you may need to allow access to `C:\Users\edebe\eds\` 
3. **Copy the files** into the current working directory (`C:\Users\edebe\OneDrive\Desktop\batch files`)

Alternatively, could you paste the contents of both files so I can proceed?
```


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-21 19:55:40
