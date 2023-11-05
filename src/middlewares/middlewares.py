import logging
from time import time

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from aiogram.dispatcher.flags import get_flag

from src.keyboards import load_default_buttons
from src.messages import NOT_AVAILABLE_NOW_MESSAGE, ALREADY_REGISTERED_MESSAGE
from src.services.service import UsersService


__all__ = ["MainMiddleware"]

class MainMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logging.info('middleware started')

        user_id = event.from_user.id
        chat_id = event.chat.id

        changeiq = get_flag(data, 'changeiq')
        reg = get_flag(data, 'reg')

        if not reg:  # Если нет флага reg, то скипаем middleware и просто обрабатываем апдейт
            logging.info('middleware started')
            return await handler(event, data)

        with UsersService() as con:
            if reg:   # Если есть флаг reg, то проверяем его содержимое (у /register и (/iq и /changeiq) отличается)
                if flag_matching(reg,'mustberegistered') and not con.is_user_registered(user_id,chat_id):  # Проверка на то, зарегестрирован ли юзер
                    logging.error('user must be registered for this command, middleware finished')
                    return
                elif flag_matching(reg, 'mustnotberegistered') and con.is_user_registered(user_id,chat_id):  # Проверка на то, не зарегестрирован ли уже пользователь
                    await event.answer(ALREADY_REGISTERED_MESSAGE, reply_markup=load_default_buttons())
                    logging.error('user must not be registered for this command, middleware finished')
                    return
            if changeiq:  # Если /changeiq, то проверяем, прошло ли достаточно времени
                call_time = con.get_call_time(user_id=user_id, chat_id=chat_id)
                if time() - call_time < 3600:  # lasttime - время предыдущего успешного запроса /changeiq в секундах
                    await event.answer(NOT_AVAILABLE_NOW_MESSAGE)
                    logging.error('not enough time left before previous change, middleware finished')
                    return

            logging.info('middleware finished: no flags found')
            
            return await handler(event, data)

def flag_matching(flag: str, flag_data) -> bool:
    return flag == flag_data