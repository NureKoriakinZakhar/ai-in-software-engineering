import re
from datetime import UTC, date, datetime
from typing import Annotated, Any, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Discriminator,
    PlainValidator,
    Tag,
    WithJsonSchema,
)

STAFF_IDS = (1, 2)


class FormError(Exception):
    def __init__(self, field: str, reason: str, message: str = "Некоректні дані запиту."):
        super().__init__(reason)
        self.message = message
        self.details = [{"field": field, "reason": reason}]


def _bounded(min_length: int, max_length: int, message: str, trim: bool) -> Any:
    def check(value: str) -> str:
        if trim:
            value = value.strip()
        if not min_length <= len(value) <= max_length:
            raise ValueError(message)
        return value

    schema = {"type": "string", "minLength": min_length, "maxLength": max_length}
    return Annotated[str, AfterValidator(check), WithJsonSchema(schema)]


def _trim(min_length: int, max_length: int, message: str | None = None) -> Any:
    message = message or f"Після trim потрібно від {min_length} до {max_length} символів."
    return _bounded(min_length, max_length, message, trim=True)


def _staff_check(message: str):
    def check(value: int) -> int:
        if value not in STAFF_IDS:
            raise ValueError(message)
        return value

    return AfterValidator(check)


_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
_DATETIME_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?(Z|[+-]\d{2}:\d{2})")


def _parse_date(value: Any) -> date:
    if not isinstance(value, str) or not _DATE_RE.fullmatch(value):
        raise ValueError("Потрібна дата ISO 8601 YYYY-MM-DD.")
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError("Неіснуюча календарна дата.") from None


def _parse_datetime(value: Any) -> datetime:
    if not isinstance(value, str) or not _DATETIME_RE.fullmatch(value):
        raise ValueError("Потрібен час RFC3339 із часовим поясом.")
    try:
        return datetime.fromisoformat(value).astimezone(UTC)
    except ValueError:
        raise ValueError("Неіснуючий момент часу.") from None


StaffId = Annotated[int, _staff_check("Допустимі 1 або 2.")]
AssigneeId = Annotated[int, _staff_check("Допустимі 1, 2 або null.")]
StudentId = _trim(1, 32)
FullName = _trim(3, 120)
Title = _trim(3, 120)
Description = _bounded(0, 2000, "Допустимо до 2000 символів (без trim).", trim=False)
Urgency = Literal["low", "medium", "high"]
Status = Literal["OPEN", "IN_PROGRESS", "CLOSED"]
RequestType = Literal["ENROLLMENT_CERTIFICATE", "STUDENT_DATA_CORRECTION"]
IsoDate = Annotated[
    date, PlainValidator(_parse_date), WithJsonSchema({"type": "string", "format": "date"})
]
Rfc3339 = Annotated[
    datetime,
    PlainValidator(_parse_datetime),
    WithJsonSchema({"type": "string", "format": "date-time"}),
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class CertificateDetailsIn(StrictModel):
    language: Literal["uk", "en"] | None = None
    purpose: _trim(3, 200) | None = None
    delivery_method: Literal["digital", "physical"] | None = None


class CorrectionDetailsIn(StrictModel):
    target_field: _trim(1, 64) | None = None
    current_value: _trim(1, 200) | None = None
    proposed_value: _trim(1, 200) | None = None


DETAILS_NAMES = ("certificate_details", "correction_details")


def _check_correction_values(details: CorrectionDetailsIn | None, prefix: str) -> None:
    if (
        details is not None
        and details.current_value is not None
        and details.current_value == details.proposed_value
    ):
        raise FormError(
            f"{prefix}.correction_details.proposed_value",
            "Запропоноване значення має відрізнятися від поточного.",
        )


class RequestCreate(StrictModel):
    student_id: StudentId
    full_name: FullName
    title: Title
    description: Description = ""
    urgency: Urgency = "medium"
    assignee_id: AssigneeId | None = None
    certificate_details: CertificateDetailsIn | None = None
    correction_details: CorrectionDetailsIn | None = None

    def check_form(self) -> None:
        given = [n for n in DETAILS_NAMES if getattr(self, n) is not None]
        for name in given:
            if not getattr(self, name).model_fields_set:
                raise FormError(f"body.{name}", "Порожній об’єкт реквізитів не допускається.")
        if len(given) == 2:
            raise FormError("body.correction_details", "Можна передати реквізити лише одного виду.")
        _check_correction_values(self.correction_details, "body")


class RequestPatch(StrictModel):
    student_id: StudentId = None
    full_name: FullName = None
    title: Title = None
    description: Description = None
    urgency: Urgency = None
    assignee_id: AssigneeId | None = None
    request_type: RequestType = None
    type_confirmed_by: StaffId = None
    certificate_details: CertificateDetailsIn | None = None
    correction_details: CorrectionDetailsIn | None = None

    def check_form(self) -> None:
        fields = self.model_fields_set
        if "request_type" in fields and "type_confirmed_by" not in fields:
            raise FormError("body.type_confirmed_by", "Передається разом із request_type.")
        if "type_confirmed_by" in fields and "request_type" not in fields:
            raise FormError("body.request_type", "Передається разом із type_confirmed_by.")
        nonempty = [
            n
            for n in DETAILS_NAMES
            if getattr(self, n) is not None and getattr(self, n).model_fields_set
        ]
        if len(nonempty) == 2:
            raise FormError("body.correction_details", "Можна передати реквізити лише одного виду.")
        if "request_type" in fields and nonempty:
            expected = (
                "certificate_details"
                if self.request_type == "ENROLLMENT_CERTIFICATE"
                else "correction_details"
            )
            if nonempty[0] != expected:
                raise FormError(
                    f"body.{nonempty[0]}", "Реквізити не відповідають підтверджуваному типу."
                )


class CertificateResult(StrictModel):
    certificate_number: _trim(1, 64)
    issued_on: IsoDate


class CorrectionResult(StrictModel):
    target_field: _trim(1, 64)
    previous_value: _trim(1, 200)
    corrected_value: _trim(1, 200)
    corrected_at: Rfc3339


RESULT_TAGS = ("certificate", "correction")


def _result_kind(value: Any) -> str:
    if isinstance(value, dict) and ("certificate_number" in value or "issued_on" in value):
        return "certificate"
    return "correction"


ResultDetails = Annotated[
    Annotated[CertificateResult, Tag("certificate")]
    | Annotated[CorrectionResult, Tag("correction")],
    Discriminator(_result_kind),
]


class ResolutionInput(StrictModel):
    resolution_code: Literal["COMPLETED", "REJECTED"]
    result_details: ResultDetails | None = None
    rejection_reason: _trim(10, 2000, "Для REJECTED потрібно від 10 до 2000 символів.") | None = (
        None
    )
    resolved_by: StaffId

    def check_form(self, prefix: str = "body.resolution") -> None:
        if self.resolution_code == "COMPLETED":
            if self.result_details is None:
                raise FormError(f"{prefix}.result_details", "Для COMPLETED потрібен результат.")
            if self.rejection_reason is not None:
                raise FormError(f"{prefix}.rejection_reason", "Для COMPLETED має бути null.")
        else:
            if self.rejection_reason is None:
                raise FormError(
                    f"{prefix}.rejection_reason", "Для REJECTED потрібно від 10 до 2000 символів."
                )
            if self.result_details is not None:
                raise FormError(f"{prefix}.result_details", "Для REJECTED має бути null.")


class StatusPatch(StrictModel):
    status: Status
    resolution: ResolutionInput = None

    def check_form(self) -> None:
        if "resolution" in self.model_fields_set:
            if self.status != "CLOSED":
                raise FormError("body.resolution", "Резолюція дозволена лише для status=CLOSED.")
            self.resolution.check_form()


class CloseInput(StrictModel):
    resolution: ResolutionInput

    def check_form(self) -> None:
        self.resolution.check_form()


class CommentCreate(StrictModel):
    author_id: StaffId
    text: _trim(1, 1000)


class Staff(BaseModel):
    id: int
    name: str


class Health(BaseModel):
    status: Literal["ok"]


class CertificateDetailsOut(BaseModel):
    language: str | None
    purpose: str | None
    delivery_method: str | None


class CorrectionDetailsOut(BaseModel):
    target_field: str | None
    current_value: str | None
    proposed_value: str | None


class CertificateResultOut(BaseModel):
    certificate_number: str
    issued_on: str


class CorrectionResultOut(BaseModel):
    target_field: str
    previous_value: str
    corrected_value: str
    corrected_at: str


class ResolutionOut(BaseModel):
    resolution_code: str
    result_details: CertificateResultOut | CorrectionResultOut | None
    rejection_reason: str | None
    resolved_by: int
    resolved_at: str


class CompletenessOut(BaseModel):
    type_confirmed: bool
    is_complete: bool
    missing_fields: list[str]


class RequestOut(BaseModel):
    id: int
    student_id: str
    full_name: str
    title: str
    description: str
    urgency: str
    status: str
    assignee_id: int | None
    request_type: str | None
    type_confirmed_by: int | None
    type_confirmed_at: str | None
    certificate_details: CertificateDetailsOut | None
    correction_details: CorrectionDetailsOut | None
    created_at: str
    resolution: ResolutionOut | None
    completeness: CompletenessOut


class CommentOut(BaseModel):
    id: int
    request_id: int
    author_id: int
    text: str
    created_at: str


def _example(summary: str, value: dict, description: str = "") -> dict:
    example = {"summary": summary, "value": value}
    if description:
        example["description"] = description
    return example


_STARTED = datetime.now(UTC).replace(microsecond=0)
_TODAY = _STARTED.date().isoformat()

CREATE_EXAMPLES = {
    "minimal": _example(
        "Мінімальне звернення",
        {
            "student_id": "S-2308001",
            "full_name": "Тестовий Студент",
            "title": "Довідка про навчання",
        },
        "Лише обов'язкові поля: description='', urgency=medium, status=OPEN.",
    ),
    "certificate": _example(
        "Довідка з повними реквізитами",
        {
            "student_id": "S-2308001",
            "full_name": "Тестовий Студент",
            "title": "Довідка про навчання",
            "description": "Потрібна довідка для подання за місцем вимоги.",
            "urgency": "high",
            "certificate_details": {
                "language": "uk",
                "purpose": "За місцем вимоги",
                "delivery_method": "digital",
            },
        },
    ),
    "correction": _example(
        "Виправлення даних студента",
        {
            "student_id": "S-2308002",
            "full_name": "Тестова Помилка",
            "title": "Виправлення прізвища",
            "urgency": "medium",
            "correction_details": {
                "target_field": "full_name",
                "current_value": "Тестова Помилка",
                "proposed_value": "Тестове Ім’я",
            },
        },
    ),
    "partial": _example(
        "Неповні реквізити довідки",
        {
            "student_id": "S-2308003",
            "full_name": "Інший Студент",
            "title": "Довідка для банку",
            "urgency": "low",
            "certificate_details": {"language": "en"},
        },
        "Пропущені поля реквізитів зберігаються як null.",
    ),
    "invalid_title": _example(
        "Помилка 422: title коротший за 3 символи",
        {"student_id": "S-2308001", "full_name": "Тестовий Студент", "title": "  Д "},
    ),
    "both_details": _example(
        "Помилка 422: реквізити двох видів",
        {
            "student_id": "S-2308001",
            "full_name": "Тестовий Студент",
            "title": "Довідка про навчання",
            "certificate_details": {"language": "uk"},
            "correction_details": {"target_field": "full_name"},
        },
    ),
}

PATCH_EXAMPLES = {
    "confirm_certificate": _example(
        "Підтвердити тип: довідка",
        {
            "request_type": "ENROLLMENT_CERTIFICATE",
            "type_confirmed_by": 1,
            "certificate_details": {
                "language": "uk",
                "purpose": "За місцем вимоги",
                "delivery_method": "digital",
            },
        },
    ),
    "confirm_correction": _example(
        "Підтвердити тип: виправлення даних",
        {"request_type": "STUDENT_DATA_CORRECTION", "type_confirmed_by": 2},
        "Реквізити довідки, якщо вони були, очищаються.",
    ),
    "merge_details": _example(
        "Доповнити реквізити (вкладений merge)",
        {"certificate_details": {"purpose": "Для подання до банку"}},
        "Змінюється лише purpose, інші поля реквізитів зберігаються.",
    ),
    "assign": _example("Призначити виконавця", {"assignee_id": 2}),
    "unassign": _example("Зняти призначення", {"assignee_id": None}),
    "edit": _example(
        "Змінити назву, опис і терміновість",
        {
            "title": "Довідка про навчання (терміново)",
            "description": "Потрібна до п'ятниці.",
            "urgency": "high",
        },
    ),
    "empty": _example("Помилка 400: порожній PATCH", {}),
    "status_in_patch": _example("Помилка 422: status у загальному PATCH", {"status": "CLOSED"}),
    "pair_missing": _example(
        "Помилка 422: тип без підтверджувача", {"request_type": "ENROLLMENT_CERTIFICATE"}
    ),
}

_CERTIFICATE_DONE = {
    "resolution_code": "COMPLETED",
    "result_details": {"certificate_number": "CERT-2026-001", "issued_on": _TODAY},
    "rejection_reason": None,
    "resolved_by": 1,
}
_CORRECTION_DONE = {
    "resolution_code": "COMPLETED",
    "result_details": {
        "target_field": "full_name",
        "previous_value": "Тестова Помилка",
        "corrected_value": "Тестове Ім’я",
        "corrected_at": _STARTED.strftime("%Y-%m-%dT%H:%M:%SZ"),
    },
    "resolved_by": 1,
}
_REJECTED = {
    "resolution_code": "REJECTED",
    "rejection_reason": "Заявлена послуга не надається цим підрозділом.",
    "resolved_by": 2,
}
_CORRECTION_NOTE = (
    "corrected_at — момент запуску сервера; підходить для звернень, створених до запуску. "
    "Для нового звернення вкажіть час між його created_at і поточним часом UTC (D-12)."
)

STATUS_EXAMPLES = {
    "start": _example(
        "Почати обробку (OPEN → IN_PROGRESS)",
        {"status": "IN_PROGRESS"},
        "Потрібні підтверджений тип і всі реквізити, інакше 409.",
    ),
    "close_certificate": _example(
        "Закрити: довідку видано", {"status": "CLOSED", "resolution": _CERTIFICATE_DONE}
    ),
    "close_correction": _example(
        "Закрити: дані виправлено",
        {"status": "CLOSED", "resolution": _CORRECTION_DONE},
        _CORRECTION_NOTE,
    ),
    "close_rejected": _example("Закрити: відмова", {"status": "CLOSED", "resolution": _REJECTED}),
    "repeat_closed": _example("Повтор CLOSED без резолюції (200 без змін)", {"status": "CLOSED"}),
    "reopen": _example("Помилка 409: CLOSED → OPEN", {"status": "OPEN"}),
}

CLOSE_EXAMPLES = {
    "certificate": _example("Довідку видано", {"resolution": _CERTIFICATE_DONE}),
    "correction": _example("Дані виправлено", {"resolution": _CORRECTION_DONE}, _CORRECTION_NOTE),
    "rejected": _example("Відмова (можлива без підтвердження типу)", {"resolution": _REJECTED}),
    "short_reason": _example(
        "Помилка 422: причина відмови коротша за 10 символів",
        {"resolution": {"resolution_code": "REJECTED", "rejection_reason": "Ні", "resolved_by": 2}},
    ),
}

COMMENT_EXAMPLES = {
    "clarify": _example(
        "Уточнення від співробітника", {"author_id": 2, "text": "Уточніть призначення довідки."}
    ),
    "done": _example(
        "Повідомлення про виконання", {"author_id": 1, "text": "Довідку підготовлено."}
    ),
    "empty_text": _example("Помилка 422: лише пробіли", {"author_id": 1, "text": "   "}),
    "bad_author": _example("Помилка 422: невідомий автор", {"author_id": 3, "text": "Текст"}),
}
