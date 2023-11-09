from aiogram import types, Router
from aiogram.filters import Command
from aiogram.enums import ParseMode
from loguru import logger

from src.messages import HELP_MESSAGE


__all__ = ["help_router"]


help_router = Router()


@help_router.message(Command('help'))
async def help_cmd(message: types.Message) -> None:
    logger.info(f"Help command was sent to {message.from_user.id}.")

    await message.reply(HELP_MESSAGE, ParseMode.MARKDOWN)
