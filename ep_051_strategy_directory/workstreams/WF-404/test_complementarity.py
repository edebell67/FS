# workstreams/WF-404/test_complementarity.py — Score transparency, suppression, cluster, tie, and stability tests.
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: proves reproducible ranking and component rationale.
import unittest
from complementarity import clusters,rank,rank_stability,score

def row(sid,corr=0,quality="SUFFICIENT"):
 return {"other_strategy_id":sid,"return_correlation":corr,"downside_correlation":corr,"joint_loss_ratio":.2,"drawdown_overlap_ratio":.3,"independent_activity":.8,"quality_state":quality}
class Tests(unittest.TestCase):
 def test_components_visible(self):self.assertEqual({"return","downside","loss","drawdown","activity"},set(score(row("B"))["components"]))
 def test_suppressed_has_no_score(self):self.assertIsNone(score(row("B",quality="SUPPRESSED")))
 def test_lower_correlation_ranks_first(self):self.assertEqual("B",rank("A",[row("C",.8),row("B",-.2)])[0]["strategy_id"])
 def test_tie_breaks_by_id(self):self.assertEqual(["B","C"],[r["strategy_id"] for r in rank("A",[row("C"),row("B")])])
 def test_clusters_deterministic(self):self.assertEqual([["A","B"],["C"]],clusters([("A","B",.1),("B","C",.8)]))
 def test_stability(self):self.assertTrue(rank_stability([["A","B"],["B","A"]],1)["stable"])
 def test_instability(self):self.assertFalse(rank_stability([["A","B","C"],["C","B","A"]],1)["stable"])
if __name__=="__main__":unittest.main()
