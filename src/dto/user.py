from dataclasses import dataclass
from typing import Mapping, Self

from .dto import DTO

__all__ = [
    "User",
]


@dataclass(slots=True, unsafe_hash=True)
class User(DTO):
    telegram_id: int
    iq: int
    chat_id: int

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        return cls(
            telegram_id=data["telegram_id"],
            iq=data["iq"],
            chat_id=data["chat_id"]
        )
