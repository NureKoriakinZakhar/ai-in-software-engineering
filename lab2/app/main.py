import os
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI

from app import api
from app.database import DEFAULT_DB_PATH, init_db
from app.models import utc_now
from app.service import RequestService


def create_app(
    db_path: str | Path | None = None, clock: Callable[[], datetime] = utc_now
) -> FastAPI:
    path = Path(db_path or os.environ.get("APP_DB_PATH") or DEFAULT_DB_PATH)
    init_db(path)
    app = FastAPI(
        title="Сервіс студентських звернень",
        version="lab02",
        description="Локальний REST API за специфікацією ЛР1 (docs/api-contract.md).",
    )
    app.state.service = RequestService(path, clock)
    app.include_router(api.router)
    api.install_error_handlers(app)
    return app
