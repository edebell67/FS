# workstreams/WF-205/cache.py — Snapshot-versioned query cache with atomic invalidation and open-state TTL.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: prevents stale snapshot reuse across atomic publishes.

import hashlib,json,time

class SnapshotCache:
 def __init__(self,open_ttl=5):self.snapshot="none";self.data={};self.open_ttl=open_ttl
 def key(self,route,query,methodology):return hashlib.sha256(json.dumps([self.snapshot,route,sorted(query.items()),methodology]).encode()).hexdigest()
 def put(self,key,value,ttl=300):self.data[key]=(value,time.monotonic()+ttl)
 def get(self,key):
  item=self.data.get(key)
  if not item or item[1]<time.monotonic():self.data.pop(key,None);return None
  return item[0]
 def publish(self,new_snapshot):self.snapshot=new_snapshot;self.data.clear()
 def put_open(self,key,value):self.put(key,value,self.open_ttl)

