from abc import ABC, abstractmethod


class IProfilePublisher(ABC):
    @abstractmethod
    async def publish_user_created(
        self,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> None:
        pass

    @abstractmethod
    async def publish_user_deleted(self, user_id: int) -> None:
        pass