from telebot.types import Message

from loader import bot


# Хэндлер, для вывода самых дорогих отелей
@bot.message_handler(commands=["high"])
def bot_echo(message: Message):
    bot.reply_to(message, "Поиск отеля по максимальной стоимости")


max_price = int(input('Введите максимальную сумму: '))
max_amount = int(input('Сколько вариантов отелей Вам предложить? '))