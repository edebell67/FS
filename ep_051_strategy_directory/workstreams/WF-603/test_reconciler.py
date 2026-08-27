"""Version history: 1.0.0 (2026-08-23) — reconciliation drills."""
import unittest
from reconciler import reconcile

I=[{"intent_id":"i1","quantity":10}]; E=[{"event_id":"a","intent_id":"i1","type":"ACK"},{"event_id":"f","intent_id":"i1","type":"FILL","filled_quantity":10}]
class Tests(unittest.TestCase):
    def test_ack_fill(self): self.assertEqual("FILL", reconcile(I,E,heartbeat_age=1,heartbeat_limit=5)["states"]["i1"])
    def test_duplicate_retry_deduplicates(self): self.assertEqual("FILL",reconcile(I+I,E+E,heartbeat_age=1,heartbeat_limit=5)["states"]["i1"])
    def test_disconnect_alerts(self): self.assertIn("HEARTBEAT_STALE",[a["code"] for a in reconcile(I,E,heartbeat_age=6,heartbeat_limit=5)["alerts"]])
    def test_missing_ack_alerts(self): self.assertIn("MISSING_ACK",[a["code"] for a in reconcile(I,[],heartbeat_age=1,heartbeat_limit=5)["alerts"]])
    def test_reject_cancel_terminal(self):
        for event_type in ("REJECT","CANCEL"):
            self.assertEqual(event_type,reconcile(I,[{"event_id":"x","intent_id":"i1","type":event_type}],heartbeat_age=1,heartbeat_limit=5)["states"]["i1"])
    def test_orphan_event_alerts(self): self.assertIn("ORPHAN_EVENT",[a["code"] for a in reconcile([],E,heartbeat_age=1,heartbeat_limit=5)["alerts"]])
    def test_drift_activates_kill(self): self.assertTrue(reconcile(I,[{"event_id":"x","intent_id":"i1","type":"FILL","filled_quantity":11}],heartbeat_age=1,heartbeat_limit=5)["kill_active"])
    def test_manual_kill(self): self.assertTrue(reconcile(I,E,heartbeat_age=1,heartbeat_limit=5,killed=True)["kill_active"])
    def test_non_finite_values_alert_and_kill(self):
        result=reconcile(I,[{"event_id":"x","intent_id":"i1","type":"FILL","filled_quantity":float("nan")}],heartbeat_age=1,heartbeat_limit=5)
        self.assertIn("INVALID_NUMERIC",[a["code"] for a in result["alerts"]]);self.assertTrue(result["kill_active"])

if __name__ == "__main__": unittest.main()
