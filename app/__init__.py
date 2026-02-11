from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .config import Config
from .db import init_db
from .routes import router


def create_app() -> FastAPI:
    app = FastAPI(title="Weather Today")
    app.state.config = Config()

    app.add_middleware(SessionMiddleware, secret_key=app.state.config.secret_key)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    @app.on_event("startup")
    def on_startup() -> None:
        init_db(app.state.config.database_url)

    app.include_router(router)
    return app
