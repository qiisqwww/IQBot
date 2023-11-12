from typing import Callable, Any, Awaitable

from loguru import logger
from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.flags import get_flag

from src.services import RedisService

__all__ = ["ThrottlingMiddleware"]


class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:

        user_id = str(event.from_user.id)

        void = get_flag(data, "void")
        if void:
            return

        async with RedisService() as storage:
            user_activity = await storage.get_user_throttling(user_id)
            if not user_activity:
                await storage.set_user_throttling(user_id)
                return await handler(event, data)

            if int(user_activity) >= 10:
                logger.warning(f"User {user_id} is spamming (event throttled).")

                return

            await storage.increase_user_throttling(user_id)
            return await handler(event, data)
