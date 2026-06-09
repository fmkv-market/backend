from abc import ABC, abstractmethod


class ISender(ABC):
    @abstractmethod
    async def send(self, recipients: list[str], subject: str) -> None:
        raise NotImplementedError