# WF-401 Coverage and Stability

- Minimum publishable sample: 30 trades per regime slice.
- Fewer than 30: `INSUFFICIENT`; zero observations: `COLLECTING`.
- UNKNOWN remains visible in coverage but cannot support a directional/volatility claim.
- API/UI must show trades, evidence window, definition version, baseline, lift and uncertainty alongside results.
- Recalculation across subperiods is required before comparative language is promoted publicly.

Fixed fixtures reconcile regime net return to the overall sample exactly; 5/5 tests pass.

