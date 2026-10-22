import importlib.util
from pathlib import Path
import unittest

TARGET = Path(__file__).parents[2] / "solution" / "database" / "migrate.py"
SPEC = importlib.util.spec_from_file_location("ep051_migrate", TARGET)
MODULE = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MODULE)

class MigrationTests(unittest.TestCase):
    def test_plan_is_complete_unique_and_hashed(self):
        result = MODULE.plan()
        self.assertEqual(7, len(result))
        self.assertEqual(len(result), len({x["id"] for x in result}))
        self.assertTrue(all(len(x["sha256"]) == 64 for x in result))

    def test_bootstrap_and_seed_are_idempotent(self):
        db = TARGET.parent
        self.assertIn("IF NOT EXISTS", (db / "schema.sql").read_text(encoding="utf-8"))
        self.assertIn("ON CONFLICT", (db / "seed.sql").read_text(encoding="utf-8"))

if __name__ == "__main__": unittest.main()
