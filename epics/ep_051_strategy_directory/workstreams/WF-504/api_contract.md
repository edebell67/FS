# WF-504 Portfolio Builder API Contract

## Version history

- 1.0.0 (2026-08-23): Initial research-builder API.

`POST /v1/portfolio-runs` accepts the versioned WF-501 capital/constraint contract plus candidate snapshot ID. It returns `run_id`, feasibility, allocations with canonical IDs and capital denominator, risk/contribution metrics, rationale, exclusions, warnings, engine/input/constraint versions, seed and WF-503 validation decision. Infeasible responses use HTTP 422 with stable violations and safe relaxation guidance. `GET /v1/portfolio-runs/{run_id}` returns immutable saved evidence. `GET /v1/portfolio-runs/{run_id}/export` exports the same evidence. Share links expose an opaque run ID only and never credentials, account data or open-trade details.

