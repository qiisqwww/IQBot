import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from src.commands import (iq_router,
                          reg_router,
                          static_router)
from src.config import BOT_TOKEN
from src.services import UsersService


async def main():
    storage = MemoryStorage()

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(storage=storage)
    dp.include_routers(iq_router,
                       reg_router,
                       static_router)
    logging.basicConfig(filename='logs/logs.log',
                        level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s %(message)s")

    with UsersService() as con:
        con.create_table()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
