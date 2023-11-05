import logging

from aiogram import types, Router, F
from aiogram.filters import Command

from src.messages import HELP_MESSAGE


__all__ = ["Router"]


router = Router


@router.message(Command('help'))
async def help_cmd(message: types.Message) -> None:
    logging.info(f"help command was sent to {message.from_user.id}")
    await message.reply(HELP_MESSAGE)