# WF-404 Complementarity Score Specification

Version 1.0.0 combines five published components on sufficient aligned samples: 25% inverse return correlation, 25% inverse downside correlation, 20% inverse joint-loss overlap, 20% inverse drawdown overlap and 10% independent-activity evidence. Each component is normalized to `[0,1]`, displayed separately and retained with sample/window/methodology. Missing or suppressed components suppress the composite; no imputation creates a recommendation.

Similar-strategy clusters use the same component distance and deterministic canonical-ID tie breaking. Closest and complementary results state inclusion/exclusion reasons. Robustness requires stable rank bands across documented 3/6/12-month windows; materially unstable pairs show a warning and are not promoted.
