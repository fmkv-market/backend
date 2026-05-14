from abc import ABC, abstractmethod


class IPublisher(ABC):
    @abstractmethod
    async def publish(self, email: str, otp: str) -> None:
        pass