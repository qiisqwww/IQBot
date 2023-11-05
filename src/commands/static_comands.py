import logging

from aiogram import types, Router, F
from aiogram.filters import Command

from src.messages import (HELP_MESSAGE,
                          STATS_MESSAGE,
                          leaderboard_message,
                          dumb_message)
from src.middlewares.middlewares import MainMiddleware
from src.services.service import UsersService


router = Router()

router.message.middleware(MainMiddleware())
router.message.filter(F.chat.type.in_({"group", "supergroup"}))  # Бот будет отвечать только в группах и супергруппах


"""@router.message(Command('leaderboard'))
async def get_leaderboard_cmd(message: types.Message) -> None:
    with UsersService() as con:
        leaderboard = con.get_leaderboard(chat_id = message.chat.id)
        await message.answer(leaderboard_message(leaderboard))

@router.message(Command('dumb'))
async def get_dumb_cmd(message: types.Message) -> None:
    with UsersService() as con:
        dumb = con.get_dumb(chat_id = message.chat.id)
        await message.answer(dumb_message(dumb[0], dumb[1]))"""

@router.message(Command('help'))
async def help_cmd(message: types.Message) -> None:
    await message.reply(HELP_MESSAGE)


@router.message(Command('stats'))
async def stats_cmd(message: types.Message) -> None:
    await message.reply(STATS_MESSAGE)