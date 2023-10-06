import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from commands import router as cmdrouter
from config.config_reader import config
from service import create_table


async def main():
    storage = MemoryStorage()  # Создаем хранилище

    bot = Bot(config.BOT_TOKEN.get_secret_value())  # Получаем токен бота из файла с конфигом
    dp = Dispatcher(storage=storage)  # Создаем диспетчер и передаем ему храналище
    dp.include_routers(cmdrouter)  # Добавляем роутеры в диспетчер
    logging.basicConfig(filename='logs/logs.log', level=logging.DEBUG)  # Указываем файл для логирования

    create_table() #  Создаем таблицу в БД если не существует

    logging.info('bot is starting')

    await bot.delete_webhook(drop_pending_updates=True)  # Игнорируем все команды, отправленные до запуска бота
    await dp.start_polling(bot)  # Запуск бота

if __name__ == '__main__':
    asyncio.run(main())
