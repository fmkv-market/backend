from dishka import provide, Provider, Scope, AnyOf


from myapp.application.interface.user import (
    UserReader,
    UserReaderEmail,
    UserSaver,
    UserDeleter,
    UserPasswordUpdater,
    UserBlockManager,
)
from myapp.infrastructure.gateways.user import UserGateway


class UserProvider(Provider):
    user_gateway = provide(
        UserGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            UserReader,
            UserSaver,
            UserReaderEmail,
            UserDeleter,
            UserPasswordUpdater,
            UserBlockManager,
        ]
    )