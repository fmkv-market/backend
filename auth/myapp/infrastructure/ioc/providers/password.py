from dishka import provide, Provider, Scope, AnyOf

from myapp.application.interface.pass_manager import IPasswordManager
from myapp.application.interface.user import UserReader, UserReaderEmail, UserSaver
from myapp.application.services.pass_manager import PasswordManager
from myapp.infrastructure.gateways.user import UserGateway


class PasswordManagerProvider(Provider):
    @provide(scope=Scope.APP)
    def get_password_manager(self) -> IPasswordManager:
        return PasswordManager()
