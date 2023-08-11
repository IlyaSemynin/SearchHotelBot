from telebot.types import Message

from loader import bot


# Хэндлер, для ввода диапазона значений
@bot.message_handler(commands=["custom"])
def bot_echo(message: Message):
    bot.reply_to(message, "Поиск отеля по максимальной стоимости")


