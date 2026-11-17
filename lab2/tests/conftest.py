from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

START = datetime(2026, 10, 10, 10, 0, 0, tzinfo=UTC)


class FakeClock:
    def __init__(self, start: datetime = START, step: int = 1):
        self.now = start
        self.step = timedelta(seconds=step)
        self.frozen = False

    def __call__(self) -> datetime:
        current = self.now
        if not self.frozen:
            self.now += self.step
        return current


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "test.sqlite3"


@pytest.fixture
def client(db_path, clock) -> TestClient:
    return TestClient(create_app(db_path, clock))


MINIMAL = {"student_id": "S-2308001", "full_name": "Тестовий Студент", "title": "Довідка"}
CERT_FULL = {"language": "uk", "purpose": "За місцем вимоги", "delivery_method": "digital"}
CORR_FULL = {"target_field": "full_name", "current_value": "A", "proposed_value": "B"}


def create(client, **extra) -> dict:
    response = client.post("/requests", json={**MINIMAL, **extra})
    assert response.status_code == 201, response.text
    return response.json()


def confirm(client, request_id: int, request_type: str, by: int = 1, **extra) -> dict:
    body = {"request_type": request_type, "type_confirmed_by": by, **extra}
    response = client.patch(f"/requests/{request_id}", json=body)
    assert response.status_code == 200, response.text
    return response.json()


def certificate_ready(client) -> dict:
    request = create(client, certificate_details=CERT_FULL)
    return confirm(client, request["id"], "ENROLLMENT_CERTIFICATE")


def correction_ready(client) -> dict:
    request = create(client, correction_details=CORR_FULL)
    return confirm(client, request["id"], "STUDENT_DATA_CORRECTION")


def reject(client, request_id: int, by: int = 1) -> dict:
    resolution = {
        "resolution_code": "REJECTED",
        "rejection_reason": "Послуга не надається.",
        "resolved_by": by,
    }
    response = client.post(f"/requests/{request_id}/close", json={"resolution": resolution})
    assert response.status_code == 200, response.text
    return response.json()


def error_of(response) -> dict:
    return response.json()["error"]


def fields_of(response) -> list[str]:
    return [d["field"] for d in error_of(response)["details"]]
