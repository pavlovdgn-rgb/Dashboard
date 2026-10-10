"""DB-API facade over remote libSQL. No production database on Vercel's /tmp disk."""
import os
import json
import sqlite3
import time
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path

_read_only = ContextVar('cloud_db_read_only', default=False)


@contextmanager
def read_only():
    """Scope read access to this request, without changing concurrent writers."""
    token = _read_only.set(True)
    try:
        yield
    finally:
        _read_only.reset(token)


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
    local_test = test_path and not os.environ.get('VERCEL')
    if local_test:
        raw = sqlite3.connect(test_path, timeout=20)
    else:
        if not configured():
            raise sqlite3.OperationalError('TURSO_DATABASE_URL and TURSO_AUTH_TOKEN are required')
        import libsql
        raw = libsql.connect(database=os.environ['TURSO_DATABASE_URL'],
                             auth_token=os.environ['TURSO_AUTH_TOKEN'], isolation_level=None)
    db = Connection(raw)
    try:
        # Reads must not reserve the single writer while snapshots/clicks arrive.
        # Keep one consistent snapshot per request; writes remain atomic.
        if _read_only.get():
            if local_test:
                db.execute('PRAGMA query_only=ON')
            db.execute('BEGIN' if local_test else 'BEGIN TRANSACTION READONLY')
        else:
            db.execute('BEGIN IMMEDIATE')
        yield db
        raw.commit()
    except BaseException:
        raw.rollback()
        raise
    finally:
        raw.close()


def migrate():
    # The common cold-start path only checks the schema; it needs no writer lock.
    with read_only():
        with connect() as db:
            existing = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cloud_schema'").fetchone()
            if existing and db.execute('SELECT version FROM cloud_schema WHERE version=3').fetchone():
                return
    with connect() as db:
        existing = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cloud_schema'").fetchone()
        if not existing or not db.execute('SELECT version FROM cloud_schema WHERE version=1').fetchone():
            db.executescript(Path(__file__).with_name('schema.sql').read_text(encoding='utf-8'))
        if not db.execute('SELECT version FROM cloud_schema WHERE version=2').fetchone():
            import live_project
            live_project.initialize(db)
            # Keep Lead Generation results, but stop every old link before exposing the new project.
            now = int(time.time() * 1000)
            for row in db.execute("SELECT id,value FROM live_studies WHERE project_id='leed-generation'"):
                config = json.loads(row['value'])
                config['enabled'] = False
                if not config.get('roundClosedAt'):
                    config['roundClosedAt'] = now
                db.execute('UPDATE live_studies SET value=? WHERE id=?', (json.dumps(config, ensure_ascii=False), row['id']))
                db.execute("UPDATE recordings SET status='stopped' WHERE study=? AND status='uploading'", (row['id'],))
            db.execute('INSERT INTO cloud_schema VALUES (2)')
        db.execute('CREATE TABLE IF NOT EXISTS deleted_studies (id TEXT PRIMARY KEY, deleted_at INTEGER NOT NULL)')
        db.execute('INSERT INTO cloud_schema VALUES (3)')
