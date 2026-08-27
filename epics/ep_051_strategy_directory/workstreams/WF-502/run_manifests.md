# WF-502 Run Manifest Contract

## Version history

- 1.0.0 (2026-08-23): Initial replay and sensitivity contract.

Every successful run records engine version, deterministic seed, input snapshot version and hash, constraint hash, objective wording, baseline, canonical-ID allocations, exclusions and sensitivity triggers. An unsuccessful run records `feasible=false`, a stable reason code, eligible count and exclusions. Replaying identical inputs, constraints, seed and engine version must produce byte-equivalent semantic output.

