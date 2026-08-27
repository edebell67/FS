# WF-205 Query and Index Plan

Indexes: canonical strategy ID; `(visibility,status,market)`; last-active; major sortable stats; period key; canonical relationship pair/window. Directory reads use precomputed snapshots and server-side keyset pagination. Cache keys include route, normalized query, snapshot and methodology. Publish changes snapshot atomically and clears prior entries; open state uses five-second TTL.
