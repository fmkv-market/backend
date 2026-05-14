from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from faststream.rabbit import RabbitBroker

from myapp.infrastructure.ioc.providers.auth import AuthProvider
from myapp.infrastructure.ioc.providers.database import DatabaseProvider
from myapp.infrastructure.ioc.providers.jwt import JWTManagerProvider
from myapp.infrastructure.ioc.providers.otp import OTPProvider
from myapp.infrastructure.ioc.providers.password import PasswordManagerProvider
from myapp.infrastructure.ioc.providers.publisher import PublisherProvider
from myapp.infrastructure.ioc.providers.redis import RedisProvider
from myapp.infrastructure.ioc.providers.settings import SettingsProvider
from myapp.infrastructure.ioc.providers.users import UserProvider


def init_di(app: FastAPI, broker: RabbitBroker):
    container = make_async_container(
        SettingsProvider(),
        DatabaseProvider(),
        UserProvider(),
        AuthProvider(),
        PasswordManagerProvider(),
        JWTManagerProvider(),
        PublisherProvider(),
        OTPProvider(),
        RedisProvider(),
        context={
            RabbitBroker: broker
        },
    )
    setup_dishka(container=container, app=app)
    return container