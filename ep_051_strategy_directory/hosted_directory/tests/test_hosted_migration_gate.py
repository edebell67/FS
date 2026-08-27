from scripts.apply_hosted_migrations import preflight_database


class Cursor:
    def __init__(self, rows):
        self.rows = rows

    def fetchall(self):
        return self.rows

    def fetchone(self):
        return self.rows[0]


class Connection:
    def __init__(self, collisions=(), can_bypass_rls=False):
        self.collisions = collisions
        self.can_bypass_rls = can_bypass_rls
        self.calls = []

    def execute(self, sql):
        self.calls.append(sql)
        if "information_schema.tables" in sql:
            return Cursor([(name,) for name in self.collisions])
        if "rolbypassrls" in sql:
            return Cursor([(self.can_bypass_rls,)])
        raise AssertionError(f"Unexpected SQL: {sql}")


def test_preflight_rejects_unknown_ep051_prefix_table_before_migrations():
    connection = Connection(collisions=("directory_unrelated",))

    try:
        preflight_database(connection)
    except RuntimeError as error:
        assert "directory_unrelated" in str(error)
    else:
        raise AssertionError("an unknown table collision must stop migration")


def test_preflight_allows_known_ep051_tables_after_interrupted_first_run():
    connection = Connection(collisions=("directory_snapshot", "intelligence_user_history"))

    can_create_retention_owner = preflight_database(connection)

    assert can_create_retention_owner is False
    assert len(connection.calls) == 2


def test_preflight_enables_retention_migration_only_for_bypass_rls_operator():
    connection = Connection(can_bypass_rls=True)

    can_create_retention_owner = preflight_database(connection)

    assert can_create_retention_owner is True
