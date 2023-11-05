import logging

from aiogram import types, Router, F
from aiogram.filters import Command

from src.messages import (your_iq_message,
                      iq_changes_message,)
from src.keyboards import load_default_buttons
from src.middlewares import IsRegMiddleware
from src.services.service import UsersService


router = Router()


router.message.middleware(IsRegMiddleware())
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


@router.message(Command('iq'))
async def get_iq_cmd(message: types.Message) -> None:
    with UsersService() as con:
        iq = con.get_iq(user_id = message.from_user.id, chat_id = message.chat.id)
        await message.reply(your_iq_message(iq),reply_markup=load_default_buttons())
        logging.info('iq command')


@router.message(Command('changeiq'),flags = {"changeiq": "true"})
async def change_iq_cmd(message: types.Message) -> None:
    with UsersService() as con:
        old_iq = con.get_iq(user_id = message.from_user.id, chat_id = message.chat.id)
        new_iq = con.change_iq(user_id = message.from_user.id,old_iq = old_iq, chat_id = message.chat.id)

        await message.reply(iq_changes_message(new_iq, old_iq),reply_markup=load_default_buttons())
        logging.info('changeiq command')
