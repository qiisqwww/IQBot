import logging

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from aiogram.dispatcher.flags import get_flag

from src.keyboards import load_default_buttons
from src.messages import ALREADY_REGISTERED_MESSAGE
from src.services.service import UsersService


__all__ = ["RegMiddleware"]


class RegMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logging.info('middleware started')

        user_id = event.from_user.id
        chat_id = event.chat.id

        reg = get_flag(data, 'reg')
        if not reg:
            return await handler(event, data)

        with UsersService() as con:
            if con.is_user_registered(user_id,chat_id):
                await event.answer(ALREADY_REGISTERED_MESSAGE, reply_markup=load_default_buttons())
                logging.error('user must not be registered for this command, middleware finished')
                return

        return await handler(event, data)