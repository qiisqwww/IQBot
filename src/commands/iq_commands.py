from aiogram import types, Router, F
from aiogram.filters import Command
from loguru import logger
from asyncpg import Pool

from src.messages import your_iq_message, iq_changes_message
from src.buttons import load_default_buttons
from src.middlewares import IsRegMiddleware, IQTimeoutMiddleware
from src.services import UsersService

__all__ = ["iq_router"]


iq_router = Router()


iq_router.message.middleware(IsRegMiddleware())
iq_router.message.middleware(IQTimeoutMiddleware())
iq_router.message.filter(F.chat.type.in_({"group", "supergroup"}))


@iq_router.message(Command('iq'))
async def get_iq_cmd(message: types.Message, pool: Pool) -> None:
    logger.info(f"Iq command was handled from {message.from_user.id}.")

    async with (pool.acquire() as con):
        users_service = UsersService(con)
        iq = await users_service.get_iq(
            user_id=int(message.from_user.id),
            chat_id=int(message.chat.id)
        )

    await message.reply(your_iq_message(iq), reply_markup=load_default_buttons())


@iq_router.message(Command('changeiq'), flags={"changeiq": "true"})
async def change_iq_cmd(message: types.Message, pool: Pool) -> None:
    logger.info(f"Changeiq command was handled from {message.from_user.id}.")

    async with pool.acquire() as con:
        users_service = UsersService(con)
        old_iq = await users_service.get_iq(
            user_id=int(message.from_user.id),
            chat_id=int(message.chat.id)
        )
        new_iq = await users_service.change_iq(
            user_id=int(message.from_user.id),
            old_iq=old_iq,
            chat_id=int(message.chat.id)
        )

    await message.reply(iq_changes_message(new_iq, old_iq), reply_markup=load_default_buttons())
