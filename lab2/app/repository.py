import json
import sqlite3

from app.models import DETAILS_KIND, KIND_TO_DETAILS

REQUEST_COLUMNS = (
    "student_id",
    "full_name",
    "title",
    "description",
    "urgency",
    "status",
    "assignee_id",
    "request_type",
    "type_confirmed_by",
    "type_confirmed_at",
)

_SELECT_REQUEST = """
SELECT r.*, d.kind AS details_kind, d.payload_json,
       s.resolution_code, s.result_details_json, s.rejection_reason,
       s.resolved_by, s.resolved_at
FROM requests r
LEFT JOIN service_details d ON d.request_id = r.id
LEFT JOIN resolutions s ON s.request_id = r.id
"""


def _to_request(row: sqlite3.Row) -> dict:
    request = {"id": row["id"], "created_at": row["created_at"]}
    request.update({column: row[column] for column in REQUEST_COLUMNS})
    request["certificate_details"] = None
    request["correction_details"] = None
    if row["details_kind"] is not None:
        request[KIND_TO_DETAILS[row["details_kind"]]] = json.loads(row["payload_json"])
    request["resolution"] = None
    if row["resolution_code"] is not None:
        result = row["result_details_json"]
        request["resolution"] = {
            "resolution_code": row["resolution_code"],
            "result_details": json.loads(result) if result is not None else None,
            "rejection_reason": row["rejection_reason"],
            "resolved_by": row["resolved_by"],
            "resolved_at": row["resolved_at"],
        }
    return request


def fetch_request(conn: sqlite3.Connection, request_id: int) -> dict | None:
    row = conn.execute(_SELECT_REQUEST + " WHERE r.id = ?", (request_id,)).fetchone()
    return _to_request(row) if row is not None else None


def fetch_requests(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(_SELECT_REQUEST + " ORDER BY r.created_at ASC, r.id ASC").fetchall()
    return [_to_request(row) for row in rows]


def request_exists(conn: sqlite3.Connection, request_id: int) -> bool:
    row = conn.execute("SELECT 1 FROM requests WHERE id = ?", (request_id,)).fetchone()
    return row is not None


def insert_request(conn: sqlite3.Connection, values: dict, created_at: str) -> int:
    columns = (*REQUEST_COLUMNS, "created_at")
    params = [values[c] for c in REQUEST_COLUMNS] + [created_at]
    placeholders = ", ".join("?" for _ in columns)
    cursor = conn.execute(
        f"INSERT INTO requests ({', '.join(columns)}) VALUES ({placeholders})", params
    )
    return cursor.lastrowid


def update_request(conn: sqlite3.Connection, request_id: int, changes: dict) -> None:
    unknown = set(changes) - set(REQUEST_COLUMNS)
    if unknown:
        raise ValueError(f"Недозволені колонки: {sorted(unknown)}")
    if not changes:
        return
    assignments = ", ".join(f"{column} = ?" for column in changes)
    conn.execute(
        f"UPDATE requests SET {assignments} WHERE id = ?",
        [*changes.values(), request_id],
    )


def save_details(conn: sqlite3.Connection, request_id: int, request: dict) -> None:
    conn.execute("DELETE FROM service_details WHERE request_id = ?", (request_id,))
    for name, kind in DETAILS_KIND.items():
        if request[name] is not None:
            conn.execute(
                "INSERT INTO service_details (request_id, kind, payload_json) VALUES (?, ?, ?)",
                (request_id, kind, json.dumps(request[name], ensure_ascii=False)),
            )


def insert_resolution(conn: sqlite3.Connection, request_id: int, resolution: dict) -> None:
    result = resolution["result_details"]
    conn.execute(
        "INSERT INTO resolutions (request_id, resolution_code, result_details_json,"
        " rejection_reason, resolved_by, resolved_at) VALUES (?, ?, ?, ?, ?, ?)",
        (
            request_id,
            resolution["resolution_code"],
            json.dumps(result, ensure_ascii=False) if result is not None else None,
            resolution["rejection_reason"],
            resolution["resolved_by"],
            resolution["resolved_at"],
        ),
    )


def insert_comment(
    conn: sqlite3.Connection, request_id: int, author_id: int, text: str, created_at: str
) -> int:
    cursor = conn.execute(
        "INSERT INTO comments (request_id, author_id, text, created_at) VALUES (?, ?, ?, ?)",
        (request_id, author_id, text, created_at),
    )
    return cursor.lastrowid


def fetch_comments(conn: sqlite3.Connection, request_id: int) -> list[dict]:
    rows = conn.execute(
        "SELECT id, request_id, author_id, text, created_at FROM comments"
        " WHERE request_id = ? ORDER BY created_at ASC, id ASC",
        (request_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def fetch_comment(conn: sqlite3.Connection, comment_id: int) -> dict:
    row = conn.execute(
        "SELECT id, request_id, author_id, text, created_at FROM comments WHERE id = ?",
        (comment_id,),
    ).fetchone()
    return dict(row)


def fetch_staff(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("SELECT id, name FROM staff ORDER BY id ASC").fetchall()
    return [dict(row) for row in rows]
