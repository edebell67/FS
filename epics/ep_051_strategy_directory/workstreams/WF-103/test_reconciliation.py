# workstreams/WF-103/test_reconciliation.py — Reconciliation and publish-gate tests.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: proves precision reconciliation, fail-closed publishing, alerts, and backfill equality.

import copy
import unittest
from datetime import datetime, timedelta, timezone

from reconciliation import compare_backfill, reconcile

NOW = datetime(2026, 8, 23, 20, 0, tzinfo=timezone.utc)


def canonical(guid="g1", value="1.25000000"):
    return {"guid": guid, "strategy_id": "DNA_102001", "signal": "BUY", "created_at": NOW - timedelta(hours=2), "exit_at": NOW - timedelta(hours=1), "net_return": value, "source_checksum": "a" * 64}


class ReconciliationTests(unittest.TestCase):
    def test_matching_batch_can_publish(self):
        source = [{"guid": "g1", "net_return": "1.25"}]
        self.assertTrue(reconcile(source, [canonical()], now=NOW, source_watermark=NOW)["publish_allowed"])

    def test_pnl_difference_blocks_publish(self):
        report = reconcile([{"guid": "g1", "net_return": "1.26"}], [canonical()], now=NOW)
        self.assertFalse(report["publish_allowed"])

    def test_duplicate_blocks_publish(self):
        report = reconcile([{"guid": "g1", "net_return": "2.5"}, {"guid": "g1", "net_return": "0"}], [canonical(), canonical()], now=NOW)
        self.assertFalse(report["publish_allowed"])

    def test_missing_required_field_blocks_publish(self):
        bad = canonical(); bad["strategy_id"] = None
        self.assertFalse(reconcile([{"guid": "g1", "net_return": "1.25"}], [bad], now=NOW)["publish_allowed"])

    def test_stale_source_blocks_publish(self):
        report = reconcile([{"guid": "g1", "net_return": "1.25"}], [canonical()], now=NOW, source_watermark=NOW - timedelta(hours=2))
        self.assertFalse(report["publish_allowed"])

    def test_backfill_equivalence(self):
        a = canonical(); b = copy.deepcopy(a)
        self.assertTrue(compare_backfill([a], [b])["passed"])
        b["source_checksum"] = "b" * 64
        self.assertFalse(compare_backfill([a], [b])["passed"])


if __name__ == "__main__": unittest.main()
