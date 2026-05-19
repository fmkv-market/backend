from abc import ABC, abstractmethod


class IProfilePublisher(ABC):
    @abstractmethod
    async def publish_user_created(self, user_id: int) -> None:
        pass
