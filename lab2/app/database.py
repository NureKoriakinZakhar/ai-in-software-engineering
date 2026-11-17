import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

DEFAULT_DB_PATH = Path("data") / "student_requests.sqlite3"

STAFF = ((1, "Agent A"), (2, "Agent B"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    full_name TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    urgency TEXT NOT NULL CHECK (urgency IN ('low', 'medium', 'high')),
    status TEXT NOT NULL CHECK (status IN ('OPEN', 'IN_PROGRESS', 'CLOSED')),
    assignee_id INTEGER REFERENCES staff(id),
    request_type TEXT CHECK (
        request_type IN ('ENROLLMENT_CERTIFICATE', 'STUDENT_DATA_CORRECTION')
    ),
    type_confirmed_by INTEGER REFERENCES staff(id),
    type_confirmed_at TEXT,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS service_details (
    request_id INTEGER PRIMARY KEY REFERENCES requests(id),
    kind TEXT NOT NULL CHECK (kind IN ('certificate', 'correction')),
    payload_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL REFERENCES requests(id),
    author_id INTEGER NOT NULL REFERENCES staff(id),
    text TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS resolutions (
    request_id INTEGER PRIMARY KEY REFERENCES requests(id),
    resolution_code TEXT NOT NULL CHECK (resolution_code IN ('COMPLETED', 'REJECTED')),
    result_details_json TEXT,
    rejection_reason TEXT,
    resolved_by INTEGER NOT NULL REFERENCES staff(id),
    resolved_at TEXT NOT NULL
);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = connect(db_path)
    try:
        conn.executescript(SCHEMA)
        with transaction(conn):
            conn.executemany("INSERT OR IGNORE INTO staff (id, name) VALUES (?, ?)", STAFF)
    finally:
        conn.close()


@contextmanager
def transaction(conn: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    conn.execute("BEGIN IMMEDIATE")
    try:
        yield conn
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    conn.execute("COMMIT")
