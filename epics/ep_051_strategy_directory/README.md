# EP051 DNA Strategy Directory

## Version history

- 1.0.0 (2026-08-23): Initial implementation/operator overview.

Evidence-led directory, analytics and research portfolio tooling for 300–500 initial DNA strategies. DNA `_S`/`_B` direction suffixes normalize to a canonical ID; descriptive names remain optional metadata. Closed history comes from `combined_trades_closed`, current state from `combined_trades_open`, and Non-DNA data remains research/backtest-only. `target reached` is an exit description; outcome derives from signed `net_return`, whose costs/commission are already included.

## What is implemented

The 44-node manifest covers contracts/governance, canonical ingestion, data quality, analytics/periods/regimes/relationships, directory/detail/compare UI, portfolio construction/validation/builder, offline broker sandbox controls, lifecycle, assurance/security, beta/launch gates, multi-market adapters and infrastructure. Every node has task, artifact and verification evidence. Live broker connectivity and external public launch are not claimed; both remain fail-closed NO-GO until their external evidence exists.

## Quick start

Windows: run `solution\setup.bat`. POSIX: run `sh solution/setup.sh`. For containers, copy the environment template from INF-004, set the required database secret, then run `docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.override.yml config` before starting services. The local directory health endpoints are `/healthz` and `/readyz`; UI is rooted at WF-301.

## Evidence and workflow

- Canonical requirements and implementation workflow are in the root Markdown files.
- Visual node links use `file:///C:/Users/edebe/eds/workstream/600_workflow/ep051/EP051_DNA_strategy_directory_implementation_workflow.html#<node>`.
- `decomposition_manifest.json` is the lifecycle authority.
- Node outputs live under `workstreams/<node>` and acceptance summaries under `verification/<node>.md`.
- Operational commands, incident response, backups and rollback are in `deploy/OPERATIONS.md`.

This is decision support and research evidence, not personalised financial advice or a forecast.

