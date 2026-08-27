# workstreams/WF-102/test_pipeline.py — Behavioral tests for canonical closed/open ingestion.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: validates idempotency, quarantine, watermarks, precision, and role separation.

import copy
import unittest

from pipeline import CanonicalIngestion


def row(guid="g1", model="DNA_102001_S", net_return="10.125", **changes):
    value = {"guid": guid, "model": model, "signal": "BUY", "created": "2026-08-23T10:00:00+00:00", "last_update": "2026-08-23T11:00:00+00:00", "g_close_time": "2026-08-23T10:45:00+00:00", "net_return": net_return, "close_type": "target reached"}
    value.update(changes)
    return value


class PipelineTests(unittest.TestCase):
    def test_closed_replay_is_idempotent(self):
        pipeline = CanonicalIngestion()
        self.assertEqual(1, pipeline.ingest("combined_trades_closed", [row()])["accepted"])
        replay = pipeline.ingest("combined_trades_closed", [row()])
        self.assertEqual(1, replay["unchanged"])
        self.assertEqual(1, len(pipeline.closed))

    def test_conflicting_closed_replay_is_quarantined(self):
        pipeline = CanonicalIngestion(); pipeline.ingest("combined_trades_closed", [row()])
        result = pipeline.ingest("combined_trades_closed", [row(net_return="11")])
        self.assertEqual(1, result["quarantined"])
        self.assertEqual("10.12500000", str(pipeline.closed["g1"]["net_return"]))

    def test_open_updates_never_enter_closed_store(self):
        pipeline = CanonicalIngestion(); open_row = row(g_close_time=None)
        pipeline.ingest("combined_trades_open", [open_row])
        updated = copy.deepcopy(open_row); updated["net_return"] = "12"
        pipeline.ingest("combined_trades_open", [updated])
        self.assertEqual({}, pipeline.closed)
        self.assertEqual("12.00000000", str(pipeline.open["g1"]["unrealized_net_return"]))

    def test_outcome_uses_net_return_not_close_type(self):
        pipeline = CanonicalIngestion(); pipeline.ingest("combined_trades_closed", [row(net_return="-2")])
        self.assertEqual("loser", pipeline.closed["g1"]["outcome"])

    def test_alias_normalization_and_lineage(self):
        pipeline = CanonicalIngestion(); pipeline.ingest("combined_trades_closed", [row()])
        self.assertEqual("DNA_102001", pipeline.closed["g1"]["strategy_id"])
        self.assertEqual("DNA_102001_S", pipeline.closed["g1"]["source_model"])

    def test_invalid_rows_are_quarantined_with_replay_state(self):
        pipeline = CanonicalIngestion(); result = pipeline.ingest("combined_trades_closed", [row(model="NON_DNA_1")])
        self.assertEqual(1, result["quarantined"])
        self.assertEqual("pending", pipeline.quarantine[0]["replay_state"])

    def test_independent_watermarks(self):
        pipeline = CanonicalIngestion(); pipeline.ingest("combined_trades_closed", [row()]); pipeline.ingest("combined_trades_open", [row(guid="o1", g_close_time=None)])
        self.assertEqual({"combined_trades_closed", "combined_trades_open"}, set(pipeline.watermarks))


if __name__ == "__main__": unittest.main()
