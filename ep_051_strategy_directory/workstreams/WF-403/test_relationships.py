# workstreams/WF-403/test_relationships.py — Canonical-pair, metric and suppression tests.
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: validates relationship evidence against independent fixtures.
import unittest
from relationships import relationship
class Tests(unittest.TestCase):
 def test_pair_order(self):self.assertEqual(("A","B"),(relationship("B","A",[(1,1)]*30)["strategy_id_a"],relationship("B","A",[(1,1)]*30)["strategy_id_b"]))
 def test_thin_suppressed(self):self.assertIsNone(relationship("A","B",[(1,2)]) ["return_correlation"])
 def test_positive_correlation(self):self.assertAlmostEqual(1,relationship("A","B",[(i,i*2) for i in range(30)])["return_correlation"])
 def test_joint_loss(self):self.assertEqual(.5,relationship("A","B",[(-1,-2),(1,-2)],min_sample=2)["joint_loss_ratio"])
 def test_drawdown_overlap(self):self.assertGreater(relationship("A","B",[(2,2),(-1,-1),(-1,-1)],min_sample=3)["drawdown_overlap_ratio"],0)
 def test_same_id_rejected(self):
  with self.assertRaises(ValueError):relationship("A","A",[])
if __name__=="__main__":unittest.main()
