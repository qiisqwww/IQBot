import asyncio

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from src.commands import (iq_router,
                          reg_router,
                          statistic_router,
                          help_router,
                          void_router)
from src.config import BOT_TOKEN, LOGGING_PATH
from src.services import UsersService
from src.middlewares.throttling_middleware import ThrottlingMiddleware


def init_logger() -> None:
    logger.add(
        LOGGING_PATH,
        compression="zip",
        rotation="500 MB",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )


async def main():
    storage = MemoryStorage()
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(storage=storage)
    dp.message.middleware(ThrottlingMiddleware())

    dp.include_routers(iq_router,
                       reg_router,
                       statistic_router,
                       help_router,
                       void_router)

    init_logger()

    with UsersService() as con:
        con.create_table()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
