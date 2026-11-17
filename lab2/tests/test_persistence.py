from fastapi.testclient import TestClient

from app.main import create_app
from tests.conftest import CERT_FULL, FakeClock, confirm, create


def test_persistence_restart(db_path, clock):
    first = TestClient(create_app(db_path, clock))
    request = create(first, certificate_details=CERT_FULL)
    confirm(first, request["id"], "ENROLLMENT_CERTIFICATE")
    first.post(f"/requests/{request['id']}/comments", json={"author_id": 2, "text": "Готово"})
    first.post(
        f"/requests/{request['id']}/close",
        json={
            "resolution": {
                "resolution_code": "COMPLETED",
                "result_details": {"certificate_number": "CERT-1", "issued_on": "2026-10-10"},
                "resolved_by": 1,
            }
        },
    )
    detail = first.get(f"/requests/{request['id']}").json()
    comments = first.get(f"/requests/{request['id']}/comments").json()
    assert detail["status"] == "CLOSED"

    second = TestClient(create_app(db_path, FakeClock()))
    assert second.get(f"/requests/{request['id']}").json() == detail
    assert second.get(f"/requests/{request['id']}/comments").json() == comments
    assert second.get("/staff").json() == [
        {"id": 1, "name": "Agent A"},
        {"id": 2, "name": "Agent B"},
    ]
    assert create(second)["id"] == request["id"] + 1


def test_test_db_is_temporary(db_path, client):
    create(client)
    assert db_path.exists()
    assert "student_requests" not in str(db_path)
