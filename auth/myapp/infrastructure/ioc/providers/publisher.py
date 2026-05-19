from dishka import provide, Provider, Scope, from_context
from faststream.rabbit import RabbitBroker

from myapp.application.interface.profile_publisher import IProfilePublisher
from myapp.application.interface.publisher import IPublisher
from myapp.infrastructure.message.profile_publisher import ProfileMessagePublisher
from myapp.infrastructure.message.publisher import SMTPMessagePublisher


class PublisherProvider(Provider):
    broker = from_context(provides=RabbitBroker, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_smtp_publisher(self, broker: RabbitBroker) -> IPublisher:
        return SMTPMessagePublisher(broker)

    @provide(scope=Scope.APP)
    async def get_profile_publisher(self, broker: RabbitBroker) -> IProfilePublisher:
        return ProfileMessagePublisher(broker)
