"""Version history: 1.0.0 (2026-08-23) — fail-closed gate suite."""
import unittest
from dataclasses import replace
from risk_gates import Preview, evaluate

BASE = Preview("run-51", "offline_sandbox", True, False, False, 0.2, 0.3, -0.01, 0.03, 5, 30, False, 1.25, 1.251, 0.01)

class GateTests(unittest.TestCase):
    def test_safe_preview_simulates_only(self): self.assertEqual("SIMULATE_ONLY", evaluate(BASE)["action"])
    def test_confirmation_required(self): self.assertIn("CONFIRMATION_REQUIRED", evaluate(replace(BASE, confirmed=False))["failures"])
    def test_live_environment_forbidden(self): self.assertIn("LIVE_ENVIRONMENT_FORBIDDEN", evaluate(replace(BASE, environment="production"))["failures"])
    def test_exposure_blocks(self): self.assertIn("EXPOSURE_LIMIT", evaluate(replace(BASE, projected_exposure=.31))["failures"])
    def test_loss_blocks(self): self.assertIn("LOSS_LIMIT", evaluate(replace(BASE, daily_loss=-.04))["failures"])
    def test_staleness_blocks(self): self.assertIn("STALE_DATA", evaluate(replace(BASE, data_age_seconds=31))["failures"])
    def test_duplicate_blocks(self): self.assertIn("DUPLICATE_INTENT", evaluate(replace(BASE, duplicate_intent=True))["failures"])
    def test_price_deviation_blocks(self): self.assertIn("PRICE_DEVIATION", evaluate(replace(BASE, preview_price=1.5))["failures"])
    def test_pause_and_kill_block(self):
        self.assertIn("PAUSED", evaluate(replace(BASE, paused=True))["failures"])
        self.assertIn("KILL_SWITCH", evaluate(replace(BASE, killed=True))["failures"])
    def test_non_finite_values_fail_closed(self):
        for field in ("projected_exposure","daily_loss","reference_price","preview_price"):
            for value in (float("nan"),float("inf"),float("-inf")):
                self.assertIn("INVALID_NUMERIC",evaluate(replace(BASE,**{field:value}))["failures"])
    def test_negative_limits_fail_closed(self):
        self.assertIn("INVALID_RANGE",evaluate(replace(BASE,exposure_limit=-1))["failures"])

if __name__ == "__main__": unittest.main()
