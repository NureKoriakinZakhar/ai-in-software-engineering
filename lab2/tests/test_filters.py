import copy

import pytest

from app.service import matches_request_type, matches_status, matches_urgency
from tests.conftest import CERT_FULL, confirm, create, fields_of, reject

PREDICATES = [
    (matches_status, "status", "OPEN", "CLOSED"),
    (matches_urgency, "urgency", "high", "low"),
]


@pytest.mark.parametrize("predicate, field, value, other", PREDICATES)
def test_predicate_none_means_no_filter(predicate, field, value, other):
    assert predicate({field: value}, None) is True
    assert predicate({field: other}, None) is True


@pytest.mark.parametrize("predicate, field, value, other", PREDICATES)
def test_predicate_exact_match(predicate, field, value, other):
    assert predicate({field: value}, value) is True
    assert predicate({field: other}, value) is False
    assert predicate({field: value}, value.swapcase()) is False


@pytest.mark.parametrize("predicate, field, value, other", PREDICATES)
def test_predicate_pure(predicate, field, value, other):
    request = {field: value, "title": "Довідка"}
    snapshot = copy.deepcopy(request)
    predicate(request, value)
    predicate(request, other)
    assert request == snapshot


def test_request_type_predicate_uses_confirmed_field():
    assert matches_request_type({"request_type": None}, "ENROLLMENT_CERTIFICATE") is False
    assert matches_request_type({"request_type": None}, None) is True


@pytest.fixture
def four(client):
    a = create(client, title="A open high", urgency="high", certificate_details=CERT_FULL)
    confirm(client, a["id"], "ENROLLMENT_CERTIFICATE")
    b = create(client, title="B open low", urgency="low")
    c = create(client, title="C closed high", urgency="high")
    d = create(client, title="D closed low", urgency="low")
    for item in (c, d):
        reject(client, item["id"], by=2)
    return {k: v["id"] for k, v in zip("abcd", (a, b, c, d), strict=True)}


def ids(client, query: str) -> list[int]:
    response = client.get(f"/requests?{query}")
    assert response.status_code == 200, response.text
    return [r["id"] for r in response.json()]


def test_filter_status(client, four):
    assert ids(client, "status=OPEN") == [four["a"], four["b"]]
    assert ids(client, "status=CLOSED") == [four["c"], four["d"]]


def test_filter_empty(client, four):
    assert ids(client, "status=IN_PROGRESS") == []
    assert ids(client, "status=OPEN&urgency=medium") == []


def test_filter_urgency(client, four):
    assert ids(client, "urgency=high") == [four["a"], four["c"]]


def test_filters_and(client, four):
    assert ids(client, "status=OPEN&urgency=high") == [four["a"]]
    assert ids(client, "status=CLOSED&urgency=low") == [four["d"]]
    assert ids(client, "status=OPEN&urgency=high&request_type=ENROLLMENT_CERTIFICATE") == [
        four["a"]
    ]
    assert ids(client, "request_type=STUDENT_DATA_CORRECTION") == []
    assert ids(client, "") == [four["a"], four["b"], four["c"], four["d"]]


@pytest.mark.parametrize(
    "query, field",
    [
        ("urgency=HIGH", "query.urgency"),
        ("status=open", "query.status"),
        ("request_type=CERT", "query.request_type"),
        ("priority=high", "query.priority"),
        ("status=OPEN&status=CLOSED", "query.status"),
    ],
)
def test_invalid_filter(client, query, field):
    response = client.get(f"/requests?{query}")
    assert response.status_code == 422
    assert fields_of(response) == [field]
