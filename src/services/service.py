import sqlite3 as sq
import logging
from random import randint
from time import time

__all__ = ["UsersService"]


class UsersService:
    _conn: sq.Connection

    def __init__(self) -> None:
        self._con = sq.connect("database/bot.db")
        logging.info('connected to database')

    def register(self,user_id: int, chat_id: int, username: str) -> None:
        cur = self._con.cursor()

        cur.execute("INSERT INTO users VALUES(?,0,0,?,?)", (user_id,chat_id,username))  # Добавляем строчку в таблицу

        logging.info('registered in database')

    def create_table(self):
        cur = self._con.cursor()
        cur_command = """CREATE TABLE IF NOT EXISTS users(
                            telegram_id INTEGER,
                            iq INTEGER NOT NULL DEFAULT 0,
                            call_time INTEGER NOT NULL DEFAULT 0,
                            chat_id INTEGER,
                            user_name INTEGER)"""

        cur.execute(cur_command)

    def get_iq(self, user_id: int, chat_id: int) -> int:
        cur = self._con.cursor()

        cur.execute("SELECT iq FROM users WHERE telegram_id == ? AND chat_id = ?",(user_id, chat_id))  # Ищем IQ юзера через его tg id
        iq = cur.fetchone()[0]

        return iq

    def change_iq(self,user_id: int, old_iq: int, chat_id: int) -> int:
        cur = self._con.cursor()

        new_iq = old_iq + randint(-10, 10)

        cur.execute("UPDATE users SET iq = ?, call_time = ? WHERE telegram_id = ? AND chat_id = ?",
                    (new_iq, time(), user_id, chat_id))  # в БД заносим новый iq и время вызова

        return new_iq

    def get_leaderboard(self,chat_id: int) -> list:
        cur = self._con.cursor()
        board = cur.execute("SELECT username, iq FROM users WHERE chat_id == ?", (chat_id,)).fetchall()
        leaderboard = sorted(board, key=lambda r: (r[1], r[0]),reverse=True)[:10 if len(board) >= 10 else len(board)]

        return leaderboard

    def get_dumb(self,chat_id:int) -> list:
        cur = self._con.cursor()
        board = cur.execute("SELECT username, iq FROM users WHERE chat_id == ?", (chat_id,)).fetchall()
        dumb = sorted(board, key=lambda r: (r[1], r[0]))[0]

        return dumb

    def get_call_time(self,user_id: int, chat_id: int) -> int:
        cur = self._con.cursor()

        cur.execute("SELECT call_time FROM users WHERE telegram_id == ? AND chat_id = ?",(user_id,chat_id))
        call_time = cur.fetchone()[0]

        return call_time

    def is_user_registered(self,user_id: int, chat_id: int) -> bool:
        cur = self._con.cursor()

        users = self._get_all_users_id(chat_id)
        return user_id in users

    def _get_users_count(self) -> int:
        cur = self._con.cursor()

        count = cur.execute("""SELECT COUNT(*) FROM users""").fetchone()[0]

        return count

    def _get_all_users_id(self,chat_id: int) -> list:
        cur = self._con.cursor()

        data = cur.execute("SELECT telegram_id FROM users WHERE chat_id == ?", (chat_id,)).fetchall()
        return [user_id for (user_id, ) in data]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            print(exc_type, exc_value, tb)
        self._con.commit()
        self._con.close()
        logging.info('disconnected from database')


