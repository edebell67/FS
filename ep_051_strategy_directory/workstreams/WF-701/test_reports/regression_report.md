# WF-701 Regression Report

## Version history

- 1.0.0 (2026-08-23): Initial full pre-release assurance run.

Result: PASS for the implemented research-directory scope.

- 20 test files executed successfully across contracts, identity, ingestion, reconciliation, analytics, regimes, alignment, relationships, portfolio construction/validation and offline sandbox gates.
- 137 automated assertions/tests passed, including the independently calculated golden analytics dataset.
- Chrome and Firefox completed the builder evidence/infeasibility journey with zero console errors; existing directory, detail, comparison and mobile screenshots remain captured by WF-301–WF-504.
- Required regression command: execute every `test_*.py` in its workstream directory; WF-003 receives `golden_dataset.json` as its argument.
- Defects: one assurance-environment gap (Firefox missing) was remediated and rerun. No unresolved severity 1–3 defect remains. Deployed topology/load thresholds remain governed by infrastructure nodes and are not misrepresented by component tests.

