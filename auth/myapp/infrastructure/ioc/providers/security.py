from dishka import Provider, provide, Scope

from myapp.application.interface.failed_attempts import IFailedAttemptsStorage
from myapp.application.interactor.block_user import BlockUserInteractor
from myapp.infrastructure.gateways.failed_attempts import FailedAttemptsRedisStorage


class SecurityProvider(Provider):
    failed_attempts_storage = provide(
        FailedAttemptsRedisStorage,
        scope=Scope.APP,
        provides=IFailedAttemptsStorage,
    )
    block_user_interactor = provide(BlockUserInteractor, scope=Scope.REQUEST)