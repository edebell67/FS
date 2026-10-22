# VERSION HISTORY v2.0.0 · 2026-09-06 · Convert persistence from local SQLite to PostgreSQL. All
#   objects now live in a dedicated `ep052` schema (never the bare `public` schema) so this app can
#   share a Postgres instance with other epics without name collisions. Connects via EP052_DATABASE_URL
#   (falls back to the platform-standard DATABASE_URL). SQLite-only concerns (PRAGMA, AUTOINCREMENT,
#   file-based WAL/backup) are gone; `user_version` is replaced by a `schema_version` row in `metadata`.
#   Existing call sites elsewhere in this package are unchanged: `db.execute(sql, params)` still takes
#   `?` placeholders and rows still support both `row['col']` and `row[0]`, via the compatibility layer
#   below. One connection per transaction() call, matching the previous per-transaction sqlite3.connect
#   pattern; a pooled connection is a reasonable later optimisation, not required for this migration.
# v1.4.1 · 2026-09-02 · Refuse future database schemas instead of silently downgrading their version on startup.
# v1.4.0 · 2026-09-02 · Persist public Arena projections atomically and backfill earlier committed records once.
# v1.3.0 · 2026-09-02 · Add immutable issued-unit baselines, published quotes and atomic trade/request records.
# v1.2.0 · 2026-09-02 · Persist owner feedback, per-agent acknowledgements/replies and reported decisions.
# v1.1.0 · 2026-09-02 · Add participant funding movements and actor-scoped delivered-query records.
# v1.0.0 · 2026-09-02 · Durable identities, scoped credentials, connections and API activity with sync-stable IDs.
from contextlib import contextmanager
from datetime import datetime, timezone
import os
import re
from uuid import uuid4

import psycopg
from psycopg import IntegrityError  # re-exported: other modules catch records.IntegrityError

SCHEMA_NAME = 'ep052'
SCHEMA_VERSION = 5

SCHEMA = f'''
CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};
CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS owners (id TEXT PRIMARY KEY,name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS agents (
 id TEXT PRIMARY KEY,owner_id TEXT NOT NULL REFERENCES owners(id),name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS credentials (
 id TEXT PRIMARY KEY,token_hash TEXT UNIQUE NOT NULL,owner_id TEXT NOT NULL REFERENCES owners(id),
 agent_id TEXT REFERENCES agents(id),role TEXT NOT NULL CHECK(role IN ('owner','agent')),
 expires_at DOUBLE PRECISION NOT NULL,revoked INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS connections (
 id TEXT PRIMARY KEY,owner_id TEXT NOT NULL REFERENCES owners(id),agent_id TEXT NOT NULL REFERENCES agents(id),
 request_id TEXT NOT NULL,fingerprint TEXT NOT NULL,connected_at DOUBLE PRECISION NOT NULL,last_seen DOUBLE PRECISION NOT NULL,
 disconnected INTEGER NOT NULL DEFAULT 0,UNIQUE(agent_id,request_id));
CREATE TABLE IF NOT EXISTS activity (
 cursor BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,event_id TEXT UNIQUE NOT NULL,occurred_at TEXT NOT NULL,
 owner_id TEXT,agent_id TEXT,operation TEXT NOT NULL,status_code INTEGER NOT NULL,request_id TEXT);
CREATE TABLE IF NOT EXISTS rate_windows (
 subject TEXT PRIMARY KEY,window_ordinal BIGINT NOT NULL,count INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS participant_allocations (
 agent_id TEXT PRIMARY KEY REFERENCES agents(id),seed_usd TEXT NOT NULL,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS participant_movements (
 id TEXT PRIMARY KEY,agent_id TEXT NOT NULL REFERENCES agents(id),operation_id TEXT NOT NULL,
 kind TEXT NOT NULL,amount_usd TEXT NOT NULL,created_at TEXT NOT NULL,UNIQUE(agent_id,operation_id));
CREATE TABLE IF NOT EXISTS query_deliveries (
 id TEXT PRIMARY KEY,agent_id TEXT NOT NULL REFERENCES agents(id),request_id TEXT NOT NULL,
 revision INTEGER NOT NULL,fingerprint TEXT NOT NULL,payload TEXT NOT NULL,fee_usd TEXT NOT NULL,
 UNIQUE(agent_id,request_id,revision));
CREATE TABLE IF NOT EXISTS feedback (
 cursor BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,id TEXT UNIQUE NOT NULL,owner_id TEXT NOT NULL REFERENCES owners(id),
 request_id TEXT NOT NULL,fingerprint TEXT NOT NULL,message TEXT NOT NULL,created_at TEXT NOT NULL,
 UNIQUE(owner_id,request_id));
CREATE TABLE IF NOT EXISTS feedback_targets (
 feedback_id TEXT NOT NULL REFERENCES feedback(id),agent_id TEXT NOT NULL REFERENCES agents(id),
 acknowledged_at TEXT,PRIMARY KEY(feedback_id,agent_id));
CREATE TABLE IF NOT EXISTS feedback_replies (
 id TEXT PRIMARY KEY,feedback_id TEXT NOT NULL REFERENCES feedback(id),agent_id TEXT NOT NULL REFERENCES agents(id),
 request_id TEXT NOT NULL,fingerprint TEXT NOT NULL,message TEXT NOT NULL,created_at TEXT NOT NULL,
 UNIQUE(agent_id,request_id));
CREATE TABLE IF NOT EXISTS decision_reports (
 cursor BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,id TEXT UNIQUE NOT NULL,agent_id TEXT NOT NULL REFERENCES agents(id),
 request_id TEXT NOT NULL,fingerprint TEXT NOT NULL,payload TEXT NOT NULL,created_at TEXT NOT NULL,
 UNIQUE(agent_id,request_id));
CREATE TABLE IF NOT EXISTS strategy_units (
 strategy_id TEXT PRIMARY KEY,issued_units INTEGER NOT NULL CHECK(issued_units>0));
CREATE TABLE IF NOT EXISTS price_quotes (
 sequence BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,id TEXT UNIQUE NOT NULL,strategy_id TEXT NOT NULL REFERENCES strategy_units(strategy_id),
 source_version TEXT NOT NULL,payload TEXT NOT NULL,published_at TEXT NOT NULL,
 UNIQUE(strategy_id,source_version));
CREATE TABLE IF NOT EXISTS trade_records (
 cursor BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,id TEXT UNIQUE NOT NULL,agent_id TEXT NOT NULL REFERENCES agents(id),
 request_id TEXT NOT NULL,strategy_id TEXT NOT NULL REFERENCES strategy_units(strategy_id),side TEXT NOT NULL CHECK(side IN ('BUY','SELL')),
 units INTEGER NOT NULL CHECK(units>0),price_id TEXT NOT NULL REFERENCES price_quotes(id),payload TEXT NOT NULL,
 UNIQUE(agent_id,request_id));
CREATE TABLE IF NOT EXISTS trade_requests (
 agent_id TEXT NOT NULL REFERENCES agents(id),request_id TEXT NOT NULL,fingerprint TEXT NOT NULL,
 status_code INTEGER NOT NULL,payload TEXT NOT NULL,PRIMARY KEY(agent_id,request_id));
CREATE TABLE IF NOT EXISTS arena_events (
 cursor BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,event_id TEXT UNIQUE NOT NULL,source_key TEXT UNIQUE NOT NULL,
 occurred_at TEXT NOT NULL,agent_id TEXT NOT NULL,operation TEXT NOT NULL,strategy_id TEXT,
 resource_id TEXT NOT NULL,request_id TEXT,payload TEXT NOT NULL);
'''

_INSERT_OR_IGNORE = re.compile(r'^\s*INSERT\s+OR\s+IGNORE\s+INTO', re.IGNORECASE)


def _translate(sql: str) -> str:
    '''sqlite -> postgres call-site compatibility: existing modules were written against
    sqlite3's `?` placeholders and `INSERT OR IGNORE`. Rather than touch every call site
    across the package, translate the two sqlite-specific forms actually in use here.
    Literal `%` (e.g. LIKE 'TRADE %') must be escaped to `%%` first -- psycopg's pyformat
    paramstyle treats any bare `%` as the start of a placeholder, params or not.'''
    if _INSERT_OR_IGNORE.match(sql):
        sql = _INSERT_OR_IGNORE.sub('INSERT INTO', sql, count=1) + ' ON CONFLICT DO NOTHING'
    return sql.replace('%', '%%').replace('?', '%s')


class _HybridRow:
    '''Supports both row['col'] and row[0], like sqlite3.Row, so existing call sites
    (some keyed, some positional) work unchanged against psycopg.'''
    __slots__ = ('_values', '_index')

    def __init__(self, index, values):
        self._index = index
        self._values = values

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._values[key]
        return self._values[self._index[key]]

    def keys(self):
        return self._index.keys()

    def __repr__(self):
        return repr(dict(zip(self._index, self._values)))


def _hybrid_row_factory(cursor):
    index = {c.name: i for i, c in enumerate(cursor.description or [])}
    return lambda values: _HybridRow(index, values)


class _CompatConnection:
    '''Wraps a psycopg connection so callers written against sqlite3's Connection.execute()
    convenience method keep working: `?` placeholders, INSERT OR IGNORE, dict/positional rows.'''

    def __init__(self, conn):
        self._conn = conn

    def execute(self, sql, params=()):
        return self._conn.execute(_translate(sql), params)

    def executemany(self, sql, seq_of_params):
        cur = self._conn.cursor()
        cur.executemany(_translate(sql), list(seq_of_params))
        return cur

    def executescript(self, script):
        cur = self._conn.cursor()
        for statement in filter(None, (s.strip() for s in script.split(';'))):
            cur.execute(statement)
        return cur

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._conn.close()


def _database_url() -> str:
    url = os.environ.get('EP052_DATABASE_URL') or os.environ.get('DATABASE_URL')
    if not url:
        raise ValueError('EP052_DATABASE_URL (or DATABASE_URL) is not set')
    return url


class Store:
    def __init__(self, database_url: str | None = None):
        self.database_url = database_url or _database_url()
        with self.transaction() as db:
            db.executescript(SCHEMA)
            row = db.execute('SELECT value FROM metadata WHERE key=?', ('schema_version',)).fetchone()
            current = int(row['value']) if row else 0
            if current > SCHEMA_VERSION:
                raise ValueError('DATABASE_SCHEMA_NEWER_THAN_APPLICATION')
            db.execute('INSERT INTO metadata VALUES (?,?) ON CONFLICT (key) DO NOTHING', ('instance_id', str(uuid4())))
            from .arena import backfill
            backfill(db)
            db.execute(
                "INSERT INTO metadata VALUES ('schema_version',?) ON CONFLICT (key) DO UPDATE SET value=excluded.value",
                (str(SCHEMA_VERSION),))

    @contextmanager
    def transaction(self, immediate=False):
        # `immediate` was SQLite's BEGIN IMMEDIATE: it serialised ALL writers on the single
        # database file, so a check-then-insert (e.g. "does this request_id already exist?"
        # then insert if not) could never race -- a second concurrent immediate transaction
        # simply blocked until the first committed, then saw its row. Postgres's MVCC has no
        # implicit equivalent: two concurrent transactions under READ COMMITTED can both pass
        # the check and both attempt the insert, and the loser gets a UniqueViolation instead
        # of blocking (caught the hard way: exact-retry/concurrent-settlement tests started
        # failing with UniqueViolation once this ran against real concurrency). A session-scoped
        # Postgres advisory lock reproduces the same whole-database single-writer serialisation:
        # it blocks other immediate transactions until this one commits/rolls back, at which
        # point it's released automatically (pg_advisory_xact_lock is transaction-scoped).
        conn = psycopg.connect(
            self.database_url,
            options=f'-c search_path={SCHEMA_NAME},public',
            row_factory=_hybrid_row_factory,
            autocommit=False,
        )
        db = _CompatConnection(conn)
        try:
            if immediate:
                db.execute('SELECT pg_advisory_xact_lock(8052)')
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def record(self, operation, status_code, actor=None, request_id=None):
        actor = actor or {}
        with self.transaction() as db:
            db.execute('INSERT INTO activity(event_id,occurred_at,owner_id,agent_id,operation,status_code,request_id) VALUES (?,?,?,?,?,?,?)',
                       (str(uuid4()), datetime.now(timezone.utc).isoformat(), actor.get('owner_id'),
                        actor.get('agent_id'), operation, status_code, request_id))

    def rate_allowed(self, subject, now, window_seconds, limit):
        window = int(now // window_seconds)
        with self.transaction(immediate=True) as db:
            row = db.execute('SELECT window_ordinal,count FROM rate_windows WHERE subject=?', (subject,)).fetchone()
            count = row['count'] + 1 if row and row['window_ordinal'] == window else 1
            db.execute('INSERT INTO rate_windows VALUES (?,?,?) ON CONFLICT(subject) DO UPDATE SET window_ordinal=excluded.window_ordinal,count=excluded.count',
                       (subject, window, count))
            return count <= limit
