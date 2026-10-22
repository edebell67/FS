"""Version history: 1.0.0 (2026-08-23) — sandbox contract tests."""
import inspect
import unittest
from adapter import OrderIntent, SandboxAdapter


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.adapter = SandboxAdapter({"EUR_GBP": "EURGBP.SANDBOX"})
        self.intent = OrderIntent("intent-1", "DNA_102001", "EUR_GBP", "BUY", 10)

    def test_capabilities_are_explicit(self):
        caps = self.adapter.capabilities()
        self.assertEqual("offline_sandbox", caps["environment"])
        self.assertIn("live_accounts", caps["unsupported"])

    def test_ack_and_synthetic_fill(self):
        events = self.adapter.submit(self.intent)
        self.assertEqual(["ACK", "FILL"], [e["type"] for e in events])
        self.assertTrue(events[1]["synthetic"])

    def test_idempotent_replay(self):
        self.assertIs(self.adapter.submit(self.intent), self.adapter.submit(self.intent))

    def test_unsupported_instrument_rejects(self):
        intent = OrderIntent("intent-2", "DNA_102001", "UNKNOWN", "SELL", 2)
        self.assertEqual("UNSUPPORTED_INSTRUMENT", self.adapter.submit(intent)[0]["reason"])

    def test_invalid_order_rejects(self):
        intent = OrderIntent("intent-3", "DNA_102001", "EUR_GBP", "BUY", 0)
        self.assertEqual("INVALID_ORDER", self.adapter.submit(intent)[0]["reason"])

    def test_non_finite_quantity_rejects(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            intent = OrderIntent(f"intent-{value}", "DNA_102001", "EUR_GBP", "BUY", value)
            self.assertEqual("INVALID_ORDER", self.adapter.submit(intent)[0]["reason"])

    def test_cancel_is_synthetic(self):
        self.assertEqual({"type": "CANCEL", "intent_id": "intent-1", "synthetic": True}, self.adapter.cancel("intent-1"))

    def test_source_has_no_network_or_secret_surface(self):
        source = inspect.getsource(__import__("adapter")).lower()
        for forbidden in ("requests", "httpx", "socket", "api_key", "password", "access_token"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
