from abc import ABC, abstractmethod

from myapp.application.dto.base import BaseDTO
from myapp.application.dto.jwt import JWTData
from myapp.application.dto.user import EmailVerifyDTO


class ILoginUser(ABC):
    @abstractmethod
    async def request_login(self, data: BaseDTO) -> None:
        raise NotImplementedError

    @abstractmethod
    async def verify_email(self, data: EmailVerifyDTO) -> JWTData:
        raise NotImplementedError