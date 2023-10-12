import logging

from aiogram import types, Router, F
from aiogram.filters import Command

from messages import (HELP_MESSAGE, START_MESSAGE, REGISTERED_MESSAGE, STATS_MESSAGE, your_iq_message,
                      iq_changes_message, leaderboard_message, dumb_message,)
from keyboards import load_start_kb, load_default_buttons
from middlewares import MainMiddleware
from service import UsersService


router = Router()

router.message.middleware(MainMiddleware())
router.message.filter(F.chat.type.in_({"group", "supergroup"}))  # Бот будет отвечать только в группах и супергруппах


@router.message(Command('start'))  # Обработка команды /start
async def start_cmd(message: types.Message) -> None:
    await message.reply(START_MESSAGE,reply_markup=load_start_kb())
    logging.info('start command')

@router.message(Command('register'),flags = {"reg" : "mustnotberegistered"})  # Обработка команды /register
async def reg_cmd(message:types.Message) -> None:
    with UsersService() as con:
        con.register(user_id = message.from_user.id,
                     chat_id = message.chat.id,
                     username = message.from_user.username)

        await message.reply(REGISTERED_MESSAGE,reply_markup=load_default_buttons())

@router.message(Command('iq'),flags = {"reg" : "mustberegistered"})  # Обработка команды /iq (Вывод IQ пользователя в чат)
async def get_iq_cmd(message: types.Message) -> None:
    with UsersService() as con:
        iq = con.get_iq(user_id = message.from_user.id, chat_id = message.chat.id)
        await message.reply(your_iq_message(iq),reply_markup=load_default_buttons())
        logging.info('iq command')

@router.message(Command('changeiq'),flags = {"changeiq" : "changeiq","reg" : "mustberegistered"})
async def change_iq_cmd(message: types.Message) -> None:  # Рандомно увеличит/уменьшит iq пользователя
    with UsersService() as con:
        old_iq = con.get_iq(user_id = message.from_user.id, chat_id = message.chat.id)
        new_iq = con.change_iq(user_id = message.from_user.id,old_iq = old_iq, chat_id = message.chat.id)

        await message.reply(iq_changes_message(new_iq, old_iq),reply_markup=load_default_buttons())
        logging.info('changeiq command')

@router.message(Command('leaderboard'))
async def get_leaderboard_cmd(message: types.Message) -> None:
    with UsersService() as con:
        leaderboard = con.get_leaderboard(chat_id = message.chat.id)
        await message.answer(leaderboard_message(leaderboard))

@router.message(Command('dumb'))
async def get_dumb_cmd(message: types.Message) -> None:
    with UsersService() as con:
        dumb = con.get_dumb(chat_id = message.chat.id)
        await message.answer(dumb_message(dumb[0], dumb[1]))

@router.message(Command('help'))  # Обработка команды help
async def help_cmd(message: types.Message) -> None:
    await message.reply(HELP_MESSAGE)

@router.message(Command('stats'))
async def stats_cmd(message: types.Message) -> None:
    await message.reply(STATS_MESSAGE)