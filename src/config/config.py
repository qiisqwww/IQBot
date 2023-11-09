from .env import StrEnv


__all__ = ["BOT_TOKEN",
           "LOGGING_PATH"]


BOT_TOKEN = StrEnv("BOT_TOKEN")
LOGGING_PATH = StrEnv("LOGGING_PATH")
