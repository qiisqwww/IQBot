from aiogram import types, Router, F
from aiogram.filters import Command
from loguru import logger
from asyncpg import Pool

from src.messages import START_MESSAGE, REGISTERED_MESSAGE
from src.buttons import load_start_kb, load_default_buttons
from src.middlewares import RegMiddleware
from src.services import UsersService

__all__ = ["reg_router"]


reg_router = Router()
reg_router.message.middleware(RegMiddleware())
reg_router.message.filter(F.chat.type.in_({"group", "supergroup"}))


@reg_router.message(Command('start'))
async def start_cmd(message: types.Message) -> None:
    logger.info(f"Start command was handled from {message.from_user.id}.")

    await message.reply(START_MESSAGE, reply_markup=load_start_kb())


@reg_router.message(Command('register'), flags={"reg": "mustnotberegistered"})
async def reg_cmd(message: types.Message, pool: Pool) -> None:
    logger.info(f"Register command was handled from {message.from_user.id}.")

    async with pool.acquire() as con:
        users_service = UsersService(con)
        await users_service.register(
            user_id=int(message.from_user.id),
            user_name=message.from_user.username,
            chat_id=int(message.chat.id)
        )

    await message.reply(REGISTERED_MESSAGE, reply_markup=load_default_buttons())
