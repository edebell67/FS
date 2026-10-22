"""Version history: 1.0.0 (2026-08-23) — WF-501 contract checks."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parent


class PortfolioContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads((ROOT / "portfolio_contract.json").read_text(encoding="utf-8"))
        cls.matrix = (ROOT / "constraint_matrix.md").read_text(encoding="utf-8")
        cls.baselines = (ROOT / "baseline_definitions.md").read_text(encoding="utf-8")

    def test_capital_has_currency_and_denominator(self):
        req = self.contract["request"]
        self.assertGreater(req["capital"]["amount"], 0)
        self.assertTrue(req["portfolio_currency"])
        self.assertTrue(req["capital"]["denominator"])

    def test_risk_and_margin_claims_have_denominators(self):
        req = self.contract["request"]
        self.assertIn("denominator", req["risk_budget"])
        self.assertIn("denominator", req["margin_policy"])

    def test_sizing_policy_is_explicit(self):
        self.assertEqual("fixed_fractional_risk", self.contract["request"]["sizing_policy"])

    def test_infeasibility_is_explained(self):
        self.assertIn("feasible=false", self.matrix)
        self.assertIn("smallest safe relaxation", self.matrix)

    def test_no_return_ranking_shortcut(self):
        combined = self.matrix + self.baselines
        self.assertIn("No “highest return” shortcut", combined)
        self.assertIn("non-return-ranked", combined)

    def test_closed_evidence_and_cost_semantics(self):
        self.assertIn("Open trades are not substituted", self.matrix)
        self.assertIn("must not be deducted again", self.matrix)
        self.assertIn("sign of `net_return`", self.matrix)

    def test_baselines_are_reproducible(self):
        for term in ("canonical IDs", "as-of timestamp", "method versions", "random seed", "exclusions"):
            self.assertIn(term, self.baselines)


if __name__ == "__main__":
    unittest.main()
