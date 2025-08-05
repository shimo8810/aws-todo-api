from fastapi import FastAPI
from mangum import Mangum

from .interface.api.router import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


app = create_app()
handler = Mangum(app)
