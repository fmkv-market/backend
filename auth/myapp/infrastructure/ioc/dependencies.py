from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from myapp.infrastructure.ioc.providers.settings import SettingsProvider


def init_di(app: FastAPI):
    container = make_async_container(
        SettingsProvider(),
    )
    setup_dishka(container=container, app=app)
    return container