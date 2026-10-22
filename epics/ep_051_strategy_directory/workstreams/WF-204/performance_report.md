# WF-204 Read-Model Performance Report

Date: 2026-08-23

- Fixture: 1,000 public strategy rows.
- Operation: filter, stable sort, public-field projection, 100-row page and evidence envelope.
- Runs: 1,000 in one Python process.
- Total: 386.89 ms; average: 0.387 ms per operation.

This proves computation baseline only. Network/database p95 remains a deployment validation gate; it is not inferred from this local measurement.

