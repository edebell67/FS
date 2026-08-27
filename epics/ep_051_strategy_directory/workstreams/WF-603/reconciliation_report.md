# WF-603 Reconciliation Report

## Version history

- 1.0.0 (2026-08-23): Initial sandbox report.

The reconciler deduplicates intent/event retries, derives ACK/FILL/REJECT/CANCEL/PENDING state, detects conflicting intents, orphan events, missing acknowledgements, stale heartbeats and filled-quantity drift. Position drift or intent conflict activates the kill state. Eight automated drills pass. Scope is synthetic WF-601 events only.

