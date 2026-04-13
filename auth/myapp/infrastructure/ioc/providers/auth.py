from dishka import provide, Provider, Scope, AnyOf

from myapp.application.interactor.login_user import EmailLoginUser
from myapp.application.interactor.register_user import EmailRegisterUser
from myapp.application.interface.login import ILoginUser
from myapp.application.interface.register import IRegisterUser


class AuthProvider(Provider):
    # TODO: Решить, как обращаться к интерфейсу и получать конкретную реализацию, если таких несколько
    email_register_interactor = provide(
        EmailRegisterUser,
        scope=Scope.REQUEST,
        provides=AnyOf[
            EmailRegisterUser,
            IRegisterUser
        ]
    )

    email_login_interactor = provide(
        EmailLoginUser,
        scope=Scope.REQUEST,
        provides=AnyOf[
            EmailLoginUser,
            ILoginUser
        ]
    )
