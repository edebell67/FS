"""Beta evidence checks. Version 1.0.0 (2026-08-23)."""
import unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
def text(node,file):return (ROOT/node/file).read_text(encoding="utf-8")
class Tests(unittest.TestCase):
 def test_directory_has_evidence_and_quality(self):
  body=text("WF-301","directory.html");self.assertIn("closed trades",body);self.assertIn("quality",body.lower())
 def test_strategy_explains_outcomes_costs_and_forecast_limit(self):
  body=text("WF-302","strategy.html");
  for term in ("costs already included","not a forecast","exit description, not an outcome"):self.assertIn(term.lower(),body.lower())
 def test_compare_explains_compatibility_and_no_winner(self):
  body=text("WF-303","compare.html");self.assertIn("Why no “winner”?",body);self.assertIn("Comparison blocked",body)
 def test_builder_explains_selection_and_exclusions(self):
  body=text("WF-504","builder.html");self.assertIn("Why these strategies?",body);self.assertIn("excluded · quality",body)
 def test_builder_preserves_warnings(self):self.assertIn("warnings",text("WF-504","builder.html"))
 def test_no_historical_outcome_tuning_claim(self):self.assertIn("Historical return was not used as a ranking shortcut",text("WF-504","builder.html"))
if __name__=="__main__":unittest.main()

