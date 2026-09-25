# EP047 schema-only archive

This is a data-free, code-derived archive created while all Render databases and application compute were suspended. It is **not** a live database dump.

Files:

- `EP047_SCHEMA_ARCHIVE.json` — Drizzle schema source, ordered raw migrations, journal, snapshots, SHA-256 integrity values, and explicit exclusions.
- `EP047_SCHEMA_ONLY_APPLY.sql` — a candidate DDL-only bundle. DML is commented out intentionally.

Do not run the SQL bundle until a live inventory confirms the destination is appropriate, required extensions are available, and a specific paid activation window is approved.
