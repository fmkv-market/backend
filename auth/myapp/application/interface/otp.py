from abc import ABC, abstractmethod


class IOTPStorage(ABC):
    @abstractmethod
    async def get(self, email: str) -> str:
        pass

    @abstractmethod
    async def delete(self, email: str) -> str:
        pass

    @abstractmethod
    async def set(self, email: str, otp: str) -> str:
        pass
