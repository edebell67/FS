# db_utils.py
"""
Database Utility Functions for PostgreSQL
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file in the parent directory
load_dotenv(Path(__file__).parent / ".env")

def get_db_connection():
    """
    Establishes and returns a new database connection.
    Each part of the application should get its own connection.
    """
    try:
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        print(f"[DEBUG] DB Connecting to: {db_name} at {db_host}:{db_port} as {db_user}")
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=os.getenv("DB_PASSWORD"),
            host=db_host,
            port=db_port
        )
        return conn
    except Exception as e:
        print(f"[ERROR] Could not connect to the database: {e}")
        raise

def execute_query(query: str, params: tuple = None, fetch: str = None, commit: bool = False):
    """
    Execute a SQL query.

    :param query: The SQL query to execute.
    :param params: The parameters to substitute in the query.
    :param fetch: Type of fetch ('one', 'all'). If None, no fetch is performed.
    :param commit: If True, commits the transaction.
    :return: The result of the fetch operation, or None.
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            
            if commit:
                conn.commit()

            if fetch == 'one':
                return cursor.fetchone()
            if fetch == 'all':
                return cursor.fetchall()
    except Exception as e:
        if conn:
            conn.rollback()
        snippet = query.strip().splitlines() if isinstance(query, str) else []
        preview = ' '.join(snippet[:3])
        print(f"[ERROR] Query failed: {e} | SQL: {preview} | Params: {params}")
        if fetch == 'all':
            return []
        if fetch == 'one':
            return {}
        return None
    finally:
        if conn:
            conn.close()

def execute_many(query: str, data_list: list):
    """
    Execute a SQL query for many items (e.g., bulk INSERT).

    :param query: The SQL query with placeholders.
    :param data_list: A list of tuples/dicts with the data to insert.
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.executemany(query, data_list)
            conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[ERROR] Bulk execution failed: {e}")
        raise
    finally:
        if conn:
            conn.close()

def execute_schema_script(script_path: str):
    """
    Executes a .sql file to set up the database schema.

    :param script_path: The full path to the .sql schema file.
    """
    try:
        with open(script_path, 'r') as f:
            sql_script = f.read()

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql_script)
            conn.commit()
        conn.close()
        print(f"[SUCCESS] Schema script '{script_path}' executed successfully.")
    except Exception as e:
        print(f"[ERROR] Schema script execution failed: {e}")
        raise


# ─────────────────────────────────────────────
# [V20260120_WS5] Helper Functions
# ─────────────────────────────────────────────

def fetch_one(query: str, params: tuple = None):
    """
    [V20260120_WS5] Execute a query and fetch one result.
    Wrapper around execute_query for convenience.
    """
    return execute_query(query, params, fetch='one')


def fetch_all(query: str, params: tuple = None):
    """
    [V20260120_WS5] Execute a query and fetch all results.
    Wrapper around execute_query for convenience.
    """
    return execute_query(query, params, fetch='all')


# ─────────────────────────────────────────────
# [V20260120_WS5] Transaction Support
# ─────────────────────────────────────────────

class Transaction:
    """
    [V20260120_WS5] Context manager for database transactions.
    Provides atomic execution with automatic rollback on error.

    Usage:
        with Transaction() as txn:
            txn.execute("INSERT INTO ...", (...))
            txn.execute("UPDATE ...", (...))
            # Auto-commits on successful exit
            # Auto-rollback on exception
    """

    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = get_db_connection()
        self.conn.autocommit = False
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
                print(f"[TRANSACTION] Rolled back due to: {exc_val}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        return False  # Don't suppress exceptions

    def execute(self, query: str, params: tuple = None, fetch: str = None):
        """
        Execute a query within the transaction.

        :param query: SQL query to execute
        :param params: Query parameters
        :param fetch: 'one' or 'all' to fetch results, None otherwise
        :return: Query result if fetch specified
        """
        self.cursor.execute(query, params)
        if fetch == 'one':
            return self.cursor.fetchone()
        if fetch == 'all':
            return self.cursor.fetchall()
        return None

    def fetchone(self):
        """Fetch one result from the last query."""
        return self.cursor.fetchone()

    def fetchall(self):
        """Fetch all results from the last query."""
        return self.cursor.fetchall()


def execute_in_transaction(queries: list) -> bool:
    """
    [V20260120_WS5] Execute multiple queries in a single transaction.

    :param queries: List of tuples [(query, params), ...]
    :return: True if successful, False if rolled back
    """
    try:
        with Transaction() as txn:
            for query, params in queries:
                txn.execute(query, params)
        return True
    except Exception as e:
        print(f"[TRANSACTION] Failed: {e}")
        return False