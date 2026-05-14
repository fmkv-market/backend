from faststream.rabbit import RabbitBroker

from myapp.application.interface.publisher import IPublisher


class SMTPMessagePublisher(IPublisher):
    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    async def publish(self, email: str, otp: str) -> None:
        await self._broker.publish({"email": email, "otp": otp}, queue="smtp.email")