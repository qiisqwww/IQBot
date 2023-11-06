import logging

from aiogram import types, Router, F
from aiogram.filters import Command

from src.messages import START_MESSAGE, REGISTERED_MESSAGE
from src.buttons import load_start_kb, load_default_buttons
from src.middlewares import RegMiddleware
from src.services.service import UsersService


router = Router()


router.message.middleware(RegMiddleware())
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


@router.message(Command('start'))
async def start_cmd(message: types.Message) -> None:
    await message.reply(START_MESSAGE,reply_markup=load_start_kb())
    logging.info('start command')


@router.message(Command('register'),flags = {"reg" : "mustnotberegistered"})
async def reg_cmd(message:types.Message) -> None:
    with UsersService() as con:
        con.register(user_id=message.from_user.id,
                     chat_id=message.chat.id)

        await message.reply(REGISTERED_MESSAGE,reply_markup=load_default_buttons())