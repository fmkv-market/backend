from faststream.rabbit import RabbitBroker

from myapp.application.interface.profile_publisher import IProfilePublisher


class ProfileMessagePublisher(IProfilePublisher):
    def __init__(self, broker: RabbitBroker) -> None:
        self._broker = broker

    async def publish_user_created(
        self,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> None:
        await self._broker.publish(
            {"user_id": user_id, "first_name": first_name, "last_name": last_name},
            queue="user.created",
        )

    async def publish_user_deleted(self, user_id: int) -> None:
        await self._broker.publish({"user_id": user_id}, queue="user.deleted")