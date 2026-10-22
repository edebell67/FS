"""Version history: 1.0.0 (2026-08-23) — launch gate tests."""
import unittest
from launch_gate import decide,REQUIRED
class Tests(unittest.TestCase):
 def test_all_evidence_can_go(self):self.assertEqual("GO",decide({k:True for k in REQUIRED})["decision"])
 def test_each_missing_gate_is_no_go(self):
  for key in REQUIRED:
   evidence={k:True for k in REQUIRED};evidence[key]=False;result=decide(evidence);self.assertEqual("NO_GO",result["decision"]);self.assertIn(key,result["missing"])
 def test_unknown_is_no_go(self):self.assertEqual("NO_GO",decide({})["decision"])
 def test_staged_traffic(self):self.assertEqual([1,5,25,50,100],decide({})["staged_traffic"])
 def test_rollback_triggers(self):self.assertIn("stale_data",decide({})["automatic_rollback_on"])
if __name__=="__main__":unittest.main()

