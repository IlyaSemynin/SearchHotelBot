from telebot.types import Message

from loader import bot


# Хэндлер, для ввода диапазона значений
@bot.message_handler(commands=["custom"])
def bot_echo(message: Message):
    bot.reply_to(message, "Поиск отеля по максимальной стоимости")


search = input('Введите услугу/товар по которым будет осуществляться поиск: ')
min_price = int(input('Введите диапазон от: '))
max_price = int(input('Введите диапазон до: '))
max_amount = int(input('Сколько вариантов отелей Вам предложить? '))
