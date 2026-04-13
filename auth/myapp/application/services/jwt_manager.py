from datetime import datetime, timezone, timedelta
from typing import Any

import jwt

from myapp.application.dto.jwt import JWTData, Payload
from myapp.application.exception.jwt import JWTDecodeException
from myapp.application.interface.jwt_manager import IJWTManager
from myapp.infrastructure.config import Settings


class JWTManager(IJWTManager):
    def __init__(self, settings: Settings) -> None:
        self.expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        self.secret = settings.JWT_SECRET_KEY
        self.algorithms = [settings.JWT_ALGORITHM]


    async def create_jwt(self, data: Payload) -> JWTData:
        to_encode = data.model_dump().copy()
        to_encode |= {"exp": self.expire}
        encoded_jwt = jwt.encode(
            to_encode, self.secret, algorithm=self.algorithms[0]
        )
        return JWTData(value=encoded_jwt)

    async def read_jwt(self, token: JWTData) -> dict[str, Any]:
        try:
            return jwt.decode(token, self.secret, algorithms=self.algorithms)
        except jwt.exceptions.DecodeError:
            raise JWTDecodeException
