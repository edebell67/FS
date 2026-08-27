# WF-602 Approval Audit Contract

## Version history

- 1.0.0 (2026-08-23): Initial sandbox approval record.

Every attempted simulation records immutable run ID, offline environment, mapped internal instruments, capital/sizing denominator, gate inputs and limits, all failures, confirmation identity/time, pause/kill state, contract versions and final action. Missing confirmation or any failed gate records `BLOCK`; a passing record can only record `SIMULATE_ONLY`. This node cannot emit live activation.

