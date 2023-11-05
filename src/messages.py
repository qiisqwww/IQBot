__all__ = ["HELP_MESSAGE", "START_MESSAGE", "REGISTERED_MESSAGE", "ALREADY_REGISTERED_MESSAGE",
           "NOT_REGISTERED_MESSAGE","NOT_AVAILABLE_NOW_MESSAGE", "your_iq_message", "iq_changes_message",
           "leaderboard_message","dumb_message"]

HELP_MESSAGE = '''Список доступных команд:
/start - Начать работу с ботом
/register - Зарегестрироваться в системе бота
/help - Список доступных команд
/iq - Узнать свой IQ
/changeiq - Изменить свой IQ'''

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

def leaderboard_message(leaderboard: list) -> str:
    leaderboard_text = f'Топ {len(leaderboard)} пользователей:\n\n'

    for i, (username, iq) in enumerate(leaderboard):
        leaderboard_text += f"{i + 1}. @{username} \t {iq} IQ\n"

    return leaderboard_text

def dumb_message(username: str, iq: int) -> str:
    dumb_text = (f'После сессии отлетает:\n\n'
                 f'-1. @{username} \t {iq} IQ')

    return dumb_text
