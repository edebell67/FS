from pathlib import Path

from scripts.apply_hosted_migrations import preflight_database


class Cursor:
    def __init__(self, rows):
        self.rows = rows

    def fetchall(self):
        return self.rows

    def fetchone(self):
        return self.rows[0]


class Connection:
    def __init__(self, collisions=(), can_create_role=True):
        self.collisions = collisions
        self.can_create_role = can_create_role
        self.calls = []

    def execute(self, sql):
        self.calls.append(sql)
        if "information_schema.tables" in sql:
            return Cursor([(name,) for name in self.collisions])
        if "rolcreaterole" in sql:
            return Cursor([(self.can_create_role,)])
        raise AssertionError(f"Unexpected SQL: {sql}")


def test_preflight_rejects_ep051_table_collision_before_migrations():
    connection = Connection(collisions=("directory_snapshot",))

    try:
        preflight_database(connection)
    except RuntimeError as error:
        assert "directory_snapshot" in str(error)
    else:
        raise AssertionError("a table collision must stop migration")


def test_preflight_rejects_missing_role_capability_before_migrations():
    connection = Connection(can_create_role=False)

    try:
        preflight_database(connection)
    except RuntimeError as error:
        assert "CREATEROLE" in str(error)
    else:
        raise AssertionError("missing CREATEROLE must stop migration")


def test_preflight_accepts_empty_ep051_namespace_with_role_capability():
    connection = Connection()

    preflight_database(connection)

    assert len(connection.calls) == 2
