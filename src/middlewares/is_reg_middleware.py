import logging
from time import time

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from aiogram.dispatcher.flags import get_flag

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
        logging.info('middleware started')

        user_id = event.from_user.id
        chat_id = event.chat.id

        changeiq = get_flag(data, "changeiq")

        with UsersService() as con:
            if not con.is_user_registered(user_id, chat_id):
                await event.answer(NOT_REGISTERED_MESSAGE, reply_markup=load_default_buttons())
                logging.error('user must be registered for this command, middleware finished')
                return

            if changeiq:
                call_time = con.get_call_time(user_id=user_id, chat_id=chat_id)
                if time() - call_time < 3600:  # lasttime - время предыдущего успешного запроса /changeiq в секундах
                    await event.answer(NOT_AVAILABLE_NOW_MESSAGE)
                    logging.error('not enough time left before previous change, middleware finished')
                    return

        return await handler(event, data)