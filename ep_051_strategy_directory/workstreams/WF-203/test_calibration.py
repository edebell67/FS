# workstreams/WF-203/test_calibration.py — Empirical threshold, cohort, stability, and suppression tests.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: validates frozen cohort quantiles and neutral numeric scoring.

import unittest
from calibration import calibrate,score

class Tests(unittest.TestCase):
 def setUp(self):self.rows=[{"cohort":"FX:GBP:1Y:v1","eligible":True,"consistency":i} for i in range(1,41)]
 def test_insufficient_suppresses(self):self.assertEqual("INSUFFICIENT",calibrate(self.rows[:10],"consistency","FX:GBP:1Y:v1","1")["status"])
 def test_empirical_thresholds_frozen(self):self.assertEqual([8.8,16.6,24.4,32.2],calibrate(self.rows,"consistency","FX:GBP:1Y:v1","1")["bands"])
 def test_other_cohort_excluded(self):self.assertEqual(40,calibrate(self.rows+[{"cohort":"OTHER","eligible":True,"consistency":999}],"consistency","FX:GBP:1Y:v1","1")["sample_size"])
 def test_numeric_band_only(self):self.assertEqual(5,score(40,calibrate(self.rows,"consistency","FX:GBP:1Y:v1","1")))
 def test_risk_direction_reversed(self):self.assertEqual(1,score(40,calibrate(self.rows,"consistency","FX:GBP:1Y:v1","1"),False))

if __name__=="__main__":unittest.main()
