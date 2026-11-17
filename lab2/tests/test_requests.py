import pytest

from tests.conftest import CERT_FULL, MINIMAL, create, error_of, fields_of


def count(client) -> int:
    return len(client.get("/requests").json())


def test_create_defaults(client):
    response = client.post("/requests", json=MINIMAL)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] >= 1
    assert body["status"] == "OPEN"
    assert body["description"] == ""
    assert body["urgency"] == "medium"
    assert body["request_type"] is None
    assert body["type_confirmed_by"] is None and body["type_confirmed_at"] is None
    assert body["assignee_id"] is None and body["resolution"] is None
    assert body["created_at"] == "2026-10-10T10:00:00Z"
    assert body["completeness"] == {
        "type_confirmed": False,
        "is_complete": False,
        "missing_fields": ["request_type"],
    }


@pytest.mark.parametrize("length, expected", [(2, 422), (3, 201), (120, 201), (121, 422)])
def test_create_title_boundaries(client, length, expected):
    title = "Д" * length
    response = client.post("/requests", json={**MINIMAL, "title": f"  {title} "})
    assert response.status_code == expected
    if expected == 201:
        assert response.json()["title"] == title
    else:
        assert fields_of(response) == ["body.title"]


@pytest.mark.parametrize(
    "change, field",
    [
        ({"student_id": None}, "body.student_id"),
        ({"title": 123}, "body.title"),
        ({"full_name": "  Аб  "}, "body.full_name"),
        ({"student_id": "   "}, "body.student_id"),
        ({"student_id": "S" * 33}, "body.student_id"),
        ({"description": "x" * 2001}, "body.description"),
        ({"urgency": "HIGH"}, "body.urgency"),
        ({"assignee_id": 3}, "body.assignee_id"),
        ({"assignee_id": "1"}, "body.assignee_id"),
        ({"id": 5}, "body.id"),
        ({"status": "CLOSED"}, "body.status"),
        ({"request_type": "ENROLLMENT_CERTIFICATE"}, "body.request_type"),
        ({"type_confirmed_by": 1}, "body.type_confirmed_by"),
        ({"created_at": "2026-10-10T10:00:00Z"}, "body.created_at"),
        ({"certificate_details": {}}, "body.certificate_details"),
        ({"certificate_details": {"language": "UK"}}, "body.certificate_details.language"),
        ({"certificate_details": {"color": "red"}}, "body.certificate_details.color"),
        (
            {
                "certificate_details": {"language": "uk"},
                "correction_details": {"target_field": "x"},
            },
            "body.correction_details",
        ),
        (
            {"correction_details": {"current_value": "A", "proposed_value": " A "}},
            "body.correction_details.proposed_value",
        ),
    ],
)
def test_create_invalid_fields(client, change, field):
    body = {**MINIMAL, **change}
    response = client.post("/requests", json=body)
    assert response.status_code == 422
    assert error_of(response)["code"] == "VALIDATION_ERROR"
    assert field in fields_of(response)
    assert count(client) == 0


def test_create_missing_required(client):
    body = {k: v for k, v in MINIMAL.items() if k != "student_id"}
    response = client.post("/requests", json=body)
    assert response.status_code == 422
    assert fields_of(response) == ["body.student_id"]
    assert count(client) == 0


def test_create_bad_json(client):
    bad = client.post(
        "/requests", content=b'{"title": ', headers={"content-type": "application/json"}
    )
    assert bad.status_code == 422
    assert fields_of(bad) == ["body"]
    assert client.post("/requests").status_code == 422
    assert count(client) == 0


def test_create_partial_details(client):
    body = create(client, certificate_details={"purpose": "  Для банку  "})
    assert body["certificate_details"] == {
        "language": None,
        "purpose": "Для банку",
        "delivery_method": None,
    }
    assert body["correction_details"] is None


def test_read_missing(client):
    created = create(client, certificate_details=CERT_FULL, urgency="high")
    assert client.get(f"/requests/{created['id']}").json() == created
    assert client.get("/requests").json() == [created]
    response = client.get("/requests/999")
    assert response.status_code == 404
    assert error_of(response) == {
        "code": "REQUEST_NOT_FOUND",
        "message": "Звернення з id=999 не знайдено.",
        "details": [],
    }


@pytest.mark.parametrize("raw", ["abc", "0", "-1", "1.5", "99999999999999999999"])
def test_read_invalid_id(client, raw):
    response = client.get(f"/requests/{raw}")
    assert response.status_code == 422
    assert fields_of(response) == ["path.id"]


def test_request_order(client, clock):
    first = create(client)
    clock.frozen = True
    second, third = create(client), create(client)
    assert second["created_at"] == third["created_at"] > first["created_at"]
    ids = [r["id"] for r in client.get("/requests").json()]
    assert ids == [first["id"], second["id"], third["id"]]
    assert len(set(ids)) == 3


def test_get_rejects_body_and_unknown_query(client):
    created = create(client)
    response = client.request("GET", f"/requests/{created['id']}", content=b"{}")
    assert response.status_code == 422
    assert fields_of(response) == ["body"]
    response = client.get(f"/requests/{created['id']}?verbose=1")
    assert fields_of(response) == ["query.verbose"]


def test_error_examples_match_contract(client):
    validation = "Некоректні дані запиту."
    response = client.post("/requests", json={**MINIMAL, "title": "  Д "})
    assert error_of(response) == {
        "code": "VALIDATION_ERROR",
        "message": validation,
        "details": [
            {"field": "body.title", "reason": "Після trim потрібно від 3 до 120 символів."}
        ],
    }
    response = client.get("/requests?urgency=HIGH")
    assert error_of(response)["details"] == [
        {"field": "query.urgency", "reason": "Допустимі low, medium, high."}
    ]
    response = client.get("/requests/abc")
    assert error_of(response)["details"] == [
        {"field": "path.id", "reason": "Потрібне додатне ціле число."}
    ]
