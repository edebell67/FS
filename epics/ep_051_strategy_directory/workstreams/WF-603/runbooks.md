# WF-603 Incident Runbooks

## Version history

- 1.0.0 (2026-08-23): Initial offline runbooks.

On stale heartbeat: pause simulation, preserve events, verify clock/transport fixture, replay from last acknowledged cursor, and resume only after green reconciliation. On drift/conflict: activate kill, prohibit new intents, snapshot intent/event ledger, identify canonical run and instrument mapping, reconcile manually, document cause, and require two-person future production approval. Never repair by deleting events or changing an immutable intent.

