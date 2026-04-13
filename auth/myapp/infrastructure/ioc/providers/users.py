from dishka import provide, Provider, Scope, AnyOf


from myapp.application.interface.user import UserReader, UserReaderEmail, UserSaver
from myapp.infrastructure.gateways.user import UserGateway


class UserProvider(Provider):
    user_gateway = provide(
        UserGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            UserReader,
            UserSaver,
            UserReaderEmail
        ]
    )