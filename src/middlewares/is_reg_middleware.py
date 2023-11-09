from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from loguru import logger

from src.buttons import load_default_buttons
from src.messages import NOT_REGISTERED_MESSAGE
from src.services.users_service import UsersService


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

        with UsersService() as con:
            if not con.is_user_registered(user_id, chat_id):
                await event.answer(NOT_REGISTERED_MESSAGE, reply_markup=load_default_buttons())
                logger.error(f'User {user_id} be registered for this command.')
                return

        return await handler(event, data)
