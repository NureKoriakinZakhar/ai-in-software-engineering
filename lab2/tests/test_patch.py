import pytest

from tests.conftest import (
    CERT_FULL,
    CORR_FULL,
    certificate_ready,
    confirm,
    correction_ready,
    create,
    error_of,
    fields_of,
    reject,
)

CERT = "ENROLLMENT_CERTIFICATE"
CORR = "STUDENT_DATA_CORRECTION"


def patch(client, request_id, body):
    return client.patch(f"/requests/{request_id}", json=body)


def get(client, request_id):
    return client.get(f"/requests/{request_id}").json()


def start(client, request_id):
    response = client.patch(f"/requests/{request_id}/status", json={"status": "IN_PROGRESS"})
    assert response.status_code == 200, response.text
    return response.json()


@pytest.mark.parametrize("confirmed", [False, True])
def test_patch_merge(client, confirmed):
    request = create(client, certificate_details={"purpose": "Для банку"})
    if confirmed:
        request = confirm(client, request["id"], CERT)
    response = patch(
        client,
        request["id"],
        {"description": "Додано опис", "certificate_details": {"language": "en"}},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == request["title"]
    assert body["description"] == "Додано опис"
    assert body["certificate_details"] == {
        "language": "en",
        "purpose": "Для банку",
        "delivery_method": None,
    }
    assert body["type_confirmed_at"] == request["type_confirmed_at"]


@pytest.mark.parametrize(
    "body",
    [
        {"title": None},
        {"description": None},
        {"urgency": None},
        {"student_id": None},
        {"full_name": None},
        {"request_type": None, "type_confirmed_by": 1},
        {"request_type": CERT, "type_confirmed_by": None},
    ],
)
def test_patch_null_nonnullable(client, body):
    request = create(client)
    response = patch(client, request["id"], body)
    assert response.status_code == 422
    assert get(client, request["id"]) == request


def test_patch_empty_unknown(client):
    request = create(client)
    for body in ({}, {"certificate_details": {}}, {"title": "Нова", "correction_details": {}}):
        response = patch(client, request["id"], body)
        assert response.status_code == 400
        assert error_of(response)["code"] == "EMPTY_PATCH"
    for body, field in (
        ({"status": "CLOSED"}, "body.status"),
        ({"foo": 1}, "body.foo"),
        ({"resolution": None}, "body.resolution"),
        ({"type_confirmed_at": "2026-10-10T10:00:00Z"}, "body.type_confirmed_at"),
    ):
        response = patch(client, request["id"], body)
        assert response.status_code == 422
        assert fields_of(response) == [field]
    assert get(client, request["id"]) == request


def test_patch_missing_request(client):
    assert patch(client, 999, {"title": "Нова назва"}).status_code == 404
    assert patch(client, 999, {"urgency": "HIGH"}).status_code == 422


@pytest.mark.parametrize(
    "body, field",
    [
        ({"title": "Нова назва", "urgency": "HIGH"}, "body.urgency"),
        ({"title": "Нова назва", "assignee_id": 8}, "body.assignee_id"),
    ],
)
def test_patch_atomic(client, body, field):
    request = create(client)
    response = patch(client, request["id"], body)
    assert response.status_code == 422
    assert fields_of(response) == [field]
    assert get(client, request["id"]) == request


def test_patch_closed(client):
    request = create(client)
    closed = reject(client, request["id"])
    for body in ({"title": "Нова назва"}, {}):
        response = patch(client, request["id"], body)
        assert response.status_code == 409
        assert error_of(response)["code"] == "REQUEST_CLOSED"
    assert get(client, request["id"]) == closed


@pytest.mark.parametrize(
    "body",
    [
        {"certificate_details": {"purpose": None}},
        {"certificate_details": None},
    ],
)
def test_progress_completeness_invariant(client, body):
    request = certificate_ready(client)
    started = start(client, request["id"])
    response = patch(client, request["id"], body)
    assert response.status_code == 409
    assert error_of(response)["code"] == "REQUEST_INCOMPLETE"
    assert get(client, request["id"]) == started
    fixed = patch(client, request["id"], {"certificate_details": {"purpose": "Для візи"}})
    assert fixed.status_code == 200


def test_applicant_edit_open_only(client):
    request = certificate_ready(client)
    response = patch(client, request["id"], {"student_id": "  S-2308002 "})
    assert response.status_code == 200
    body = response.json()
    assert body["student_id"] == "S-2308002"
    for key in ("request_type", "type_confirmed_by", "type_confirmed_at"):
        assert body[key] == request[key]
    started = start(client, request["id"])
    for change in ({"student_id": "S-1"}, {"full_name": "Інший Студент"}):
        response = patch(client, request["id"], change)
        assert response.status_code == 409
        assert error_of(response)["code"] == "APPLICANT_LOCKED"
    assert get(client, request["id"]) == started


def test_patch_merge_correction_conflict(client):
    request = create(client, correction_details=CORR_FULL)
    response = patch(client, request["id"], {"correction_details": {"current_value": "B"}})
    assert response.status_code == 422
    assert fields_of(response) == ["body.correction_details.current_value"]
    assert get(client, request["id"])["correction_details"] == CORR_FULL


def test_confirmation_pair(client):
    request = create(client)
    response = patch(client, request["id"], {"request_type": CERT})
    assert response.status_code == 422
    assert fields_of(response) == ["body.type_confirmed_by"]
    response = patch(client, request["id"], {"type_confirmed_by": 1})
    assert fields_of(response) == ["body.request_type"]
    assert get(client, request["id"]) == request


def test_change_type_clears_old(client):
    request = create(client, certificate_details=CERT_FULL)
    response = patch(
        client,
        request["id"],
        {
            "request_type": CORR,
            "type_confirmed_by": 2,
            "correction_details": {"target_field": "full_name"},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["certificate_details"] is None
    assert body["correction_details"] == {
        "target_field": "full_name",
        "current_value": None,
        "proposed_value": None,
    }
    assert body["completeness"] == {
        "type_confirmed": True,
        "is_complete": False,
        "missing_fields": ["correction_details.current_value", "correction_details.proposed_value"],
    }


def test_first_confirmation_keeps_matching_details(client):
    request = create(client, certificate_details={"purpose": "Для банку"})
    body = confirm(client, request["id"], CERT)
    assert body["certificate_details"]["purpose"] == "Для банку"
    assert body["completeness"]["missing_fields"] == [
        "certificate_details.language",
        "certificate_details.delivery_method",
    ]


def test_change_type_atomic(client):
    request = certificate_ready(client)
    response = patch(
        client,
        request["id"],
        {
            "request_type": CORR,
            "type_confirmed_by": 2,
            "correction_details": {"target_field": "x" * 65},
        },
    )
    assert response.status_code == 422
    assert fields_of(response) == ["body.correction_details.target_field"]
    assert get(client, request["id"]) == request


def test_confirmation_repeat(client):
    request = certificate_ready(client)
    same = confirm(client, request["id"], CERT, by=1)
    assert same["type_confirmed_at"] == request["type_confirmed_at"]
    other = confirm(client, request["id"], CERT, by=2)
    assert other["type_confirmed_by"] == 2
    assert other["type_confirmed_at"] > request["type_confirmed_at"]


def test_type_locked_in_progress(client):
    request = certificate_ready(client)
    started = start(client, request["id"])
    assert confirm(client, request["id"], CERT, by=1) == started
    for by, rtype in ((2, CERT), (1, CORR)):
        response = patch(client, request["id"], {"request_type": rtype, "type_confirmed_by": by})
        assert response.status_code == 409
        assert error_of(response)["code"] == "TYPE_LOCKED"
    assert get(client, request["id"]) == started


def test_details_must_match_confirmed_type(client):
    request = certificate_ready(client)
    response = patch(client, request["id"], {"correction_details": {"target_field": "x"}})
    assert response.status_code == 422
    assert fields_of(response) == ["body.correction_details"]
    response = patch(
        client,
        request["id"],
        {"request_type": CORR, "type_confirmed_by": 1, "certificate_details": {"language": "en"}},
    )
    assert response.status_code == 422
    assert fields_of(response) == ["body.certificate_details"]
    assert get(client, request["id"]) == request


def test_correction_ready_is_complete(client):
    assert correction_ready(client)["completeness"]["is_complete"] is True


def test_assign_known(client):
    request = create(client)
    response = patch(client, request["id"], {"assignee_id": 2})
    assert response.status_code == 200
    assert response.json()["assignee_id"] == 2


@pytest.mark.parametrize("in_progress", [False, True])
def test_unassign(client, in_progress):
    request = certificate_ready(client)
    patch(client, request["id"], {"assignee_id": 2})
    if in_progress:
        start(client, request["id"])
    response = patch(client, request["id"], {"assignee_id": None})
    assert response.status_code == 200
    assert response.json()["assignee_id"] is None


@pytest.mark.parametrize("value", [3, True, "1", 0, 1.0])
def test_assign_invalid(client, value):
    request = create(client)
    patch(client, request["id"], {"assignee_id": 1})
    response = patch(client, request["id"], {"assignee_id": value})
    assert response.status_code == 422
    assert fields_of(response) == ["body.assignee_id"]
    assert get(client, request["id"])["assignee_id"] == 1


def test_patch_error_examples(client):
    request = create(client)
    assert error_of(patch(client, request["id"], {})) == {
        "code": "EMPTY_PATCH",
        "message": "Не передано жодної зміни.",
        "details": [
            {
                "field": "body",
                "reason": "Передайте хоча б одне поле; вкладений об’єкт не може бути порожнім.",
            }
        ],
    }
    assert error_of(patch(client, request["id"], {"assignee_id": 3}))["details"] == [
        {"field": "body.assignee_id", "reason": "Допустимі 1, 2 або null."}
    ]
    response = client.patch(
        f"/requests/{request['id']}", content=b"", headers={"content-type": "application/json"}
    )
    assert response.status_code == 422
    assert get(client, request["id"]) == request
