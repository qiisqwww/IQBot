from typing import Callable, Any, Awaitable

from loguru import logger
from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.flags import get_flag

from src.messages import NOT_AVAILABLE_NOW_MESSAGE
from src.services import RedisService

__all__ = ["IQTimeoutMiddleware"]


class IQTimeoutMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:

        user_id = str(event.from_user.id)
        chat_id = str(event.from_user.id)

        changeiq = get_flag(data, "changeiq")
        if not changeiq:
            return await handler(event,data)

        with RedisService() as storage:
            if storage.get_user_chngiq(user_id+chat_id):
                await event.answer(NOT_AVAILABLE_NOW_MESSAGE)
                logger.warning(f'Not enough time left before change for {user_id}.')
                return

            storage.set_user_chngiq(user_id+chat_id)
            return await handler(event, data)