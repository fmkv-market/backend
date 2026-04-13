from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from myapp.infrastructure.ioc.providers.auth import AuthProvider
from myapp.infrastructure.ioc.providers.database import DatabaseProvider
from myapp.infrastructure.ioc.providers.jwt import JWTManagerProvider
from myapp.infrastructure.ioc.providers.password import PasswordManagerProvider
from myapp.infrastructure.ioc.providers.settings import SettingsProvider
from myapp.infrastructure.ioc.providers.users import UserProvider


def init_di(app: FastAPI):
    container = make_async_container(
        SettingsProvider(),
        DatabaseProvider(),
        UserProvider(),
        AuthProvider(),
        PasswordManagerProvider(),
        JWTManagerProvider(),
    )
    setup_dishka(container=container, app=app)
    return container