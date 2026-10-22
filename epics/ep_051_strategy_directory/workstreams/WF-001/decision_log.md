# Decision Log - EP051 DNA Strategy Directory

## Assumptions
1. **Trade Exit Times**: Assumed `COALESCE(g_close_time, last_update)` is accurate for exit times until validated against source behaviour.
2. **Capital/Equity Basis**: Drawdown percentages and risk-adjusted returns (e.g., Sortino) require explicit capital/equity definition; if absent, only monetary drawdown is published.
3. **Data Availability**: FX data is readily available and sufficient to generate the initial 300-500 DNA strategy population.
4. **Costs**: Commission/costs are already incorporated into trade results (`net_return`) and will not be double-counted.

## Exclusions
1. **Broker Integration**: Broker/platform integrations (WF-601 to WF-604) are excluded from the initial public release path.
2. **Non-DNA Trades**: Isolated to research/validation; excluded from the public directory.

## Decisions
- **D-001**: Baseline requirements accepted as defined in `dna_strategy_directory_requirements.md`.
- **D-002**: Workstreams 601-604 (Broker integration) reclassified as deferred and non-blocking for initial launch, per agent message board consensus (message `20260823T174919777_codex_5990bd0a`).
