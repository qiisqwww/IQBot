from dataclasses import dataclass
from typing import Mapping, Self

__all__ = [
    "User",
]


@dataclass(slots=True, unsafe_hash=True)
class User():
    telegram_id: int
    user_name: str
    iq: int
    chat_id: int

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        return cls(
            telegram_id=data["telegram_id"],
            user_name=data["user_name"],
            iq=data["iq"],
            chat_id=data["chat_id"]
        )
