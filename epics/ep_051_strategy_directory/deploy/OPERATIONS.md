# EP051 Operations

## Version history

- 1.0.0 (2026-08-23): Initial operator guide.

## Start and verify

1. Validate runtime with `solution/setup.bat` or `solution/setup.sh`.
2. Create environment configuration from the versioned template; supply secrets through the runtime secret mechanism, never Git or browser variables.
3. Render Compose config and confirm `db`, `cache`, `directory`, `worker` plus private network isolation.
4. Run migrations before publishing a snapshot; migration failure stops startup.
5. Check `/healthz`, `/readyz`, snapshot age, DQ reconciliation and methodology/schema versions.

## Routine operation

Ingest closed/open sources separately, quarantine invalid rows, reconcile counts/sums/watermarks, publish immutable analytics snapshots, atomically invalidate caches, and verify directory/detail/search/portfolio smoke journeys. Open state is owner-scoped and never mixed into closed metrics. Every publish records run ID, source snapshot, code/method versions and evidence links.

## Incident and rollback

P1 private-data/credential/integrity incidents: disable the affected route, preserve evidence, activate incident command and meet the 15-minute acknowledgement SLA. P2 stale/failed publish: freeze writes and serve the last known-good snapshot with a visible warning. Rollback changes traffic/pointers to a previously verified immutable artifact and schema-compatible snapshot; never delete evidence or rewrite historical trades. Use INF-008 procedures for backup/restore and environment rollback.

## Deferred boundaries

The broker profile is offline/synthetic only. No network transport, credential, live account or activation exists. Public launch remains NO-GO until real beta, deployed load/SLO/DQ and rollback evidence plus named approvals pass.

