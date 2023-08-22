from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config_data.config import DEFAULT_COMMANDS


def buttons_command() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for command, desk in DEFAULT_COMMANDS:
        print(command)
        print(desk)
        keyboard.add(InlineKeyboardButton(text=desk, callback_data=f'/{command}'))
    return keyboard
