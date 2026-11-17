from typing import Annotated

from fastapi import APIRouter, Body, Depends, FastAPI, Path, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas import (
    CLOSE_EXAMPLES,
    COMMENT_EXAMPLES,
    CREATE_EXAMPLES,
    PATCH_EXAMPLES,
    RESULT_TAGS,
    STATUS_EXAMPLES,
    CloseInput,
    CommentCreate,
    CommentOut,
    FormError,
    Health,
    RequestCreate,
    RequestOut,
    RequestPatch,
    RequestType,
    Staff,
    Status,
    StatusPatch,
    Urgency,
)
from app.service import ApiError, RequestService

MAX_SQLITE_INT = 2**63 - 1
RequestId = Annotated[
    int,
    Path(
        gt=0,
        le=MAX_SQLITE_INT,
        openapi_examples={
            "first": {"summary": "Звернення id=1", "value": 1},
            "missing": {"summary": "Помилка 404: id=999", "value": 999},
        },
    ),
]


def get_service(request: Request) -> RequestService:
    return request.app.state.service


PARAMS_MESSAGE = "Некоректні параметри запиту"


def query_guard(*allowed: str, message: str = "Некоректні дані запиту."):
    def check(request: Request) -> None:
        seen: set[str] = set()
        for key, _ in request.query_params.multi_items():
            if key not in allowed:
                raise FormError(f"query.{key}", "Невідомий параметр.", message)
            if key in seen:
                raise FormError(f"query.{key}", "Параметр не можна повторювати.", message)
            seen.add(key)

    return Depends(check)


def no_body(message: str = "Некоректні дані запиту."):
    async def check(request: Request) -> None:
        if await request.body():
            raise FormError("body", "GET не приймає тіла запиту.", message)

    return Depends(check)


NoBody = no_body()
Service = Annotated[RequestService, Depends(get_service)]

router = APIRouter()


@router.get(
    "/health",
    response_model=Health,
    dependencies=[query_guard(message=PARAMS_MESSAGE), no_body(PARAMS_MESSAGE)],
)
def health() -> dict:
    return {"status": "ok"}


@router.get(
    "/staff",
    response_model=list[Staff],
    dependencies=[query_guard(message=PARAMS_MESSAGE), no_body(PARAMS_MESSAGE)],
)
def list_staff(service: Service) -> list[dict]:
    return service.list_staff()


@router.post("/requests", status_code=201, response_model=RequestOut, dependencies=[query_guard()])
def create_request(
    body: Annotated[RequestCreate, Body(openapi_examples=CREATE_EXAMPLES)], service: Service
) -> dict:
    body.check_form()
    return service.create_request(body)


@router.get(
    "/requests",
    response_model=list[RequestOut],
    dependencies=[query_guard("status", "urgency", "request_type"), NoBody],
)
def list_requests(
    service: Service,
    status: Status | None = Query(
        None,
        openapi_examples={
            "OPEN": {"summary": "OPEN", "value": "OPEN"},
            "IN_PROGRESS": {"summary": "IN_PROGRESS", "value": "IN_PROGRESS"},
            "CLOSED": {"summary": "CLOSED", "value": "CLOSED"},
        },
    ),
    urgency: Urgency | None = Query(
        None,
        openapi_examples={
            "low": {"summary": "low", "value": "low"},
            "medium": {"summary": "medium", "value": "medium"},
            "high": {"summary": "high", "value": "high"},
        },
    ),
    request_type: RequestType | None = Query(
        None,
        openapi_examples={
            "ENROLLMENT_CERTIFICATE": {
                "summary": "ENROLLMENT_CERTIFICATE",
                "value": "ENROLLMENT_CERTIFICATE",
            },
            "STUDENT_DATA_CORRECTION": {
                "summary": "STUDENT_DATA_CORRECTION",
                "value": "STUDENT_DATA_CORRECTION",
            },
        },
    ),
) -> list[dict]:
    return service.list_requests(status, urgency, request_type)


@router.get("/requests/{id}", response_model=RequestOut, dependencies=[query_guard(), NoBody])
def get_request(id: RequestId, service: Service) -> dict:
    return service.get_request(id)


@router.patch("/requests/{id}", response_model=RequestOut, dependencies=[query_guard()])
def patch_request(
    id: RequestId,
    body: Annotated[RequestPatch, Body(openapi_examples=PATCH_EXAMPLES)],
    service: Service,
) -> dict:
    body.check_form()
    return service.patch_request(id, body)


@router.patch("/requests/{id}/status", response_model=RequestOut, dependencies=[query_guard()])
def change_status(
    id: RequestId,
    body: Annotated[StatusPatch, Body(openapi_examples=STATUS_EXAMPLES)],
    service: Service,
) -> dict:
    body.check_form()
    return service.change_status(id, body.status, body.resolution)


@router.post("/requests/{id}/close", response_model=RequestOut, dependencies=[query_guard()])
def close_request(
    id: RequestId,
    body: Annotated[CloseInput, Body(openapi_examples=CLOSE_EXAMPLES)],
    service: Service,
) -> dict:
    body.check_form()
    return service.close_request(id, body.resolution)


@router.post(
    "/requests/{id}/comments",
    status_code=201,
    response_model=CommentOut,
    dependencies=[query_guard()],
)
def add_comment(
    id: RequestId,
    body: Annotated[CommentCreate, Body(openapi_examples=COMMENT_EXAMPLES)],
    service: Service,
) -> dict:
    return service.add_comment(id, body)


@router.get(
    "/requests/{id}/comments", response_model=list[CommentOut], dependencies=[query_guard(), NoBody]
)
def list_comments(id: RequestId, service: Service) -> list[dict]:
    return service.list_comments(id)


_TYPE_ERRORS = (
    "string_type",
    "int_type",
    "bool_type",
    "model_type",
    "dict_type",
    "model_attributes_type",
    "literal_error",
    "enum",
)


def _reason(error: dict) -> str:
    kind = error["type"]
    ctx = error.get("ctx") or {}
    if error.get("input", ...) is None and kind in _TYPE_ERRORS:
        return "null не допускається."
    if kind == "missing":
        return "Обов’язкове поле відсутнє."
    if kind == "extra_forbidden":
        return "Невідоме або заборонене поле."
    if kind == "json_invalid":
        return "Некоректний JSON."
    if kind == "literal_error":
        expected = str(ctx.get("expected", "")).replace(" or ", ", ").replace("'", "")
        return f"Допустимі {expected}."
    if kind == "value_error":
        return str(ctx.get("error", "Некоректне значення."))
    if kind in ("model_type", "dict_type", "model_attributes_type"):
        return "Очікується JSON-об’єкт."
    if kind in ("int_parsing", "greater_than", "less_than_equal"):
        return "Потрібне додатне ціле число."
    if kind.endswith("_type"):
        return "Неправильний тип значення; автоматичне приведення не виконується."
    return "Некоректне значення."


def _field(error: dict) -> str:
    if error["type"] == "json_invalid":
        return "body"
    parts = [str(p) for p in error["loc"] if p not in RESULT_TAGS]
    return ".".join(parts)


def error_body(code: str, message: str, details: list) -> dict:
    return {"error": {"code": code, "message": message, "details": details}}


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    def _validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        details: list[dict] = []
        for error in exc.errors():
            item = {"field": _field(error), "reason": _reason(error)}
            if item not in details:
                details.append(item)
        return JSONResponse(
            status_code=422,
            content=error_body("VALIDATION_ERROR", "Некоректні дані запиту.", details),
        )

    @app.exception_handler(FormError)
    def _form(_: Request, exc: FormError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=error_body("VALIDATION_ERROR", exc.message, exc.details),
        )

    @app.exception_handler(ApiError)
    def _domain(_: Request, exc: ApiError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status, content=error_body(exc.code, exc.message, exc.details)
        )
