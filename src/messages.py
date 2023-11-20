from src.dto import User

__all__ = ["HELP_MESSAGE",
           "START_MESSAGE",
           "REGISTERED_MESSAGE",
           "ALREADY_REGISTERED_MESSAGE",
           "NOT_REGISTERED_MESSAGE",
           "NOT_AVAILABLE_NOW_MESSAGE",
           "your_iq_message",
           "iq_changes_message",
           "leaderboard_message",
           "dumb_message"]

HELP_MESSAGE = '''*Список доступных команд:*

/start - Начать работу с ботом
/register - Зарегестрироваться в системе бота
/help - Список доступных команд
/iq - Узнать свой IQ
/changeiq - Изменить свой IQ
/leaderboard - 10 самых умных участников
/dump - участник с самым низким IQ'''

START_MESSAGE = '''Привет!
Для регистрации в системе бота пропиши команду /register'''

REGISTERED_MESSAGE = '''
Вы были успешно зарегестрированы в системе!'''

STATS_MESSAGE = '''
In develop'''

ALREADY_REGISTERED_MESSAGE = '''
Вы уже зарегестрированы в системе'''

NOT_REGISTERED_MESSAGE = '''
Вы еще не зарегестрированы в системе. Для регистрации введите /register'''

NOT_AVAILABLE_NOW_MESSAGE = '''
Доступно раз в час'''


def your_iq_message(iq: int) -> str:
    if 60 < iq < 78: return f'Ваш IQ равен {iq}'
    return f'Ваш IQ равен {iq}'


def iq_changes_message(old_iq: int, new_iq: int) -> str:
    if old_iq == new_iq:
        return 'Ваш IQ не изменился!'
    elif old_iq > new_iq:
        return f'Поздравляем! Ваш iq вырос на {old_iq - new_iq}'
    return f'К сожалению, Ваш iq уменьшился на {new_iq - old_iq}'


def leaderboard_message(leaderboard: list[User]) -> str:
    leaderboard_text = f'Топ {len(leaderboard)} пользователей:\n\n'

    i = 0
    for leader in leaderboard:
        leaderboard_text += f"""{i + 1}. <a href="tg://user?id={leader.telegram_id}">{leader.user_name} </a>{leader.iq} IQ\n"""
        i+=1

    return leaderboard_text


def dumb_message(dumb: User) -> str:
    dumb_text = (f"""После сессии отлетает:\n\n"""
                 f"""-1. <a href="tg://user?id={dumb.telegram_id}">{dumb.user_name} </a> {dumb.iq} IQ""")

    return dumb_text
