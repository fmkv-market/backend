from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from faststream.rabbit import RabbitBroker

from myapp.infrastructure.ioc.providers.cart import CartProvider
from myapp.infrastructure.ioc.providers.database import DatabaseProvider
from myapp.infrastructure.ioc.providers.interactors import InteractorProvider
from myapp.infrastructure.ioc.providers.settings import SettingsProvider


def init_di(app: FastAPI, broker: RabbitBroker):
    container = make_async_container(
        SettingsProvider(),
        DatabaseProvider(),
        CartProvider(),
        InteractorProvider(),
        context={
            RabbitBroker: broker,
        },
    )
    setup_dishka(container=container, app=app)
    return container
