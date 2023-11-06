import logging

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.enums import ParseMode

from src.messages import (STATS_MESSAGE,
                          leaderboard_message,
                          dumb_message)
from src.middlewares import IsRegMiddleware
from src.services.service import UsersService


router = Router()


router.message.middleware(IsRegMiddleware())
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


@router.message(Command('leaderboard'))
async def get_leaderboard_cmd(message: types.Message) -> None:
    with UsersService() as con:
        leaderboard = con.get_leaderboard(chat_id = message.chat.id)
    await message.answer(leaderboard_message(leaderboard),
                         parse_mode=ParseMode.HTML)


@router.message(Command('dumb'))
async def get_dumb_cmd(message: types.Message) -> None:
    with UsersService() as con:
        dumb = con.get_dumb(chat_id = message.chat.id)

    await message.answer(dumb_message(dumb[0], dumb[1]),
                        parse_mode=ParseMode.HTML)


"""@router.message(Command('stats'))
async def stats_cmd(message: types.Message) -> None:
    await message.reply(STATS_MESSAGE)"""
