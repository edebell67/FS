# WF-203 Score Calibration Specification

Scores are calibrated only within comparable `(market, currency/basis, evidence_window, methodology_version)` cohorts. A cohort requires at least 30 eligible strategies and each strategy requires the governed sample threshold. Otherwise the result is `COLLECTING` or `INSUFFICIENT`, with raw components only.

The initial score set is consistency, risk, activity and direction balance. Thresholds are empirical cohort quantiles (20/40/60/80) frozen with population checksum and version. Public labels are neutral numeric bands `1–5`; marketing labels are prohibited. Every response displays raw inputs, cohort, quantile thresholds, sample size, as-of date and version.

