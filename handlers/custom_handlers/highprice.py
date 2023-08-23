import json
import re
import requests
from keyboards.reply.buttons import yes_or_no_button, currency, photo_count_keyboard
from loader import bot
from states.user_data import UserInfoState
from telebot.types import Message, ReplyKeyboardRemove
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.custom_handlers.calendar import calendar_command
from handlers.custom_handlers.api_request import search
from config_data import config


@bot.message_handler(commands=["high"])
def start_script(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.wait_city, message.chat.id)
    bot.send_message(message.from_user.id, f"{message.from_user.first_name},вы выбрали команду для поиска "
                                           f"дорогих отелей. Чтобы продолжить введите город",
                     reply_markup=ReplyKeyboardRemove())
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["command"] = message.text
        data["user_id"] = message.from_user.id


@bot.message_handler(state=UserInfoState.wait_city)
def wait_city(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    try:
        bot.send_message(message.from_user.id, "Уточните название города:", reply_markup=city_markup(message.text))
    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так, повторите попытку")
        bot.delete_state(message.from_user.id)


@bot.callback_query_handler(func=lambda call: True)
def get_city(call) -> None:
    if call.message:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['city'] = call.data
        choice_currency(call)


def choice_currency(call) -> None:
    bot.send_message(call.from_user.id, f"Выбранный город: {call.data}. Выберите валюту:", reply_markup=currency())
    bot.set_state(call.from_user.id, UserInfoState.currency_selection, call.message.chat.id)


@bot.message_handler(state=UserInfoState.currency_selection)
def get_night_price(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["currency"] = message.text
    bot.send_message(message.from_user.id, f"Выбранная валюта: {message.text}. Выберите дату заезда:",
                     reply_markup=ReplyKeyboardRemove())
    calendar_command(message)


@bot.message_handler(state=UserInfoState.count)
def get_count(message: Message) -> None:
    bot.send_message(message.from_user.id, f"Выбранное кол-во отелей: {message.text}. Нужны ли фото отелей?",
                     reply_markup=yes_or_no_button())
    bot.set_state(message.from_user.id, UserInfoState.photo_count, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["count"] = message.text


@bot.message_handler(state=UserInfoState.photo_count)
def get_photo_count(message: Message) -> None:
    if message.text.lower() == 'да':
        bot.send_message(message.from_user.id, 'Выберите кол-во фото на каждый отель',
                         reply_markup=photo_count_keyboard())
        bot.set_state(message.from_user.id, UserInfoState.photo, message.chat.id)
    elif message.text.lower() == 'нет':
        bot.set_state(message.from_user.id, UserInfoState.photo, message.chat.id)
        get_photo(message)


@bot.message_handler(state=UserInfoState.photo)
def get_photo(message: Message) -> None:
    bot.send_message(message.from_user.id, "Вы указали следующие параметры: ", reply_markup=ReplyKeyboardRemove())
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["count_photo"] = message.text
    text = f"Город: {data['city']}\nДата заезда: {data['check_in']}\nДата выезда: {data['check_out']}\n" \
           f"Кол-во отелей: {data['count']}\nКол-во фото: {data['count_photo']}\nКоманда: {data['command']}\n"
    bot.send_message(message.from_user.id, text)
    bot.send_message(message.from_user.id, "Выполняю поиск, пожалуйста подождите...")
    search(message, data)


def city_founding(city):
    url_search = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring_search = {"query": city, "locale": "en_UK", "currency": "USD"}

    response = requests.request("GET", url_search, headers=config.headers, params=querystring_search)
    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, response.text)
    if find:
        suggestions = json.loads(f"{{{find[0]}}}")

    cities = list()
    for dest_id in suggestions['entities']:
        clear = r'<.*?>|</.*?>'
        clear_destination = re.sub(clear, '', dest_id['caption'])
        cities.append({'city_name': clear_destination, 'destination_id': dest_id['destinationId']})
    return cities


def city_markup(city):
    cities = city_founding(city)
    destinations = InlineKeyboardMarkup()
    for city in cities:
        exact_location = list()
        exact_location.append(city['city_name'].split(','))
        txt = ''.join(exact_location[0][0:2])
        destinations.add(InlineKeyboardButton(text=txt, callback_data=txt))
    return destinations