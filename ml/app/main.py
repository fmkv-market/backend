from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import health, recommendations
from app.composition.container import build_container
from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.container = build_container(settings)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.include_router(health.router)
    app.include_router(recommendations.router)
    return app


app = create_app()
