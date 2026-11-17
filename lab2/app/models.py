from datetime import UTC, datetime

CERTIFICATE = "ENROLLMENT_CERTIFICATE"
CORRECTION = "STUDENT_DATA_CORRECTION"

SERVICE_CATALOG: dict[str, tuple[str, tuple[str, ...]]] = {
    CERTIFICATE: ("certificate_details", ("language", "purpose", "delivery_method")),
    CORRECTION: (
        "correction_details",
        ("target_field", "current_value", "proposed_value"),
    ),
}
DETAILS_FIELDS = {name: fields for name, fields in SERVICE_CATALOG.values()}
DETAILS_KIND = {"certificate_details": "certificate", "correction_details": "correction"}
KIND_TO_DETAILS = {kind: name for name, kind in DETAILS_KIND.items()}
TYPE_FOR_DETAILS = {name: rtype for rtype, (name, _) in SERVICE_CATALOG.items()}


def details_for_type(request_type: str) -> str:
    return SERVICE_CATALOG[request_type][0]


def full_details(details_name: str, values: dict) -> dict:
    return {field: values.get(field) for field in DETAILS_FIELDS[details_name]}


def completeness(request: dict) -> dict:
    request_type = request["request_type"]
    confirmed = (
        request_type is not None
        and request["type_confirmed_by"] is not None
        and request["type_confirmed_at"] is not None
    )
    if not confirmed:
        return {"type_confirmed": False, "is_complete": False, "missing_fields": ["request_type"]}
    details_name, required = SERVICE_CATALOG[request_type]
    details = request[details_name] or {}
    missing = [f"{details_name}.{f}" for f in required if details.get(f) is None]
    return {"type_confirmed": True, "is_complete": not missing, "missing_fields": missing}


def format_ts(moment: datetime) -> str:
    return moment.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ts(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def utc_now() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)
