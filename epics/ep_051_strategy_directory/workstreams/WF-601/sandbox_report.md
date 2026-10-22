# WF-601 Sandbox Report

## Version history

- 1.0.0 (2026-08-23): Initial contract-test report.

Result: PASS. Seven of seven tests passed. The in-memory adapter advertises its offline environment, returns deterministic synthetic lifecycle events, replays duplicate intent IDs idempotently, rejects invalid and unsupported orders, and contains no network or credential surface. This evidence does not authorize or imply live broker deployment.

