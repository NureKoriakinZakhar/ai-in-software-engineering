import copy
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from app import repository
from app.database import connect, transaction
from app.models import (
    TYPE_FOR_DETAILS,
    completeness,
    details_for_type,
    format_ts,
    full_details,
    parse_ts,
)
from app.schemas import (
    DETAILS_NAMES,
    CertificateResult,
    CommentCreate,
    CorrectionResult,
    RequestCreate,
    RequestPatch,
    ResolutionInput,
)

OPEN, IN_PROGRESS, CLOSED = "OPEN", "IN_PROGRESS", "CLOSED"


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, details: list | None = None):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.details = details or []


def not_found(request_id: int) -> ApiError:
    return ApiError(404, "REQUEST_NOT_FOUND", f"Звернення з id={request_id} не знайдено.")


def validation(field: str, reason: str) -> ApiError:
    return ApiError(
        422, "VALIDATION_ERROR", "Некоректні дані запиту.", [{"field": field, "reason": reason}]
    )


def incomplete(missing: list[str], message: str) -> ApiError:
    details = [
        {"field": f"request.{m}", "reason": "Обов’язкове поле не заповнено."} for m in missing
    ]
    return ApiError(409, "REQUEST_INCOMPLETE", message, details)


def user_resolution(resolution: ResolutionInput) -> dict:
    result = resolution.result_details
    if isinstance(result, CertificateResult):
        result = {
            "certificate_number": result.certificate_number,
            "issued_on": result.issued_on.isoformat(),
        }
    elif isinstance(result, CorrectionResult):
        result = {
            "target_field": result.target_field,
            "previous_value": result.previous_value,
            "corrected_value": result.corrected_value,
            "corrected_at": result.corrected_at.isoformat().replace("+00:00", "Z"),
        }
    return {
        "resolution_code": resolution.resolution_code,
        "result_details": result,
        "rejection_reason": resolution.rejection_reason,
        "resolved_by": resolution.resolved_by,
    }


def matches_status(request: dict, value: str | None) -> bool:
    result = False

    if value is None:
        result = True
    else:
        status = request["status"]
        if status == value:
            result = True
        else:
            result = False

    if result:
        return True
    else:
        return False


def matches_urgency(request: dict, value: str | None) -> bool:
    return value is None or request["urgency"] == value


def matches_request_type(request: dict, value: str | None) -> bool:
    return value is None or request["request_type"] == value


def with_completeness(request: dict) -> dict:
    return {**request, "completeness": completeness(request)}


class RequestService:
    def __init__(self, db_path: Path, clock: Callable[[], datetime]):
        self.db_path = db_path
        self.clock = clock

    def _now(self) -> str:
        return format_ts(self.clock())

    def _connect(self):
        return connect(self.db_path)

    @staticmethod
    def _load(conn, request_id: int) -> dict:
        request = repository.fetch_request(conn, request_id)
        if request is None:
            raise not_found(request_id)
        return request

    def list_staff(self) -> list[dict]:
        conn = self._connect()
        try:
            return repository.fetch_staff(conn)
        finally:
            conn.close()

    def create_request(self, data: RequestCreate) -> dict:
        values = {
            "student_id": data.student_id,
            "full_name": data.full_name,
            "title": data.title,
            "description": data.description,
            "urgency": data.urgency,
            "status": OPEN,
            "assignee_id": data.assignee_id,
            "request_type": None,
            "type_confirmed_by": None,
            "type_confirmed_at": None,
        }
        for name in DETAILS_NAMES:
            details = getattr(data, name)
            values[name] = None if details is None else full_details(name, details.model_dump())
        conn = self._connect()
        try:
            with transaction(conn):
                request_id = repository.insert_request(conn, values, self._now())
                repository.save_details(conn, request_id, values)
            return with_completeness(self._load(conn, request_id))
        finally:
            conn.close()

    def get_request(self, request_id: int) -> dict:
        conn = self._connect()
        try:
            return with_completeness(self._load(conn, request_id))
        finally:
            conn.close()

    def list_requests(
        self, status: str | None = None, urgency: str | None = None, request_type: str | None = None
    ) -> list[dict]:
        conn = self._connect()
        try:
            requests = repository.fetch_requests(conn)
        finally:
            conn.close()
        return [
            with_completeness(r)
            for r in requests
            if matches_status(r, status)
            and matches_urgency(r, urgency)
            and matches_request_type(r, request_type)
        ]

    def patch_request(self, request_id: int, patch: RequestPatch) -> dict:
        fields = patch.model_fields_set
        conn = self._connect()
        try:
            with transaction(conn):
                current = self._load(conn, request_id)
                if current["status"] == CLOSED:
                    raise ApiError(
                        409,
                        "REQUEST_CLOSED",
                        "Закрите звернення не редагується.",
                        [{"field": "request.status", "reason": "Статус CLOSED є фінальним."}],
                    )
                self._check_not_empty(patch)
                candidate = self._build_candidate(current, patch, fields)
                self._check_candidate(current, candidate, patch, fields)
                self._save(conn, request_id, current, candidate)
            return with_completeness(self._load(conn, request_id))
        finally:
            conn.close()

    @staticmethod
    def _check_not_empty(patch: RequestPatch) -> None:
        empty_nested = any(
            getattr(patch, name) is not None and not getattr(patch, name).model_fields_set
            for name in DETAILS_NAMES
            if name in patch.model_fields_set
        )
        if not patch.model_fields_set or empty_nested:
            raise ApiError(
                400,
                "EMPTY_PATCH",
                "Не передано жодної зміни.",
                [
                    {
                        "field": "body",
                        "reason": "Передайте хоча б одне поле; вкладений об’єкт не може бути порожнім.",
                    }
                ],
            )

    def _build_candidate(self, current: dict, patch: RequestPatch, fields: set) -> dict:
        status = current["status"]
        if status == IN_PROGRESS:
            locked = [f for f in ("student_id", "full_name") if f in fields]
            if locked:
                raise ApiError(
                    409,
                    "APPLICANT_LOCKED",
                    "Заявник змінюється лише в OPEN.",
                    [{"field": f"body.{f}", "reason": "Звернення вже в обробці."} for f in locked],
                )
        candidate = copy.deepcopy(current)
        for name in ("student_id", "full_name", "title", "description", "urgency", "assignee_id"):
            if name in fields:
                candidate[name] = getattr(patch, name)

        if "request_type" in fields:
            pair = (patch.request_type, patch.type_confirmed_by)
            same_pair = pair == (current["request_type"], current["type_confirmed_by"])
            if status == IN_PROGRESS and not same_pair:
                raise ApiError(
                    409,
                    "TYPE_LOCKED",
                    "Підтвердження не змінюється під час обробки.",
                    [{"field": "body.request_type", "reason": "Звернення вже в обробці."}],
                )
            if not same_pair:
                candidate["request_type"], candidate["type_confirmed_by"] = pair
                candidate["type_confirmed_at"] = self._now()
            keep = details_for_type(patch.request_type)
            for name in DETAILS_NAMES:
                if name != keep:
                    candidate[name] = None

        for name in DETAILS_NAMES:
            if name not in fields:
                continue
            value = getattr(patch, name)
            if value is None:
                candidate[name] = None
                continue
            merged = full_details(name, candidate[name] or {})
            merged.update({key: getattr(value, key) for key in value.model_fields_set})
            candidate[name] = merged
        return candidate

    @staticmethod
    def _check_candidate(current: dict, candidate: dict, patch: RequestPatch, fields: set):
        present = [n for n in DETAILS_NAMES if candidate[n] is not None]
        request_type = candidate["request_type"]
        for name in present:
            if request_type is not None and TYPE_FOR_DETAILS[name] != request_type:
                raise validation(f"body.{name}", "Реквізити не відповідають підтвердженому типу.")
        if len(present) == 2:
            raise validation(
                "body.certificate_details"
                if "certificate_details" in fields
                else "body.correction_details",
                "Звернення може мати реквізити лише одного виду.",
            )

        correction = candidate["correction_details"]
        if (
            correction is not None
            and correction["current_value"] is not None
            and correction["current_value"] == correction["proposed_value"]
        ):
            passed = patch.correction_details.model_fields_set
            field = "proposed_value" if "proposed_value" in passed else "current_value"
            raise validation(
                f"body.correction_details.{field}",
                "Запропоноване значення має відрізнятися від поточного.",
            )

        if current["status"] == IN_PROGRESS:
            state = completeness(candidate)
            if not state["is_complete"]:
                raise incomplete(
                    state["missing_fields"], "Зміна порушує комплектність звернення в обробці."
                )

    @staticmethod
    def _save(conn, request_id: int, current: dict, candidate: dict) -> None:
        changes = {
            column: candidate[column]
            for column in repository.REQUEST_COLUMNS
            if candidate[column] != current[column]
        }
        repository.update_request(conn, request_id, changes)
        if any(candidate[n] != current[n] for n in DETAILS_NAMES):
            repository.save_details(conn, request_id, candidate)

    def change_status(
        self, request_id: int, status: str, resolution: ResolutionInput | None
    ) -> dict:
        conn = self._connect()
        try:
            with transaction(conn):
                current = self._load(conn, request_id)
                source = current["status"]
                if status == CLOSED:
                    self._close(conn, current, resolution, required=source != CLOSED)
                elif source == CLOSED or (source == IN_PROGRESS and status == OPEN):
                    reason = (
                        "Фінальний стан не змінюється."
                        if source == CLOSED
                        else "Повернення в OPEN після початку обробки заборонене."
                    )
                    raise ApiError(
                        409,
                        "INVALID_TRANSITION",
                        f"Перехід {source} → {status} заборонений.",
                        [{"field": "request.status", "reason": reason}],
                    )
                elif source == OPEN and status == IN_PROGRESS:
                    self._check_ready(current, closing=False)
                    repository.update_request(conn, request_id, {"status": IN_PROGRESS})
            return with_completeness(self._load(conn, request_id))
        finally:
            conn.close()

    def close_request(self, request_id: int, resolution: ResolutionInput) -> dict:
        return self.change_status(request_id, CLOSED, resolution)

    @staticmethod
    def _check_ready(request: dict, closing: bool) -> None:
        state = completeness(request)
        if not state["type_confirmed"]:
            if closing:
                message = "Не можна зафіксувати виконання без підтвердженого типу."
                reason = "Підтвердьте тип співробітником."
            else:
                message = "Тип звернення не підтверджено."
                reason = "Передайте request_type і type_confirmed_by через PATCH звернення."
            raise ApiError(
                409,
                "TYPE_NOT_CONFIRMED",
                message,
                [{"field": "request.request_type", "reason": reason}],
            )
        if not state["is_complete"]:
            message = (
                "Для фіксації виконання бракує даних."
                if closing
                else "Для початку обробки бракує даних."
            )
            raise incomplete(state["missing_fields"], message)

    def _close(
        self, conn, current: dict, resolution: ResolutionInput | None, required: bool
    ) -> None:
        if resolution is None:
            if required:
                raise validation("body.resolution", "Для закриття потрібна resolution.")
            return
        stored = current["resolution"]
        resolved_at = stored["resolved_at"] if stored else self._now()
        if resolution.resolution_code == "COMPLETED" and stored is None:
            self._check_ready(current, closing=True)
            self._check_result_kind(current, resolution.result_details)
        self._check_time_bounds(current, resolution.result_details, resolved_at)
        candidate = {**user_resolution(resolution), "resolved_at": resolved_at}
        if stored is not None:
            if candidate != stored:
                raise ApiError(
                    409,
                    "RESOLUTION_CONFLICT",
                    "Резолюцію вже зафіксовано.",
                    [
                        {
                            "field": "body.resolution",
                            "reason": "Збережену резолюцію не можна змінити.",
                        }
                    ],
                )
            return
        repository.insert_resolution(conn, current["id"], candidate)
        repository.update_request(conn, current["id"], {"status": CLOSED})

    @staticmethod
    def _check_result_kind(current: dict, result) -> None:
        expected = (
            CertificateResult
            if current["request_type"] == "ENROLLMENT_CERTIFICATE"
            else CorrectionResult
        )
        if not isinstance(result, expected):
            raise ApiError(
                409,
                "RESULT_MISMATCH",
                "Результат не відповідає послузі.",
                [
                    {
                        "field": "body.resolution.result_details",
                        "reason": "Різновид результату не відповідає підтвердженому типу.",
                    }
                ],
            )
        if expected is CorrectionResult:
            details = current["correction_details"]
            pairs = (
                ("target_field", "target_field"),
                ("previous_value", "current_value"),
                ("corrected_value", "proposed_value"),
            )
            wrong = [
                {
                    "field": f"body.resolution.result_details.{name}",
                    "reason": f"Має дорівнювати correction_details.{source}.",
                }
                for name, source in pairs
                if getattr(result, name) != details[source]
            ]
            if wrong:
                raise ApiError(409, "RESULT_MISMATCH", "Результат не відповідає реквізитам.", wrong)

    @staticmethod
    def _check_time_bounds(current: dict, result, resolved_at: str) -> None:
        created, closed = parse_ts(current["created_at"]), parse_ts(resolved_at)
        if isinstance(result, CertificateResult):
            if not created.date() <= result.issued_on <= closed.date():
                raise validation(
                    "body.resolution.result_details.issued_on",
                    "Дата має бути між датою створення та датою закриття (UTC).",
                )
        elif isinstance(result, CorrectionResult):
            if not created <= result.corrected_at <= closed:
                raise validation(
                    "body.resolution.result_details.corrected_at",
                    "Час має бути між created_at і resolved_at.",
                )

    def add_comment(self, request_id: int, data: CommentCreate) -> dict:
        conn = self._connect()
        try:
            with transaction(conn):
                if not repository.request_exists(conn, request_id):
                    raise not_found(request_id)
                comment_id = repository.insert_comment(
                    conn, request_id, data.author_id, data.text, self._now()
                )
            return repository.fetch_comment(conn, comment_id)
        finally:
            conn.close()

    def list_comments(self, request_id: int) -> list[dict]:
        conn = self._connect()
        try:
            if not repository.request_exists(conn, request_id):
                raise not_found(request_id)
            return repository.fetch_comments(conn, request_id)
        finally:
            conn.close()
