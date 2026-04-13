import jwt

from myapp.infrastructure.config import Settings


class DecodeJWTInteractor:
    def __init__(self, settings: Settings):
        self.secret = settings.JWT_SECRET_KEY
        self.algorithms = [settings.JWT_ALGORITHM]


    async def __call__(self, token: str | None) -> dict[str, str]:
        return jwt.decode(token, self.secret, algorithms=self.algorithms)
