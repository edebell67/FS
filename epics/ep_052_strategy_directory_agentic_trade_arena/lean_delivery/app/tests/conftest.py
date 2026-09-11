# VERSION HISTORY v2.0.0 · 2026-09-06 · Isolate each test with its own throwaway Postgres database
#   (was a throwaway SQLite file) to match records.py's move off sqlite3. Each test gets a uniquely
#   named `ep052_test_<hash>` database on the admin server, created before and dropped after; the
#   app under test finds it via EP052_DATABASE_URL exactly as it would find a real deployment's URL.
#   Point EP052_TEST_DATABASE_ADMIN_URL at a real Postgres server to run this suite (defaults to a
#   local throwaway instance on port 5544 for dev use); CREATE/DROP DATABASE need a role with that
#   privilege on the admin connection, not on the per-test database itself.
import hashlib
import os

import psycopg
import pytest

ADMIN_URL = os.environ.get('EP052_TEST_DATABASE_ADMIN_URL', 'postgresql://postgres@localhost:5544/postgres')


def _test_db_name(nodeid: str) -> str:
    # Postgres identifiers cap at 63 bytes; nodeid (file::test[params]) is often longer and
    # contains characters identifiers can't hold, so hash it into a fixed-width safe suffix.
    return 'ep052_test_' + hashlib.sha1(nodeid.encode()).hexdigest()[:16]


@pytest.fixture(autouse=True)
def isolated_exchange_database(request, monkeypatch):
    name = _test_db_name(request.node.nodeid)
    with psycopg.connect(ADMIN_URL, autocommit=True) as admin:
        admin.execute(f'DROP DATABASE IF EXISTS {name}')
        admin.execute(f'CREATE DATABASE {name}')
    database_url = ADMIN_URL.rsplit('/', 1)[0] + '/' + name
    monkeypatch.setenv('EP052_DATABASE_URL', database_url)
    try:
        yield database_url
    finally:
        with psycopg.connect(ADMIN_URL, autocommit=True) as admin:
            admin.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='{name}' AND pid<>pg_backend_pid()")
            admin.execute(f'DROP DATABASE IF EXISTS {name}')
