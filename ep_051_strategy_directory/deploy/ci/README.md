# EP051 CI Quality Gates

Run `python deploy/ci/quality_gates.py` from any clean checkout. The command validates the 44-node manifest and task paths, secret-safe environment contract, deterministic migration inventory, and health suite. It emits `verification/ci_quality_report.json` and exits non-zero on any failed gate. A release system must retain that immutable report with the source revision and must not promote on failure.
