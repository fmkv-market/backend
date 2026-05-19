from dishka import provide, Provider, Scope, AnyOf

from myapp.application.interface.profile import IProfileSaver, IProfileReader, IProfileUpdater
from myapp.infrastructure.gateways.profile import ProfileGateway


class ProfileProvider(Provider):
    profile_gateway = provide(
        ProfileGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            ProfileGateway,
            IProfileSaver,
            IProfileReader,
            IProfileUpdater,
        ],
    )
