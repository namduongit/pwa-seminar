from core.setting import get_setting
from redis.asyncio import Redis

setting = get_setting()

redis_client: Redis | None = None


async def connect_redis() -> None:
    global redis_client
    redis_client = Redis(
        host=setting.REDIS_HOST,
        port=setting.REDIS_PORT,
        db=setting.REDIS_DB,
        decode_responses=True,
    )

    await redis_client.ping()


async def close_redis() -> None:
    if redis_client is not None:
        await redis_client.aclose()


def get_redis() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis is not initialized")

    return redis_client
