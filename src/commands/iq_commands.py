import logging

from aiogram import types, Router, F
from aiogram.filters import Command

from src.messages import (your_iq_message,
                      iq_changes_message,)
from src.keyboards import load_default_buttons
from src.middlewares.middlewares import MainMiddleware
from src.services.service import UsersService


router = Router()

router.message.middleware(MainMiddleware())
router.message.filter(F.chat.type.in_({"group", "supergroup"}))  # Бот будет отвечать только в группах и супергруппах


@router.message(Command('iq'),flags = {"reg" : "mustberegistered"})  # Обработка команды /iq (Вывод IQ пользователя в чат)
async def get_iq_cmd(message: types.Message) -> None:
    with UsersService() as con:
        iq = con.get_iq(user_id = message.from_user.id, chat_id = message.chat.id)
        await message.reply(your_iq_message(iq),reply_markup=load_default_buttons())
        logging.info('iq command')


@router.message(Command('changeiq'),flags = {"changeiq" : "changeiq","reg" : "mustberegistered"})
async def change_iq_cmd(message: types.Message) -> None:  # Рандомно увеличит/уменьшит iq пользователя
    with UsersService() as con:
        old_iq = con.get_iq(user_id = message.from_user.id, chat_id = message.chat.id)
        new_iq = con.change_iq(user_id = message.from_user.id,old_iq = old_iq, chat_id = message.chat.id)

        await message.reply(iq_changes_message(new_iq, old_iq),reply_markup=load_default_buttons())
        logging.info('changeiq command')
