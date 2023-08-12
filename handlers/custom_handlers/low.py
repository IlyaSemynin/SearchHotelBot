from loader import bot
from telebot.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from states.user_data import UserInputState
from utils.api_request import destination_id


# Хэндлер, для вывода самых бюджетных отелей
@bot.message_handler(commands=["low"])
def low_price(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInputState.input_city, message.chat.id)
    bot.send_message(message.from_user.id, 'Вы выбрали команду для поиска бюджетных отелей. Чтобы начать поиск, '
                                           'укажите, пожалуйста, город: ', reply_markup=ReplyKeyboardRemove())


@bot.message_handler(state=UserInputState.input_city)
def input_city(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Отличный выбор, записал! Теперь введите сколько отелей Вам '
                                               'предложить, но не более 20-ти вариантов: ')
        bot.set_state(message.from_user.id, UserInputState.count_hotel, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['input_city'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Название города должно содержать только буквы')


@bot.message_handler(state=UserInputState.count_hotel)
def count_hotel(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал!')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count_hotel'] = message.text

        text = "Ищем отели с самой низкой стоимостью в городе: {city}\n"\
               "Вариантов будет предложено: {count}".format(city=data['input_city'], count=data['count_hotel'])

        bot.send_message(message.from_user.id, text)

        possible_options = destination_id(data['input_city'])
        print(possible_options)
    else:
        bot.send_message(message.from_user.id, 'Извините, количество отелей должно быть цифрой и не должно превышать '
                                               '20-ти вариантов')



