from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from loguru import logger
from asyncpg import Pool

from src.messages import (STATS_MESSAGE,
                          leaderboard_message,
                          dumb_message)
from src.middlewares import IsRegMiddleware
from src.services import UsersService

__all__ = ["statistic_router"]


statistic_router = Router()

statistic_router.message.middleware(IsRegMiddleware())
statistic_router.message.filter(F.chat.type.in_({"group", "supergroup"}))


@statistic_router.message(Command('leaderboard'))
async def get_leaderboard_cmd(message: types.Message, pool: Pool) -> None:
    logger.info(f"Leaderboard was sent to {message.from_user.id}.")

    async with pool.acquire() as con:
        users_service = UsersService(con)
        leaderboard = await users_service.get_leaderboard(chat_id=message.chat.id)

    await message.answer(
        leaderboard_message(leaderboard),
        parse_mode=ParseMode.HTML
    )


@statistic_router.message(Command('dumb'))
async def get_dumb_cmd(message: types.Message, pool: Pool) -> None:
    logger.info(f"Dumb was sent to {message.from_user.id}.")

    async with pool.acquire() as con:
        users_serivce = UsersService(con)
        dumb = await users_serivce.get_dumb(chat_id=int(message.chat.id))

    await message.answer(dumb_message(dumb), parse_mode=ParseMode.HTML)


"""@router.message(Command('stats'))
async def stats_cmd(message: types.Message) -> None:
    await message.reply(STATS_MESSAGE)"""
