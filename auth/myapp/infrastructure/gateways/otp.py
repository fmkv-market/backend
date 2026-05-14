from myapp.application.interface.otp import IOTPStorage
from redis.asyncio import Redis


class OTPRedisStorage(IOTPStorage):
    def __init__(self, redis_client: Redis):
        self._client = redis_client

    async def set(self, email: str, otp: str, ex=300):
        await self._client.set(f"otp:{email}", otp, ex=300)

    async def delete(self, email: str):
        await self._client.delete(f"otp:{email}")

    async def get(self, email: str):
        return await self._client.get(f"otp:{email}")
