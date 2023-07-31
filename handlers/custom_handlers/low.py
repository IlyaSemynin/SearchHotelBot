from telebot.types import Message

from loader import bot


# Хэндлер, для вывода самых бюджетных отелей
@bot.message_handler(commands=["low"])
def bot_echo(message: Message):
    bot.reply_to(message, "Поиск отеля по минимальной стоимости")


min_price = int(input('Введите минимальную сумму: '))
max_amount = int(input('Сколько вариантов отелей Вам предложить? '))