from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


# Помощь по командам бота
@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    """
    Стандартная команда help. Выводит в чат бота возможные команды.
    :param message: Message
    :return: None
    """
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
