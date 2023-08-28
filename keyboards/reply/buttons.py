from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from loader import bot
from telebot import types
from loguru import logger
from telebot.types import Message, Dict


def show_cities_buttons(message: Message, possible_cities: Dict):
    """
    Функция, из словаря возможных городов, формирует клавиатуру с вариантами городов, и посылает её в чат.
    : param message : Message
    : param possible_cities : Dict словарь, с возможными вариантами городов
    : return : None
    """
    logger.info(f'Вывод кнопок с вариантами городов пользователю. User_id: {message.chat.id}')
    keyboards_cities = types.InlineKeyboardMarkup()
    for key, value in possible_cities.items():
        keyboards_cities.add(types.InlineKeyboardButton(text=value["regionNames"], callback_data=value["gaiaId"]))

    return keyboards_cities
    # bot.send_message(message.from_user.id, "Пожалуйста, выберите город", reply_markup=keyboards_cities)


def count_hotel_button() -> ReplyKeyboardMarkup:
    """Кнопки для кол-ва выводимых отелей"""
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton('1'))
    keyboard.add(KeyboardButton('2'))
    keyboard.add(KeyboardButton('3'))
    keyboard.add(KeyboardButton('4'))
    keyboard.add(KeyboardButton('5'))
    return keyboard


def yes_or_no_button() -> ReplyKeyboardMarkup:
    """Кнопки 'Да' и 'Нет'"""
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton("Да"))
    keyboard.add(KeyboardButton("Нет"))
    return keyboard


def currency() -> ReplyKeyboardMarkup:
    """Кнопки выбора валюты"""
    keyboard = ReplyKeyboardMarkup()
    keyboard.add((KeyboardButton("USD")))
    keyboard.add((KeyboardButton("EUR")))
    return keyboard


def photo_count_keyboard() -> ReplyKeyboardMarkup:
    """Кнопки кол-ва фото отелей"""
    keyboard = ReplyKeyboardMarkup()
    keyboard.add((KeyboardButton("1")))
    keyboard.add((KeyboardButton("2")))
    keyboard.add((KeyboardButton("3")))
    keyboard.add((KeyboardButton("4")))
    keyboard.add((KeyboardButton("5")))
    return keyboard


def delete_history() -> ReplyKeyboardMarkup:
    """Кнопка для очистки истории"""
    keyboard = ReplyKeyboardMarkup()
    keyboard.add((KeyboardButton("Очистить историю")))
    return keyboard

