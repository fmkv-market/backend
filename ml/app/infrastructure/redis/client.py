import redis

from app.config import Settings


def create_redis_client(settings: Settings) -> redis.Redis:
    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        password=settings.redis_pass or None,
        decode_responses=False,
    )
