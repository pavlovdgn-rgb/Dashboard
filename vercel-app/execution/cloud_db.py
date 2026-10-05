"""DB-API facade over remote libSQL. No production database on Vercel's /tmp disk."""
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path


class Row:
    def __init__(self, columns, values):
        self.columns = columns
        self.values = tuple(values)
        self.mapping = dict(zip(columns, self.values))

    def __getitem__(self, key):
        return self.values[key] if isinstance(key, (int, slice)) else self.mapping[key]

    def keys(self):
        return self.columns

    def __iter__(self):
        return iter(self.values)


class Cursor:
    def __init__(self, cursor):
        self.cursor = cursor
        self.columns = [column[0] for column in (cursor.description or [])]

    def fetchone(self):
        row = self.cursor.fetchone()
        return None if row is None else Row(self.columns, row)

    def fetchall(self):
        return [Row(self.columns, row) for row in self.cursor.fetchall()]

    def __iter__(self):
        return iter(self.fetchall())


class Connection:
    def __init__(self, raw):
        self.raw = raw

    def execute(self, sql, parameters=()):
        try:
            return Cursor(self.raw.execute(sql, parameters))
        except Exception as error:
            raise sqlite3.OperationalError('Cloud database operation failed') from error

    def executescript(self, sql):
        # Migrations contain no triggers or semicolons inside literal values.
        for statement in sql.split(';'):
            if statement.strip():
                self.execute(statement)


def configured():
    return bool(os.environ.get('TURSO_DATABASE_URL') and os.environ.get('TURSO_AUTH_TOKEN'))


@contextmanager
def connect(_path=None):
    test_path = os.environ.get('UXLAB_TEST_DB')
    if test_path and not os.environ.get('VERCEL'):
        raw = sqlite3.connect(test_path, timeout=20)
    else:
        if not configured():
            raise sqlite3.OperationalError('TURSO_DATABASE_URL and TURSO_AUTH_TOKEN are required')
        import libsql
        raw = libsql.connect(database=os.environ['TURSO_DATABASE_URL'],
                             auth_token=os.environ['TURSO_AUTH_TOKEN'], isolation_level=None)
    db = Connection(raw)
    try:
        # A whole API operation is atomic, including identity checks followed by inserts.
        db.execute('BEGIN IMMEDIATE')
        yield db
        raw.commit()
    except BaseException:
        raw.rollback()
        raise
    finally:
        raw.close()


def migrate():
    with connect() as db:
        existing = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cloud_schema'").fetchone()
        if existing and db.execute('SELECT version FROM cloud_schema WHERE version=1').fetchone():
            return
        db.executescript(Path(__file__).with_name('schema.sql').read_text(encoding='utf-8'))
