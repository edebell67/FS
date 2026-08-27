import unittest
from checks import liveness, readiness

class HealthTests(unittest.TestCase):
    def test_liveness(self): self.assertEqual(200, liveness()[0])
    def test_ready_with_broker_disabled(self):
        code, body = readiness({"EP051_BROKER_PROFILE": "disabled", "EP051_SNAPSHOT": "test"})
        self.assertEqual(200, code); self.assertEqual("ready", body["status"])
    def test_refuses_unapproved_broker_profile(self):
        code, body = readiness({"EP051_BROKER_PROFILE": "live"})
        self.assertEqual(503, code); self.assertFalse(body["checks"]["broker_disabled"])

if __name__ == "__main__": unittest.main()
