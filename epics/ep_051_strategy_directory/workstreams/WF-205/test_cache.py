# workstreams/WF-205/test_cache.py — Snapshot, invalidation, key, and TTL correctness tests.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: proves stale content cannot survive publish and cache keys are query/version scoped.

import time,unittest
from cache import SnapshotCache
class Tests(unittest.TestCase):
 def test_query_changes_key(self):
  c=SnapshotCache();self.assertNotEqual(c.key("list",{"a":1},"1"),c.key("list",{"a":2},"1"))
 def test_methodology_changes_key(self):
  c=SnapshotCache();self.assertNotEqual(c.key("list",{},"1"),c.key("list",{},"2"))
 def test_publish_clears_stale(self):
  c=SnapshotCache();k=c.key("list",{},"1");c.put(k,"old");c.publish("new");self.assertIsNone(c.get(k))
 def test_snapshot_changes_key(self):
  c=SnapshotCache();a=c.key("list",{},"1");c.publish("new");self.assertNotEqual(a,c.key("list",{},"1"))
 def test_open_ttl(self):
  c=SnapshotCache(open_ttl=.001);c.put_open("o",1);time.sleep(.003);self.assertIsNone(c.get("o"))
if __name__=="__main__":unittest.main()
