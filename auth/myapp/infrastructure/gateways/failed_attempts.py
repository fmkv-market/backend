from redis.asyncio import Redis

from myapp.application.interface.failed_attempts import IFailedAttemptsStorage

_TTL = 900  # 15 минут


class FailedAttemptsRedisStorage(IFailedAttemptsStorage):
    def __init__(self, redis_client: Redis) -> None:
        self._client = redis_client

    def _key(self, email: str) -> str:
        return f"failed_login:{email}"

    async def increment(self, email: str) -> int:
        key = self._key(email)
        count = await self._client.incr(key)
        if count == 1:
            await self._client.expire(key, _TTL)
        return count

    async def reset(self, email: str) -> None:
        await self._client.delete(self._key(email))