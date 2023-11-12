from loguru import logger

import redis.asyncio as redis

__all__ = ["RedisService"]


class RedisService:
    _con: redis.Redis

    async def set_user_chngiq(self, user_id: str) -> None:
        await self._con.set("chng"+user_id, "True", ex=3600)

    async def get_user_chngiq(self, user_id: str) -> bool:
        return await self._con.get("chng"+user_id) is not None

    async def set_user_throttling(self, user_id: str) -> None:
        await self._con.set("thr"+user_id, 0, ex=10)

    async def increase_user_throttling(self, user_id: str) -> None:
        await self._con.incr("thr"+user_id)

    async def get_user_throttling(self, user_id: str) -> int:
        return await self._con.get("thr"+user_id)

    async def __aenter__(self) -> "RedisService":
        self._con = redis.Redis(host="redis",
                                port=6379,
                                decode_responses=True)
        return self

    async def __aexit__(self, exc_type, *_) -> None:
        if exc_type is not None:
            logger.error(exc_type)

        await self._con.aclose()
