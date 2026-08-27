# WF-703 Feedback Decisions

## Version history

- 1.0.0 (2026-08-23): Initial evidence-driven decisions.

| Observation | Decision | Evidence |
|---|---|---|
| Users may interpret highest return as “best” | Keep no-winner and no-return-shortcut explanations | WF-303/WF-504 browser evidence |
| “Target reached” may be assumed profitable | Retain explicit exit-description warning; outcome remains net-return sign | WF-302 |
| Open state could be mistaken for historical evidence | Keep isolated current-state panel and freshness timestamp | WF-302/WF-204 |
| Incompatible evidence can invite false ranking | Block ranking and show basis/window reason | WF-303 |
| Portfolio rationale may feel opaque | Preserve why-selected, exclusions, constraints, seed and limitation evidence | WF-504 |
| Security review found account/search/safety integrity gaps | Fix controls; do not tune historical returns to improve perception | WF-702, 56 tests |

Feedback changes wording, navigation, warnings and evidence presentation only. Historical records, outcomes, samples and metrics are never altered to improve beta sentiment.

