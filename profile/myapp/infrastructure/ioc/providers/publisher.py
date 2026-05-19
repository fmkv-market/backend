from dishka import provide, Provider, Scope, AnyOf, from_context
from faststream.rabbit import RabbitBroker

from myapp.application.interface.publisher import IPublisher
from myapp.application.interface.user import UserReader, UserReaderEmail, UserSaver
from myapp.infrastructure.gateways.user import UserGateway
from myapp.infrastructure.message.publisher import SMTPMessagePublisher


class PublisherProvider(Provider):
    broker = from_context(provides=RabbitBroker, scope=Scope.APP)
    @provide(scope=Scope.APP)
    async def get_publisher(self, broker: RabbitBroker) -> IPublisher:
        return SMTPMessagePublisher(broker)
