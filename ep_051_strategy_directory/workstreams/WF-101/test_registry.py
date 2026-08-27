# workstreams/WF-101/test_registry.py — Unit and contract coverage for immutable DNA registry behavior.
#
# VERSION HISTORY
# v1.1.0 · 2026-08-23 · Adds migration-contract assertions so persistence controls are validated with the Python registry behavior.
# v1.0.0 · 2026-08-23 · Initial version: tests normalization, collision rejection, immutable hashes, and mutable names.

from __future__ import annotations

import copy
import unittest
from pathlib import Path

from generate_seed_manifest import build_records
from registry import definition_hash, normalize_strategy_id, validate_seed_records


class RegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = build_records()

    def test_population_and_normalized_aliases(self) -> None:
        self.assertEqual(300, len(self.records))
        self.assertEqual("DNA_102001", normalize_strategy_id(" dna_102001_s "))
        self.assertEqual("DNA_102001", normalize_strategy_id("DNA_102001_B"))

    def test_manifest_has_unique_ids_aliases_and_definitions(self) -> None:
        validate_seed_records(self.records)

    def test_definition_change_changes_hash(self) -> None:
        original = self.records[0]["definition"]
        changed = copy.deepcopy(original)
        changed["entry_lookback"] += 1
        self.assertNotEqual(definition_hash(original), definition_hash(changed))

    def test_descriptive_name_does_not_change_definition_hash(self) -> None:
        record = copy.deepcopy(self.records[0])
        before = record["definition_hash"]
        record["descriptive_name"] = "Name supplied later"
        self.assertEqual(before, definition_hash(record["definition"]))

    def test_collision_is_rejected(self) -> None:
        records = copy.deepcopy(self.records)
        records[1]["strategy_id"] = records[0]["strategy_id"]
        with self.assertRaisesRegex(ValueError, "duplicate canonical strategy ID"):
            validate_seed_records(records)

    def test_invalid_non_dna_identifier_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            normalize_strategy_id("NON_DNA_102001")

    def test_migration_enforces_lineage_aliases_and_immutability(self) -> None:
        migration = (Path(__file__).parent / "migrations" / "001_strategy_registry.sql").read_text(encoding="utf-8")
        required_contracts = (
            "CREATE TABLE IF NOT EXISTS dna_directory.dna_strategy (",
            "CREATE TABLE IF NOT EXISTS dna_directory.dna_strategy_definition (",
            "CREATE TABLE IF NOT EXISTS dna_directory.dna_strategy_source_alias (",
            "UNIQUE (definition_hash)",
            "prevent_definition_identity_mutation",
            "descriptive_name text",
        )
        for contract in required_contracts:
            with self.subTest(contract=contract):
                self.assertIn(contract, migration)


if __name__ == "__main__":
    unittest.main()
