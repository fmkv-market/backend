from dishka import make_async_container
import dishka_faststream as dishka_faststream
from fastapi import FastAPI
from faststream.asgi import AsgiFastStream

from myapp.infrastructure.ioc.providers.database import DatabaseProvider
from myapp.infrastructure.ioc.providers.services import SenderProvider
from myapp.infrastructure.ioc.providers.settings import SettingsProvider


def init_di(app: AsgiFastStream):
    container = make_async_container(
        SettingsProvider(),
        DatabaseProvider(),
        SenderProvider(),

    )
    dishka_faststream.setup_dishka(container=container, app=app)
    return container
