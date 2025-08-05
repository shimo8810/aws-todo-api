from fastapi import FastAPI
from mangum import Mangum

from .infrastructure.db.dydb_task_list_repository import (
    get_dynamodb_task_list_repository,
)
from .interface.api.dependencies import get_task_list_repository
from .interface.api.router import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.dependency_overrides[get_task_list_repository] = (
        get_dynamodb_task_list_repository
    )

    app.include_router(router)
    return app


app = create_app()
handler = Mangum(app)
