from dishka import provide, Provider, Scope, AnyOf

from myapp.application.interactor.change_password import AdminChangePasswordInteractor
from myapp.application.interactor.delete_user import DeleteUserInteractor
from myapp.application.interactor.login_user import EmailLoginUser
from myapp.application.interactor.register_user import EmailRegisterUser
from myapp.application.interface.login import ILoginUser
from myapp.application.interface.register import IRegisterUser


class AuthProvider(Provider):
    delete_user_interactor = provide(DeleteUserInteractor, scope=Scope.REQUEST)
    admin_change_password_interactor = provide(AdminChangePasswordInteractor, scope=Scope.REQUEST)

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
