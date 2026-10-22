# WF-604 Audit Samples

## Version history

- 1.0.0 (2026-08-23): Initial audit examples.

`active → paused`: actor `ops-1`, reason `relationship drift threshold`, evidence `ev-1`; deployment eligibility false, history retained. `paused → active`: actor `ops-2`, reason `review cleared`, evidence `ev-2`; new sandbox simulations permitted. Each record contains canonical ID, from/to, UTC time, trusted subject, reason, evidence and definition version; records are append-only.

