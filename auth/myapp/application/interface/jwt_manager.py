from typing import Protocol, Any

from myapp.application.dto.jwt import JWTData, Payload


class IJWTManager(Protocol):

    async def create_jwt(self, data: Payload) -> JWTData: pass

    async def read_jwt(self, token: JWTData) -> dict[str, Any]: pass
