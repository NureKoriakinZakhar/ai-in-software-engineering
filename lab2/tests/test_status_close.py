import pytest

from tests.conftest import (
    CERT_FULL,
    certificate_ready,
    correction_ready,
    create,
    error_of,
    fields_of,
)

CERT_DONE = {
    "resolution_code": "COMPLETED",
    "result_details": {"certificate_number": "CERT-2026-001", "issued_on": "2026-10-10"},
    "resolved_by": 1,
}
REJECT = {
    "resolution_code": "REJECTED",
    "rejection_reason": "Заявлена послуга не надається.",
    "resolved_by": 2,
}


def corr_done(**override) -> dict:
    result = {
        "target_field": "full_name",
        "previous_value": "A",
        "corrected_value": "B",
        "corrected_at": "2026-10-10T10:00:00Z",
    }
    result.update(override)
    return {"resolution_code": "COMPLETED", "result_details": result, "resolved_by": 1}


def status(client, request_id, value, **extra):
    return client.patch(f"/requests/{request_id}/status", json={"status": value, **extra})


def close(client, request_id, resolution):
    return client.post(f"/requests/{request_id}/close", json={"resolution": resolution})


def closed_request(client) -> dict:
    request = certificate_ready(client)
    assert close(client, request["id"], CERT_DONE).status_code == 200
    return client.get(f"/requests/{request['id']}").json()


def test_confirm_start(client):
    request = create(client, certificate_details=CERT_FULL)
    confirmed = client.patch(
        f"/requests/{request['id']}",
        json={"request_type": "ENROLLMENT_CERTIFICATE", "type_confirmed_by": 1},
    )
    assert confirmed.status_code == 200
    assert confirmed.json()["completeness"]["type_confirmed"] is True
    started = status(client, request["id"], "IN_PROGRESS")
    assert started.status_code == 200
    assert started.json()["status"] == "IN_PROGRESS"


def test_start_incomplete(client):
    request = create(client)
    response = status(client, request["id"], "IN_PROGRESS")
    assert response.status_code == 409
    assert error_of(response)["code"] == "TYPE_NOT_CONFIRMED"

    partial = create(client, certificate_details={"language": "uk", "delivery_method": "digital"})
    client.patch(
        f"/requests/{partial['id']}",
        json={"request_type": "ENROLLMENT_CERTIFICATE", "type_confirmed_by": 1},
    )
    response = status(client, partial["id"], "IN_PROGRESS")
    assert response.status_code == 409
    assert error_of(response)["code"] == "REQUEST_INCOMPLETE"
    assert fields_of(response) == ["request.certificate_details.purpose"]
    for item in (request, partial):
        assert client.get(f"/requests/{item['id']}").json()["status"] == "OPEN"


def test_progress_noop_backward(client):
    request = certificate_ready(client)
    started = status(client, request["id"], "IN_PROGRESS").json()
    again = status(client, request["id"], "IN_PROGRESS")
    assert again.status_code == 200
    assert again.json() == started
    back = status(client, request["id"], "OPEN")
    assert back.status_code == 409
    assert error_of(back)["code"] == "INVALID_TRANSITION"
    assert client.get(f"/requests/{request['id']}").json() == started


def test_transition_matrix_remaining(client):
    request = create(client)
    same = status(client, request["id"], "OPEN")
    assert same.status_code == 200
    assert same.json() == request
    closed = closed_request(client)
    response = status(client, closed["id"], "IN_PROGRESS")
    assert response.status_code == 409
    assert error_of(response)["code"] == "INVALID_TRANSITION"
    assert client.get(f"/requests/{closed['id']}").json() == closed


@pytest.mark.parametrize("target", ["OPEN", "IN_PROGRESS"])
def test_resolution_only_for_closed(client, target):
    request = certificate_ready(client)
    response = status(client, request["id"], target, resolution=REJECT)
    assert response.status_code == 422
    assert fields_of(response) == ["body.resolution"]


def test_closed_cannot_reopen(client):
    closed = closed_request(client)
    response = status(client, closed["id"], "OPEN")
    assert response.status_code == 409
    assert error_of(response) == {
        "code": "INVALID_TRANSITION",
        "message": "Перехід CLOSED → OPEN заборонений.",
        "details": [{"field": "request.status", "reason": "Фінальний стан не змінюється."}],
    }
    repeat = status(client, closed["id"], "CLOSED")
    assert repeat.status_code == 200
    assert repeat.json() == closed
    assert client.get(f"/requests/{closed['id']}").json() == closed


def test_close_completed(client):
    request = certificate_ready(client)
    response = close(client, request["id"], CERT_DONE)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "CLOSED"
    assert body["resolution"]["result_details"] == CERT_DONE["result_details"]
    assert body["resolution"]["rejection_reason"] is None
    assert body["resolution"]["resolved_at"].endswith("Z")


def test_close_rejected(client):
    request = create(client)
    response = close(client, request["id"], REJECT)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "CLOSED"
    assert body["resolution"]["result_details"] is None
    assert body["completeness"]["is_complete"] is False


@pytest.mark.parametrize(
    "resolution, field",
    [
        ({"resolution_code": "COMPLETED", "resolved_by": 1}, "body.resolution.result_details"),
        ({**REJECT, "rejection_reason": "123456789"}, "body.resolution.rejection_reason"),
        ({**REJECT, "rejection_reason": "  Коротко  "}, "body.resolution.rejection_reason"),
        (
            {**CERT_DONE, "rejection_reason": "Причина відмови тут"},
            "body.resolution.rejection_reason",
        ),
        ({**CERT_DONE, "resolved_by": 3}, "body.resolution.resolved_by"),
        ({**CERT_DONE, "resolved_at": "2026-10-10T10:00:00Z"}, "body.resolution.resolved_at"),
    ],
)
def test_resolution_invalid(client, resolution, field):
    request = certificate_ready(client)
    response = close(client, request["id"], resolution)
    assert response.status_code == 422
    assert field in fields_of(response)
    assert client.get(f"/requests/{request['id']}").json() == request


def test_close_requires_resolution(client):
    request = certificate_ready(client)
    assert status(client, request["id"], "CLOSED").status_code == 422
    assert client.post(f"/requests/{request['id']}/close", json={}).status_code == 422
    assert client.get(f"/requests/{request['id']}").json() == request


def test_completed_requires_confirmation(client):
    request = create(client, certificate_details=CERT_FULL)
    response = close(client, request["id"], CERT_DONE)
    assert response.status_code == 409
    assert error_of(response)["code"] == "TYPE_NOT_CONFIRMED"
    assert error_of(response) == {
        "code": "TYPE_NOT_CONFIRMED",
        "message": "Не можна зафіксувати виконання без підтвердженого типу.",
        "details": [{"field": "request.request_type", "reason": "Підтвердьте тип співробітником."}],
    }


def test_close_idempotence(client):
    closed = closed_request(client)
    repeat = close(client, closed["id"], {**CERT_DONE, "rejection_reason": None})
    assert repeat.status_code == 200
    assert repeat.json()["resolution"]["resolved_at"] == closed["resolution"]["resolved_at"]
    other = {
        **CERT_DONE,
        "result_details": {"certificate_number": "CERT-2", "issued_on": "2026-10-10"},
    }
    for response in (
        close(client, closed["id"], other),
        status(client, closed["id"], "CLOSED", resolution=other),
    ):
        assert response.status_code == 409
        assert error_of(response)["code"] == "RESOLUTION_CONFLICT"
    assert client.get(f"/requests/{closed['id']}").json() == closed


def test_close_correction_match(client):
    request = correction_ready(client)
    status(client, request["id"], "IN_PROGRESS")
    wrong = status(client, request["id"], "CLOSED", resolution=corr_done(corrected_value="C"))
    assert wrong.status_code == 409
    assert error_of(wrong)["code"] == "RESULT_MISMATCH"
    assert fields_of(wrong) == ["body.resolution.result_details.corrected_value"]
    kind = status(client, request["id"], "CLOSED", resolution=CERT_DONE)
    assert error_of(kind)["code"] == "RESULT_MISMATCH"
    assert client.get(f"/requests/{request['id']}").json()["status"] == "IN_PROGRESS"
    ok = status(client, request["id"], "CLOSED", resolution=corr_done())
    assert ok.status_code == 200
    assert ok.json()["status"] == "CLOSED"


def test_result_time_bounds(client):
    correction = correction_ready(client)
    status(client, correction["id"], "IN_PROGRESS")
    future = status(
        client,
        correction["id"],
        "CLOSED",
        resolution=corr_done(corrected_at="2026-10-11T00:00:00Z"),
    )
    assert future.status_code == 422
    assert fields_of(future) == ["body.resolution.result_details.corrected_at"]
    before = status(
        client,
        correction["id"],
        "CLOSED",
        resolution=corr_done(corrected_at="2026-10-09T23:59:59Z"),
    )
    assert before.status_code == 422
    stored = client.get(f"/requests/{correction['id']}").json()
    assert stored["status"] == "IN_PROGRESS" and stored["resolution"] is None

    certificate = certificate_ready(client)
    status(client, certificate["id"], "IN_PROGRESS")
    late = {**CERT_DONE, "result_details": {"certificate_number": "C-1", "issued_on": "2026-10-11"}}
    response = close(client, certificate["id"], late)
    assert response.status_code == 422
    assert fields_of(response) == ["body.resolution.result_details.issued_on"]
    assert client.get(f"/requests/{certificate['id']}").json()["status"] == "IN_PROGRESS"
    early = {
        **CERT_DONE,
        "result_details": {"certificate_number": "C-1", "issued_on": "2026-10-09"},
    }
    response = close(client, certificate["id"], early)
    assert response.status_code == 422
    assert fields_of(response) == ["body.resolution.result_details.issued_on"]
    assert client.get(f"/requests/{certificate['id']}").json()["resolution"] is None


def test_corrected_at_timezone_normalized(client):
    request = correction_ready(client)
    response = close(client, request["id"], corr_done(corrected_at="2026-10-10T13:00:00+03:00"))
    assert response.status_code == 200
    assert response.json()["resolution"]["result_details"]["corrected_at"] == (
        "2026-10-10T10:00:00Z"
    )


def test_status_error_examples(client):
    request = create(client)
    response = status(client, request["id"], "IN_PROGRESS")
    assert error_of(response) == {
        "code": "TYPE_NOT_CONFIRMED",
        "message": "Тип звернення не підтверджено.",
        "details": [
            {
                "field": "request.request_type",
                "reason": "Передайте request_type і type_confirmed_by через PATCH звернення.",
            }
        ],
    }
    response = status(client, request["id"], "DONE")
    assert error_of(response)["details"] == [
        {"field": "body.status", "reason": "Допустимі OPEN, IN_PROGRESS, CLOSED."}
    ]
    response = close(client, request["id"], {**REJECT, "rejection_reason": "123456789"})
    assert error_of(response)["details"] == [
        {
            "field": "body.resolution.rejection_reason",
            "reason": "Для REJECTED потрібно від 10 до 2000 символів.",
        }
    ]
