import pytest

from tests.conftest import error_of


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_staff_list(client):
    response = client.get("/staff")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Agent A"}, {"id": 2, "name": "Agent B"}]


@pytest.mark.parametrize("path", ["/health?foo=1", "/staff?foo=1"])
def test_unknown_query_rejected(client, path):
    response = client.get(path)
    assert response.status_code == 422
    assert error_of(response) == {
        "code": "VALIDATION_ERROR",
        "message": "Некоректні параметри запиту",
        "details": [{"field": "query.foo", "reason": "Невідомий параметр."}],
    }


def test_body_in_get_rejected(client):
    response = client.request("GET", "/staff", content=b'{"x":1}')
    assert response.status_code == 422
    assert error_of(response)["details"][0]["field"] == "body"
