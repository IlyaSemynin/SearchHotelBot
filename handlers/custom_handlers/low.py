import json
import re
import requests
from keyboards.inline import commands_buttons
from loader import bot
from telebot.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from states.user_data import UserInputState
from config_data import config


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

            text = "Ищем отели с самой низкой стоимостью в городе: {city}\n" \
                   "Вариантов будет предложено: {count}".format(city=data['input_city'], count=data['count_hotel'])

            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, 'Извините, количество отелей должно быть цифрой и не должно превышать '
                                               '20-ти вариантов')


def city_founding(city):
    global suggestions
    url_search = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring_search = {"query": city, "locale": "en_UK", "currency": "USD"}

    headers = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url_search, headers=headers, params=querystring_search)
    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, response.text)
    if find:
        suggestions = json.loads(f"{{{find[0]}}}")

    cities = list()

    for dest_id in suggestions['entities']:  # Обрабатываем результат
        clear = r'<.*?>|</.*?>'
        clear_destination = re.sub(clear, '', dest_id['caption'])
        cities.append({'city_name': clear_destination, 'destination_id': dest_id['destinationId']})
    return cities


def city_markup(city):
    cities = city_founding(city)
    # Функция "city_founding" уже возвращает список словарей с нужным именем и id
    destinations = InlineKeyboardMarkup()
    for city in cities:
        exact_location = [city['input_city'].split(',')]
        txt = ''.join(exact_location[0][0:2])
        destinations.add(InlineKeyboardButton(text=txt,
                                              callback_data=txt))
    return destinations


