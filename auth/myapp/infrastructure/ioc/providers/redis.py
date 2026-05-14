from typing import AsyncGenerator

from dishka import Provider, provide, Scope
from redis.asyncio import Redis

from myapp.infrastructure.config import Settings


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_session(self, settings: Settings) -> AsyncGenerator[Redis, None]:
        redis = await Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        yield redis
        await redis.close()