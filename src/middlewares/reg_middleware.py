from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from aiogram.dispatcher.flags import get_flag
from loguru import logger

from src.buttons import load_default_buttons
from src.messages import ALREADY_REGISTERED_MESSAGE
from src.services import UsersService
from src.database import get_pool


__all__ = ["RegMiddleware"]


class RegMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        user_id = int(event.from_user.id)
        chat_id = int(event.chat.id)
        reg = get_flag(data, 'reg')

        if not reg:
            return await handler(event, data)

        pool = await get_pool()

        async with pool.acquire() as con:
            users_service = UsersService(con)
            if await users_service.is_user_registered(user_id, chat_id):
                await event.answer(ALREADY_REGISTERED_MESSAGE, reply_markup=load_default_buttons())
                logger.warning(f'User {user_id} must not be registered to be registrated.')
                return

        return await handler(event, data)
