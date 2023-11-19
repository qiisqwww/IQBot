from .env import StrEnv


__all__ = [
    "BOT_TOKEN",
    "LOGGING_PATH",
    "DB_USER",
    "DB_PASS",
    "DB_NAME",
    "DB_HOST",
    "DB_HOST"
]


BOT_TOKEN = StrEnv("BOT_TOKEN")
LOGGING_PATH = StrEnv("LOGGING_PATH")
DB_USER=StrEnv("DB_USER")
DB_PASS=StrEnv("DB_PASS")
DB_NAME=StrEnv("DB_NAME")
DB_PORT=StrEnv("DB_PORT")
DB_HOST = StrEnv("DB_HOST")