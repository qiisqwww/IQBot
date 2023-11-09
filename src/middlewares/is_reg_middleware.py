from time import time

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from aiogram.dispatcher.flags import get_flag
from loguru import logger

from src.buttons import load_default_buttons
from src.messages import (NOT_REGISTERED_MESSAGE,
                          NOT_AVAILABLE_NOW_MESSAGE)
from src.services.service import UsersService


__all__ = ["IsRegMiddleware"]


class IsRegMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        user_id = event.from_user.id
        chat_id = event.chat.id

        changeiq = get_flag(data, "changeiq")

        with UsersService() as con:
            if not con.is_user_registered(user_id, chat_id):
                await event.answer(NOT_REGISTERED_MESSAGE, reply_markup=load_default_buttons())
                logger.error(f'User {user_id} be registered for this command.')
                return

            if changeiq:
                call_time = con.get_call_time(user_id=user_id, chat_id=chat_id)
                if time() - call_time < 3600:  # lasttime - время предыдущего успешного запроса /changeiq в секундах
                    await event.answer(NOT_AVAILABLE_NOW_MESSAGE)
                    logger.error(f'Not enough time left before change for {user_id}.')
                    return

        return await handler(event, data)
