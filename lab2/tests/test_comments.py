import pytest

from tests.conftest import create, error_of, fields_of, reject


def comment(client, request_id, text="Уточніть призначення довідки.", author_id=1):
    return client.post(
        f"/requests/{request_id}/comments", json={"author_id": author_id, "text": text}
    )


def test_comment_closed(client):
    request = create(client)
    reject(client, request["id"])
    response = comment(client, request["id"], text=" Уточнення ")
    assert response.status_code == 201
    body = response.json()
    assert body["text"] == "Уточнення"
    assert body["request_id"] == request["id"] and body["id"] >= 1
    assert body["created_at"].endswith("Z")
    listed = client.get(f"/requests/{request['id']}/comments")
    assert listed.status_code == 200
    assert listed.json() == [body]


@pytest.mark.parametrize(
    "text, expected",
    [
        ("x" * 1000, 201),
        ("x" * 1001, 422),
        ("   ", 422),
        ("", 422),
        (None, 422),
        (5, 422),
    ],
)
def test_comment_boundaries(client, text, expected):
    request = create(client)
    response = comment(client, request["id"], text=text)
    assert response.status_code == expected
    if expected == 422:
        assert fields_of(response) == ["body.text"]
    count = len(client.get(f"/requests/{request['id']}/comments").json())
    assert count == (1 if expected == 201 else 0)


def test_comment_missing(client):
    for response in (comment(client, 999), client.get("/requests/999/comments")):
        assert response.status_code == 404
        assert error_of(response)["code"] == "REQUEST_NOT_FOUND"


@pytest.mark.parametrize("author_id", [3, 0, True, "1"])
def test_comment_author(client, author_id):
    request = create(client)
    response = comment(client, request["id"], author_id=author_id)
    assert response.status_code == 422
    assert fields_of(response) == ["body.author_id"]


@pytest.mark.parametrize("extra", [{"id": 1}, {"request_id": 1}, {"created_at": "x"}])
def test_comment_server_fields_forbidden(client, extra):
    request = create(client)
    response = client.post(
        f"/requests/{request['id']}/comments", json={"author_id": 1, "text": "Текст", **extra}
    )
    assert response.status_code == 422


def test_comment_order(client, clock):
    request = create(client)
    ids = [comment(client, request["id"], text=f"c{i}").json()["id"] for i in range(3)]
    clock.frozen = True
    ids += [comment(client, request["id"], text=f"same{i}").json()["id"] for i in range(2)]
    listed = client.get(f"/requests/{request['id']}/comments").json()
    assert [c["id"] for c in listed] == ids
    assert listed[3]["created_at"] == listed[4]["created_at"]
    assert client.get(f"/requests/{create(client)['id']}/comments").json() == []


def test_comment_error_example(client):
    request = create(client)
    assert error_of(comment(client, request["id"], text=" "))["details"] == [
        {"field": "body.text", "reason": "Після trim потрібно від 1 до 1000 символів."}
    ]
