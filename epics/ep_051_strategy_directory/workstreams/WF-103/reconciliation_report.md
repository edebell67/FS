# WF-103 Reconciliation Evidence

Result: PASS

- Matching source/canonical fixture: publish allowed.
- P&L variance greater than `0.00000001`: publish blocked.
- Duplicate canonical GUID: publish blocked.
- Missing required field: publish blocked.
- Closed-source age greater than one hour: publish blocked.
- Incremental/backfill signature equality: pass; changed checksum: fail.
- Test suite: 6 passed, 0 failed.

