"""Version history: 1.0.0 (2026-08-23) — lifecycle tests."""
import unittest
from lifecycle import transition,evaluate_flags

P={"role":"operator","subject":"ops-1"};R={"strategy_id":"DNA_102001","state":"active","deployment_eligible":True,"history":[{"from":"eligible","to":"active"}]}
class Tests(unittest.TestCase):
 def test_pause_stops_new_deployment_and_preserves_history(self):
  out=transition(R,"paused",principal=P,reason="drift",evidence_id="ev-1");self.assertFalse(out["deployment_eligible"]);self.assertEqual(2,len(out["history"]))
 def test_resume_is_audited(self):self.assertTrue(transition({**R,"state":"paused"},"active",principal=P,reason="cleared",evidence_id="ev-2")["deployment_eligible"])
 def test_unauthorized_rejected(self):
  with self.assertRaises(PermissionError):transition(R,"paused",principal={"role":"user","subject":"u"},reason="x",evidence_id="e")
 def test_invalid_transition_rejected(self):
  with self.assertRaises(ValueError):transition(R,"eligible",principal=P,reason="x",evidence_id="e")
 def test_reason_and_evidence_required(self):
  with self.assertRaises(ValueError):transition(R,"paused",principal=P,reason="",evidence_id="")
 def test_retired_is_terminal(self):
  with self.assertRaises(ValueError):transition({**R,"state":"retired"},"active",principal=P,reason="x",evidence_id="e")
 def test_all_flags(self):self.assertEqual(["STALE","DRIFT","DEFINITION_MISMATCH"],evaluate_flags(data_age_seconds=11,age_limit_seconds=10,observed_drift=.2,drift_limit=.1,definition_version="1",required_definition_version="2"))

if __name__=="__main__":unittest.main()

