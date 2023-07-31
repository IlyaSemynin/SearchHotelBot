from loader import bot
from telebot import TeleBot
# This example show how to use inline keyboards and process button presses
from config_data import config
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = TeleBot(token=config.BOT_TOKEN)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())


bot.infinity_polling()















@bot.message_handler(commands=['button'])
def button_message(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Старт")
	markup.add(item1)
	bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)