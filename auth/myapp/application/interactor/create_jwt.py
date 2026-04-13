from datetime import datetime, timezone, timedelta

import jwt

from myapp.application.dto.jwt import JWT
from myapp.infrastructure.config import Settings


class CreateJWTInteractor:
    def __init__(self, settings: Settings) -> None:
        self.expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        self.secret = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM

    async def __call__(self, data: dict) -> JWT:
        to_encode = data.copy()
        to_encode |= {"exp": self.expire}
        encoded_jwt = jwt.encode(
            to_encode, self.secret, algorithm=self.algorithm
        )
        return encoded_jwt
