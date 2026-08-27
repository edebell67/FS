# EP051 Rollback Runbook

Version 1.0.0 — 2026-08-23

Rollback triggers include readiness failure, error/SLO breach, stale or incorrect data, security incident, migration failure, or reconciliation gate failure.

1. Stop promotion, preserve logs/evidence, and remove the affected release from traffic.
2. Route traffic to the last approved immutable application release. Keep broker profile disabled.
3. If data changed, prefer a forward corrective migration. Restore the verified pre-release backup only after incident lead and database owner approval, into isolation first.
4. Run health, CI, data-quality, reconciliation and smoke checks; compare snapshot/release IDs.
5. Re-enable traffic gradually, monitor thresholds, document outcome and open corrective actions.

Rollback does not authorize public launch. WF-704 remains NO-GO until external beta and deployed SLO/load/data-quality/rollback evidence exists and authorized operators approve promotion.
