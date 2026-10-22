"""Version history: 1.0.0 (2026-08-23) — optimizer constraint tests."""
import unittest
from engine import Candidate, optimise


C = {
    "minimum_strategies": 3, "maximum_strategies": 4,
    "maximum_strategy_weight": 0.4, "maximum_cluster_weight": 0.7,
    "maximum_market_weight": 0.7, "minimum_history_closed_trades": 30,
    "eligible_quality_states": ["VALID"],
}
ITEMS = [
    Candidate("DNA_102001", "c1", "FX", .10), Candidate("DNA_102002", "c1", "FX", .12),
    Candidate("DNA_102003", "c2", "INDEX", .09), Candidate("DNA_102004", "c3", "METAL", .14),
    Candidate("DNA_102005", "c4", "FX", .07, quality="QUARANTINED"),
    Candidate("DNA_102006", "c4", "INDEX", .08, closed_trades=12),
]


class EngineTests(unittest.TestCase):
    def test_reproducible_from_version_seed_inputs(self):
        self.assertEqual(optimise(ITEMS, C, seed=51, input_version="snap-1"), optimise(ITEMS, C, seed=51, input_version="snap-1"))

    def test_allocations_sum_to_one(self):
        result = optimise(ITEMS, C, seed=51, input_version="snap-1")
        self.assertAlmostEqual(1.0, sum(result["allocations"].values()))

    def test_all_hard_caps_hold(self):
        result = optimise(ITEMS, C, seed=51, input_version="snap-1")
        self.assertTrue(result["feasible"])
        self.assertGreaterEqual(len(result["allocations"]), C["minimum_strategies"])
        self.assertTrue(all(w <= C["maximum_strategy_weight"] for w in result["allocations"].values()))

    def test_quality_and_history_exclusions_are_explicit(self):
        result = optimise(ITEMS, C, seed=51, input_version="snap-1")
        self.assertIn({"strategy_id": "DNA_102005", "reasons": ["QUALITY"]}, result["exclusions"])
        self.assertIn({"strategy_id": "DNA_102006", "reasons": ["HISTORY"]}, result["exclusions"])

    def test_no_return_input_or_ranking(self):
        result = optimise(ITEMS, C, seed=51, input_version="snap-1")
        self.assertIn("returns are not ranked", result["objective"])

    def test_infeasible_is_explained(self):
        impossible = dict(C, minimum_strategies=5)
        result = optimise(ITEMS, impossible, seed=51, input_version="snap-1")
        self.assertEqual({"feasible": False, "reason_code": "INVALID_STRATEGY_COUNT"}, {k: result[k] for k in ("feasible", "reason_code")})

    def test_manifest_has_replay_keys(self):
        result = optimise(ITEMS, C, seed=51, input_version="snap-1")
        for key in ("engine_version", "seed", "input_version", "input_hash", "constraint_hash", "sensitivity"):
            self.assertIn(key, result)

    def test_candidate_budget_rejects_without_search(self):
        many = [Candidate(f"DNA_{i:06d}", f"c{i}", f"m{i}", .1) for i in range(41)]
        self.assertEqual("CANDIDATE_BUDGET_EXCEEDED", optimise(many, C, seed=1, input_version="snap")["reason_code"])

    def test_combination_budget_rejects_without_accumulation(self):
        many = [Candidate(f"DNA_{i:06d}", f"c{i}", f"m{i}", .1) for i in range(30)]
        constraints = dict(C, minimum_strategies=10, maximum_strategies=12)
        self.assertEqual("SEARCH_BUDGET_EXCEEDED", optimise(many, constraints, seed=1, input_version="snap")["reason_code"])


if __name__ == "__main__":
    unittest.main()
