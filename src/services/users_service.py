from random import randint

from loguru import logger

from src.services.service import Service
from src.dto import User


class UsersService(Service):
    async def register(self, user_id: int, user_name: str, chat_id: int) -> None:
        query = ("INSERT INTO users "
                 "(telegram_id, user_name, iq, chat_id)"
                 "VALUES ($1, $2, 0, $3)")

        await self._con.execute(query, user_id, user_name, chat_id)

    async def get_iq(self, user_id: int, chat_id: int) -> int:
        query = "SELECT iq FROM users WHERE telegram_id = $1 AND chat_id = $2"
        iq = await self._con.fetchval(query, user_id, chat_id)

        return iq

    async def change_iq(self, user_id: int, old_iq: int, chat_id: int) -> int:
        query = "UPDATE users SET iq = $1 WHERE telegram_id = $2 AND chat_id = $3"
        new_iq = old_iq + randint(-10, 10)

        await self._con.execute(query, new_iq, user_id, chat_id)
        return new_iq

    async def get_leaderboard(self, chat_id: int) -> list:
        query = "SELECT * FROM users WHERE chat_id = $1"
        records = await self._con.fetch(query, chat_id)

        board = [User.from_mapping(record) for record in records]

        if len(board) < 10:
            return board
        return board[:10]

    async def get_dumb(self, chat_id: int) -> User:
        query = "SELECT * FROM users WHERE chat_id = $1"
        records = await self._con.fetch(query, chat_id)

        board = [User.from_mapping(record) for record in records]
        return board[-1]

    async def is_user_registered(self, user_id: int, chat_id: int) -> bool:
        query = "SELECT telegram_id FROM users WHERE chat_id = $1"
        records = await self._con.fetch(query, chat_id)

        for record in records:
            if record["telegram_id"] == user_id:
                return True

        return False

    async def _get_users_count(self) -> int:
        query = "SELECT COUNT(*) FROM users"
        count = await self._con.execute(query)

        return count
