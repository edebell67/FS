"""Version history: 1.0.0 (2026-08-23) — promotion gate tests."""
import unittest
from validation import validate_run


def valid_run():
    return {
        "train_end": "2025-12-31T23:59:59Z", "holdout_start": "2026-01-01T00:00:00Z",
        "universe_as_of": "2025-12-31T23:59:59Z", "required_regimes": ["risk_on", "risk_off"],
        "regime_results": {"risk_on": {}, "risk_off": {}},
        "benchmarks": {"equal_weight": {}, "simple_selection": {}},
        "risk_disclosures": ["drawdown", "concentration"], "sensitivity_runs": ["weight_cap_minus_5pct"],
    }


class ValidationTests(unittest.TestCase):
    def test_valid_run_promotes(self):
        self.assertEqual({"approved": True, "failures": [], "decision": "PROMOTE"}, validate_run(valid_run()))

    def test_temporal_overlap_holds(self):
        run = valid_run(); run["holdout_start"] = run["train_end"]
        self.assertIn("TEMPORAL_LEAKAGE", validate_run(run)["failures"])

    def test_survivorship_risk_holds(self):
        run = valid_run(); run["universe_as_of"] = "2026-01-02T00:00:00Z"
        self.assertIn("SURVIVORSHIP_RISK", validate_run(run)["failures"])

    def test_missing_regime_holds(self):
        run = valid_run(); del run["regime_results"]["risk_off"]
        self.assertIn("REGIME_COVERAGE", validate_run(run)["failures"])

    def test_missing_baseline_holds(self):
        run = valid_run(); del run["benchmarks"]["simple_selection"]
        self.assertIn("BASELINE_MISSING", validate_run(run)["failures"])

    def test_missing_risks_holds(self):
        run = valid_run(); run["risk_disclosures"] = []
        self.assertIn("RISKS_MISSING", validate_run(run)["failures"])

    def test_missing_sensitivity_holds(self):
        run = valid_run(); run["sensitivity_runs"] = []
        self.assertEqual("HOLD", validate_run(run)["decision"])

    def test_offset_timestamp_cannot_bypass_survivorship_gate(self):
        run = valid_run(); run["train_end"]="2025-12-31T23:59:59+01:00"; run["universe_as_of"]="2025-12-31T23:30:00+00:00"
        self.assertIn("SURVIVORSHIP_RISK",validate_run(run)["failures"])

    def test_naive_timestamp_rejected(self):
        run=valid_run();run["universe_as_of"]="2025-12-31T20:00:00"
        with self.assertRaises(ValueError):validate_run(run)


if __name__ == "__main__": unittest.main()
