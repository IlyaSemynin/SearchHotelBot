from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    """
    Стандартная команда start. Выводит в чат приветствие и кратко рассказывает, что умеет бот.
    :param message: Message
    :return: None
    """
    bot.send_message(
        message.from_user.id,
        f"Привет, {message.from_user.full_name}!\nЯ - бот для поиска отелей."
        f"\nВоспользовавшись кнопкой 'Меню' ты можешь увидеть команды. Выбери то, "
        f"что тебя интересует и мы начнём.\nДля вызова помощи по командам используй /help ",
    )

