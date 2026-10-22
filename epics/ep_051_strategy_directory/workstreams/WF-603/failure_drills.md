# WF-603 Failure Drills

## Version history

- 1.0.0 (2026-08-23): Initial drills.

Duplicate intent/event retry is idempotent; disconnect triggers heartbeat alert; missing ACK, orphan event and terminal reject/cancel reconcile; overfill drift and intent conflict fail closed to kill; manual kill persists. Each drill records input fixture, expected state/alert, observed result and test version.

